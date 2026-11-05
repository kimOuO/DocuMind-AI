"""Registration, login, logout and session validation rules."""

from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.core.security import (
    hash_password,
    hash_session_token,
    new_session_token,
    verify_password,
)
from app.models import User


def normalise_username(username: str) -> str:
    return username.strip().lower()


class AuthService:
    def __init__(self, db: AsyncSession, settings: Settings) -> None:
        self._db = db
        self._repo = AuthRepository(db)
        self._settings = settings

    async def register(self, username: str, password: str) -> User:
        username = normalise_username(username)
        if await self._repo.get_user_by_username(username) is not None:
            raise ApiError(409, "USERNAME_TAKEN", "This username is already in use.")
        try:
            user = await self._repo.add_user(
                username, hash_password(password), display_name=username
            )
            await self._db.commit()
        except IntegrityError as exc:  # lost a race with another registration
            await self._db.rollback()
            raise ApiError(409, "USERNAME_TAKEN", "This username is already in use.") from exc
        return user

    async def login(
        self, username: str, password: str, presented_token: str | None
    ) -> tuple[User, str]:
        """Check credentials and start a new session.

        A brand-new token is issued on every login. Any session the request
        arrived with is deleted first, so a token known before login can never
        become an authenticated session (session fixation).
        """
        user = await self._repo.get_user_by_username(normalise_username(username))
        if not verify_password(user.password_hash if user else None, password) or user is None:
            # Same answer for an unknown user and a wrong password.
            raise ApiError(401, "INVALID_CREDENTIALS", "Incorrect username or password.")

        if presented_token:
            await self._repo.delete_session(hash_session_token(presented_token))
        token, token_hash = new_session_token()
        expires_at = datetime.now(UTC) + timedelta(hours=self._settings.session_ttl_hours)
        await self._repo.add_session(user.id, token_hash, expires_at)
        await self._repo.touch_last_login(user)
        await self._db.commit()
        return user, token

    async def logout(self, presented_token: str | None) -> None:
        if presented_token:
            await self._repo.delete_session(hash_session_token(presented_token))
            await self._db.commit()

    async def authenticate(self, presented_token: str | None) -> User:
        """Return the user owning a valid session, or raise 401."""
        if not presented_token:
            raise ApiError(401, "NOT_AUTHENTICATED", "Please log in.")
        token_hash = hash_session_token(presented_token)
        found = await self._repo.get_session_with_user(token_hash)
        if found is None:
            raise ApiError(401, "NOT_AUTHENTICATED", "Please log in.")
        session, user = found
        if session.expires_at <= datetime.now(UTC):
            await self._repo.delete_session(token_hash)
            await self._db.commit()
            raise ApiError(401, "SESSION_EXPIRED", "Your session has expired. Please log in again.")
        return user
