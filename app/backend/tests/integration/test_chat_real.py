"""A question answered end to end by the real models (bge-m3 and qwen3).

Run with:  pytest -m llm tests/integration/test_chat_real.py -s
"""

import json
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
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.conftest import register_and_login

pytestmark = [pytest.mark.llm, pytest.mark.db]

SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
QUESTION = "Performance of ablated versions of LightRAG"


async def test_the_paper_is_indexed_and_a_question_gets_a_cited_streamed_answer(
    client: TestClient, db: psycopg.Connection
) -> None:
    """AC-04 and AC-05 with the real models; every call stays within the limit."""
    register_and_login(client, "kim")
    settings = get_settings()
    uploaded = client.post(
        "/api/v1/documents", files={"file": ("2410.05779v3.pdf", SAMPLE_PDF.read_bytes())}
    ).json()
    runner = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=FileStorage(settings.data_dir),
        tokenizer=Qwen3TokenCounter(),
        embedder=OllamaEmbedder(settings),
        settings=settings,
    )
    assert await runner.run(uuid.UUID(uploaded["jobs"][0]["id"])) is JobOutcome.COMPLETED
    conversation = client.post("/api/v1/conversations", json={}).json()["id"]

    response = client.post(
        f"/api/v1/conversations/{conversation}/messages", json={"question": QUESTION}
    )

    assert response.status_code == 200
    stream = []
    for block in response.text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    by_name = dict(stream)
    answer = "".join(data["text"] for name, data in stream if name == "delta")
    print(f"\nsources: {[(s['index'], s['page_start'], s['score']) for s in by_name['sources']]}")
    print(f"usage: {by_name['usage']}  done: {by_name['done']}")
    print(f"answer:\n{answer}")

    # Streamed in many pieces, finished naturally, and grounded in cited sources.
    assert sum(1 for name, _ in stream if name == "delta") > 5
    assert by_name["done"]["status"] == "completed"
    assert by_name["done"]["answered"] is True
    assert by_name["done"]["cited"]
    assert len(by_name["sources"]) == settings.top_k
    usage = by_name["usage"]
    assert usage["prompt_tokens"] + usage["completion_tokens"] <= settings.llm_context_limit
    # The ledger agrees, and the local estimate was not below what Ollama measured.
    call = db.execute(
        "SELECT status, estimated_prompt_tokens, prompt_tokens, completion_tokens FROM llm_calls"
    ).fetchone()
    assert call is not None
    assert call[0] == "completed"
    assert call[2] == usage["prompt_tokens"] and call[3] == usage["completion_tokens"]
    assert call[1] >= call[2]
    report = client.get("/api/v1/llm-calls").json()
    assert report["underestimate_events"] == 0
    assert report["measured"]["max_total_tokens"] <= settings.llm_context_limit
