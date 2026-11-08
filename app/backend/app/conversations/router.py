"""HTTP endpoints for conversations: create, list, read, delete."""

import uuid
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import current_user
from app.conversations.service import ConversationService
from app.core.database import get_session
from app.models import Conversation, Message, User

router = APIRouter(tags=["conversations"])

ConversationId = Annotated[uuid.UUID, Path(alias="id")]


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=200)


class ConversationResponse(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    status: str
    answered: bool | None
    sources: list[dict[str, Any]]
    # The answer's sampling temperature (AC-60); null for questions and the model default.
    temperature: float | None
    created_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: list[MessageResponse]


def _summary(conversation: Conversation) -> ConversationResponse:
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


def message_response(message: Message) -> MessageResponse:
    return MessageResponse(
        id=message.id,
        role=message.role,
        content=message.content,
        status=message.status,
        answered=message.answered,
        sources=list(message.sources),
        temperature=message.temperature,
        created_at=message.created_at,
    )


def get_conversation_service(db: AsyncSession = Depends(get_session)) -> ConversationService:
    return ConversationService(db)


@router.post("/conversations", status_code=201, response_model=ConversationResponse)
async def create_conversation(
    body: ConversationCreate,
    user: User = Depends(current_user),
    service: ConversationService = Depends(get_conversation_service),
) -> ConversationResponse:
    return _summary(await service.create(user, body.title))


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    user: User = Depends(current_user),
    service: ConversationService = Depends(get_conversation_service),
) -> list[ConversationResponse]:
    return [_summary(c) for c in await service.list_conversations(user)]


@router.get("/conversations/{id}", response_model=ConversationDetailResponse)
async def read_conversation(
    conversation_id: ConversationId,
    user: User = Depends(current_user),
    service: ConversationService = Depends(get_conversation_service),
) -> ConversationDetailResponse:
    view = await service.get(user, conversation_id)
    return ConversationDetailResponse(
        **_summary(view.conversation).model_dump(),
        messages=[message_response(m) for m in view.messages],
    )


@router.delete("/conversations/{id}", status_code=204)
async def delete_conversation(
    conversation_id: ConversationId,
    user: User = Depends(current_user),
    service: ConversationService = Depends(get_conversation_service),
) -> None:
    await service.delete(user, conversation_id)
