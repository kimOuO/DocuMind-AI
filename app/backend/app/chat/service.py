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

from app.chat.prompting import (
    build_answer_prompt,
    build_summary_prompt,
    cited_indexes,
    question_language,
    source_payload,
    summary_source_payload,
)
from app.chat.repository import ChatRepository
from app.chat.routing import question_type
from app.conversations.service import ConversationService
from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.llm.embedding import Embedder, EmbeddingError
from app.llm.gateway import CallContext, ContextBudgetExceeded, LLMCallFailed, LLMGateway, LLMResult
from app.llm.tokenizer import TokenCounter
from app.models import User
from app.retrieval.service import RetrievalService, SearchScope
from app.summarization.repository import DocumentSummaryState, SummaryRepository

logger = logging.getLogger(__name__)

# Budget of one answer call (docs/02-specs/02-architecture.md, section 4.3).
ANSWER_MAX_OUTPUT_TOKENS = 2_500
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


@dataclass(frozen=True)
class ChatEvent:
    name: str
    data: Any


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

        user_message_id, assistant_message_id = await ChatRepository(self._db).add_exchange(
            conversation, question
        )
        await self._db.commit()
        return PreparedQuestion(
            actor, conversation.id, user_message_id, assistant_message_id, question, scope
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
            # Rewriting the question from the conversation so far comes with AC-16.
            kind = question_type(prepared.question)
            yield ChatEvent("route", {"type": kind, "standalone_question": prepared.question})

            evidence = (
                await self._summary_evidence(prepared)
                if kind == "summary"
                else await self._retrieval_evidence(prepared)
            )
            async with self._sessions() as session, session.begin():
                await ChatRepository(session).start_streaming(
                    prepared.assistant_message_id, evidence.sources
                )
            yield ChatEvent("sources", evidence.sources)

            if evidence.prompt is None:
                # No summary to answer from: say so, without spending a call (AC-42).
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
                        "finish_reason": None,
                    },
                )
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
            if complete and evidence.note:
                # Documents whose summary was not available are named after the answer.
                received.append("\n\n" + evidence.note)
                yield ChatEvent("delta", {"text": "\n\n" + evidence.note})
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
                    "unverified_numbers": [],
                    "finish_reason": result.finish_reason.value,
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

    async def _retrieval_evidence(self, prepared: PreparedQuestion) -> Evidence:
        async with self._sessions() as session:
            chunks = await RetrievalService(session, self._embedder, self._settings).search(
                prepared.actor, prepared.scope, prepared.question
            )
        prompt, used = build_answer_prompt(
            prepared.question, chunks, self._counter, EVIDENCE_TOKEN_BUDGET
        )
        sources = [source_payload(index, chunk) for index, chunk in enumerate(used, start=1)]
        return Evidence(prompt, sources, "")

    async def _summary_evidence(self, prepared: PreparedQuestion) -> Evidence:
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
            prepared.question, summaries, self._counter, evidence_budget=EVIDENCE_TOKEN_BUDGET
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
    return {"code": "EMBEDDING_UNAVAILABLE", "detail": str(error)}
