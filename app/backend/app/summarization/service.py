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
import re
import uuid
from enum import StrEnum
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.chat.evidence import (
    MatrixCell,
    build_matrix,
    matrix_text,
    method_aliases,
    method_definitions,
)
from app.chat.verification import NumberCheck, OverstatedClaim, numbers_in, verify_numbers
from app.chat.verification import PageText as CheckedPage
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
    repair_prompt,
    section_prompt,
)

logger = logging.getLogger(__name__)

MAX_REASON_LENGTH = 500
RETRY_REMINDER = (
    "\n\n(The previous attempt ran past the length limit and was discarded. Keep to the word "
    "limit above: a compact summary, not a list of every item.)\n"
)
# D77/M5: qwen3.6 ran past the limit twice on the same appendix unit. A last attempt, firmer
# and at temperature 0 (the model's most likely text, not a sample); the summary still
# fails if that one is cut too — a cut text is never stored.
RETRY_REMINDER_FIRM = (
    "\n\n(Two attempts ran past the length limit and were discarded. Write at most 150 "
    "words in one or two paragraphs. Do not list, quote or reproduce the items of the "
    "section; name what it contains.)\n"
)
RETRIES: tuple[tuple[str, float | None], ...] = ((RETRY_REMINDER, None), (RETRY_REMINDER_FIRM, 0.0))


# Sentence ends; a page marker's "p." or "pp." and the usual abbreviations are not ends.
_SENTENCES = re.compile(
    r"(?<!\bp\.)(?<!\bpp\.)(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bvs\.)(?<=[.!?。！？])\s+"
)


def _repair_evidence(
    check: NumberCheck, cells: list[MatrixCell], counter: TokenCounter
) -> tuple[list[str], str]:
    """What the model is shown about each contradiction (D87 B3: traceable figures, never
    just "this is wrong"): for a figure under the wrong labels, where the table really has
    it and the table's figures for the labels the summary gave, with the differences; for
    a claim of winning everywhere, the cells that go the other way. The excerpt is the
    matrix rows of the conditions involved."""
    evidence: list[str] = []
    involved: list[MatrixCell] = []
    for m in check.mislabelled:
        where = " / ".join(", ".join(labels) for labels in m.source_labels)
        line = (
            f'"{m.sentence}": {m.number} is given as {", ".join(m.answer_labels)}; in the table '
            f"{m.number} is {where}."
        )
        condition = [
            c
            for c in cells
            if c.row in m.answer_labels and (not c.group or c.group in m.answer_labels)
        ]
        named = [c for c in condition if c.column in m.answer_labels]
        if condition:
            involved.extend(condition)
            table = condition[0].table
            page = condition[0].page
            figures = "; ".join(
                f"{c.column} {c.value}"
                + (f" (paired with {c.paired_with})" if c.paired_with else "")
                for c in condition[:8]
            )
            line += f" The table's figures for that condition ({table}, p. {page}): {figures}."
        for a in named[:1]:
            deltas = [
                f"{a.column} {a.value} vs {b.column} {b.value}{_delta_text(a.value, b.value)}"
                for b in condition
                if b.column != a.column
            ]
            if deltas:
                line += " Differences: " + "; ".join(deltas[:5]) + "."
        evidence.append(line)
    for number in check.unverified:
        # D88: a figure that appears nowhere on the summary's pages ("Diversity (71.2%)")
        # is not the paper's. The model is told which figures the pages do hold.
        evidence.append(
            f"{number} appears nowhere on the pages this summary covers; it is not a figure "
            f"of the document. Keep only figures that the table excerpts below show."
        )
    for o in _contradicted_claims(check):
        line = (
            f'"{o.sentence}": in the table {o.method} is above the compared methods in '
            f"{o.higher} cells and below in {o.lower}; the cases below: "
            + "; ".join(o.examples[:6])
            + "."
        )
        evidence.append(line)
    seen: set[tuple[str, str, str, int]] = set()
    unique = []
    for c in involved:
        key = (c.table, c.group, c.row, c.block)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    excerpt_cells = [c for c in cells if (c.table, c.group, c.row, c.block) in seen]
    excerpts, _ = matrix_text(excerpt_cells, counter, budget=600) if excerpt_cells else ("", [])
    return evidence, excerpts


_PAGE_MARKER = re.compile(r"\(pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\)")


def _same_sentence(written: str, reported: str) -> bool:
    """Whether a sentence of the summary is the one a check reported: the check strips page
    markers and citations and may tidy spacing, so both sides are compared normalised."""

    def normalise(text: str) -> str:
        text = _PAGE_MARKER.sub(" ", text)
        text = re.sub(r"\[\s*\d+(?:\s*,\s*\d+)*\s*\]", " ", text)
        return re.sub(r"\W+", " ", text).strip().lower()

    a, b = normalise(written), normalise(reported)
    return bool(a) and bool(b) and (a == b or a in b or b in a)


def _needs_repair(verification: dict[str, Any]) -> bool:
    """D87 B1 triggers on a contradiction; D88 also on a figure the pages do not hold."""
    return verification["status"] == "CONTRADICTED" or bool(verification.get("unverified"))


def _contradicted_claims(check: NumberCheck) -> list[OverstatedClaim]:
    """Claims of winning everywhere that the tables contradict; an "unresolved" claim (no
    shared cells) is not evidence against the summary."""
    return [o for o in check.overstated if o.status == "contradicted"]


def _delta_text(a: str, b: str) -> str:
    try:
        x = float(a.replace(",", "").rstrip("%"))
        y = float(b.replace(",", "").rstrip("%"))
    except ValueError:
        return ""
    diff = x - y
    if a.endswith("%") and b.endswith("%") and y:
        return f" ({diff:+.1f} pp, {diff / y * 100:+.1f}% relative)"
    return f" ({diff:+g})"


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
        repair: bool = False,
    ) -> None:
        self._sessions = sessions
        self._storage = storage
        self._counter = counter
        self._gateway = gateway
        self._input_budget = input_budget
        # D87 experiment B: rewrite a summary once when its figures contradict its tables.
        self._repair = repair
        self.repair_reports: list[dict[str, Any]] = []
        # D75/D76: what the number check found in each summary; kept in memory for the
        # experiment's records and the tests (the status itself is stored with the summary).
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
                verification = await self._verification(
                    claimed, unit.title, text, unit.page_start, unit.page_end
                )
                if self._repair and _needs_repair(verification):
                    text, verification = await self._repair_summary(
                        claimed, unit.title, text, unit.page_start, unit.page_end, context
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
                        verification=verification,
                    )
                )

            if not await self._progress(job_id, len(units), total):
                return SummaryOutcome.ABANDONED
            document_text = await self._summarise_document(claimed, sections, context)
            document_verification = await self._verification(
                claimed,
                "document",
                document_text,
                min(s.page_start for s in sections),
                max(s.page_end for s in sections),
            )
            if self._repair and _needs_repair(document_verification):
                document_text, document_verification = await self._repair_summary(
                    claimed,
                    "document",
                    document_text,
                    min(s.page_start for s in sections),
                    max(s.page_end for s in sections),
                    context,
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
                verification=document_verification,
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

    async def _verification(
        self, claimed: ClaimedSummaryJob, what: str, text: str, page_start: int, page_end: int
    ) -> dict[str, Any]:
        """D76: how the summary's figures stand against the chunks of its pages. Nothing is
        rewritten here (D75's correction of summaries proved unsafe); D87's repair, when on,
        runs on a CONTRADICTED result and re-checks. VERIFIED means every figure was found,
        none contradicts a table and no claim of winning everywhere is contradicted; "nothing
        found wrong" alone is UNCERTAIN when a figure could not be located or resolved."""
        checked = await self._check(claimed, text, page_start, page_end)
        if checked is None:
            rows_missing = not await self._page_rows(claimed, page_start, page_end)
            report = {
                "status": "NOT_CHECKED",
                "contradicted": [],
                "unverified": [],
                "unresolved": [],
                "checked_figures": 0,
                "reason": "no chunks for the pages"
                if rows_missing
                else "no figures in the summary",
            }
        else:
            check, _cells, figures = checked
            report = self._report(check, figures)
        if report["status"] != "VERIFIED":
            logger.info("Summary of %s: %s (%s)", what, report["status"], report)
        self.verification_reports.append(
            {"summary": what, "pages": [page_start, page_end], **report}
        )
        return report

    async def _page_rows(
        self, claimed: ClaimedSummaryJob, page_start: int, page_end: int
    ) -> list[tuple[int, str]]:
        async with self._sessions() as session:
            return await IngestionRepository(session).chunk_texts_for_pages(
                claimed.document_id, page_start, page_end
            )

    async def _check(
        self, claimed: ClaimedSummaryJob, text: str, page_start: int, page_end: int
    ) -> tuple[NumberCheck, list[MatrixCell], list[str]] | None:
        """The number check of a summary against its pages' chunks, with the table cells
        it was checked against; None when there is nothing to check."""
        rows = await self._page_rows(claimed, page_start, page_end)
        figures = numbers_in(text)
        if not rows or not figures:
            return None
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
        return verify_numbers(text, pages, aliases), cells, figures

    @staticmethod
    def _report(check: NumberCheck, figures: list[str]) -> dict[str, Any]:
        overstated = _contradicted_claims(check)
        if check.mislabelled or overstated:
            status = "CONTRADICTED"
        elif check.unverified or check.unresolved:
            status = "UNCERTAIN"
        else:
            status = "VERIFIED"
        return {
            "status": status,
            "contradicted": [m.number for m in check.mislabelled],
            "overstated": [o.sentence for o in overstated],
            "unverified": check.unverified,
            "unresolved": [u.number for u in check.unresolved],
            "checked_figures": len(figures),
        }

    async def _repair_summary(
        self,
        claimed: ClaimedSummaryJob,
        what: str,
        text: str,
        page_start: int,
        page_end: int,
        context: CallContext,
    ) -> tuple[str, dict[str, Any]]:
        """D87 experiment B: one evidence-guided rewrite of the contradicted sentences, then a
        re-check; sentences that still contradict the tables are removed. Returns the text
        to store and its verification report (with the repair's record)."""
        checked = await self._check(claimed, text, page_start, page_end)
        if checked is None:
            return text, self.verification_reports[-1]
        check, cells, _ = checked
        evidence, excerpts = _repair_evidence(check, cells, self._counter)
        prompt = repair_prompt(claimed.filename, what, text, evidence, excerpts)
        rewritten = await self._generate(prompt, "summary_repair", context, what, temperature=0.0)
        model_changed = rewritten.strip() != text.strip()
        removed: list[str] = []
        after = await self._check(claimed, rewritten, page_start, page_end)
        if after is not None and (
            after[0].mislabelled or _contradicted_claims(after[0]) or after[0].unverified
        ):
            # The rewrite did not settle it: the sentences still contradicted, and those
            # with a figure the pages do not hold, go, so that no unverified figure is
            # stored as trusted.
            offending = {m.sentence for m in after[0].mislabelled} | {
                o.sentence for o in _contradicted_claims(after[0])
            }
            for sentence in _SENTENCES.split(rewritten):
                if any(number in sentence for number in after[0].unverified):
                    offending.add(sentence.strip())
            kept, removed = [], []
            for sentence in _SENTENCES.split(rewritten):
                if not sentence.strip():
                    continue
                if any(_same_sentence(sentence, o) for o in offending):
                    removed.append(sentence.strip())
                else:
                    kept.append(sentence)
            rewritten = " ".join(kept).strip()
            after = await self._check(claimed, rewritten, page_start, page_end)
        if not rewritten:
            # Nothing left: keep the original text with its CONTRADICTED status.
            rewritten, after = text, checked
        report = (
            self._report(after[0], after[2])
            if after is not None
            else {
                "status": "NOT_CHECKED",
                "contradicted": [],
                "overstated": [],
                "unverified": [],
                "unresolved": [],
                "checked_figures": 0,
            }
        )
        report["repair"] = {
            "before": self._report(check, checked[2])["status"],
            "evidence": evidence,
            "rewritten": model_changed,
            "removed_sentences": removed,
            "after": report["status"],
        }
        self.repair_reports.append({"summary": what, "pages": [page_start, page_end], **report})
        logger.info("Summary of %s repaired: %s", what, report["repair"])
        return rewritten, report

    async def _generate(
        self,
        prompt: str,
        purpose: str,
        context: CallContext,
        what: str,
        temperature: float | None = None,
    ) -> str:
        result = await self._gateway.generate(
            prompt,
            purpose=purpose,
            max_output_tokens=SUMMARY_MAX_OUTPUT_TOKENS,
            context=context,
            temperature=temperature,
        )
        for attempt, (reminder, temperature) in enumerate(RETRIES, start=1):
            if result.finish_reason.is_complete:
                break
            # The model ran past the output limit (seen on one appendix unit, D75/D77): told
            # so and asked again; the text that was cut is never used.
            logger.info("Summary of %s ran past the output limit; retry %d", what, attempt)
            result = await self._gateway.generate(
                prompt + reminder,
                purpose=purpose,
                max_output_tokens=SUMMARY_MAX_OUTPUT_TOKENS,
                context=context,
                temperature=temperature,
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
