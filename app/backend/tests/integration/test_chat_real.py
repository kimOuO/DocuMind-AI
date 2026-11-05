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
    for source in by_name["sources"]:
        print(f"  [{source['index']}] p{source['page_start']} {source['snippet'][:70]!r}")
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


# Characters that exist only in Simplified Chinese; none may appear in an answer.
SIMPLIFIED_ONLY = "国们这为对说时会学关现还从进间们种实发体样问题级义论样变统对双检图据"


async def test_a_chinese_question_is_answered_in_traditional_chinese(
    client: TestClient, db: psycopg.Connection
) -> None:
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
        f"/api/v1/conversations/{conversation}/messages",
        json={"question": "LightRAG 的雙層檢索是什麼？"},
    )

    answer = "".join(
        json.loads(block.split("\n", 1)[1].removeprefix("data: "))["text"]
        for block in response.text.strip().split("\n\n")
        if block.startswith("event: delta")
    )
    print(f"\nanswer:\n{answer}")
    assert answer
    simplified = [c for c in answer if c in SIMPLIFIED_ONLY]
    assert simplified == [], f"Simplified characters in the answer: {simplified}"

    # AC-16: a follow-up with a pronoun is rewritten from the conversation first.
    follow_up = client.post(
        f"/api/v1/conversations/{conversation}/messages",
        json={"question": "那它的缺點呢？"},
    )
    stream = []
    for block in follow_up.text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    by_name = dict(stream)
    rewritten = by_name["route"]["standalone_question"]
    follow_up_answer = "".join(d["text"] for n, d in stream if n == "delta")
    rewrite_call = db.execute(
        "SELECT status, finish_reason, prompt_tokens, completion_tokens FROM llm_calls "
        "WHERE purpose = 'rewrite'"
    ).fetchone()
    print(f"\nfollow-up rewritten as: {rewritten}\nrewrite call: {rewrite_call}")
    print(f"follow-up answer:\n{follow_up_answer}")
    assert rewrite_call is not None and rewrite_call[0] == "completed"
    assert rewrite_call[2] + rewrite_call[3] <= settings.llm_context_limit
    assert rewritten != "那它的缺點呢？"
    assert any(word in rewritten for word in ("LightRAG", "雙層", "檢索"))


async def test_a_question_the_paper_cannot_answer_is_refused_before_any_llm_call(
    client: TestClient, db: psycopg.Connection
) -> None:
    """AC-15 with the real embedder: baking sourdough bread scores below the threshold."""
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
    question = "如何在家烤酸種麵包？"

    # What the retriever sees, for the record (the threshold is calibrated in P4).
    async with get_sessionmaker()() as session:
        from app.models import User
        from app.retrieval.service import RetrievalService, SearchScope

        actor = await session.get(User, uuid.UUID(client.get("/api/v1/users/me").json()["id"]))
        assert actor is not None
        chunks = await RetrievalService(session, OllamaEmbedder(settings), settings).search(
            actor, SearchScope("all", [uuid.UUID(uploaded["id"])]), question
        )
    print(f"\ntop similarities for {question!r}: {[round(c.score, 3) for c in chunks]}")

    response = client.post(
        f"/api/v1/conversations/{conversation}/messages", json={"question": question}
    )

    stream = []
    for block in response.text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    by_name = dict(stream)
    print(f"done: {by_name['done']}")
    assert chunks[0].score < settings.min_similarity
    assert by_name["done"]["answered"] is False
    assert by_name["sources"] == []
    assert "usage" not in by_name
    assert db.execute("SELECT count(*) FROM llm_calls").fetchone() == (0,)
