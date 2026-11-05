"""Scheduling, retrying and recovering index jobs through the API.

Covers AC-37 (retry), AC-39 (recovery after a restart) and the retry part of
AC-32 (another user's document). Jobs are run explicitly with a fake embedder;
the scheduler is replaced by one that only records.
"""

import uuid
from collections.abc import Callable
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.ingestion.repository import RESTART_REASON, IngestionRepository
from app.ingestion.scheduler import get_job_scheduler
from app.llm.tokenizer import Qwen3TokenCounter
from app.main import create_app
from tests.conftest import ALLOWED_ORIGIN
from tests.fakes import FakeEmbedder, RecordingScheduler
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
TEXT = b"LightRAG combines graph structures with dual-level retrieval.\n"


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def scheduler() -> RecordingScheduler:
    return RecordingScheduler()


@pytest.fixture()
def user(client: TestClient, scheduler: RecordingScheduler) -> TestClient:
    base = get_settings().data_dir
    for path in (p for p in base.rglob("*") if p.is_file()) if base.exists() else []:
        path.unlink()
    client.app.dependency_overrides[get_job_scheduler] = lambda: scheduler  # type: ignore[attr-defined]
    register_and_login(client, "kim")
    return client


@pytest.fixture()
def other(make_client: Callable[..., TestClient]) -> TestClient:
    client = make_client()
    register_and_login(client, "lee")
    return client


def upload(client: TestClient, name: str = "notes.txt", content: bytes = TEXT) -> tuple[str, str]:
    response = client.post(DOCUMENTS, files={"file": (name, content)})
    assert response.status_code == 202, response.text
    body = response.json()
    return body["id"], body["jobs"][0]["id"]


async def run(tokenizer: Qwen3TokenCounter, job_id: str, embedder: FakeEmbedder) -> JobOutcome:
    settings = get_settings()
    runner = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=FileStorage(settings.data_dir),
        tokenizer=tokenizer,
        embedder=embedder,
        settings=settings,
    )
    return await runner.run(uuid.UUID(job_id))


def jobs(db: psycopg.Connection, document_id: str) -> list[tuple]:
    return db.execute(
        "SELECT retry_count, status FROM ingestion_jobs "
        "WHERE document_id = %s ORDER BY retry_count",
        (document_id,),
    ).fetchall()


def test_uploading_schedules_the_new_index_job(
    user: TestClient, scheduler: RecordingScheduler
) -> None:
    document_id, job_id = upload(user)

    assert scheduler.scheduled == [(job_id, document_id)]


def test_uploading_the_same_content_again_schedules_nothing(
    user: TestClient, scheduler: RecordingScheduler
) -> None:
    upload(user)

    again = user.post(DOCUMENTS, files={"file": ("copy.txt", TEXT)})

    assert again.status_code == 200
    assert len(scheduler.scheduled) == 1


def test_deleting_tells_the_scheduler_to_stop_the_documents_job(
    user: TestClient, scheduler: RecordingScheduler
) -> None:
    document_id, _ = upload(user)

    assert user.delete(f"{DOCUMENTS}/{document_id}").status_code == 204

    assert scheduler.cancelled == [document_id]


async def test_a_failed_document_can_be_retried_and_becomes_ready(
    user: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    scheduler: RecordingScheduler,
) -> None:
    """AC-37: retry makes it ready, without duplicate chunks, and keeps the job history."""
    document_id, first_job = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    assert await run(tokenizer, first_job, FakeEmbedder(fail_on_call=1)) is JobOutcome.FAILED

    response = user.post(f"{DOCUMENTS}/{document_id}/retry")

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "processing"
    assert body["error"] is None
    retry_job = body["jobs"][0]
    assert (retry_job["status"], retry_job["retry_count"]) == ("queued", 1)
    assert scheduler.scheduled[-1] == (retry_job["id"], document_id)
    assert jobs(db, document_id) == [(0, "failed"), (1, "queued")]

    assert await run(tokenizer, retry_job["id"], FakeEmbedder()) is JobOutcome.COMPLETED

    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert (document["status"], document["chunk_count"], document["error"]) == ("ready", 48, None)
    assert jobs(db, document_id) == [(0, "failed"), (1, "completed")]
    ordinals = db.execute(
        "SELECT ordinal FROM chunks WHERE document_id = %s ORDER BY ordinal", (document_id,)
    ).fetchall()
    assert [row[0] for row in ordinals] == list(range(48))


async def test_a_second_retry_increases_the_count_again(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user)
    await run(tokenizer, job_id, FakeEmbedder(fail_on_call=0))
    retry = user.post(f"{DOCUMENTS}/{document_id}/retry").json()["jobs"][0]["id"]
    await run(tokenizer, retry, FakeEmbedder(fail_on_call=0))

    again = user.post(f"{DOCUMENTS}/{document_id}/retry")

    assert again.status_code == 202
    assert again.json()["jobs"][0]["retry_count"] == 2
    assert jobs(db, document_id) == [(0, "failed"), (1, "failed"), (2, "queued")]


async def test_only_a_failed_document_can_be_retried(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user)

    # Still waiting to be processed.
    waiting = user.post(f"{DOCUMENTS}/{document_id}/retry")
    assert (waiting.status_code, waiting.json()["code"]) == (409, "RETRY_NOT_ALLOWED")

    await run(tokenizer, job_id, FakeEmbedder())
    ready = user.post(f"{DOCUMENTS}/{document_id}/retry")
    assert (ready.status_code, ready.json()["code"]) == (409, "RETRY_NOT_ALLOWED")
    assert jobs(db, document_id) == [(0, "completed")]


async def test_a_retry_that_is_already_queued_cannot_be_requested_twice(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user)
    await run(tokenizer, job_id, FakeEmbedder(fail_on_call=0))
    assert user.post(f"{DOCUMENTS}/{document_id}/retry").status_code == 202

    second = user.post(f"{DOCUMENTS}/{document_id}/retry")

    assert second.status_code == 409
    assert jobs(db, document_id) == [(0, "failed"), (1, "queued")]


async def test_another_users_document_cannot_be_retried(
    user: TestClient, other: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-32 (retry): the answer is the same as for a document that does not exist."""
    document_id, job_id = upload(user)
    await run(tokenizer, job_id, FakeEmbedder(fail_on_call=0))

    stranger = other.post(f"{DOCUMENTS}/{document_id}/retry")
    missing = other.post(f"{DOCUMENTS}/{uuid.uuid4()}/retry")

    assert stranger.status_code == missing.status_code == 404
    assert stranger.json() == missing.json()
    assert jobs(db, document_id) == [(0, "failed")]
    assert user.get(f"{DOCUMENTS}/{document_id}").json()["status"] == "failed"


async def _recover() -> int:
    async with get_sessionmaker()() as session, session.begin():
        return await IngestionRepository(session).fail_unfinished_jobs(RESTART_REASON)


async def test_unfinished_jobs_are_failed_at_startup_and_can_be_retried(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-39: queued and running jobs become failed; the documents can be retried."""
    queued_document, _ = upload(user, "queued.txt", b"queued when the server stopped\n")
    running_document, running_job = upload(
        user, "running.txt", b"running when the server stopped\n"
    )
    async with get_sessionmaker()() as session, session.begin():
        assert await IngestionRepository(session).claim_index_job(uuid.UUID(running_job))
    ready_document, ready_job = upload(user, "ready.txt", b"already indexed\n")
    await run(tokenizer, ready_job, FakeEmbedder())
    failed_document, failed_job = upload(user, "failed.txt", b"failed earlier\n")
    await run(tokenizer, failed_job, FakeEmbedder(fail_on_call=0))

    assert await _recover() == 2

    documents = {d["id"]: d for d in user.get(DOCUMENTS).json()}
    for document_id in (queued_document, running_document):
        assert documents[document_id]["status"] == "failed"
        assert documents[document_id]["error"] == RESTART_REASON
        job = user.get(f"{DOCUMENTS}/{document_id}").json()["jobs"][0]
        assert (job["status"], job["error"]) == ("failed", RESTART_REASON)
        assert job["completed_at"] is not None
    # Finished work is left alone.
    assert documents[ready_document]["status"] == "ready"
    assert documents[failed_document]["error"] != RESTART_REASON
    # Running it again changes nothing.
    assert await _recover() == 0

    retry = user.post(f"{DOCUMENTS}/{running_document}/retry")
    assert retry.status_code == 202
    assert (
        await run(tokenizer, retry.json()["jobs"][0]["id"], FakeEmbedder()) is JobOutcome.COMPLETED
    )
    assert user.get(f"{DOCUMENTS}/{running_document}").json()["status"] == "ready"


def test_starting_the_application_recovers_unfinished_jobs(
    user: TestClient, db: psycopg.Connection
) -> None:
    """AC-39 through the real startup path."""
    document_id, _ = upload(user)

    # Entering the context runs the application's startup, as a restart would.
    with TestClient(create_app(), headers={"Origin": ALLOWED_ORIGIN}) as restarted:
        assert restarted.get("/api/v1/health").status_code == 200
        status = db.execute(
            "SELECT d.status, j.status, j.error FROM documents d JOIN ingestion_jobs j "
            "ON j.document_id = d.id WHERE d.id = %s",
            (document_id,),
        ).fetchone()

    assert status == ("failed", "failed", RESTART_REASON)
