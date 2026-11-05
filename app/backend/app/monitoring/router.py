"""Health endpoint (public): reports whether the database and the LLM server are reachable."""

from typing import Literal, Protocol

import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text

from app.core.database import get_engine
from app.core.env_loader import Settings, get_settings

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
    )
