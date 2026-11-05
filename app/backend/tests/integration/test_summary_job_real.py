"""The paper summarised by the real model: calls, tokens and the page tags on numbers.

Run with:  pytest -m llm tests/integration/test_summary_job_real.py -s
"""

import re
import time
import uuid
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.llm.embedding import OllamaEmbedder
from app.llm.gateway import OllamaGateway
from app.llm.tokenizer import Qwen3TokenCounter
from app.summarization.service import SummaryJobRunner, SummaryOutcome
from tests.integration.conftest import register_and_login

pytestmark = [pytest.mark.llm, pytest.mark.db]

SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
PAGE_TAG = re.compile(r"\(p\. ?(\d{1,2})\)")


async def test_the_paper_is_summarised_within_the_budget_with_page_tags(
    client: TestClient, db: psycopg.Connection
) -> None:
    register_and_login(client, "kim")
    settings = get_settings()
    counter = Qwen3TokenCounter()
    storage = FileStorage(settings.data_dir)
    uploaded = client.post(
        "/api/v1/documents", files={"file": ("2410.05779v3.pdf", SAMPLE_PDF.read_bytes())}
    ).json()
    index = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        tokenizer=counter,
        embedder=OllamaEmbedder(settings),
        settings=settings,
    )
    assert await index.run(uuid.UUID(uploaded["jobs"][0]["id"])) is JobOutcome.COMPLETED
    summary = SummaryJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        counter=counter,
        gateway=OllamaGateway(settings=settings, sessions=get_sessionmaker(), counter=counter),
    )

    started = time.perf_counter()
    outcome = await summary.run(index.queued_summary_jobs[uuid.UUID(uploaded["jobs"][0]["id"])])
    elapsed = time.perf_counter() - started

    assert outcome is SummaryOutcome.COMPLETED
    rows = db.execute(
        "SELECT level, ordinal, title, page_start, page_end, token_count, text FROM summaries "
        "ORDER BY level, ordinal"
    ).fetchall()
    calls = db.execute(
        "SELECT purpose, status, finish_reason, prompt_tokens, completion_tokens, duration_ms "
        "FROM llm_calls ORDER BY created_at"
    ).fetchall()
    print(
        f"\n{len(calls)} calls in {elapsed:.0f}s; "
        f"max prompt+completion = {max(c[3] + c[4] for c in calls)}"
    )
    for level, ordinal, title, start, end, tokens, text in rows:
        tags = PAGE_TAG.findall(text)
        print(
            f"  {level:8} {ordinal} {str(title)[:32]:32} p{start}-{end} {tokens:4} tokens, "
            f"page tags {sorted(set(tags))}"
        )
    document_text = next(r[6] for r in rows if r[0] == "document")
    print(f"\ndocument summary:\n{document_text}")

    assert all(c[1] == "completed" and c[2] == "stop" for c in calls)
    assert all(c[3] + c[4] <= settings.llm_context_limit for c in calls)
    assert client.get("/api/v1/llm-calls").json()["underestimate_events"] == 0
    # Numbers in section summaries carry page tags that lie within the section's pages.
    for level, _, title, start, end, _, text in rows:
        if level != "section":
            continue
        for page in map(int, PAGE_TAG.findall(text)):
            assert start <= page <= end, (title, page, start, end)
    assert PAGE_TAG.search(document_text), "the document summary keeps at least one page tag"
