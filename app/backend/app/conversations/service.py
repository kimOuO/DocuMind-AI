"""Rules for creating, listing, reading and deleting conversations.

Every method takes the acting user explicitly.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.repository import ConversationRepository
from app.core.errors import ApiError
from app.models import Conversation, Message, User


@dataclass(frozen=True)
class ConversationView:
    conversation: Conversation
    messages: list[Message]


class ConversationService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = ConversationRepository(db)

    async def create(self, actor: User, title: str | None) -> Conversation:
        conversation = await self._repo.add(actor.id, (title or "").strip())
        await self._db.commit()
        return conversation

    async def list_conversations(self, actor: User) -> list[Conversation]:
        return await self._repo.list_for_owner(actor.id)

    async def get(self, actor: User, conversation_id: uuid.UUID) -> ConversationView:
        conversation = await self.owned(actor, conversation_id)
        return ConversationView(conversation, await self._repo.messages(actor.id, conversation_id))

    async def delete(self, actor: User, conversation_id: uuid.UUID) -> None:
        conversation = await self.owned(actor, conversation_id)
        await self._repo.delete(conversation)
        await self._db.commit()

    async def owned(self, actor: User, conversation_id: uuid.UUID) -> Conversation:
        conversation = await self._repo.get(actor.id, conversation_id)
        if conversation is None:
            # Same answer whether it does not exist or belongs to someone else.
            raise ApiError(404, "CONVERSATION_NOT_FOUND", "Conversation not found.")
        return conversation
