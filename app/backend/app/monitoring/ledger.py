"""The LLM call ledger as a user may see it: only their own calls."""

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.ledger import LedgerRepository, LedgerSummary
from app.models import LLMCall, User


@dataclass(frozen=True)
class LedgerReport:
    summary: LedgerSummary
    calls: list[LLMCall]


class LedgerService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = LedgerRepository(db)

    async def report(
        self,
        actor: User,
        *,
        conversation_id: uuid.UUID | None,
        document_id: uuid.UUID | None,
        limit: int,
    ) -> LedgerReport:
        """The actor's calls, newest first, with totals over all that match.

        The filters narrow the actor's own calls; they can never reach anyone
        else's, whatever ids are passed.
        """
        summary = await self._repo.summarise(
            actor.id, conversation_id=conversation_id, document_id=document_id
        )
        calls = await self._repo.list_for_owner(
            actor.id, conversation_id=conversation_id, document_id=document_id, limit=limit
        )
        return LedgerReport(summary, calls)
