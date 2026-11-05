"""Data access for conversations and their messages.

Every query takes the owner: a conversation that belongs to someone else is
indistinguishable from one that does not exist.
"""

import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Conversation, Message


class ConversationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def add(self, owner_id: uuid.UUID, title: str) -> Conversation:
        conversation = Conversation(owner_id=owner_id, title=title)
        self._db.add(conversation)
        await self._db.flush()
        await self._db.refresh(conversation)
        return conversation

    async def get(self, owner_id: uuid.UUID, conversation_id: uuid.UUID) -> Conversation | None:
        return await self._db.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id, Conversation.owner_id == owner_id
            )
        )

    async def list_for_owner(self, owner_id: uuid.UUID) -> list[Conversation]:
        result = await self._db.scalars(
            select(Conversation)
            .where(Conversation.owner_id == owner_id)
            .order_by(Conversation.updated_at.desc(), Conversation.id)
        )
        return list(result)

    async def messages(self, owner_id: uuid.UUID, conversation_id: uuid.UUID) -> list[Message]:
        """The messages of the owner's conversation, oldest first."""
        result = await self._db.scalars(
            select(Message)
            .join(Conversation, Conversation.id == Message.conversation_id)
            .where(Message.conversation_id == conversation_id, Conversation.owner_id == owner_id)
            .order_by(Message.created_at, Message.id)
        )
        return list(result)

    async def delete(self, conversation: Conversation) -> None:
        # Messages go with it (ON DELETE CASCADE); LLM call records keep their
        # row and lose the reference (ON DELETE SET NULL).
        await self._db.execute(delete(Conversation).where(Conversation.id == conversation.id))
