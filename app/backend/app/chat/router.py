"""HTTP endpoint for asking a question in a conversation."""

import uuid
from collections.abc import AsyncIterator
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import current_user
from app.chat.service import ChatService
from app.core.database import get_session, get_sessionmaker
from app.core.env_loader import Settings, get_settings
from app.core.sse import SSE_HEADERS, format_sse
from app.ingestion.scheduler import JobScheduler, get_job_scheduler
from app.llm.embedding import Embedder, OllamaEmbedder
from app.llm.gateway import LLMGateway, OllamaGateway
from app.llm.tokenizer import get_token_counter
from app.models import User

router = APIRouter(tags=["chat"])

ConversationId = Annotated[uuid.UUID, Path(alias="id")]


class QuestionBody(BaseModel):
    question: str = Field(min_length=1, max_length=20_000)
    document_ids: list[uuid.UUID] | None = None
    # The answer call's sampling temperature (AC-60, D94); omitted = ANSWER_TEMPERATURE.
    temperature: float | None = Field(default=None, ge=0.0, le=1.0)
    # D101: "summary" builds the summary tree of the documents in scope first (when they
    # have none) and answers from it; the question text is the record shown in the chat.
    action: Literal["summary"] | None = None


def get_embedder(settings: Settings = Depends(get_settings)) -> Embedder:
    return OllamaEmbedder(settings)


def get_llm_gateway(settings: Settings = Depends(get_settings)) -> LLMGateway:
    return OllamaGateway(
        settings=settings, sessions=get_sessionmaker(), counter=get_token_counter()
    )


@router.post("/conversations/{id}/messages")
async def ask(
    conversation_id: ConversationId,
    body: QuestionBody,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
    embedder: Embedder = Depends(get_embedder),
    gateway: LLMGateway = Depends(get_llm_gateway),
    scheduler: JobScheduler = Depends(get_job_scheduler),
) -> StreamingResponse:
    """Ask a question. The answer arrives as server-sent events, ending with `done` or `error`."""
    service = ChatService(
        db,
        sessions=get_sessionmaker(),
        settings=settings,
        counter=get_token_counter(),
        embedder=embedder,
        gateway=gateway,
        scheduler=scheduler,
    )
    # Every check happens here, before the stream starts: a refused question
    # gets an ordinary error response and leaves nothing behind.
    prepared = await service.prepare(
        user, conversation_id, body.question, body.document_ids, body.temperature, body.action
    )
    # The answer can take a while and uses short sessions of its own.
    await db.close()

    async def body_stream() -> AsyncIterator[str]:
        async for event in service.answer(prepared):
            yield format_sse(event.name, event.data)

    return StreamingResponse(body_stream(), media_type="text/event-stream", headers=SSE_HEADERS)
