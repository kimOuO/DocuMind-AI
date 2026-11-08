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
import re
import uuid
from collections.abc import AsyncIterator, Sequence
from contextlib import aclosing
from dataclasses import dataclass, field, replace
from functools import partial
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.chat.citation_check import DoubtfulCitation, SourceText, check_citations
from app.chat.correction import Correction, correct, strip_step_numbering
from app.chat.evidence import (
    MATRIX_TOKEN_BUDGET,
    ArithmeticIssue,
    Completeness,
    ConclusionIssue,
    DirectionIssue,
    analysis_preamble,
    arithmetic_note,
    build_matrix,
    check_arithmetic,
    check_completeness,
    check_conclusions,
    check_directions,
    comparison_facts,
    derived_numbers,
    facts_block,
    matrix_cells_of_pages,
    matrix_text,
    method_aliases,
    method_definitions,
    minimal_table_text,
    named_columns,
    overall_status,
)
from app.chat.memory import (
    FOLLOW_UP_MAX_OUTPUT_TOKENS,
    MEMORY_TOKEN_BUDGET,
    REWRITE_HEAD_TOKENS,
    REWRITE_MEMORY_BUDGET,
    HistoryMessage,
    build_memory,
    clean_rewrite,
    follow_up_prompt,
    parse_follow_up,
    rewrite_prompt,
)
from app.chat.navigation import (
    CHUNKS_PER_TARGET,
    COVERED,
    EvidenceCandidate,
    MapEntry,
    PlanItem,
    TargetCandidates,
    analyst_preamble,
    build_map,
    build_navigation_prompt,
    coverage_of,
    describe_retrieved,
    parse_plan,
    roles_preamble,
    select_evidence,
)
from app.chat.prompting import (
    CONVERSATION_BUDGET,
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
    Aliases,
    NumberCheck,
    PageText,
    check_note,
    claim_note,
    label_note,
    numbers_in,
    verify_numbers,
)
from app.conversations.repository import ConversationRepository
from app.conversations.service import ConversationService
from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.llm.embedding import Embedder, EmbeddingError, EmbeddingInputError
from app.llm.gateway import CallContext, ContextBudgetExceeded, LLMCallFailed, LLMGateway, LLMResult
from app.llm.tokenizer import TokenCounter
from app.models import Message, User
from app.retrieval.expansion import MAX_FOLLOWING, table_context
from app.retrieval.repository import RetrievalRepository, RetrievedChunk
from app.retrieval.service import RetrievalService, SearchScope
from app.summarization.repository import DocumentSummaryState, StoredSummary, SummaryRepository

logger = logging.getLogger(__name__)

# Budget of one answer call (docs/02-specs/02-architecture.md, section 4.3).
ANSWER_MAX_OUTPUT_TOKENS = 2_500
_TABLE_CAPTION_LINE = re.compile(r"^\s*(Table\s+\d+)\s*[.:]", re.IGNORECASE)
# D73: how many of a target's chunks are ranked before the turns start.
NAVIGATION_CANDIDATES_PER_TARGET = 3 * CHUNKS_PER_TARGET
DELIVERY_PIECE = 400  # characters per delta when a finished text is delivered (two-call mode)
EVIDENCE_TOKEN_BUDGET = 5_500
# D88: how many of the closest passages the model sees when none reaches MIN_SIMILARITY.
BELOW_THRESHOLD_PASSAGES = 3
# D87 experiment A: the room the comparison facts may take before the sources (single mode).
FACTS_TOKEN_BUDGET = 1400  # D92: exception wording; D96: the figures of each pair
# D95: the rewrite of a follow-up is deterministic; it was the one call still sampling at the
# model's default (0.6), so the same follow-up could be rewritten differently each time.
REWRITE_TEMPERATURE = 0.0
# D95: a rewrite longer than this many times the question (plus the allowance) has added
# material the user did not ask — the model pads "compare LightRAG with GraphRAG" with both
# definitions from the memory, 8 → 66 tokens — and is discarded. Real follow-ups grow far
# less: 「那它的缺點呢？」 6 → 9, "and its drawbacks?" 4 → 13 tokens.
REWRITE_GROWTH_FACTOR = 2  # D96: tightened from 3 and 12 (a 9-token question grew to 35)
REWRITE_GROWTH_ALLOWANCE = 10
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
    # The sampling temperature of the answer call: the request's value, else the server's
    # ANSWER_TEMPERATURE; None means the model's default (AC-60, D94).
    temperature: float | None = None
    # D99: the chunks the previous completed answer cited as sources, for a follow-up that
    # retrieval cannot place (every candidate below the similarity threshold).
    previous_chunk_ids: tuple[uuid.UUID, ...] = ()
    # D99: the model's judgement of this question (None before it is made or without earlier turns).
    follow_up: bool | None = None


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
    # D74: the direction of two-figure comparisons, and whether a question about variants
    # got every variant under one condition; both read off the tables of the cited pages.
    directions: list[DirectionIssue] = field(default_factory=list)
    completeness: Completeness = field(
        default_factory=lambda: Completeness("not_applicable", [], [], None)
    )
    # D76: conclusions that count exceptions, checked against the comparison facts; and
    # ratios the answer derives, checked by arithmetic.
    conclusions: list[ConclusionIssue] = field(default_factory=list)
    arithmetic: list[ArithmeticIssue] = field(default_factory=list)


@dataclass(frozen=True)
class Evidence:
    """What the answer is produced from. No prompt means there is nothing to send."""

    prompt: str | None
    sources: list[dict[str, Any]]
    # Shown after the answer: documents whose summary could not be used, if any.
    note: str
    # D87 experiment A: what the program's comparison facts did to this prompt.
    facts_info: dict[str, Any] | None = None
    # The facts block itself: figures the program computed (counts, differences) are the
    # answer's to repeat, and are not "unverified" when the pages do not hold them (D88).
    facts_text: str = ""


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
        temperature: float | None = None,
    ) -> PreparedQuestion:
        """Check the question and store it with a pending answer. `temperature` is the
        request's choice for the answer call (0–1, validated by the router); omitted, the
        server's setting applies (AC-60)."""
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
        previous_chunk_ids = _previous_chunk_ids(earlier)
        if temperature is None:
            temperature = self._settings.answer_temperature
        user_message_id, assistant_message_id = await ChatRepository(self._db).add_exchange(
            conversation, question, temperature
        )
        await self._db.commit()
        return PreparedQuestion(
            actor,
            conversation.id,
            user_message_id,
            assistant_message_id,
            question,
            scope,
            history,
            temperature,
            previous_chunk_ids,
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
                    "temperature": prepared.temperature,
                },
            )
            # A follow-up is first made to stand on its own (AC-16); the retrieval and the
            # answer work from that standalone question. The route is decided by the
            # question as the user asked it (D95): a rewrite that adds words such as
            # "document summary" must not send a content question to the summary tree.
            question, follow_up, pre_calls = await self._standalone_question(prepared)
            prepared = replace(prepared, follow_up=follow_up)
            kind = question_type(prepared.question)
            if kind == "summary" and await self._summary_tree_skipped(prepared):
                # D91: the documents were uploaded without a summary tree; the question is
                # answered from retrieval. D97 (user): without a note after the answer —
                # the route event and the document's summary status already say so.
                kind = "retrieval"
            yield ChatEvent(
                "route",
                {"type": kind, "standalone_question": question, "follow_up": follow_up},
            )

            # D71: experimental modes. "roles" only changes the prompt (same evidence);
            # "navigate" adds a navigation call whose located places are fetched and put
            # behind the retrieved sources. "single" (default) changes nothing.
            mode = self._settings.answer_mode
            preamble = ""
            navigation: dict[str, Any] | None = None
            extra_calls: list[LLMResult] = []
            added: list[RetrievedChunk] = []
            chunks: list[RetrievedChunk] | None = None
            embedding: list[float] | None = None
            if kind != "summary":
                chunks, embedding = await self._search(prepared, question)
            if mode in ("roles", "navigate") and (kind == "summary" or chunks is not None):
                entries, summaries = await self._document_map(prepared)
                if mode == "roles":
                    preamble = roles_preamble(entries)
                else:
                    yield ChatEvent("stage", {"stage": "navigating"})
                    base_tokens = (
                        sum(s.token_count for s in summaries)
                        if kind == "summary"
                        else sum(c.token_count for c in chunks or [])
                    )
                    # The matrix of a fetched table (D74) goes into the same prompt: its
                    # room is reserved here, or a full table's matrix would not fit.
                    reserved = MATRIX_TOKEN_BUDGET if kind != "summary" else 0
                    navigation, items, added, nav_result = await self._navigate(
                        prepared,
                        question,
                        entries,
                        chunks or [],
                        embedding,
                        budget=max(EVIDENCE_TOKEN_BUDGET - base_tokens - reserved, 0),
                    )
                    if nav_result is not None:
                        extra_calls.append(nav_result)
                    if items:
                        preamble = analyst_preamble(items)
                    if kind != "summary" and nav_result is not None:
                        # D74: the structured evidence of what the Analyst will read,
                        # numbered as the answer prompt will number it.
                        indexed = list(enumerate([*(chunks or []), *added], start=1))
                        cells = build_matrix(indexed)
                        definitions = method_definitions(indexed, {c.column for c in cells})
                        facts = comparison_facts(cells, question)
                        # B5 baseline (2026-11-07, user's decision): the facts are recorded
                        # and used by the checks, not shown to the model — unless
                        # ANSWER_FACTS says so (D87 experiment A).
                        shown_facts = facts if self._settings.answer_facts != "off" else ()
                        preamble += analysis_preamble(
                            cells,
                            definitions,
                            self._counter,
                            budget=MATRIX_TOKEN_BUDGET,
                            facts=shown_facts,
                        )
                        # D76: tables the sources name but the chunker did not rewrite cell
                        # by cell have no matrix — a coverage gap, not a verified table.
                        with_cells = {c.source_index for c in cells}
                        gaps = sorted(
                            f"{m.group(1).title()} [{i}]"
                            for i, c in indexed
                            if i not in with_cells
                            and (m := _TABLE_CAPTION_LINE.match(c.text.strip()))
                        )
                        shown, left_out = matrix_text(
                            cells, self._counter, budget=MATRIX_TOKEN_BUDGET
                        )
                        navigation["matrix"] = {
                            "cells": len(cells),
                            "tables": sorted({f"{c.table} [{c.source_index}]" for c in cells}),
                            # What the model was shown, and the tables left out for size.
                            "shown_tokens": self._counter.count(shown) if shown else 0,
                            "left_out": left_out,
                            "definitions": [d.method for d in definitions],
                            "facts": len(facts),
                            "coverage_gaps": gaps,
                        }
            evidence = (
                await self._summary_evidence(
                    prepared, question, preamble=preamble, added=added, navigation=navigation
                )
                if kind == "summary"
                else self._evidence_from_chunks(
                    prepared,
                    question,
                    chunks,
                    preamble,
                    added,
                    await self._document_cards(prepared),
                )
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
                        "direction_issues": [],
                        "completeness": _completeness_payload(None),
                        "conclusion_issues": [],
                        "arithmetic_issues": [],
                        "analysis_status": None,
                        "finish_reason": None,
                        "revision": None,
                        "navigation": navigation,
                        "correction": None,
                        "facts": evidence.facts_info,
                    },
                )
                return

            if self._settings.answer_revision:
                # Experimental two-call mode (D69): nothing is streamed; the draft is
                # checked, revised once when faulted, and the chosen text sent at the end.
                async for event in self._answer_in_two_calls(
                    prepared, question, evidence, received, navigation, extra_calls
                ):
                    yield event
                return
            if mode == "navigate" and navigation is not None:
                # D75: the Analyst's answer is checked against the tables and corrected
                # deterministically before it is sent; no streaming, no extra call.
                async for event in self._answer_with_correction(
                    prepared, question, evidence, received, navigation, extra_calls
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
                temperature=prepared.temperature,
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
            directions: list[DirectionIssue] = []
            completeness: Completeness | None = None
            conclusions: list[ConclusionIssue] = []
            arithmetic: list[ArithmeticIssue] = []
            if complete:
                text = "".join(received)
                pages = await self._pages(prepared, evidence, cited)
                check = verify_numbers(text, pages)
                # D74: the direction of two-figure comparisons, and whether a question
                # about variants got every variant under one condition.
                directions = check_directions(text, pages)
                completeness = check_completeness(question, text, pages)
                conclusions = check_conclusions(
                    text, comparison_facts(matrix_cells_of_pages(pages), question)
                )
                arithmetic = check_arithmetic(text, pages)
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
                check = _without_program_figures(check, evidence.facts_text)
                check = _without_derived_figures(check, derived_numbers(text, pages))
                language = question_language(prepared.question)
                notes = [evidence.note] if evidence.note else []
                # D98: the check notes are a debug aid; the demo shows the answer alone. The
                # results still reach the `done` event and the ledger-side analyses.
                if self._settings.check_notes:
                    if check.unverified:
                        notes.append(check_note(check.unverified, language))
                    if check.mislabelled:
                        notes.append(label_note(check.mislabelled, language))
                    if any(c.status == "contradicted" for c in check.overstated):
                        notes.append(claim_note(check.overstated, language))
                    if any(a.status == "inconsistent" for a in arithmetic):
                        # D96: a difference the answer derived that its figures do not give.
                        notes.append(arithmetic_note(arithmetic, language))
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
            yield (
                self._usage([*extra_calls, result])
                if extra_calls
                else ChatEvent(
                    "usage",
                    {
                        "prompt_tokens": result.prompt_tokens,
                        "completion_tokens": result.completion_tokens,
                        "limit": self._settings.llm_context_limit,
                        # D100 (user): every call of this question, each under the limit.
                        "breakdown": [
                            {
                                "purpose": purpose,
                                "prompt_tokens": call.prompt_tokens,
                                "completion_tokens": call.completion_tokens,
                            }
                            for purpose, call in [*pre_calls, ("answer", result)]
                        ],
                    },
                )
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
                    "direction_issues": [
                        {
                            "sentence": d.sentence,
                            "left": d.left,
                            "right": d.right,
                            "status": d.status,
                            "detail": d.detail,
                        }
                        for d in directions
                    ],
                    "completeness": _completeness_payload(completeness),
                    "conclusion_issues": _conclusion_payload(conclusions),
                    "arithmetic_issues": _arithmetic_payload(arithmetic),
                    "analysis_status": overall_status(
                        check, directions, completeness, conclusions, arithmetic
                    )
                    if completeness is not None
                    else None,
                    "finish_reason": result.finish_reason.value,
                    "revision": None,
                    "navigation": navigation,
                    "correction": None,
                    "facts": evidence.facts_info,
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

    async def _standalone_question(
        self, prepared: PreparedQuestion
    ) -> tuple[str, bool | None, list[tuple[str, LLMResult]]]:
        """The question rewritten from the conversation so far, or as asked, and whether
        the model judged it a follow-up (None: no earlier turns, or the judgement failed).

        Without earlier turns there is nothing to resolve and no call is made. With
        them, one short call decides whether the question leans on the conversation
        (D99, the user's design: the model judges, not a keyword rule); a NEW question is
        used as asked. A follow-up is rewritten; a rewrite that fails, is cut short, is
        not a single line, exceeds the question budget or grew far beyond the question
        (it added material, D95) is not used: the question is kept as asked, and every
        call is in the ledger either way.
        """
        memory = build_memory(
            list(prepared.history), self._counter, budget_tokens=MEMORY_TOKEN_BUDGET
        )
        if not memory:
            return prepared.question, None, []
        calls: list[tuple[str, LLMResult]] = []
        context = CallContext(
            owner_id=prepared.actor.id,
            conversation_id=prepared.conversation_id,
            message_id=prepared.assistant_message_id,
        )
        follow_up: bool | None = None
        try:
            judged = await self._gateway.generate(
                follow_up_prompt(memory, prepared.question),
                purpose="follow_up",
                temperature=REWRITE_TEMPERATURE,
                max_output_tokens=FOLLOW_UP_MAX_OUTPUT_TOKENS,
                context=context,
            )
            follow_up = parse_follow_up(judged.text)
            calls.append(("follow_up", judged))
        except (LLMCallFailed, ContextBudgetExceeded) as error:
            logger.warning("Follow-up judgement skipped, the question is rewritten: %s", error)
        if follow_up is False:
            return prepared.question, False, calls
        # D100: the rewrite sees more of the conversation than the judgement, including the
        # head of a long previous answer (where its conclusions and figures are).
        rewrite_memory = build_memory(
            list(prepared.history),
            self._counter,
            budget_tokens=REWRITE_MEMORY_BUDGET,
            head_tokens=REWRITE_HEAD_TOKENS,
        )
        try:
            result = await self._gateway.generate(
                rewrite_prompt(rewrite_memory, prepared.question),
                purpose="rewrite",
                temperature=REWRITE_TEMPERATURE,
                max_output_tokens=self._settings.question_token_budget,
                context=context,
            )
        except (LLMCallFailed, ContextBudgetExceeded) as error:
            logger.warning("Rewrite skipped, question used as asked: %s", error)
            return prepared.question, follow_up, calls
        calls.append(("rewrite", result))
        if not result.finish_reason.is_complete:
            return prepared.question, follow_up, calls
        rewritten = clean_rewrite(result.text)
        if rewritten is None:
            return prepared.question, follow_up, calls
        length = self._counter.count(rewritten)
        grown = length > REWRITE_GROWTH_FACTOR * self._counter.count(prepared.question) + (
            REWRITE_GROWTH_ALLOWANCE
        )
        if length > self._settings.question_token_budget or grown:
            return prepared.question, follow_up, calls
        return rewritten, follow_up, calls

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
        self,
        prepared: PreparedQuestion,
        question: str,
        text: str,
        evidence: Evidence,
        aliases: Aliases | None = None,
    ) -> "Assessment":
        """Every deterministic check on one candidate answer, and what faults it (D69).
        Method aliases (D75) let the checks recognise a method by its stated operation."""
        cited = cited_indexes(text, len(evidence.sources))
        pages = await self._pages(prepared, evidence, cited)
        check = _without_program_figures(verify_numbers(text, pages, aliases), evidence.facts_text)
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
        return Assessment(
            text,
            cited,
            check,
            doubts,
            triggers,
            check_directions(text, pages, aliases),
            check_completeness(question, text, pages, aliases),
            check_conclusions(text, comparison_facts(matrix_cells_of_pages(pages), question)),
            check_arithmetic(text, pages),
        )

    def _notes(self, check: NumberCheck, evidence: Evidence, language: str) -> list[str]:
        check = _without_program_figures(check, evidence.facts_text)
        notes = [evidence.note] if evidence.note else []
        if not self._settings.check_notes:  # D98: debug mode only
            return notes
        if check.unverified:
            notes.append(check_note(check.unverified, language))
        if check.mislabelled:
            notes.append(label_note(check.mislabelled, language))
        if any(c.status == "contradicted" for c in check.overstated):
            notes.append(claim_note(check.overstated, language))
        return notes

    async def _answer_with_correction(
        self,
        prepared: PreparedQuestion,
        question: str,
        evidence: Evidence,
        received: list[str],
        navigation: dict[str, Any],
        earlier_calls: Sequence[LLMResult] = (),
    ) -> AsyncIterator[ChatEvent]:
        """D75 navigate mode: one answer call, then the deterministic checks and the
        deterministic correction of what the tables contradict (one pass, re-checked), then
        the text is sent in pieces. The answer is held in memory until then."""
        assert evidence.prompt is not None
        context = CallContext(
            owner_id=prepared.actor.id,
            conversation_id=prepared.conversation_id,
            message_id=prepared.assistant_message_id,
        )
        language = question_language(prepared.question)
        yield ChatEvent("stage", {"stage": "generating"})
        result = await self._gateway.generate(
            evidence.prompt,
            purpose="answer",
            temperature=prepared.temperature,
            max_output_tokens=ANSWER_MAX_OUTPUT_TOKENS,
            context=context,
        )
        calls = [*earlier_calls, result]
        if not result.finish_reason.is_complete:
            received.append(result.text)
            yield ChatEvent("stage", {"stage": "finalizing"})
            yield ChatEvent("delta", {"text": result.text})
            await self._finish(prepared, status="interrupted", content=result.text, answered=None)
            yield self._usage(calls)
            yield ChatEvent(
                "done",
                self._done_payload(
                    "interrupted",
                    None,
                    None,
                    result.finish_reason.value,
                    None,
                    navigation,
                    facts_info=evidence.facts_info,
                ),
            )
            return

        yield ChatEvent("stage", {"stage": "verifying"})
        aliases = self._aliases(evidence)
        text = strip_step_numbering(result.text.strip())
        cited = cited_indexes(text, len(evidence.sources))
        pages = await self._pages(prepared, evidence, cited)
        fixed: Correction = correct(text, pages, aliases=aliases)
        applied = self._settings.auto_correction
        if not applied:
            # The checks' proposals are recorded; the text stays as the model wrote it.
            fixed = Correction(text, fixed.edits, fixed.removed, fixed.remaining, fixed.uncertain)
        info: dict[str, Any] = {
            "applied": applied,
            "changed": applied and fixed.text != text,
            "edits": fixed.edits,
            "removed": fixed.removed,
            "remaining": fixed.remaining,
            "reverted": fixed.reverted,
            "uncertain": [
                {"sentence": i.sentence, "cue": i.cue, "left": i.left, "right": i.right}
                for i in fixed.uncertain
            ],
            "step_numbering_stripped": text != result.text.strip(),
        }
        if info["changed"]:
            yield ChatEvent("stage", {"stage": "correcting"})
        final = await self._assess(prepared, question, fixed.text, evidence, aliases)

        yield ChatEvent("stage", {"stage": "finalizing"})
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
            self._done_payload(
                "completed",
                answered,
                final,
                result.finish_reason.value,
                None,
                navigation,
                info,
                facts_info=evidence.facts_info,
            ),
        )

    @staticmethod
    def _aliases(evidence: Evidence) -> Aliases:
        """Method aliases read from the definitions in the evidence's chunk sources (D75)."""
        indexed = [
            (
                s["index"],
                RetrievedChunk(
                    uuid.uuid4(),
                    uuid.UUID(s["document_id"]),
                    s["filename"],
                    s["page_start"],
                    0,
                    s["snippet"] or "",
                    0,
                    None,
                    s["origin"],
                ),
            )
            for s in evidence.sources
            if s["kind"] == "chunk"
        ]
        cells = build_matrix(indexed)
        return method_aliases(method_definitions(indexed, {c.column for c in cells}))

    async def _answer_in_two_calls(
        self,
        prepared: PreparedQuestion,
        question: str,
        evidence: Evidence,
        received: list[str],
        navigation: dict[str, Any] | None = None,
        earlier_calls: Sequence[LLMResult] = (),
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
            temperature=prepared.temperature,
            max_output_tokens=ANSWER_MAX_OUTPUT_TOKENS,
            context=context,
        )
        calls = [*earlier_calls, first]
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
                    "interrupted",
                    None,
                    None,
                    first.finish_reason.value,
                    {"mode": mode},
                    navigation,
                    facts_info=evidence.facts_info,
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
            self._done_payload(
                "completed",
                answered,
                final,
                calls[-1].finish_reason.value,
                info,
                navigation,
                facts_info=evidence.facts_info,
            ),
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
        navigation: dict[str, Any] | None = None,
        correction: dict[str, Any] | None = None,
        facts_info: dict[str, Any] | None = None,
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
            "direction_issues": [
                {
                    "sentence": d.sentence,
                    "left": d.left,
                    "right": d.right,
                    "status": d.status,
                    "detail": d.detail,
                }
                for d in (assessment.directions if assessment else [])
            ],
            "completeness": _completeness_payload(assessment.completeness if assessment else None),
            "conclusion_issues": _conclusion_payload(assessment.conclusions if assessment else []),
            "arithmetic_issues": _arithmetic_payload(assessment.arithmetic if assessment else []),
            "analysis_status": overall_status(
                check,
                assessment.directions if assessment else [],
                assessment.completeness
                if assessment
                else Completeness("not_applicable", [], [], None),
                assessment.conclusions if assessment else [],
                assessment.arithmetic if assessment else [],
            )
            if assessment
            else None,
            "finish_reason": finish_reason,
            "revision": revision,
            "navigation": navigation,
            "correction": correction,
            "facts": facts_info,
        }

    async def _search(
        self, prepared: PreparedQuestion, question: str
    ) -> tuple[list[RetrievedChunk] | None, list[float]]:
        """The retrieved chunks with their table context (or None when nothing is close
        enough, AC-15: then nothing is sent to the model and the user is told so), and
        the question's embedding, which the navigate mode reuses."""
        async with self._sessions() as session:
            retrieval = RetrievalService(session, self._embedder, self._settings)
            embedding = await retrieval.embed(question)
            chunks = await retrieval.search(prepared.actor, prepared.scope, question, embedding)
            best = chunks[0].score if chunks else None
            if best is not None and best >= self._settings.min_similarity:
                return await retrieval.with_table_context(prepared.actor, chunks), embedding
            # D88 (user's decision): nothing is similar enough, but the model is asked all
            # the same, with the closest passages to judge for itself — a question put in
            # other words than the document's, a question about the platform, small talk.
            # It is told to say so when the documents do not cover the question.
            logger.info(
                "Best similarity %s below %s: the closest passages go to the model as such",
                None if best is None else round(best, 3),
                self._settings.min_similarity,
            )
            closest = chunks[:BELOW_THRESHOLD_PASSAGES]
            # D99: a follow-up that retrieval cannot place keeps the previous turn's sources
            # — "where does it lose?" after an answer built on a table needs that table.
            previous = await retrieval.previous_sources(prepared.actor, prepared.previous_chunk_ids)
            seen = {c.chunk_id for c in previous}
            merged = [*previous, *[c for c in closest if c.chunk_id not in seen]]
            return await retrieval.with_table_context(prepared.actor, merged), embedding

    async def _summary_tree_skipped(self, prepared: PreparedQuestion) -> bool:
        """Whether every document in scope was uploaded without a summary tree (D91)."""
        async with self._sessions() as session:
            states = await SummaryRepository(session).states(
                prepared.actor.id, prepared.scope.document_ids
            )
        return bool(states) and all(state.summary_status == "skipped" for state in states)

    async def _document_cards(self, prepared: PreparedQuestion) -> list[StoredSummary]:
        """The whole-document summaries of the documents in scope, for the prompt's
        "Documents in scope" lines (D88)."""
        async with self._sessions() as session:
            summaries = await SummaryRepository(session).ready_summaries(
                prepared.actor.id, prepared.scope.document_ids
            )
        return [s for s in summaries if s.level == "document"]

    def _evidence_from_chunks(
        self,
        prepared: PreparedQuestion,
        question: str,
        chunks: list[RetrievedChunk] | None,
        preamble: str = "",
        added: Sequence[RetrievedChunk] = (),
        cards: Sequence[StoredSummary] = (),
    ) -> Evidence:
        if chunks is None:
            return Evidence(None, [], _NOTHING_RELEVANT[question_language(prepared.question)])
        candidates = [*chunks, *added]
        facts_info = None
        if self._settings.answer_facts != "off":
            candidates, block, facts_info = self._with_facts(question, candidates)
            preamble = block + preamble
        prompt, used = build_answer_prompt(
            question,
            candidates,
            self._counter,
            EVIDENCE_TOKEN_BUDGET,
            preamble=preamble,
            documents=cards,
            conversation=self._conversation(prepared),
            # The answer's language follows the user's own words, not the rewrite's (D99).
            language=question_language(prepared.question),
        )
        sources = [source_payload(index, chunk) for index, chunk in enumerate(used, start=1)]
        return Evidence(prompt, sources, "", facts_info, preamble if facts_info else "")

    def _conversation(self, prepared: PreparedQuestion) -> str:
        """The conversation so far for the answer prompt (D99), within its budget; empty
        when the setting is off or there are no earlier turns."""
        mode = self._settings.answer_context
        if mode == "off" or (mode == "follow_up" and prepared.follow_up is not True):
            return ""
        return build_memory(
            list(prepared.history), self._counter, budget_tokens=CONVERSATION_BUDGET
        )

    def _with_facts(
        self, question: str, candidates: list[RetrievedChunk]
    ) -> tuple[list[RetrievedChunk], str, dict[str, Any]]:
        """D87 experiment A. inject: the comparison facts that bear on the question, as a
        block before the sources. replace: also, a table chunk whose cells the facts come
        from is shown as the rows of the columns the question names (caption kept, same
        source number); a table whose columns the question does not name is left whole."""
        indexed = list(enumerate(candidates, start=1))
        cells = build_matrix(indexed)
        facts = comparison_facts(cells, question)
        block = facts_block(facts, self._counter, budget=FACTS_TOKEN_BUDGET)
        replaced: list[int] = []
        if self._settings.answer_facts == "replace" and facts:
            named = named_columns(cells, question)
            rewritten = []
            for index, chunk in indexed:
                own = [c for c in cells if c.source_index == index]
                minimal = (
                    minimal_table_text(own, chunk.text.splitlines()[0], named) if own else None
                )
                if minimal is None:
                    rewritten.append(chunk)
                else:
                    replaced.append(index)
                    rewritten.append(
                        RetrievedChunk(
                            chunk.chunk_id,
                            chunk.document_id,
                            chunk.filename,
                            chunk.page,
                            chunk.ordinal,
                            minimal,
                            self._counter.count(minimal),
                            chunk.score,
                            chunk.origin,
                        )
                    )
            candidates = rewritten
        info = {
            "mode": self._settings.answer_facts,
            "cells": len(cells),
            "facts": len(facts),
            "block_tokens": self._counter.count(block) if block else 0,
            "replaced_sources": replaced,
        }
        return candidates, block, info

    async def _retrieval_evidence(self, prepared: PreparedQuestion, question: str) -> Evidence:
        chunks, _ = await self._search(prepared, question)
        return self._evidence_from_chunks(prepared, question, chunks)

    async def _summary_evidence(
        self,
        prepared: PreparedQuestion,
        question: str,
        *,
        preamble: str = "",
        added: Sequence[RetrievedChunk] = (),
        navigation: dict[str, Any] | None = None,
    ) -> Evidence:
        """The stored summaries of the documents in scope; the ones without are named.
        Chunks the Navigator's targets selected (D71/D73) come after the summaries."""
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
            question,
            summaries,
            self._counter,
            evidence_budget=EVIDENCE_TOKEN_BUDGET,
            preamble=preamble,
            extra_chunks=list(added),
            language=language,
        )
        if navigation is not None:
            # The prompt builder has the last word on the budget: a selected chunk it
            # left out is recorded as such.
            kept = {c.chunk_id for c in used if isinstance(c, RetrievedChunk)}
            dropped = {c.ordinal for c in added if c.chunk_id not in kept}
            for entry in navigation["log"]:
                if entry["kept"] and entry["target"] is not None and entry["ordinal"] in dropped:
                    entry["kept"] = False
                    entry["reason"] = "over the evidence budget"
            navigation["kept"] = len(kept)
            navigation["excluded_budget"] = sum(
                1 for e in navigation["log"] if e["reason"] == "over the evidence budget"
            )
        sources = [
            source_payload(index, item)
            if isinstance(item, RetrievedChunk)
            else summary_source_payload(index, item)
            for index, item in enumerate(used, start=1)
        ]
        return Evidence(prompt, sources, note)

    async def _document_map(
        self, prepared: PreparedQuestion
    ) -> tuple[list[MapEntry], list[StoredSummary]]:
        """Sections and subsections (from the heading lines of the chunks; the section
        summaries where no heading was recognised) and table/figure captions of the
        documents in scope (D71, D73), with the stored summaries themselves."""
        async with self._sessions() as session:
            summaries = await SummaryRepository(session).ready_summaries(
                prepared.actor.id, prepared.scope.document_ids
            )
            repository = RetrievalRepository(session)
            documents = prepared.scope.document_ids
            captions = await repository.caption_lines(prepared.actor.id, documents)
            headings = await repository.heading_lines(prepared.actor.id, documents)
            pages = await repository.chunk_pages(prepared.actor.id, documents)
        return build_map(summaries, captions, headings, pages), summaries

    async def _navigate(
        self,
        prepared: PreparedQuestion,
        question: str,
        entries: list[MapEntry],
        chunks: list[RetrievedChunk],
        embedding: list[float] | None,
        *,
        budget: int,
    ) -> tuple[dict[str, Any], list[PlanItem], list[RetrievedChunk], LLMResult | None]:
        """D73 navigate mode: ask for targets (place, need, priority), locate each on the
        map, rank its candidate chunks within the located range by similarity to the
        question and to the need (tables and figures by structure), and let the targets
        take turns at the remaining budget. A plan call that fails or does not fit
        leaves the evidence as retrieved."""
        prompt, max_output = build_navigation_prompt(
            question,
            entries,
            describe_retrieved(chunks, entries),
            self._counter,
            self._settings.llm_context_limit,
        )
        context = CallContext(
            owner_id=prepared.actor.id,
            conversation_id=prepared.conversation_id,
            message_id=prepared.assistant_message_id,
        )
        info: dict[str, Any] = {
            "map_entries": len(entries),
            "plan": None,
            "items": [],
            "located": 0,
            "fetched": 0,
            "kept": 0,
            "excluded_budget": 0,
            "skipped": None,
            "budget": budget,
            # The retrieved sources' tokens; evidence_tokens becomes the total once the
            # targets' chunks are added.
            "retrieved_tokens": sum(c.token_count for c in chunks),
            "evidence_tokens": sum(c.token_count for c in chunks),
            "embedding": {"texts": 0, "failed": None},
            "log": [
                {
                    "ordinal": c.ordinal,
                    "page": c.page,
                    "kept": True,
                    "reason": c.origin,
                    "target": None,
                    "score": None,
                }
                for c in chunks
            ],
        }
        try:
            result = await self._gateway.generate(
                prompt,
                purpose="navigate",
                max_output_tokens=max_output,
                context=context,
                temperature=self._settings.navigation_temperature,
            )
        except ContextBudgetExceeded:
            info["skipped"] = "budget"
            return info, [], [], None
        except LLMCallFailed as error:
            logger.warning("Navigation call failed, answering from the retrieval: %s", error)
            info["skipped"] = "failed"
            return info, [], [], None
        items = parse_plan(result.text, entries)
        info["plan"] = result.text
        info["located"] = sum(1 for i in items if i.located)

        # D74: what the retrieved sources already cover, by structure. A required target
        # that is covered fetches nothing; when every required target is covered, the
        # supplementary ones fetch nothing either.
        coverage = {id(item): coverage_of(item, chunks) for item in items}
        required_items = [i for i in items if i.priority == "required"]
        all_required_covered = bool(required_items) and all(
            coverage[id(i)][0] == COVERED for i in required_items
        )
        info["coverage"] = [
            {"location": i.location, "status": coverage[id(i)][0], "reason": coverage[id(i)][1]}
            for i in items
        ]
        # One embedding call for every distinct need; when it fails, the question alone
        # ranks the candidates (and a question without an embedding leaves document order).
        needs = list(
            dict.fromkeys(
                i.need
                for i in items
                if i.located
                and i.need
                and not (i.priority == "required" and coverage[id(i)][0] == COVERED)
                and not (i.priority != "required" and all_required_covered)
            )
        )
        need_vectors: dict[str, list[float]] = {}
        if needs:
            info["embedding"]["texts"] = len(needs)
            try:
                need_vectors = dict(zip(needs, await self._embedder.embed(needs), strict=True))
            except EmbeddingError as error:
                info["embedding"]["failed"] = _describe(error)["code"]
                logger.warning("Need embeddings failed, ranking by the question only: %s", error)

        targets: list[TargetCandidates] = []
        scope = prepared.scope.document_ids
        async with self._sessions() as session:
            repository = RetrievalRepository(session)
            for item in items:
                status = coverage[id(item)][0]
                document_id = (
                    item.entry.document_id
                    if item.entry
                    else (scope[0] if len(scope) == 1 else None)
                )
                if not item.located or document_id is None:
                    # Not on the map, or an explicit page with several documents in scope.
                    targets.append(TargetCandidates(item, [], status))
                    continue
                if (item.priority == "required" and status == COVERED) or (
                    item.priority != "required" and all_required_covered
                ):
                    targets.append(TargetCandidates(item, [], status))
                    continue
                need_vector = need_vectors.get(item.need)
                vectors = [v for v in (embedding, need_vector) if v is not None]
                scored = partial(_scored, embedding is not None, need_vector is not None)

                entry = item.entry
                if entry is not None and entry.kind in ("table", "figure"):
                    # By structure: the caption's chunk, then the discussion after it (D62).
                    assert entry.ordinal_start is not None
                    ranked = await repository.rank_chunks(
                        prepared.actor.id,
                        document_id,
                        vectors,
                        ordinals=(entry.ordinal_start, entry.ordinal_start),
                        limit=1,
                    )
                    candidates = [
                        EvidenceCandidate(c, *scored(sc), structural=True) for c, sc in ranked
                    ]
                    if ranked:
                        following = await repository.chunks_after(
                            prepared.actor.id,
                            document_id,
                            entry.ordinal_start,
                            limit=MAX_FOLLOWING,
                        )
                        candidates.extend(
                            EvidenceCandidate(c, None, None, structural=True)
                            for c in table_context(ranked[0][0], following, set())
                        )
                else:
                    by_chunks = (
                        entry is not None
                        and entry.ordinal_start is not None
                        and entry.ordinal_end is not None
                    )
                    ranked = await repository.rank_chunks(
                        prepared.actor.id,
                        document_id,
                        vectors,
                        ordinals=(entry.ordinal_start, entry.ordinal_end)  # type: ignore[union-attr,arg-type]
                        if by_chunks
                        else None,
                        pages=None if by_chunks else item.pages,
                        limit=NAVIGATION_CANDIDATES_PER_TARGET,
                    )
                    candidates = [EvidenceCandidate(c, *scored(sc)) for c, sc in ranked]
                info["fetched"] += len(candidates)
                targets.append(TargetCandidates(item, candidates, status))
        selection = select_evidence(
            chunks,
            targets,
            budget=budget + sum(c.token_count for c in chunks),
            floor=self._settings.min_similarity,
        )
        added = selection.chunks[len(chunks) :]
        info["log"] = selection.log
        info["items"] = [
            {"text": i.text, "located": i.located, "pages": i.pages, **record}
            for i, record in zip(items, selection.targets, strict=True)
        ]
        info["kept"] = len(added)
        info["excluded_budget"] = sum(
            1 for e in selection.log if e["reason"] == "over the evidence budget"
        )
        info["evidence_tokens"] = selection.evidence_tokens
        info["unmet_required"] = selection.unmet_required
        info["supplementary_used"] = selection.supplementary_used
        return info, items, added, result

    async def _finish(
        self, prepared: PreparedQuestion, *, status: str, content: str, answered: bool | None
    ) -> None:
        async with self._sessions() as session, session.begin():
            await ChatRepository(session).finish(
                prepared.assistant_message_id, status=status, content=content, answered=answered
            )


def _previous_chunk_ids(earlier: Sequence[Message]) -> tuple[uuid.UUID, ...]:
    """The chunk ids the last completed answer cited (D99); none when it had no chunk
    sources (a summary answer) or when the sources predate the chunk_id field."""
    for message in reversed(earlier):
        if message.role == "assistant" and message.status == "completed":
            ids = []
            for source in message.sources:
                if source.get("kind") == "chunk" and source.get("chunk_id"):
                    try:
                        ids.append(uuid.UUID(str(source["chunk_id"])))
                    except ValueError:
                        continue
            return tuple(ids)
    return ()


def _without_derived_figures(check: NumberCheck, derived: Sequence[str]) -> NumberCheck:
    """The check without the "unverified" figures the answer derived from two table
    figures (D96): those are judged by arithmetic, not looked for on the pages."""
    if not derived or not check.unverified:
        return check
    kept = [n for n in check.unverified if n not in set(derived)]
    if len(kept) == len(check.unverified):
        return check
    return NumberCheck(check.verified, kept, check.mislabelled, check.unresolved, check.overstated)


def _without_program_figures(check: NumberCheck, facts_text: str) -> NumberCheck:
    """The check without the "unverified" figures that the injected facts block states
    (D88): "13 of 16", "-1.2 pp" are the program's arithmetic, repeated by the answer."""
    if not facts_text or not check.unverified:
        return check
    stated = {n.replace(",", "").rstrip("%") for n in numbers_in(facts_text)}
    kept = [n for n in check.unverified if n.replace(",", "").rstrip("%") not in stated]
    if len(kept) == len(check.unverified):
        return check
    return NumberCheck(check.verified, kept, check.mislabelled, check.unresolved, check.overstated)


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


def _conclusion_payload(issues: Sequence[ConclusionIssue]) -> list[dict[str, Any]]:
    return [{"sentence": i.sentence, "status": i.status, "detail": i.detail} for i in issues]


def _arithmetic_payload(issues: Sequence[ArithmeticIssue]) -> list[dict[str, Any]]:
    return [
        {
            "sentence": i.sentence,
            "stated": i.stated,
            "computed": i.computed,
            "status": i.status,
            "detail": i.detail,
        }
        for i in issues
    ]


def _completeness_payload(completeness: Completeness | None) -> dict[str, Any]:
    c = completeness or Completeness("not_applicable", [], [], None)
    return {
        "status": c.status,
        "required": c.required,
        "missing": c.missing,
        "condition": c.condition,
    }


def _scored(
    has_question: bool, has_need: bool, scores: list[float]
) -> tuple[float | None, float | None]:
    """A ranked row's scores split into (question score, need score): the question's
    vector comes first when it was used, the need's second."""
    values = iter(scores)
    question_score = next(values) if has_question else None
    need_score = next(values) if has_need else None
    return question_score, need_score


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
