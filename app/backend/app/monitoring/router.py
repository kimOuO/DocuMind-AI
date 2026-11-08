"""Monitoring endpoints: the public health check and each user's LLM call ledger."""

import uuid
from datetime import datetime
from typing import Annotated, Literal, Protocol

import httpx
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import current_user
from app.core.database import get_engine, get_session
from app.core.env_loader import Settings, get_settings
from app.models import LLMCall, User
from app.monitoring.ledger import LedgerService

router = APIRouter(tags=["health"])


class DependencyStatus(BaseModel):
    ok: bool
    detail: str = ""


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    database: DependencyStatus
    ollama: DependencyStatus
    llm_model: str
    embed_model: str
    llm_context_limit: int
    # The server's default answer temperature (AC-60); None = the model's default.
    answer_temperature: float | None


class HealthProbe(Protocol):
    async def database(self) -> DependencyStatus: ...

    async def ollama(self) -> DependencyStatus: ...


class LiveHealthProbe:
    """Probes the real dependencies. Never raises: failures become ``ok=False``."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def database(self) -> DependencyStatus:
        try:
            async with get_engine().connect() as conn:
                version = await conn.scalar(
                    text("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
                )
        except Exception as exc:
            return DependencyStatus(ok=False, detail=f"{type(exc).__name__}: {exc}"[:200])
        if version is None:
            return DependencyStatus(ok=False, detail="pgvector extension is not installed")
        return DependencyStatus(ok=True, detail=f"pgvector {version}")

    async def ollama(self) -> DependencyStatus:
        wanted = {self._settings.llm_model, self._settings.embed_model}
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self._settings.ollama_base_url}/api/tags")
                resp.raise_for_status()
        except Exception as exc:
            return DependencyStatus(ok=False, detail=f"{type(exc).__name__}: {exc}"[:200])
        available = {m["name"] for m in resp.json().get("models", [])}
        # Ollama lists untagged pulls as "<name>:latest".
        missing = sorted(m for m in wanted if m not in available and f"{m}:latest" not in available)
        if missing:
            return DependencyStatus(ok=False, detail=f"missing models: {', '.join(missing)}")
        return DependencyStatus(ok=True, detail="models available")


def get_health_probe(settings: Settings = Depends(get_settings)) -> HealthProbe:
    return LiveHealthProbe(settings)


@router.get("/health", response_model=HealthResponse)
async def health(
    probe: HealthProbe = Depends(get_health_probe),
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    database = await probe.database()
    ollama = await probe.ollama()
    return HealthResponse(
        status="ok" if database.ok and ollama.ok else "degraded",
        database=database,
        ollama=ollama,
        llm_model=settings.llm_model,
        embed_model=settings.embed_model,
        llm_context_limit=settings.llm_context_limit,
        answer_temperature=settings.answer_temperature,
    )


class MeasuredTotals(BaseModel):
    count: int
    max_total_tokens: int | None


class UnmeasuredTotals(BaseModel):
    count: int
    max_budget_upper_bound: int | None


class LLMCallResponse(BaseModel):
    id: uuid.UUID
    purpose: str
    model: str
    status: str
    finish_reason: str | None
    estimated_prompt_tokens: int
    max_output_tokens: int
    budget_upper_bound: int
    # Reported by Ollama. None means the value is not known.
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    received_output_tokens_estimated: int | None
    error: str | None
    duration_ms: int | None
    created_at: datetime


class LedgerResponse(BaseModel):
    limit: int
    measured: MeasuredTotals
    unmeasured: UnmeasuredTotals
    underestimate_events: int
    calls: list[LLMCallResponse]


def _call(call: LLMCall) -> LLMCallResponse:
    measured = call.prompt_tokens is not None and call.completion_tokens is not None
    return LLMCallResponse(
        id=call.id,
        purpose=call.purpose,
        model=call.model,
        status=call.status,
        finish_reason=call.finish_reason,
        estimated_prompt_tokens=call.estimated_prompt_tokens,
        max_output_tokens=call.max_output_tokens,
        budget_upper_bound=call.estimated_prompt_tokens + call.max_output_tokens,
        prompt_tokens=call.prompt_tokens,
        completion_tokens=call.completion_tokens,
        total_tokens=(call.prompt_tokens or 0) + (call.completion_tokens or 0)
        if measured
        else None,
        received_output_tokens_estimated=call.received_output_tokens_estimated,
        error=call.error,
        duration_ms=call.duration_ms,
        created_at=call.created_at,
    )


@router.get("/llm-calls", response_model=LedgerResponse, tags=["ledger"])
async def llm_calls(
    conversation_id: uuid.UUID | None = None,
    document_id: uuid.UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> LedgerResponse:
    """The caller's LLM calls. Measured and unmeasured calls are totalled apart."""
    report = await LedgerService(db).report(
        user, conversation_id=conversation_id, document_id=document_id, limit=limit
    )
    summary = report.summary
    return LedgerResponse(
        limit=settings.llm_context_limit,
        measured=MeasuredTotals(
            count=summary.measured_count, max_total_tokens=summary.max_measured_total
        ),
        unmeasured=UnmeasuredTotals(
            count=summary.unmeasured_count,
            max_budget_upper_bound=summary.max_unmeasured_upper_bound,
        ),
        underestimate_events=summary.underestimate_events,
        calls=[_call(call) for call in report.calls],
    )
