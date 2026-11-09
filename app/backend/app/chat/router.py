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
from app.core.errors import ApiError
from app.core.sse import SSE_HEADERS, format_sse
from app.ingestion.scheduler import JobScheduler, get_job_scheduler
from app.llm.embedding import Embedder, OllamaEmbedder
from app.llm.gateway import LLMGateway, OllamaGateway
from app.llm.tokenizer import get_token_counter, get_token_counter_for
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
    # D104 (AC-63): the generation model for every call of this question — one of the
    # models the server offers (GET /health `llm_models`); omitted = the default.
    model: str | None = Field(default=None, max_length=100)


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
    # D104 (AC-63): the model this question uses. The settings, the tokenizer and the
    # gateway all follow it, so the budget guard counts with that model's own tokenizer.
    chosen = settings.for_model(body.model)
    if chosen is None:
        raise ApiError(
            422,
            "UNKNOWN_MODEL",
            f"Model {body.model!r} is not offered; choose one of {settings.llm_models()}.",
        )
    counter = get_token_counter()
    if chosen is not settings:
        counter = get_token_counter_for(chosen.tokenizer_path, chosen.tokenizer_sha256)
        gateway = gateway.for_settings(chosen, counter)
    service = ChatService(
        db,
        sessions=get_sessionmaker(),
        settings=chosen,
        counter=counter,
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
