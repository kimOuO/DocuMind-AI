"""HTTP endpoints for accounts: register, login, logout, current user."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.core.database import get_session
from app.core.env_loader import Settings, get_settings
from app.core.security import SESSION_COOKIE_NAME
from app.models import User

router = APIRouter()

SessionCookie = Annotated[str | None, Cookie(alias=SESSION_COOKIE_NAME)]


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    # No length rules here: a login attempt must not reveal which rule failed.
    username: str = Field(max_length=128)
    password: str = Field(max_length=1024)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    display_name: str
    answer_language: str
    answer_detail: str
    created_at: datetime
    last_login_at: datetime | None


def get_auth_service(
    db: AsyncSession = Depends(get_session), settings: Settings = Depends(get_settings)
) -> AuthService:
    return AuthService(db, settings)


async def current_user(
    token: SessionCookie = None, service: AuthService = Depends(get_auth_service)
) -> User:
    """Dependency for every endpoint that requires a logged-in user."""
    return await service.authenticate(token)


@router.post("/auth/register", status_code=201, response_model=UserResponse, tags=["auth"])
async def register(body: Credentials, service: AuthService = Depends(get_auth_service)) -> User:
    return await service.register(body.username, body.password)


@router.post("/auth/login", response_model=UserResponse, tags=["auth"])
async def login(
    body: LoginRequest,
    response: Response,
    token: SessionCookie = None,
    service: AuthService = Depends(get_auth_service),
    settings: Settings = Depends(get_settings),
) -> User:
    user, new_token = await service.login(body.username, body.password, token)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        new_token,
        max_age=settings.session_ttl_hours * 3600,
        httponly=True,
        samesite="lax",
        secure=settings.session_cookie_secure,
        path="/",
    )
    return user


@router.post("/auth/logout", status_code=204, tags=["auth"])
async def logout(
    response: Response,
    token: SessionCookie = None,
    _: User = Depends(current_user),
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.logout(token)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")


@router.get("/users/me", response_model=UserResponse, tags=["users"])
async def read_me(user: User = Depends(current_user)) -> User:
    return user
