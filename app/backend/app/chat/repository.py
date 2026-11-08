"""Data access for the messages of a question and its answer.

The conversation is checked against its owner by the conversation service
before anything here is called. Updates to an answer in progress address it by
message id and only apply while it is still unfinished, so the first outcome
recorded stands.
"""

import uuid
from typing import Any

from sqlalchemy import func, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Conversation, Message

UNFINISHED = ("pending", "streaming")
TITLE_LENGTH = 40


class ChatRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def add_exchange(
        self, conversation: Conversation, question: str, temperature: float | None = None
    ) -> tuple[uuid.UUID, uuid.UUID]:
        """Store the question and an empty, pending answer (with the temperature its
        answer call will use, AC-60). Returns their ids."""
        # clock_timestamp() differs between the two rows; now() would be the same
        # for both and leave their order undefined.
        user = Message(
            conversation_id=conversation.id,
            role="user",
            content=question,
            status="completed",
            created_at=func.clock_timestamp(),
        )
        self._db.add(user)
        await self._db.flush()
        assistant = Message(
            conversation_id=conversation.id,
            role="assistant",
            content="",
            status="pending",
            temperature=temperature,
            created_at=func.clock_timestamp(),
        )
        self._db.add(assistant)
        if not conversation.title:
            conversation.title = question[:TITLE_LENGTH]
        conversation.updated_at = func.now()
        await self._db.flush()
        return user.id, assistant.id

    async def start_streaming(self, message_id: uuid.UUID, sources: list[dict[str, Any]]) -> None:
        await self._db.execute(
            update(Message)
            .where(Message.id == message_id, Message.status == "pending")
            .values(status="streaming", sources=sources)
        )

    async def save_content(self, message_id: uuid.UUID, content: str) -> None:
        await self._db.execute(
            update(Message)
            .where(Message.id == message_id, Message.status == "streaming")
            .values(content=content)
        )

    async def finish(
        self, message_id: uuid.UUID, *, status: str, content: str, answered: bool | None
    ) -> None:
        await self._db.execute(
            update(Message)
            .where(Message.id == message_id, Message.status.in_(UNFINISHED))
            .values(status=status, content=content, answered=answered)
        )

    async def interrupt_unfinished(self) -> int:
        """At startup: an answer still in progress was cut off by the previous shutdown."""
        result = await self._db.execute(
            update(Message)
            .where(Message.role == "assistant", Message.status.in_(UNFINISHED))
            .values(status="interrupted")
        )
        assert isinstance(result, CursorResult)
        return result.rowcount
