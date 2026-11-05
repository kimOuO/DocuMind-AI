"""The ledger of LLM calls: one row per call that was actually sent.

A row is written before the request goes out and updated when the call ends,
so failed and interrupted calls leave a record too. The measured columns hold
only what Ollama reported; when that is not available they stay NULL, and the
estimate made before sending is never copied into them.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import ColumnElement, and_, func, or_, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LLMCall

RESTART_REASON = "The call was interrupted because the service restarted."
INPUT_EXCEEDS_CONTEXT = "INPUT_EXCEEDS_CONTEXT"

# A call counts as measured only when Ollama reported both numbers.
MEASURED = and_(LLMCall.prompt_tokens.is_not(None), LLMCall.completion_tokens.is_not(None))


@dataclass(frozen=True)
class LedgerSummary:
    measured_count: int
    max_measured_total: int | None
    unmeasured_count: int
    max_unmeasured_upper_bound: int | None
    underestimate_events: int


@dataclass(frozen=True)
class CallContext:
    """Who a call is made for, and what it belongs to."""

    owner_id: uuid.UUID
    conversation_id: uuid.UUID | None = None
    message_id: uuid.UUID | None = None
    document_id: uuid.UUID | None = None


class LedgerRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def open(
        self,
        context: CallContext,
        *,
        purpose: str,
        model: str,
        estimated_prompt_tokens: int,
        max_output_tokens: int,
    ) -> uuid.UUID:
        """Record a call that passed the budget check and is about to be sent."""
        call = LLMCall(
            owner_id=context.owner_id,
            conversation_id=context.conversation_id,
            message_id=context.message_id,
            document_id=context.document_id,
            purpose=purpose,
            model=model,
            status="pending",
            estimated_prompt_tokens=estimated_prompt_tokens,
            max_output_tokens=max_output_tokens,
        )
        self._db.add(call)
        await self._db.flush()
        return call.id

    async def complete(
        self,
        call_id: uuid.UUID,
        *,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        finish_reason: str,
        duration_ms: int,
    ) -> None:
        await self._close(
            call_id,
            status="completed",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            finish_reason=finish_reason,
            duration_ms=duration_ms,
        )

    async def fail(
        self,
        call_id: uuid.UUID,
        *,
        error: str,
        duration_ms: int,
        received_output_tokens_estimated: int | None = None,
    ) -> None:
        await self._close(
            call_id,
            status="failed",
            error=error,
            duration_ms=duration_ms,
            received_output_tokens_estimated=received_output_tokens_estimated,
        )

    async def interrupt(
        self,
        call_id: uuid.UUID,
        *,
        finish_reason: str,
        duration_ms: int,
        received_output_tokens_estimated: int,
    ) -> None:
        await self._close(
            call_id,
            status="interrupted",
            finish_reason=finish_reason,
            duration_ms=duration_ms,
            received_output_tokens_estimated=received_output_tokens_estimated,
        )

    async def _close(self, call_id: uuid.UUID, **values: object) -> None:
        # Only a pending call can be closed: the first outcome recorded stands.
        await self._db.execute(
            update(LLMCall)
            .where(LLMCall.id == call_id, LLMCall.status == "pending")
            .values(**values)
        )

    async def fail_pending(self, reason: str) -> int:
        """At startup: a call still pending was cut off by the previous shutdown."""
        result = await self._db.execute(
            update(LLMCall).where(LLMCall.status == "pending").values(status="failed", error=reason)
        )
        assert isinstance(result, CursorResult)
        return result.rowcount

    async def list_for_owner(
        self,
        owner_id: uuid.UUID,
        *,
        conversation_id: uuid.UUID | None,
        document_id: uuid.UUID | None,
        limit: int,
    ) -> list[LLMCall]:
        result = await self._db.scalars(
            select(LLMCall)
            .where(*_filters(owner_id, conversation_id, document_id))
            .order_by(LLMCall.created_at.desc(), LLMCall.id)
            .limit(limit)
        )
        return list(result)

    async def summarise(
        self,
        owner_id: uuid.UUID,
        *,
        conversation_id: uuid.UUID | None,
        document_id: uuid.UUID | None,
    ) -> LedgerSummary:
        """Totals over all of the owner's matching calls, measured and unmeasured apart."""
        underestimated = or_(
            LLMCall.prompt_tokens > LLMCall.estimated_prompt_tokens,
            # Ollama refused the input: the local count had let it through.
            LLMCall.error.like(f"{INPUT_EXCEEDS_CONTEXT}%"),
        )
        row = (
            await self._db.execute(
                select(
                    func.count().filter(MEASURED),
                    func.max(LLMCall.prompt_tokens + LLMCall.completion_tokens).filter(MEASURED),
                    func.count().filter(~MEASURED),
                    func.max(LLMCall.estimated_prompt_tokens + LLMCall.max_output_tokens).filter(
                        ~MEASURED
                    ),
                    func.count().filter(underestimated),
                ).where(*_filters(owner_id, conversation_id, document_id))
            )
        ).one()
        return LedgerSummary(*row)


def _filters(
    owner_id: uuid.UUID, conversation_id: uuid.UUID | None, document_id: uuid.UUID | None
) -> list[ColumnElement[bool]]:
    filters: list[ColumnElement[bool]] = [LLMCall.owner_id == owner_id]
    if conversation_id is not None:
        filters.append(LLMCall.conversation_id == conversation_id)
    if document_id is not None:
        filters.append(LLMCall.document_id == document_id)
    return filters
