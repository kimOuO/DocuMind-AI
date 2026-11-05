"""The index job: parse, chunk, embed and store, with progress and safe failure.

Runs against the real PostgreSQL with a fake embedder. Covers AC-01 and AC-03
(stored chunks), AC-36 (failure leaves nothing behind), AC-38 (deletion) and
AC-46 (deleting a document while it is being processed).
"""

import asyncio
import threading
import uuid
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import EMBED_BATCH_SIZE, IndexJobRunner, JobOutcome
from app.ingestion.repository import ChunkRecord, IngestionRepository
from app.llm.tokenizer import Qwen3TokenCounter
from app.models import Chunk
from tests.fakes import FakeEmbedder, fake_vector
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
LONG_TEXT = ("LightRAG combines graph structures with dual-level retrieval. " * 400).encode()
SHORT_TEXT = b"LightRAG combines graph structures with dual-level retrieval.\n"


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def user(client: TestClient) -> TestClient:
    base = get_settings().data_dir
    for path in (p for p in base.rglob("*") if p.is_file()) if base.exists() else []:
        path.unlink()
    register_and_login(client, "kim")
    return client


def upload(client: TestClient, name: str, content: bytes) -> tuple[uuid.UUID, uuid.UUID]:
    """Upload a file and return (document id, id of its queued index job)."""
    response = client.post(DOCUMENTS, files={"file": (name, content)})
    assert response.status_code == 202, response.text
    body = response.json()
    assert body["status"] == "uploaded"
    return uuid.UUID(body["id"]), uuid.UUID(body["jobs"][0]["id"])


def runner(tokenizer: Qwen3TokenCounter, embedder: FakeEmbedder) -> IndexJobRunner:
    settings = get_settings()
    return IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=FileStorage(settings.data_dir),
        tokenizer=tokenizer,
        embedder=embedder,
        settings=settings,
    )


def one(db: psycopg.Connection, query: str, *params: object) -> tuple:
    row = db.execute(query, params).fetchone()
    assert row is not None
    return row


def stored_files() -> list[Path]:
    base = get_settings().data_dir
    return sorted(p for p in base.rglob("*") if p.is_file()) if base.exists() else []


@pytest.mark.parametrize(
    ("name", "content", "pages"),
    [
        ("notes.txt", SHORT_TEXT, 1),
        ("notes.md", b"# LightRAG\n\nGraph-based text indexing.\n", 1),
        ("paper.pdf", SAMPLE_PDF.read_bytes(), 16),
    ],
)
async def test_each_format_is_indexed_and_becomes_ready(
    user: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    name: str,
    content: bytes,
    pages: int,
) -> None:
    """AC-01: PDF, TXT and Markdown are all indexed and listed as ready."""
    document_id, job_id = upload(user, name, content)

    outcome = await runner(tokenizer, FakeEmbedder()).run(job_id)

    assert outcome is JobOutcome.COMPLETED
    listed = user.get(DOCUMENTS).json()
    assert [(d["filename"], d["status"], d["page_count"]) for d in listed] == [
        (name, "ready", pages)
    ]
    assert listed[0]["chunk_count"] >= 1
    assert listed[0]["error"] is None
    job = user.get(f"{DOCUMENTS}/{document_id}").json()["jobs"][0]
    assert job["status"] == "completed"
    assert job["error"] is None
    assert job["started_at"] is not None and job["completed_at"] is not None
    assert job["progress_current"] == job["progress_total"] == listed[0]["chunk_count"]


async def test_the_paper_is_stored_as_chunks_within_the_size_and_with_pages(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-03: every stored chunk fits the chunk size and records its page."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    embedder = FakeEmbedder()

    await runner(tokenizer, embedder).run(job_id)

    rows = db.execute(
        "SELECT ordinal, page, token_count, text, vector_dims(embedding) FROM chunks "
        "WHERE document_id = %s ORDER BY ordinal",
        (document_id,),
    ).fetchall()
    assert len(rows) == 46  # 44 fixed-size chunks and the two tables (pages 7 and 8)
    assert [row[0] for row in rows] == list(range(46))
    assert {row[1] for row in rows} == set(range(1, 17))
    # Only the two table regions may exceed the chunk size (AC-14), by at most 4x.
    oversize = [row for row in rows if row[2] > get_settings().chunk_size]
    assert [(row[1], row[3][:8]) for row in oversize] == [(7, "Table 1:"), (8, "Table 2:")]
    assert all(0 < row[2] <= 4 * get_settings().chunk_size for row in rows)
    assert all(row[2] == tokenizer.count(row[3]) for row in rows)
    assert all(row[4] == 1024 for row in rows)
    # Embedded in batches, in order, each chunk exactly once.
    assert [len(call) for call in embedder.calls] == [EMBED_BATCH_SIZE, EMBED_BATCH_SIZE, 14]
    assert [text for call in embedder.calls for text in call] == [row[3] for row in rows]


async def test_progress_is_recorded_on_the_job_while_it_runs(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    _, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    seen: list[tuple] = []

    async def observe(call: int) -> None:
        seen.append(
            one(
                db,
                "SELECT j.status, j.stage, j.progress_current, j.progress_total, d.status "
                "FROM ingestion_jobs j JOIN documents d ON d.id = j.document_id WHERE j.id = %s",
                job_id,
            )
        )

    await runner(tokenizer, FakeEmbedder(before_call=observe)).run(job_id)

    assert seen == [
        ("running", "embedding", 0, 46, "processing"),
        ("running", "embedding", 16, 46, "processing"),
        ("running", "embedding", 32, 46, "processing"),
    ]


async def test_an_embedding_failure_leaves_no_chunks_and_marks_both_failed(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-36: the document and the job are failed with a reason; nothing is half-written."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())

    outcome = await runner(tokenizer, FakeEmbedder(fail_on_call=1)).run(job_id)

    assert outcome is JobOutcome.FAILED
    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert document["status"] == "failed"
    assert "simulated failure" in document["error"]
    assert document["chunk_count"] == 0
    assert document["page_count"] is None
    job = document["jobs"][0]
    assert job["status"] == "failed"
    assert "simulated failure" in job["error"]
    assert job["completed_at"] is not None
    assert one(db, "SELECT count(*) FROM chunks")[0] == 0


async def test_a_file_without_text_fails_with_a_reason_the_user_can_read(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "blank.txt", b" \n\t\n ")

    outcome = await runner(tokenizer, FakeEmbedder()).run(job_id)

    assert outcome is JobOutcome.FAILED
    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert document["status"] == "failed"
    assert document["error"].startswith("No text could be extracted")


async def test_a_text_file_in_another_encoding_fails_with_a_clear_message(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "big5.txt", "繁體中文的文件".encode("big5"))

    await runner(tokenizer, FakeEmbedder()).run(job_id)

    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert document["status"] == "failed"
    assert "not encoded as UTF-8" in document["error"]


async def test_a_job_runs_only_once(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    _, job_id = upload(user, "notes.txt", SHORT_TEXT)
    embedder = FakeEmbedder()
    await runner(tokenizer, embedder).run(job_id)

    second = await runner(tokenizer, embedder).run(job_id)

    assert second is JobOutcome.ABANDONED
    assert len(embedder.calls) == 1
    assert one(db, "SELECT count(*) FROM chunks")[0] == 1


async def test_an_unknown_job_is_ignored(
    db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    assert await runner(tokenizer, FakeEmbedder()).run(uuid.uuid4()) is JobOutcome.ABANDONED


async def test_deleting_a_ready_document_removes_chunks_jobs_and_file(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-38 (chunks, jobs and the file; summaries are added in P3)."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    await runner(tokenizer, FakeEmbedder()).run(job_id)
    assert one(db, "SELECT count(*) FROM chunks")[0] == 46

    assert user.delete(f"{DOCUMENTS}/{document_id}").status_code == 204

    for table in ("documents", "ingestion_jobs", "chunks"):
        assert one(db, f"SELECT count(*) FROM {table}")[0] == 0
    assert stored_files() == []


async def test_deleting_a_document_while_it_is_processed_leaves_nothing_behind(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-46: after deletion the running job writes nothing and stops early."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    reached_embedding = asyncio.Event()
    may_continue = asyncio.Event()

    async def pause(call: int) -> None:
        if call == 0:
            reached_embedding.set()
            await may_continue.wait()

    embedder = FakeEmbedder(before_call=pause)
    task = asyncio.create_task(runner(tokenizer, embedder).run(job_id))
    await asyncio.wait_for(reached_embedding.wait(), timeout=30)

    # The job is in the middle of embedding when the user deletes the document.
    response = await asyncio.to_thread(user.delete, f"{DOCUMENTS}/{document_id}")
    assert response.status_code == 204
    may_continue.set()
    outcome = await asyncio.wait_for(task, timeout=30)

    assert outcome is JobOutcome.ABANDONED
    # It noticed before the next batch: no further embedding work was done.
    assert len(embedder.calls) == 1
    for table in ("documents", "ingestion_jobs", "chunks"):
        assert one(db, f"SELECT count(*) FROM {table}")[0] == 0
    assert stored_files() == []


def _records(count: int) -> list[ChunkRecord]:
    return [
        ChunkRecord(
            ordinal=i, page=1, text=f"chunk {i}", token_count=2, embedding=fake_vector(f"{i}")
        )
        for i in range(count)
    ]


async def _claim(job_id: uuid.UUID) -> None:
    async with get_sessionmaker()() as session, session.begin():
        assert await IngestionRepository(session).claim_index_job(job_id) is not None


async def test_a_deletion_that_arrives_during_the_final_write_waits_and_then_removes_everything(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-46, first ordering: the write commits first, the deletion then removes it all."""
    document_id, job_id = upload(user, "notes.txt", SHORT_TEXT)
    await _claim(job_id)
    deleted = threading.Event()

    def delete_document() -> None:
        with psycopg.connect(
            db.info.dsn, password=get_settings().db_password, autocommit=True
        ) as conn:
            conn.execute("DELETE FROM documents WHERE id = %s", (document_id,))
        deleted.set()

    async with get_sessionmaker()() as session, session.begin():
        written = await IngestionRepository(session).complete_index_job(
            job_id, page_count=1, chunks=_records(3)
        )
        assert written
        thread = threading.Thread(target=delete_document)
        thread.start()
        # The deletion cannot proceed while the write holds the document.
        await asyncio.sleep(0.5)
        assert not deleted.is_set()
    await asyncio.to_thread(thread.join, 10)

    assert deleted.is_set()
    for table in ("documents", "ingestion_jobs", "chunks"):
        assert one(db, f"SELECT count(*) FROM {table}")[0] == 0


async def test_a_write_that_arrives_during_a_deletion_waits_and_then_writes_nothing(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-46, second ordering: the deletion commits first, the write gives up."""
    document_id, job_id = upload(user, "notes.txt", SHORT_TEXT)
    await _claim(job_id)

    async def write() -> bool:
        async with get_sessionmaker()() as session, session.begin():
            return await IngestionRepository(session).complete_index_job(
                job_id, page_count=1, chunks=_records(3)
            )

    with psycopg.connect(db.info.dsn, password=get_settings().db_password) as deleting:
        deleting.execute("DELETE FROM documents WHERE id = %s", (document_id,))
        task = asyncio.create_task(write())
        # The write cannot proceed while the deletion is not yet committed.
        await asyncio.sleep(0.5)
        assert not task.done()
        deleting.commit()
    written = await asyncio.wait_for(task, timeout=10)

    assert written is None
    for table in ("documents", "ingestion_jobs", "chunks"):
        assert one(db, f"SELECT count(*) FROM {table}")[0] == 0


async def test_progress_is_not_recorded_for_a_job_that_is_no_longer_running(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    _, job_id = upload(user, "notes.txt", SHORT_TEXT)

    async with get_sessionmaker()() as session, session.begin():
        still_running = await IngestionRepository(session).set_progress(job_id, "embedding", 1, 2)

    # The job is queued, not running.
    assert still_running is False
    assert one(db, "SELECT stage FROM ingestion_jobs WHERE id = %s", job_id)[0] is None


async def test_chunks_are_only_reachable_through_their_document(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "notes.txt", SHORT_TEXT)
    await runner(tokenizer, FakeEmbedder()).run(job_id)

    async with get_sessionmaker()() as session:
        chunks = list(await session.scalars(select(Chunk).where(Chunk.document_id == document_id)))

    assert [chunk.text for chunk in chunks] == [SHORT_TEXT.decode().strip()]
    assert len(chunks[0].embedding) == 1024
