"""FastAPI application entry point."""

from fastapi import APIRouter, Depends, FastAPI

from app.auth import router as auth
from app.core.errors import install_error_handlers
from app.core.origin import verify_origin
from app.documents import router as documents
from app.monitoring import router as monitoring

API_PREFIX = "/api/v1"

# Endpoints that do not require a logged-in user (acceptance criterion AC-30).
PUBLIC_PATHS = frozenset(
    {
        f"{API_PREFIX}/auth/register",
        f"{API_PREFIX}/auth/login",
        f"{API_PREFIX}/health",
    }
)


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
    )
    install_error_handlers(app)

    # Every API route passes the origin check before anything else runs.
    api = APIRouter(prefix=API_PREFIX, dependencies=[Depends(verify_origin)])
    api.include_router(auth.router)
    api.include_router(documents.router)
    api.include_router(monitoring.router)
    app.include_router(api)
    return app


app = create_app()
