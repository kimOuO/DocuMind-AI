"""The summary job: section summaries and the document summary, built after indexing.

Runs against the real PostgreSQL with a fake embedder and a stubbed Ollama.
Covers the automatic queueing after indexing, storage with sources, progress,
failure (AC-42: the document stays ready), retry of the summary, deletion while
summarising, and the ledger rows (AC-17).
"""

import asyncio
import uuid
from pathlib import Path

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.dispatcher import JobDispatcher
from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.ingestion.scheduler import get_job_scheduler
from app.llm.gateway import OllamaGateway
from app.llm.tokenizer import Qwen3TokenCounter
from app.summarization.service import SummaryJobRunner, SummaryOutcome
from tests.fakes import FakeEmbedder, RecordingScheduler, StubSummariser
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
NOTE = (
    b"# Notes on LightRAG\n\nGraphs help retrieval.\n\n## Indexing\n\nEntities become nodes. "
    b"Win rate 67.6%.\n\n## Retrieval\n\nTwo levels.\n"
)


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def user(client: TestClient) -> TestClient:
    client.app.dependency_overrides[get_job_scheduler] = lambda: RecordingScheduler()  # type: ignore[attr-defined]
    register_and_login(client, "kim")
    return client


def runners(tokenizer: Qwen3TokenCounter, model: StubSummariser, *, input_budget: int = 6_000):
    settings = get_settings()
    storage = FileStorage(settings.data_dir)
    index = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        tokenizer=tokenizer,
        embedder=FakeEmbedder(),
        settings=settings,
    )
    summary = SummaryJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        counter=tokenizer,
        gateway=OllamaGateway(
            settings=settings,
            sessions=get_sessionmaker(),
            counter=tokenizer,
            transport=httpx.MockTransport(model),
        ),
        input_budget=input_budget,
    )
    return (
        index,
        summary,
        JobDispatcher(sessions=get_sessionmaker(), index_runner=index, summary_runner=summary),
    )


def upload(client: TestClient, name: str, content: bytes) -> tuple[str, str]:
    body = client.post(DOCUMENTS, files={"file": (name, content)}).json()
    return body["id"], body["jobs"][0]["id"]


def summaries(db: psycopg.Connection, document_id: str) -> list[tuple]:
    return db.execute(
        "SELECT level, ordinal, title, page_start, page_end, text, "
        "cardinality(source_chunk_ids), cardinality(source_summary_ids) "
        "FROM summaries WHERE document_id = %s ORDER BY level, ordinal",
        (document_id,),
    ).fetchall()


def jobs(db: psycopg.Connection, document_id: str) -> list[tuple]:
    return db.execute(
        "SELECT kind, status, stage, progress_current, progress_total, retry_count "
        "FROM ingestion_jobs "
        "WHERE document_id = %s ORDER BY created_at",
        (document_id,),
    ).fetchall()


async def test_indexing_queues_the_summary_and_the_dispatcher_builds_it(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "notes.md", NOTE)
    model = StubSummariser()
    _, _, dispatcher = runners(tokenizer, model)

    await dispatcher.run(uuid.UUID(job_id))

    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert (document["status"], document["summary_status"]) == ("ready", "ready")
    assert jobs(db, document_id) == [
        ("index", "completed", "embedding", 1, 1, 0),
        ("summary", "completed", "summarizing", 2, 2, 0),
    ]
    # The whole note fits one unit: one section summary and the document summary.
    rows = summaries(db, document_id)
    assert [(r[0], r[1], r[2], r[3], r[4]) for r in rows] == [
        ("document", 0, None, 1, 1),
        ("section", 1, "Notes on LightRAG", 1, 1),
    ]
    document_row, section_row = rows
    assert section_row[5].startswith("Summary of Notes on LightRAG")
    assert (section_row[6], section_row[7]) == (1, 0)  # made from the note's single chunk
    assert (document_row[6], document_row[7]) == (0, 1)  # merged from the one section summary
    # Two LLM calls, both in the ledger with the document as context.
    calls = db.execute(
        "SELECT purpose, status, document_id FROM llm_calls ORDER BY created_at"
    ).fetchall()
    assert calls == [
        ("section_summary", "completed", uuid.UUID(document_id)),
        ("document_summary", "completed", uuid.UUID(document_id)),
    ]
    # The section prompt carried the page marker; the document prompt the section summary.
    assert "[page 1]\n# Notes on LightRAG" in model.prompts[0]
    assert "[Notes on LightRAG]\nSummary of Notes on LightRAG" in model.prompts[1]


async def test_the_paper_gets_one_summary_per_section_with_progress(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    model = StubSummariser()
    index, summary, _ = runners(tokenizer, model)
    assert await index.run(uuid.UUID(job_id)) is JobOutcome.COMPLETED
    summary_job = index.queued_summary_jobs[uuid.UUID(job_id)]
    seen: list[tuple] = []
    original = summary._progress

    async def spy(job_id: uuid.UUID, current: int, total: int) -> bool:
        seen.append((current, total))
        return await original(job_id, current, total)

    summary._progress = spy  # type: ignore[method-assign]

    assert await summary.run(summary_job) is SummaryOutcome.COMPLETED

    rows = summaries(db, document_id)
    sections = [r for r in rows if r[0] == "section"]
    assert [(r[2], r[3], r[4]) for r in sections] == [
        ("Front matter", 1, 1),
        ("INTRODUCTION", 1, 2),
        ("RETRIEVAL-AUGMENTED GENERATION", 2, 3),
        ("THE LIGHT RAG ARCHITECTURE", 3, 5),
        ("EVALUATION", 5, 10),
        ("RELATED WORK", 10, 10),
        ("CONCLUSION", 10, 10),
        ("APPENDIX", 13, 16),
    ]
    # Every section summary is linked to the chunks of its pages.
    chunk_pages = dict(
        db.execute("SELECT id, page FROM chunks WHERE document_id = %s", (document_id,)).fetchall()
    )
    for row in db.execute(
        "SELECT page_start, page_end, source_chunk_ids FROM summaries WHERE level = 'section'"
    ).fetchall():
        assert row[2] and all(row[0] <= chunk_pages[cid] <= row[1] for cid in row[2])
    document_row = next(r for r in rows if r[0] == "document")
    assert (document_row[3], document_row[4], document_row[7]) == (1, 16, 8)
    assert seen == [(i, 9) for i in range(9)]
    assert user.get(f"{DOCUMENTS}/{document_id}").json()["summary_status"] == "ready"
    assert len(model.prompts) == 9


async def test_too_many_section_summaries_are_condensed_in_groups_first(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    model = StubSummariser()
    index, summary, _ = runners(tokenizer, model, input_budget=120)
    assert await index.run(uuid.UUID(job_id)) is JobOutcome.COMPLETED

    assert (
        await summary.run(index.queued_summary_jobs[uuid.UUID(job_id)]) is SummaryOutcome.COMPLETED
    )

    condensing = [p for p in model.prompts if p.rstrip().endswith("Condensed summary:")]
    assert condensing  # the section summaries did not fit one merge call
    assert model.prompts[-1].rstrip().endswith("Overall summary:")
    assert user.get(f"{DOCUMENTS}/{document_id}").json()["summary_status"] == "ready"


async def test_a_failing_summary_leaves_the_document_ready_and_can_be_retried(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-42 (storage side) and summary retry."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    _, _, dispatcher = runners(tokenizer, StubSummariser(fail_on_call=3))

    await dispatcher.run(uuid.UUID(job_id))

    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert (document["status"], document["summary_status"]) == ("ready", "failed")
    assert document["error"] is None
    summary_job = next(j for j in document["jobs"] if j["kind"] == "summary")
    assert summary_job["status"] == "failed" and "500" in summary_job["error"]
    assert summaries(db, document_id) == []
    assert db.execute("SELECT count(*) FROM chunks").fetchone() == (46,)

    retry = user.post(f"{DOCUMENTS}/{document_id}/retry")
    assert retry.status_code == 202
    retried = next(j for j in retry.json()["jobs"] if j["kind"] == "summary")
    assert (retried["status"], retried["retry_count"]) == ("queued", 1)
    _, summary, _ = runners(tokenizer, StubSummariser())
    assert await summary.run(uuid.UUID(retried["id"])) is SummaryOutcome.COMPLETED
    assert user.get(f"{DOCUMENTS}/{document_id}").json()["summary_status"] == "ready"
    assert len([r for r in summaries(db, document_id) if r[0] == "section"]) == 8


async def test_a_summary_cut_short_once_is_retried_once_and_the_retry_is_stored(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """D75: the first section call runs past the output limit; the job asks once more, with
    a reminder, and stores the complete retry. Both calls are in the ledger."""
    model = StubSummariser(cut_short_calls=frozenset({0}))
    _, _, dispatcher = runners(tokenizer, model)
    document_id, job_id = upload(user, "notes.md", NOTE)

    await dispatcher.run(uuid.UUID(job_id))

    assert "ran past the length limit" in model.prompts[1]
    assert model.prompts[1].startswith(model.prompts[0])
    assert any(row[0] == "section" for row in summaries(db, document_id))
    assert jobs(db, document_id)[-1][1] == "completed"
    finish = db.execute(
        "SELECT finish_reason FROM llm_calls WHERE purpose = 'section_summary' ORDER BY created_at"
    ).fetchall()
    reasons = [f for (f,) in finish]
    assert reasons[0] in ("output_limit", "context_exhausted") and reasons[1] == "stop"


async def test_a_summary_the_model_cut_short_is_not_stored(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "notes.md", NOTE)
    _, _, dispatcher = runners(tokenizer, StubSummariser(cut_short=True))

    await dispatcher.run(uuid.UUID(job_id))

    document = user.get(f"{DOCUMENTS}/{document_id}").json()
    assert document["summary_status"] == "failed"
    assert (
        "stopped before finishing"
        in next(j for j in document["jobs"] if j["kind"] == "summary")["error"]
    )
    assert summaries(db, document_id) == []


async def test_retry_is_refused_while_the_summary_is_fine(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id, job_id = upload(user, "notes.md", NOTE)
    _, _, dispatcher = runners(tokenizer, StubSummariser())
    await dispatcher.run(uuid.UUID(job_id))

    response = user.post(f"{DOCUMENTS}/{document_id}/retry")

    assert (response.status_code, response.json()["code"]) == (409, "RETRY_NOT_ALLOWED")


async def test_deleting_a_document_while_it_is_summarised_leaves_nothing_behind(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-46 for summaries."""
    document_id, job_id = upload(user, "paper.pdf", SAMPLE_PDF.read_bytes())
    model = StubSummariser()
    index, summary, _ = runners(tokenizer, model)
    assert await index.run(uuid.UUID(job_id)) is JobOutcome.COMPLETED
    summary_job = index.queued_summary_jobs[uuid.UUID(job_id)]
    reached = asyncio.Event()
    may_continue = asyncio.Event()
    original = summary._progress

    async def pause(job_id: uuid.UUID, current: int, total: int) -> bool:
        if current == 2:
            reached.set()
            await may_continue.wait()
        return await original(job_id, current, total)

    summary._progress = pause  # type: ignore[method-assign]
    task = asyncio.create_task(summary.run(summary_job))
    await asyncio.wait_for(reached.wait(), timeout=30)

    assert (await asyncio.to_thread(user.delete, f"{DOCUMENTS}/{document_id}")).status_code == 204
    may_continue.set()
    outcome = await asyncio.wait_for(task, timeout=30)

    assert outcome is SummaryOutcome.ABANDONED
    assert len(model.prompts) == 2  # no further summary calls after the deletion
    for table in ("documents", "ingestion_jobs", "chunks", "summaries"):
        assert db.execute(f"SELECT count(*) FROM {table}").fetchone() == (0,)
    # The two calls that were made stay in the ledger, with the document reference cleared.
    assert db.execute("SELECT count(*), count(document_id) FROM llm_calls").fetchone() == (2, 0)


class MisattributingSummariser(StubSummariser):
    """Plays a model whose section summary credits one method with another's figure."""

    def __call__(self, request: httpx.Request) -> httpx.Response:
        response = super().__call__(request)
        body = response.json()
        if "Summary of" in body.get("response", ""):
            body["response"] = (
                "The -High variant, which removes high-level retrieval, reaches 67.6% in "
                "Agriculture Comprehensiveness, while LightRAG reaches 67.6% (p. 1)."
            )
            return httpx.Response(200, json=body)
        return response


ABLATION_TABLE = (
    "Table 2: Win rates of the variants.\n"
    "Agriculture Mix\n"
    "LightRAG -High LightRAG -High\n"
    "Comprehensiveness 67.6% 65.2% 61.2% 59.6%\n"
    "Diversity 60.0% 62.0% 50.0% 52.0%\n"
    "Overall 67.6% 64.8% 60.0% 57.6%\n"
    "The -High variant removes high-level retrieval."
)


async def test_a_section_summary_that_credits_another_methods_figure_is_corrected_before_storage(
    user: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """D75 (the Q1 case): the summary gives -High the full model's 67.6%; the table of the
    section's chunks has -High at 65.2% under those labels, so the figure is replaced —
    read from the table, never invented — and the corrected summary is what is stored."""
    model = MisattributingSummariser()
    _, summary, dispatcher = runners(tokenizer, model)
    document_id, job_id = upload(user, "ablation.txt", ABLATION_TABLE.encode())

    await dispatcher.run(uuid.UUID(job_id))

    stored = summaries(db, document_id)
    section = next(row for row in stored if row[0] == "section")
    assert "reaches 65.2% in Agriculture Comprehensiveness" in section[5]
    assert "67.6%" in section[5]  # LightRAG's own figure stays
    report = summary.verification_reports[0]
    assert report["mislabelled_before"] == ["67.6%"]
    assert [(e["kind"], e["before"], e["after"]) for e in report["edits"]] == [
        ("figure", "67.6%", "65.2%")
    ]
    assert report["mislabelled_after"] == [] and report["changed"] is True
