"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI

from app.auth import router as auth
from app.chat import router as chat
from app.chat.repository import ChatRepository
from app.conversations import router as conversations
from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.core.errors import install_error_handlers
from app.core.origin import verify_origin
from app.documents import router as documents
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner
from app.ingestion.repository import RESTART_REASON, IngestionRepository
from app.ingestion.scheduler import InProcessScheduler
from app.llm import ledger
from app.llm.embedding import OllamaEmbedder
from app.llm.tokenizer import get_token_counter
from app.monitoring import router as monitoring

logger = logging.getLogger(__name__)

API_PREFIX = "/api/v1"

# Endpoints that do not require a logged-in user (acceptance criterion AC-30).
PUBLIC_PATHS = frozenset(
    {
        f"{API_PREFIX}/auth/register",
        f"{API_PREFIX}/auth/login",
        f"{API_PREFIX}/health",
    }
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Recover from the previous shutdown, then start background processing."""
    settings = get_settings()
    sessions = get_sessionmaker()
    # Nothing is running yet, so a job still marked unfinished was interrupted.
    async with sessions() as session, session.begin():
        interrupted = await IngestionRepository(session).fail_unfinished_jobs(RESTART_REASON)
        await ledger.LedgerRepository(session).fail_pending(ledger.RESTART_REASON)
        await ChatRepository(session).interrupt_unfinished()
    if interrupted:
        logger.warning("Marked %d interrupted processing job(s) as failed", interrupted)

    scheduler = InProcessScheduler(
        IndexJobRunner(
            sessions=sessions,
            storage=FileStorage(settings.data_dir),
            tokenizer=get_token_counter(),
            embedder=OllamaEmbedder(settings),
            settings=settings,
        )
    )
    app.state.job_scheduler = scheduler
    try:
        yield
    finally:
        await scheduler.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DocuMind-AI",
        description="A document management and question-answering platform "
        "that keeps every LLM call within a 10K-token context.",
        version="0.2.0",
        docs_url=f"{API_PREFIX}/docs",
        openapi_url=f"{API_PREFIX}/openapi.json",
        redoc_url=None,
        swagger_ui_oauth2_redirect_url=None,
        lifespan=lifespan,
    )
    install_error_handlers(app)

    # Every API route passes the origin check before anything else runs.
    api = APIRouter(prefix=API_PREFIX, dependencies=[Depends(verify_origin)])
    api.include_router(auth.router)
    api.include_router(documents.router)
    api.include_router(conversations.router)
    api.include_router(chat.router)
    api.include_router(monitoring.router)
    app.include_router(api)
    return app


app = create_app()
