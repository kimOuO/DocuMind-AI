"""The summary job: build section summaries and the document summary.

    claim -> parse -> split into units -> one LLM call per unit -> merge -> store all at once

Runs after the index job of a document completed. Nothing is stored until the
end, and then everything in one transaction, so a failure leaves no partial
summaries; the document itself stays ready for ordinary questions (AC-42).
Before each call the job checks that it is still wanted: if its document was
deleted, it stops without writing.
"""

import asyncio
import logging
import uuid
from enum import StrEnum
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.chat.correction import correct
from app.chat.evidence import build_matrix, method_aliases, method_definitions
from app.chat.verification import PageText as CheckedPage
from app.chat.verification import verify_numbers
from app.documents.storage import FileStorage
from app.ingestion.headings import find_headings
from app.ingestion.parsing import DocumentParseError, parse_document
from app.ingestion.repository import ClaimedSummaryJob, IngestionRepository, SummaryRecord
from app.ingestion.sections import SummaryUnit, plan_summary_units
from app.llm.gateway import CallContext, ContextBudgetExceeded, LLMCallFailed, LLMGateway
from app.llm.tokenizer import TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.prompting import (
    SECTION_INPUT_BUDGET,
    SUMMARY_MAX_OUTPUT_TOKENS,
    PageText,
    document_prompt,
    group_within_budget,
    merge_prompt,
    section_prompt,
)

logger = logging.getLogger(__name__)

MAX_REASON_LENGTH = 500
RETRY_REMINDER = (
    "\n\n(The previous attempt ran past the length limit and was discarded. Keep to the word "
    "limit above: a compact summary, not a list of every item.)\n"
)


class SummaryOutcome(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class IncompleteSummary(Exception):
    """The model stopped before finishing a summary; it is not stored."""


class SummaryJobRunner:
    def __init__(
        self,
        *,
        sessions: async_sessionmaker[AsyncSession],
        storage: FileStorage,
        counter: TokenCounter,
        gateway: LLMGateway,
        input_budget: int = SECTION_INPUT_BUDGET,
    ) -> None:
        self._sessions = sessions
        self._storage = storage
        self._counter = counter
        self._gateway = gateway
        self._input_budget = input_budget
        # D75: what the number check found in each summary and what was corrected; kept in
        # memory for the experiment's records and the tests, not stored.
        self.verification_reports: list[dict[str, Any]] = []

    async def run(self, job_id: uuid.UUID) -> SummaryOutcome:
        async with self._sessions() as session, session.begin():
            claimed = await IngestionRepository(session).claim_summary_job(job_id)
        if claimed is None:
            return SummaryOutcome.ABANDONED

        try:
            path = self._storage.absolute(claimed.storage_path)
            pages = await asyncio.to_thread(parse_document, path, claimed.media_type)
            units = plan_summary_units(
                pages, find_headings(pages), self._counter, budget_tokens=self._input_budget
            )
            total = len(units) + 1  # the document summary is the last step
            context = CallContext(owner_id=claimed.owner_id, document_id=claimed.document_id)

            sections: list[SummaryRecord] = []
            for ordinal, unit in enumerate(units, start=1):
                # Also the moment to notice that the document was deleted.
                if not await self._progress(job_id, ordinal - 1, total):
                    return SummaryOutcome.ABANDONED
                text = await self._summarise_section(claimed, unit, context)
                async with self._sessions() as session:
                    chunk_ids = await IngestionRepository(session).chunk_ids_for_pages(
                        claimed.document_id, unit.page_start, unit.page_end
                    )
                text = await self._verified(
                    claimed, unit.title, text, unit.page_start, unit.page_end
                )
                sections.append(
                    SummaryRecord(
                        level="section",
                        ordinal=ordinal,
                        title=unit.title,
                        page_start=unit.page_start,
                        page_end=unit.page_end,
                        source_chunk_ids=chunk_ids,
                        text=text,
                        token_count=self._counter.count(text),
                    )
                )

            if not await self._progress(job_id, len(units), total):
                return SummaryOutcome.ABANDONED
            document_text = await self._summarise_document(claimed, sections, context)
            document_text = await self._verified(
                claimed,
                "document",
                document_text,
                min(s.page_start for s in sections),
                max(s.page_end for s in sections),
            )
            document_summary = SummaryRecord(
                level="document",
                ordinal=0,
                title=None,
                page_start=min(s.page_start for s in sections),
                page_end=max(s.page_end for s in sections),
                source_chunk_ids=[],
                text=document_text,
                token_count=self._counter.count(document_text),
            )
            async with self._sessions() as session, session.begin():
                written = await IngestionRepository(session).complete_summary_job(
                    job_id, sections=sections, document_summary=document_summary
                )
            return SummaryOutcome.COMPLETED if written else SummaryOutcome.ABANDONED
        except (
            DocumentParseError,
            LLMCallFailed,
            ContextBudgetExceeded,
            IncompleteSummary,
        ) as error:
            return await self._fail(job_id, str(error))
        except Exception:
            logger.exception("Summary job %s failed unexpectedly", job_id)
            return await self._fail(job_id, "The summary could not be built.")

    async def _summarise_section(
        self, claimed: ClaimedSummaryJob, unit: SummaryUnit, context: CallContext
    ) -> str:
        prompt = section_prompt(
            claimed.filename,
            unit.title,
            [PageText(piece.page, piece.text) for piece in unit.pages],
        )
        return await self._generate(prompt, "section_summary", context, unit.title)

    async def _summarise_document(
        self, claimed: ClaimedSummaryJob, sections: list[SummaryRecord], context: CallContext
    ) -> str:
        items = [(s.title or "Front matter", s.text) for s in sections]
        # Too many section summaries for one call: condense them in groups first.
        while len(group_within_budget(items, self._counter, self._input_budget)) > 1:
            condensed = []
            for index, group in enumerate(
                group_within_budget(items, self._counter, self._input_budget), start=1
            ):
                text = await self._generate(
                    merge_prompt(claimed.filename, group),
                    "document_summary",
                    context,
                    f"merge group {index}",
                )
                condensed.append((f"Part {index}", text))
            items = condensed
        return await self._generate(
            document_prompt(claimed.filename, items), "document_summary", context, "document"
        )

    async def _verified(
        self, claimed: ClaimedSummaryJob, what: str, text: str, page_start: int, page_end: int
    ) -> str:
        """D75: the summary checked against the chunks of its pages — a figure under labels
        the tables contradict is corrected when the table gives one reading and removed
        otherwise, a figure found nowhere on the pages is removed; the result is checked
        again and the outcome recorded. No model call."""
        async with self._sessions() as session:
            rows = await IngestionRepository(session).chunk_texts_for_pages(
                claimed.document_id, page_start, page_end
            )
        if not rows:
            return text
        by_page: dict[int, list[str]] = {}
        for page, chunk_text in rows:
            by_page.setdefault(page, []).append(chunk_text)
        pages = [
            CheckedPage(claimed.document_id, page, "\n".join(texts))
            for page, texts in sorted(by_page.items())
        ]
        indexed = [
            (
                i,
                RetrievedChunk(
                    uuid.uuid4(), claimed.document_id, claimed.filename, page, i, t, 0, None
                ),
            )
            for i, (page, t) in enumerate(rows, start=1)
        ]
        cells = build_matrix(indexed)
        aliases = method_aliases(method_definitions(indexed, {c.column for c in cells}))
        before = verify_numbers(text, pages, aliases)
        fixed = correct(text, pages, aliases=aliases, unverified=before.unverified)
        after = verify_numbers(fixed.text, pages, aliases)
        self.verification_reports.append(
            {
                "summary": what,
                "pages": [page_start, page_end],
                "mislabelled_before": [m.number for m in before.mislabelled],
                "unverified_before": before.unverified,
                "edits": fixed.edits,
                "removed": fixed.removed,
                "remaining": fixed.remaining,
                "mislabelled_after": [m.number for m in after.mislabelled],
                "changed": fixed.text != text,
            }
        )
        if fixed.text != text:
            logger.info(
                "Summary of %s corrected: %d edits, %d removals, %d remaining",
                what,
                len(fixed.edits),
                len(fixed.removed),
                len(fixed.remaining),
            )
        return fixed.text

    async def _generate(self, prompt: str, purpose: str, context: CallContext, what: str) -> str:
        result = await self._gateway.generate(
            prompt, purpose=purpose, max_output_tokens=SUMMARY_MAX_OUTPUT_TOKENS, context=context
        )
        if not result.finish_reason.is_complete:
            # The model ran past the output limit (seen twice on one appendix unit, D75):
            # one more attempt, told so; the text that was cut is never used.
            logger.info("Summary of %s ran past the output limit; retrying once", what)
            result = await self._gateway.generate(
                prompt + RETRY_REMINDER,
                purpose=purpose,
                max_output_tokens=SUMMARY_MAX_OUTPUT_TOKENS,
                context=context,
            )
        if not result.finish_reason.is_complete:
            raise IncompleteSummary(
                f"The model stopped before finishing the summary of {what} "
                f"({result.finish_reason.value})."
            )
        text = result.text.strip()
        if not text:
            raise IncompleteSummary(f"The model returned an empty summary for {what}.")
        return text

    async def _progress(self, job_id: uuid.UUID, current: int, total: int) -> bool:
        async with self._sessions() as session, session.begin():
            return await IngestionRepository(session).set_progress(
                job_id, "summarizing", current, total
            )

    async def _fail(self, job_id: uuid.UUID, reason: str) -> SummaryOutcome:
        async with self._sessions() as session, session.begin():
            failed = await IngestionRepository(session).fail_job(job_id, reason[:MAX_REASON_LENGTH])
        return SummaryOutcome.FAILED if failed else SummaryOutcome.ABANDONED
