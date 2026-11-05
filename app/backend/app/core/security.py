"""Password hashing and session tokens.

Passwords are hashed with Argon2id through argon2-cffi (library defaults, which
follow RFC 9106). Nothing here implements its own cryptography.
"""

import hashlib
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_hasher = PasswordHasher()
# Verified against when the username does not exist, so that "unknown user" and
# "wrong password" take a similar amount of time.
_DUMMY_HASH = _hasher.hash("documind-dummy-password")

SESSION_COOKIE_NAME = "documind_session"


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except (VerificationError, InvalidHashError):
        return False


def new_session_token() -> tuple[str, str]:
    """Return ``(token, token_hash)``. Only the hash is stored in the database."""
    token = secrets.token_urlsafe(32)
    return token, hash_session_token(token)


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
