"""GET /documents/{id}/events: progress as server-sent events.

Covers the progress-stream part of AC-32 and the visible progress required by
the P2-C milestone.
"""

import asyncio
import json
import uuid
from collections.abc import Callable
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents import router as documents_router
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner
from app.llm.tokenizer import Qwen3TokenCounter
from tests.fakes import FakeEmbedder
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
TEXT = b"LightRAG combines graph structures with dual-level retrieval.\n"


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def user(client: TestClient) -> TestClient:
    register_and_login(client, "kim")
    return client


@pytest.fixture()
def other(make_client: Callable[..., TestClient]) -> TestClient:
    client = make_client()
    register_and_login(client, "lee")
    return client


def upload(client: TestClient, name: str = "notes.txt", content: bytes = TEXT) -> tuple[str, str]:
    body = client.post(DOCUMENTS, files={"file": (name, content)}).json()
    return body["id"], body["jobs"][0]["id"]


def runner(tokenizer: Qwen3TokenCounter, embedder: FakeEmbedder) -> IndexJobRunner:
    settings = get_settings()
    return IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=FileStorage(settings.data_dir),
        tokenizer=tokenizer,
        embedder=embedder,
        settings=settings,
    )


def parse(stream: str) -> list[tuple[str, dict]]:
    events = []
    for block in stream.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        events.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    return events


async def test_a_ready_document_reports_its_status_and_ends(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user)
    await runner(tokenizer, FakeEmbedder()).run(uuid.UUID(job_id))

    response = user.get(f"{DOCUMENTS}/{document_id}/events")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert parse(response.text) == [
        ("status", {"status": "ready", "summary_status": "none"}),
        ("done", {"status": "ready", "summary_status": "none"}),
    ]


async def test_a_failed_document_reports_why(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user)
    await runner(tokenizer, FakeEmbedder(fail_on_call=0)).run(uuid.UUID(job_id))

    events = parse(user.get(f"{DOCUMENTS}/{document_id}/events").text)

    assert [name for name, _ in events] == ["status", "error", "done"]
    assert events[1][1]["kind"] == "index"
    assert "simulated failure" in events[1][1]["detail"]


async def test_progress_is_streamed_while_the_document_is_processed(
    user: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(documents_router, "EVENT_POLL_SECONDS", 0.05)
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())

    async def slowly(call: int) -> None:
        await asyncio.sleep(0.3)  # long enough for the stream to see each batch

    stream = asyncio.create_task(asyncio.to_thread(user.get, f"{DOCUMENTS}/{document_id}/events"))
    await asyncio.sleep(0.2)  # the stream is open before the job starts
    await runner(tokenizer, FakeEmbedder(before_call=slowly)).run(uuid.UUID(job_id))
    response = await asyncio.wait_for(stream, timeout=30)

    events = parse(response.text)
    assert events[0] == ("status", {"status": "uploaded", "summary_status": "none"})
    assert ("status", {"status": "processing", "summary_status": "none"}) in events
    progress = [data for name, data in events if name == "progress"]
    assert {"kind": "index", "stage": "embedding", "current": 0, "total": 48} in progress
    assert {"kind": "index", "stage": "embedding", "current": 32, "total": 48} in progress
    assert events[-2:] == [
        ("status", {"status": "ready", "summary_status": "none"}),
        ("done", {"status": "ready", "summary_status": "none"}),
    ]


async def test_another_users_progress_cannot_be_watched(
    user: TestClient, other: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-32 (progress stream): same answer as for a document that does not exist."""
    document_id, job_id = upload(user)
    await runner(tokenizer, FakeEmbedder()).run(uuid.UUID(job_id))

    stranger = other.get(f"{DOCUMENTS}/{document_id}/events")
    missing = other.get(f"{DOCUMENTS}/{uuid.uuid4()}/events")

    assert stranger.status_code == missing.status_code == 404
    assert stranger.json() == missing.json()
    assert stranger.headers["content-type"].startswith("application/json")
