"""Request-origin verification for state-changing requests (CSRF defence).

Rule (docs/02-specs/02-architecture.md, section 2.4):
- only POST, PATCH and DELETE (and PUT, should one ever exist) are checked;
- if ``Origin`` is present it must be in the allow-list;
- if ``Origin`` is absent, the origin of ``Referer`` is used instead;
- if neither is present, or the origin is not allowed, the request is refused.

This runs before authentication, so it also covers register, login and logout.
"""

from urllib.parse import urlsplit

from fastapi import Depends, Request

from app.core.env_loader import Settings, get_settings
from app.core.errors import ApiError

SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


def request_origin(origin: str | None, referer: str | None) -> str | None:
    """The origin a request claims to come from, or None if it states none."""
    if origin:
        return origin.rstrip("/")
    if referer:
        parts = urlsplit(referer)
        if parts.scheme and parts.netloc:
            return f"{parts.scheme}://{parts.netloc}"
    return None


def is_origin_allowed(origin: str | None, referer: str | None, allowed: frozenset[str]) -> bool:
    claimed = request_origin(origin, referer)
    return claimed is not None and claimed in allowed


def verify_origin(request: Request, settings: Settings = Depends(get_settings)) -> None:
    if request.method in SAFE_METHODS:
        return
    if not is_origin_allowed(
        request.headers.get("origin"), request.headers.get("referer"), settings.allowed_origin_set
    ):
        raise ApiError(
            403, "ORIGIN_NOT_ALLOWED", "This request did not come from an allowed origin."
        )
