"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api import health


def create_app() -> FastAPI:
    app = FastAPI(
        title="DocuMind-AI",
        description="Chat with your documents under a 10K-token LLM context limit.",
        version="0.1.0",
    )
    app.include_router(health.router, prefix="/api")
    return app


app = create_app()
