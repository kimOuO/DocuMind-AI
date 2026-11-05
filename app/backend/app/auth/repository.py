"""Data access for users and sessions."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Session, User


class AuthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_user_by_username(self, username: str) -> User | None:
        return await self._db.scalar(select(User).where(User.username == username))

    async def add_user(self, username: str, password_hash: str, display_name: str) -> User:
        user = User(username=username, password_hash=password_hash, display_name=display_name)
        self._db.add(user)
        await self._db.flush()
        await self._db.refresh(user)
        return user

    async def touch_last_login(self, user: User) -> None:
        user.last_login_at = datetime.now(UTC)
        await self._db.flush()
        await self._db.refresh(user)

    async def add_session(self, user_id: uuid.UUID, token_hash: str, expires_at: datetime) -> None:
        self._db.add(Session(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
        await self._db.flush()

    async def get_session_with_user(self, token_hash: str) -> tuple[Session, User] | None:
        row = (
            await self._db.execute(
                select(Session, User)
                .join(User, User.id == Session.user_id)
                .where(Session.token_hash == token_hash)
            )
        ).first()
        return (row[0], row[1]) if row else None

    async def delete_session(self, token_hash: str) -> None:
        await self._db.execute(delete(Session).where(Session.token_hash == token_hash))
