"""Answering a question in a conversation, from the asker's own documents.

    check -> store the question and a pending answer -> retrieve -> pack the
    prompt within its budget -> stream the answer -> read its citations

The checks happen before anything is stored or sent: a question that fails one
creates no message and causes no LLM call.
"""

import asyncio
import logging
import uuid
from collections.abc import AsyncIterator
from contextlib import aclosing
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.chat.prompting import build_answer_prompt, cited_indexes, source_payload
from app.chat.repository import ChatRepository
from app.conversations.service import ConversationService
from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.llm.embedding import Embedder, EmbeddingError
from app.llm.gateway import CallContext, ContextBudgetExceeded, LLMCallFailed, LLMGateway, LLMResult
from app.llm.tokenizer import TokenCounter
from app.models import User
from app.retrieval.service import RetrievalService, SearchScope

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
            # Rewriting the question and recognising summary questions come in P3.
            yield ChatEvent(
                "route", {"type": "retrieval", "standalone_question": prepared.question}
            )

            async with self._sessions() as session:
                chunks = await RetrievalService(session, self._embedder, self._settings).search(
                    prepared.actor, prepared.scope, prepared.question
                )
            prompt, used = build_answer_prompt(
                prepared.question, chunks, self._counter, EVIDENCE_TOKEN_BUDGET
            )
            sources = [source_payload(index, chunk) for index, chunk in enumerate(used, start=1)]
            async with self._sessions() as session, session.begin():
                await ChatRepository(session).start_streaming(
                    prepared.assistant_message_id, sources
                )
            yield ChatEvent("sources", sources)

            result: LLMResult | None = None
            context = CallContext(
                owner_id=prepared.actor.id,
                conversation_id=prepared.conversation_id,
                message_id=prepared.assistant_message_id,
            )
            stream = self._gateway.stream(
                prompt,
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

            text = "".join(received)
            cited = cited_indexes(text, len(sources))
            # A stream that ended normally is not necessarily a finished answer:
            # only a natural stop is. Anything else is kept, marked interrupted.
            complete = result.finish_reason.is_complete
            status = "completed" if complete else "interrupted"
            answered = bool(cited) if complete else None
            await self._finish(prepared, status=status, content=text, answered=answered)
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

    async def _finish(
        self, prepared: PreparedQuestion, *, status: str, content: str, answered: bool | None
    ) -> None:
        async with self._sessions() as session, session.begin():
            await ChatRepository(session).finish(
                prepared.assistant_message_id, status=status, content=content, answered=answered
            )


def _describe(error: Exception) -> dict[str, str]:
    if isinstance(error, LLMCallFailed):
        return {"code": error.code, "detail": error.detail}
    if isinstance(error, ContextBudgetExceeded):
        return {"code": "CONTEXT_BUDGET_EXCEEDED", "detail": str(error)}
    return {"code": "EMBEDDING_UNAVAILABLE", "detail": str(error)}
