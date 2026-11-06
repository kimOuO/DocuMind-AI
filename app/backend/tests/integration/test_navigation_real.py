"""Navigation questions with the real models: where in the paper to look (section, table,
figure, page), in the default single-call mode. Answers are printed for a hand check
against the paper's structure (evaluation/ground-truth/paper-structure.json).

Run with:  pytest -m llm tests/integration/test_navigation_real.py -s
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
QUESTIONS = [
    "Which section and which table of the paper report the performance of the ablated "
    "versions of LightRAG, and on which page?",
    "Where in the paper is LightRAG compared with GraphRAG? Name the sections, tables and "
    "figures to look at.",
    "In which section is the dual-level retrieval paradigm described?",
    "消融實驗的結果要看論文的哪一節、哪個表格、第幾頁？",
    "Which table gives the statistics of the four datasets, and where is it?",
]


async def test_where_to_look_questions(client: TestClient, db: psycopg.Connection) -> None:
    register_and_login(client, "kim")
    settings = get_settings()
    assert settings.answer_revision is False  # the default single-call mode
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

    for question in QUESTIONS:
        conversation = client.post("/api/v1/conversations", json={}).json()["id"]
        response = client.post(
            f"/api/v1/conversations/{conversation}/messages", json={"question": question}
        )
        assert response.status_code == 200, response.text
        stream = []
        for block in response.text.strip().split("\n\n"):
            name, data = block.split("\n", 1)
            stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
        by_name = dict(stream)
        answer = "".join(d["text"] for n, d in stream if n == "delta")
        print(f"\n######## Q: {question}")
        print(f"route: {by_name['route']['type']}  usage: {by_name.get('usage')}")
        for s in by_name.get("sources", []):
            print(f"  [{s['index']}] p{s['page_start']} {s['origin']:13} {s['snippet'][:70]!r}")
        print(f"answer:\n{answer}")
        print(f"events: {[n for n, _ in stream]}")
        if "error" in by_name:
            print(f"error: {by_name['error']}")
        if "done" in by_name:
            print(f"done: cited={by_name['done']['cited']} answered={by_name['done']['answered']}")
