"""Answering a question in a conversation, from the asker's own documents.

    check -> store the question and a pending answer -> route -> gather the
    evidence (retrieved chunks, or the stored summaries) -> pack the prompt
    within its budget -> stream the answer -> read its citations

The checks happen before anything is stored or sent: a question that fails one
creates no message and causes no LLM call. A summary question whose documents
have no ready summary is answered without a call either (AC-42).
"""

import asyncio
import logging
import uuid
from collections.abc import AsyncIterator
from contextlib import aclosing
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.chat.citation_check import DoubtfulCitation, SourceText, check_citations
from app.chat.memory import (
    MEMORY_TOKEN_BUDGET,
    HistoryMessage,
    build_memory,
    clean_rewrite,
    rewrite_prompt,
)
from app.chat.prompting import (
    build_answer_prompt,
    build_summary_prompt,
    cited_indexes,
    question_language,
    source_payload,
    summary_source_payload,
)
from app.chat.repository import ChatRepository
from app.chat.revision import (
    Candidate,
    Trigger,
    build_revision_prompt,
    choose_final,
    find_triggers,
    invalid_citations,
    missing_coverage,
)
from app.chat.routing import question_type
from app.chat.verification import (
    NumberCheck,
    PageText,
    check_note,
    claim_note,
    label_note,
    verify_numbers,
)
from app.conversations.repository import ConversationRepository
from app.conversations.service import ConversationService
from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.llm.embedding import Embedder, EmbeddingError, EmbeddingInputError
from app.llm.gateway import CallContext, ContextBudgetExceeded, LLMCallFailed, LLMGateway, LLMResult
from app.llm.tokenizer import TokenCounter
from app.models import User
from app.retrieval.repository import RetrievalRepository
from app.retrieval.service import RetrievalService, SearchScope
from app.summarization.repository import DocumentSummaryState, SummaryRepository

logger = logging.getLogger(__name__)

# Budget of one answer call (docs/02-specs/02-architecture.md, section 4.3).
ANSWER_MAX_OUTPUT_TOKENS = 2_500
DELIVERY_PIECE = 400  # characters per delta when a finished text is delivered (two-call mode)
EVIDENCE_TOKEN_BUDGET = 5_500
# The answer is saved to the database every this many pieces while it streams.
SAVE_EVERY = 20


@dataclass(frozen=True)
class PreparedQuestion:
    """A question that passed every check; its two messages are stored."""

    actor: User
    conversation_id: uuid.UUID
    user_message_id: uuid.UUID
    assistant_message_id: uuid.UUID
    question: str
    scope: SearchScope
    # The conversation before this question, oldest first (memory for a follow-up).
    history: tuple[HistoryMessage, ...] = ()


@dataclass(frozen=True)
class ChatEvent:
    name: str
    data: Any


@dataclass(frozen=True)
class Assessment:
    """One candidate answer with every deterministic check applied to it (D69)."""

    text: str
    cited: list[int]
    check: NumberCheck
    doubts: list[DoubtfulCitation]
    triggers: list[Trigger]


@dataclass(frozen=True)
class Evidence:
    """What the answer is produced from. No prompt means there is nothing to send."""

    prompt: str | None
    sources: list[dict[str, Any]]
    # Shown after the answer: documents whose summary could not be used, if any.
    note: str


class ChatService:
    def __init__(
        self,
        db: AsyncSession,
        *,
        sessions: async_sessionmaker[AsyncSession],
        settings: Settings,
        counter: TokenCounter,
        embedder: Embedder,
        gateway: LLMGateway,
    ) -> None:
        self._db = db
        self._sessions = sessions
        self._settings = settings
        self._counter = counter
        self._embedder = embedder
        self._gateway = gateway

    async def prepare(
        self,
        actor: User,
        conversation_id: uuid.UUID,
        question: str,
        document_ids: list[uuid.UUID] | None,
    ) -> PreparedQuestion:
        """Check the question and store it with a pending answer."""
        conversation = await ConversationService(self._db).owned(actor, conversation_id)

        question = question.strip()
        if not question:
            raise ApiError(422, "EMPTY_QUESTION", "The question is empty.")
        budget = self._settings.question_token_budget
        tokens = self._counter.count(question)
        if tokens > budget:
            # Refused, never truncated: the user decides what to leave out.
            raise ApiError(
                422,
                "QUESTION_TOO_LONG",
                f"The question is {tokens} tokens long; the limit is {budget}. Please shorten it.",
            )

        scope = await RetrievalService(self._db, self._embedder, self._settings).resolve_scope(
            actor, document_ids
        )

        earlier = await ConversationRepository(self._db).messages(actor.id, conversation.id)
        history = tuple(HistoryMessage(m.role, m.content, m.status) for m in earlier)
        user_message_id, assistant_message_id = await ChatRepository(self._db).add_exchange(
            conversation, question
        )
        await self._db.commit()
        return PreparedQuestion(
            actor, conversation.id, user_message_id, assistant_message_id, question, scope, history
        )

    async def answer(self, prepared: PreparedQuestion) -> AsyncIterator[ChatEvent]:
        """Produce the answer as events. The stored message always ends in a final state."""
        received: list[str] = []
        try:
            yield ChatEvent(
                "start",
                {
                    "user_message_id": str(prepared.user_message_id),
                    "assistant_message_id": str(prepared.assistant_message_id),
                    "scope": {
                        "mode": prepared.scope.mode,
                        "document_ids": [str(i) for i in prepared.scope.document_ids],
                    },
                },
            )
            # A follow-up is first made to stand on its own (AC-16); the route, the
            # retrieval and the answer all work from that standalone question.
            question = await self._standalone_question(prepared)
            kind = question_type(question)
            yield ChatEvent("route", {"type": kind, "standalone_question": question})

            evidence = (
                await self._summary_evidence(prepared, question)
                if kind == "summary"
                else await self._retrieval_evidence(prepared, question)
            )
            async with self._sessions() as session, session.begin():
                await ChatRepository(session).start_streaming(
                    prepared.assistant_message_id, evidence.sources
                )
            yield ChatEvent("sources", evidence.sources)

            if evidence.prompt is None:
                # Nothing to answer from (no ready summary, AC-42; or nothing similar
                # enough, AC-15): say so, without spending a call.
                yield ChatEvent("delta", {"text": evidence.note})
                await self._finish(
                    prepared, status="completed", content=evidence.note, answered=False
                )
                yield ChatEvent(
                    "done",
                    {
                        "status": "completed",
                        "answered": False,
                        "cited": [],
                        "unverified_numbers": [],
                        "verified_numbers": [],
                        "mislabelled_numbers": [],
                        "unresolved_numbers": [],
                        "overstated_claims": [],
                        "doubtful_citations": [],
                        "finish_reason": None,
                        "revision": None,
                    },
                )
                return

            if self._settings.answer_revision:
                # Experimental two-call mode (D69): nothing is streamed; the draft is
                # checked, revised once when faulted, and the chosen text sent at the end.
                async for event in self._answer_in_two_calls(
                    prepared, question, evidence, received
                ):
                    yield event
                return

            result: LLMResult | None = None
            context = CallContext(
                owner_id=prepared.actor.id,
                conversation_id=prepared.conversation_id,
                message_id=prepared.assistant_message_id,
            )
            stream = self._gateway.stream(
                evidence.prompt,
                purpose="answer",
                max_output_tokens=ANSWER_MAX_OUTPUT_TOKENS,
                context=context,
            )
            # Closing the stream when this generator is closed lets the gateway
            # record the call as interrupted right away.
            async with aclosing(stream) as pieces:  # type: ignore[type-var]
                async for piece in pieces:
                    if piece.result is not None:
                        result = piece.result
                        continue
                    received.append(piece.text)
                    if len(received) % SAVE_EVERY == 0:
                        async with self._sessions() as session, session.begin():
                            await ChatRepository(session).save_content(
                                prepared.assistant_message_id, "".join(received)
                            )
                    yield ChatEvent("delta", {"text": piece.text})
            if result is None:
                raise LLMCallFailed("LLM_UNAVAILABLE", "The answer ended without a result.")

            cited = cited_indexes("".join(received), len(evidence.sources))
            # A stream that ended normally is not necessarily a finished answer:
            # only a natural stop is. Anything else is kept, marked interrupted.
            complete = result.finish_reason.is_complete
            check = NumberCheck([], [], [], [], [])
            doubts = []
            if complete:
                check = await self._check_numbers(prepared, "".join(received), evidence, cited)
                # AC-13 (D68): statements whose citation points at the wrong source.
                doubts = check_citations(
                    "".join(received),
                    [
                        SourceText(
                            s["index"],
                            s["snippet"],
                            uuid.UUID(s["document_id"]),
                            s["page_start"],
                            s["page_end"],
                        )
                        for s in evidence.sources
                        if s["kind"] == "chunk"  # a summary paraphrases: word overlap says little
                    ],
                )
                language = question_language(prepared.question)
                notes = [evidence.note] if evidence.note else []
                if check.unverified:
                    notes.append(check_note(check.unverified, language))
                if check.mislabelled:
                    notes.append(label_note(check.mislabelled, language))
                if any(c.status == "contradicted" for c in check.overstated):
                    notes.append(claim_note(check.overstated, language))
                for note in notes:
                    # Said after the answer, as part of it: documents whose summary was
                    # not available, and numbers that could not be checked.
                    received.append("\n\n" + note)
                    yield ChatEvent("delta", {"text": "\n\n" + note})
            status = "completed" if complete else "interrupted"
            answered = bool(cited) if complete else None
            await self._finish(
                prepared, status=status, content="".join(received), answered=answered
            )
            yield ChatEvent(
                "usage",
                {
                    "prompt_tokens": result.prompt_tokens,
                    "completion_tokens": result.completion_tokens,
                    "limit": self._settings.llm_context_limit,
                },
            )
            yield ChatEvent(
                "done",
                {
                    "status": status,
                    "answered": answered,
                    "cited": cited,
                    "unverified_numbers": check.unverified,
                    "verified_numbers": [
                        {
                            "number": v.number,
                            "document_id": str(v.document_id),
                            "page": v.page,
                            "snippet": v.snippet,
                        }
                        for v in check.verified
                    ],
                    "mislabelled_numbers": [
                        {
                            "number": m.number,
                            "answer_labels": m.answer_labels,
                            "source_labels": m.source_labels,
                            "sentence": m.sentence,
                        }
                        for m in check.mislabelled
                    ],
                    "unresolved_numbers": [
                        {
                            "number": u.number,
                            "answer_labels": u.answer_labels,
                            "source_labels": u.source_labels,
                            "sentence": u.sentence,
                            "reason": u.reason,
                        }
                        for u in check.unresolved
                    ],
                    "overstated_claims": [
                        {
                            "sentence": c.sentence,
                            "method": c.method,
                            "compared": c.compared,
                            "higher": c.higher,
                            "lower": c.lower,
                            "examples": c.examples,
                            "status": c.status,
                            "reason": c.reason,
                        }
                        for c in check.overstated
                    ],
                    "doubtful_citations": [
                        {
                            "sentence": d.sentence,
                            "cited": d.cited,
                            "closer": d.closer,
                            "coverage_cited": d.coverage_cited,
                            "coverage_closer": d.coverage_closer,
                        }
                        for d in doubts
                    ],
                    "finish_reason": result.finish_reason.value,
                    "revision": None,
                },
            )
        except (asyncio.CancelledError, GeneratorExit):
            # The reader went away. Keep what was produced, marked as unfinished.
            await asyncio.shield(
                self._finish(
                    prepared, status="interrupted", content="".join(received), answered=None
                )
            )
            raise
        except (EmbeddingError, LLMCallFailed, ContextBudgetExceeded) as error:
            await self._finish(prepared, status="failed", content="".join(received), answered=None)
            yield ChatEvent("error", _describe(error))
        except Exception:
            logger.exception("Answering message %s failed", prepared.assistant_message_id)
            await self._finish(prepared, status="failed", content="".join(received), answered=None)
            yield ChatEvent(
                "error", {"code": "INTERNAL_ERROR", "detail": "The answer could not be produced."}
            )

    async def _standalone_question(self, prepared: PreparedQuestion) -> str:
        """The question rewritten from the conversation so far, or as asked.

        Without earlier turns there is nothing to resolve and no call is made.
        A rewrite that fails, is cut short, is not a single line or exceeds the
        question budget is not used: the question is kept as asked, and the
        call is in the ledger either way.
        """
        memory = build_memory(
            list(prepared.history), self._counter, budget_tokens=MEMORY_TOKEN_BUDGET
        )
        if not memory:
            return prepared.question
        context = CallContext(
            owner_id=prepared.actor.id,
            conversation_id=prepared.conversation_id,
            message_id=prepared.assistant_message_id,
        )
        try:
            result = await self._gateway.generate(
                rewrite_prompt(memory, prepared.question),
                purpose="rewrite",
                max_output_tokens=self._settings.question_token_budget,
                context=context,
            )
        except (LLMCallFailed, ContextBudgetExceeded) as error:
            logger.warning("Rewrite skipped, question used as asked: %s", error)
            return prepared.question
        if not result.finish_reason.is_complete:
            return prepared.question
        rewritten = clean_rewrite(result.text)
        too_long = (
            rewritten is not None
            and self._counter.count(rewritten) > self._settings.question_token_budget
        )
        if rewritten is None or too_long:
            return prepared.question
        return rewritten

    async def _check_numbers(
        self, prepared: PreparedQuestion, answer: str, evidence: Evidence, cited: list[int]
    ) -> NumberCheck:
        """AC-26: look the answer's numbers up on the pages of the cited sources."""
        return verify_numbers(answer, await self._pages(prepared, evidence, cited))

    async def _pages(
        self, prepared: PreparedQuestion, evidence: Evidence, cited: list[int]
    ) -> list[PageText]:
        """The original text of the pages the cited sources cover (all sources if none is cited)."""
        sources = [evidence.sources[i - 1] for i in cited] or evidence.sources
        ranges = list(
            dict.fromkeys(
                (uuid.UUID(s["document_id"]), s["page_start"], s["page_end"]) for s in sources
            )
        )
        async with self._sessions() as session:
            rows = await RetrievalRepository(session).page_texts(prepared.actor.id, ranges)
        return [PageText(*row) for row in rows]

    async def _assess(
        self, prepared: PreparedQuestion, question: str, text: str, evidence: Evidence
    ) -> "Assessment":
        """Every deterministic check on one candidate answer, and what faults it (D69)."""
        cited = cited_indexes(text, len(evidence.sources))
        pages = await self._pages(prepared, evidence, cited)
        check = verify_numbers(text, pages)
        doubts = check_citations(
            text,
            [
                SourceText(
                    s["index"],
                    s["snippet"],
                    uuid.UUID(s["document_id"]),
                    s["page_start"],
                    s["page_end"],
                )
                for s in evidence.sources
                if s["kind"] == "chunk"
            ],
        )
        invalid = invalid_citations(text, len(evidence.sources))
        missing = (
            missing_coverage(question, text, pages) if self._settings.revision_completeness else []
        )
        triggers = find_triggers(
            check,
            doubts,
            invalid=invalid,
            missing=missing,
            soft=self._settings.revision_soft_triggers,
        )
        return Assessment(text, cited, check, doubts, triggers)

    def _notes(self, check: NumberCheck, evidence: Evidence, language: str) -> list[str]:
        notes = [evidence.note] if evidence.note else []
        if check.unverified:
            notes.append(check_note(check.unverified, language))
        if check.mislabelled:
            notes.append(label_note(check.mislabelled, language))
        if any(c.status == "contradicted" for c in check.overstated):
            notes.append(claim_note(check.overstated, language))
        return notes

    async def _answer_in_two_calls(
        self, prepared: PreparedQuestion, question: str, evidence: Evidence, received: list[str]
    ) -> AsyncIterator[ChatEvent]:
        """D69: draft, check, revise once when faulted and the budget allows, check again,
        choose by severity, then send the chosen text. Both calls go through the gateway's
        budget check and ledger. The draft is held in memory only: a client that leaves
        before "finalizing" gets an interrupted, empty message."""
        assert evidence.prompt is not None
        context = CallContext(
            owner_id=prepared.actor.id,
            conversation_id=prepared.conversation_id,
            message_id=prepared.assistant_message_id,
        )
        language = question_language(prepared.question)
        mode = "always" if self._settings.revision_always else "conditional"
        yield ChatEvent("stage", {"stage": "generating"})
        first = await self._gateway.generate(
            evidence.prompt,
            purpose="answer",
            max_output_tokens=ANSWER_MAX_OUTPUT_TOKENS,
            context=context,
        )
        calls = [first]
        if not first.finish_reason.is_complete:
            # Cut short: not an answer to check or revise. Kept, marked interrupted.
            received.append(first.text)
            yield ChatEvent("stage", {"stage": "finalizing"})
            yield ChatEvent("delta", {"text": first.text})
            await self._finish(prepared, status="interrupted", content=first.text, answered=None)
            yield self._usage(calls)
            yield ChatEvent(
                "done",
                self._done_payload(
                    "interrupted", None, None, first.finish_reason.value, {"mode": mode}
                ),
            )
            return

        yield ChatEvent("stage", {"stage": "verifying"})
        draft = await self._assess(prepared, question, first.text, evidence)
        info: dict[str, Any] = {
            "mode": mode,
            "triggered": bool(draft.triggers),
            "draft_triggers": [t.as_dict() for t in draft.triggers],
            "revision_triggers": [],
            "skipped": None,
            # Both texts travel with the event for the experiment's records; neither is
            # stored, and the client shows only the chosen one.
            "draft_text": first.text,
            "revision_text": None,
        }
        revision: Assessment | None = None
        if draft.triggers or self._settings.revision_always:
            built = build_revision_prompt(
                question,
                evidence.sources,
                first.text,
                draft.triggers,
                self._counter,
                self._settings.llm_context_limit,
            )
            if built is None:
                info["skipped"] = "budget"
            else:
                prompt, max_output = built
                yield ChatEvent("stage", {"stage": "revising"})
                try:
                    second = await self._gateway.generate(
                        prompt, purpose="revise", max_output_tokens=max_output, context=context
                    )
                except ContextBudgetExceeded:
                    info["skipped"] = "budget"
                except LLMCallFailed as error:
                    logger.warning("Revision call failed, keeping the draft: %s", error)
                    info["skipped"] = "failed"
                else:
                    calls.append(second)
                    info["revision_text"] = second.text
                    if second.finish_reason.is_complete:
                        yield ChatEvent("stage", {"stage": "verifying"})
                        revision = await self._assess(prepared, question, second.text, evidence)
                        info["revision_triggers"] = [t.as_dict() for t in revision.triggers]
                    else:
                        info["skipped"] = "revision cut short"
        choice = choose_final(
            Candidate(first.text, draft.triggers),
            None if revision is None else Candidate(revision.text, revision.triggers),
        )
        final = revision if choice.chosen == "revision" and revision is not None else draft
        info.update({"chosen": choice.chosen, "status": choice.status, "reason": choice.reason})

        yield ChatEvent("stage", {"stage": "finalizing"})
        # Delivery of a finished text in pieces: not model streaming (AC-04 is for the
        # default mode).
        for start in range(0, len(final.text), DELIVERY_PIECE):
            piece = final.text[start : start + DELIVERY_PIECE]
            received.append(piece)
            yield ChatEvent("delta", {"text": piece})
        for note in self._notes(final.check, evidence, language):
            received.append("\n\n" + note)
            yield ChatEvent("delta", {"text": "\n\n" + note})
        answered = bool(final.cited)
        await self._finish(
            prepared, status="completed", content="".join(received), answered=answered
        )
        yield self._usage(calls)
        yield ChatEvent(
            "done",
            self._done_payload("completed", answered, final, calls[-1].finish_reason.value, info),
        )

    @staticmethod
    def _usage(calls: list[LLMResult]) -> ChatEvent:
        return ChatEvent(
            "usage",
            {
                "prompt_tokens": sum(c.prompt_tokens for c in calls),
                "completion_tokens": sum(c.completion_tokens for c in calls),
                "limit": None,
                "calls": len(calls),
            },
        )

    @staticmethod
    def _done_payload(
        status: str,
        answered: bool | None,
        assessment: "Assessment | None",
        finish_reason: str | None,
        revision: dict[str, Any] | None,
    ) -> dict[str, Any]:
        check = assessment.check if assessment else NumberCheck([], [], [], [], [])
        doubts = assessment.doubts if assessment else []
        return {
            "status": status,
            "answered": answered,
            "cited": assessment.cited if assessment else [],
            "unverified_numbers": check.unverified,
            "verified_numbers": [
                {
                    "number": v.number,
                    "document_id": str(v.document_id),
                    "page": v.page,
                    "snippet": v.snippet,
                }
                for v in check.verified
            ],
            "mislabelled_numbers": [
                {
                    "number": m.number,
                    "answer_labels": m.answer_labels,
                    "source_labels": m.source_labels,
                    "sentence": m.sentence,
                }
                for m in check.mislabelled
            ],
            "unresolved_numbers": [
                {
                    "number": u.number,
                    "answer_labels": u.answer_labels,
                    "source_labels": u.source_labels,
                    "sentence": u.sentence,
                    "reason": u.reason,
                }
                for u in check.unresolved
            ],
            "overstated_claims": [
                {
                    "sentence": c.sentence,
                    "method": c.method,
                    "compared": c.compared,
                    "higher": c.higher,
                    "lower": c.lower,
                    "examples": c.examples,
                    "status": c.status,
                    "reason": c.reason,
                }
                for c in check.overstated
            ],
            "doubtful_citations": [
                {
                    "sentence": d.sentence,
                    "cited": d.cited,
                    "closer": d.closer,
                    "coverage_cited": d.coverage_cited,
                    "coverage_closer": d.coverage_closer,
                }
                for d in doubts
            ],
            "finish_reason": finish_reason,
            "revision": revision,
        }

    async def _retrieval_evidence(self, prepared: PreparedQuestion, question: str) -> Evidence:
        async with self._sessions() as session:
            retrieval = RetrievalService(session, self._embedder, self._settings)
            chunks = await retrieval.search(prepared.actor, prepared.scope, question)
            # First line of defence against made-up answers (AC-15): nothing close
            # enough was found, so nothing is sent to the model and the user is told so.
            best = chunks[0].score if chunks else None
            if best is not None and best >= self._settings.min_similarity:
                chunks = await retrieval.with_table_context(prepared.actor, chunks)
        if best is None or best < self._settings.min_similarity:
            logger.info(
                "Question refused: best similarity %s below %s",
                None if best is None else round(best, 3),
                self._settings.min_similarity,
            )
            return Evidence(None, [], _NOTHING_RELEVANT[question_language(prepared.question)])
        prompt, used = build_answer_prompt(question, chunks, self._counter, EVIDENCE_TOKEN_BUDGET)
        sources = [source_payload(index, chunk) for index, chunk in enumerate(used, start=1)]
        return Evidence(prompt, sources, "")

    async def _summary_evidence(self, prepared: PreparedQuestion, question: str) -> Evidence:
        """The stored summaries of the documents in scope; the ones without are named."""
        async with self._sessions() as session:
            repository = SummaryRepository(session)
            states = await repository.states(prepared.actor.id, prepared.scope.document_ids)
            summaries = await repository.ready_summaries(
                prepared.actor.id, prepared.scope.document_ids
            )
        missing = [state for state in states if state.summary_status != "ready"]
        language = question_language(prepared.question)
        note = _unavailable_note(missing, language, nothing_ready=not summaries)
        if not summaries:
            return Evidence(None, [], note)
        prompt, used = build_summary_prompt(
            question, summaries, self._counter, evidence_budget=EVIDENCE_TOKEN_BUDGET
        )
        sources = [summary_source_payload(index, s) for index, s in enumerate(used, start=1)]
        return Evidence(prompt, sources, note)

    async def _finish(
        self, prepared: PreparedQuestion, *, status: str, content: str, answered: bool | None
    ) -> None:
        async with self._sessions() as session, session.begin():
            await ChatRepository(session).finish(
                prepared.assistant_message_id, status=status, content=content, answered=answered
            )


# Said instead of an answer when no retrieved chunk is similar enough to the question.
_NOTHING_RELEVANT = {
    "other": "The documents do not contain content related to this question.",
    "zh": "文件中找不到與這個問題相關的內容。",
}

_UNAVAILABLE = {
    "other": {
        "line": 'The summary of "{filename}" is not available ({reason}), so it was left out.',
        "none": "not started yet",
        "processing": "still being produced",
        "failed": "it failed and can be retried",
        "closing": "Ask again once the summary is ready, or ask a specific question about the "
        "content instead.",
    },
    "zh": {
        "line": "「{filename}」的摘要尚未就緒（{reason}），這次未納入。",
        "none": "尚未開始",
        "processing": "處理中",
        "failed": "產生失敗，可重試",
        "closing": "摘要完成後可再問一次，或改問文件內容的具體問題。",
    },
}


def _unavailable_note(
    missing: list[DocumentSummaryState], language: str, *, nothing_ready: bool
) -> str:
    """Names the documents whose summary could not be used, in the question's language."""
    words = _UNAVAILABLE[language]
    lines = [
        words["line"].format(filename=state.filename, reason=words[state.summary_status])
        for state in missing
    ]
    if nothing_ready:
        lines.append(words["closing"])
    return "\n".join(lines)


def _describe(error: Exception) -> dict[str, str]:
    if isinstance(error, LLMCallFailed):
        return {"code": error.code, "detail": error.detail}
    if isinstance(error, ContextBudgetExceeded):
        return {"code": "CONTEXT_BUDGET_EXCEEDED", "detail": str(error)}
    if isinstance(error, EmbeddingInputError):
        # The service is up; this text cannot be embedded. Rewording helps, waiting does not.
        return {"code": "EMBEDDING_INPUT_FAILED", "detail": str(error)}
    return {"code": "EMBEDDING_UNAVAILABLE", "detail": str(error)}
