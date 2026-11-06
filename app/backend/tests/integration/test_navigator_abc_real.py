"""D71 A/B/C experiment with the real models: C = single call (default), A = roles in one
prompt, B = navigate (plan call, plan-driven fetch, answer call), on the same questions,
documents and settings, in one run. Every run is written to
evaluation/navigator-abc/runs/<arm>-<question>-<run>.json with the full text of every
source the answering call saw, so that Evidence Coverage can be computed offline
against evaluation/ground-truth/evidence-locations.json; the key facts never reach the
model.

Run with:  pytest -m llm tests/integration/test_navigator_abc_real.py -s
Narrow it with the environment: ABC_ARMS=C,A ABC_QUESTIONS=Q2,Q3 ABC_RUNS=1
Label a rerun of one arm so that it does not overwrite the earlier records (D73: the
reworked navigate mode is recorded as B2): ABC_ARMS=B ABC_LABEL=B2
"""

import json
import os
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

ROOT = Path(__file__).resolve().parents[4]
LIGHTRAG = ROOT / "sample-documents" / "2410.05779v3.pdf"
GRAPHRAG = ROOT / "sample-documents" / "2404.16130v2.pdf"
RUNS_DIR = ROOT / "evaluation" / "navigator-abc" / "runs"

QUESTIONS = {
    "Q1": ("summary this document.", "lightrag"),
    "Q2": ("compare lightRAG with GraphRAG", "lightrag"),
    "Q3": ("Performance of ablated versions of LightRAG", "lightrag"),
    "G1": (
        "How many context units and tokens do the root-level community summaries (C0) and the "
        "source-text summarization (TS) use on the Podcast and News datasets?",
        "graphrag",
    ),
    "G2": (
        "Compare condition C2 with vector RAG (SS) on comprehensiveness in the Podcast and News "
        "datasets",
        "graphrag",
    ),
}
ARMS = {"C": "single", "A": "roles", "B": "navigate"}


def _plan() -> dict[str, dict[str, int]]:
    arms = os.environ.get("ABC_ARMS", "C,A,B").split(",")
    questions = os.environ.get("ABC_QUESTIONS", ",".join(QUESTIONS)).split(",")
    runs = int(os.environ.get("ABC_RUNS", "3"))
    return {arm: {q: runs for q in questions} for arm in arms}


def _events(text: str) -> list[tuple[str, dict]]:
    stream = []
    for block in text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    return stream


async def test_abc_experiment(client: TestClient, db: psycopg.Connection) -> None:
    register_and_login(client, "kim")
    settings = get_settings()
    counter = Qwen3TokenCounter()
    storage = FileStorage(settings.data_dir)
    sessions = get_sessionmaker()
    index = IndexJobRunner(
        sessions=sessions,
        storage=storage,
        tokenizer=counter,
        embedder=OllamaEmbedder(settings),
        settings=settings,
    )
    summary = SummaryJobRunner(
        sessions=sessions,
        storage=storage,
        counter=counter,
        gateway=OllamaGateway(settings=settings, sessions=sessions, counter=counter),
    )
    documents: dict[str, str] = {}
    for key, path in (("lightrag", LIGHTRAG), ("graphrag", GRAPHRAG)):
        uploaded = client.post(
            "/api/v1/documents", files={"file": (path.name, path.read_bytes())}
        ).json()
        job = uuid.UUID(uploaded["jobs"][0]["id"])
        assert await index.run(job) is JobOutcome.COMPLETED
        documents[key] = uploaded["id"]
        # Both documents get their summaries: the document map needs the section titles
        # and page ranges, and Q1 needs the stored summaries.
        assert await summary.run(index.queued_summary_jobs[job]) is SummaryOutcome.COMPLETED
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    label = os.environ.get("ABC_LABEL")
    for arm, questions in _plan().items():
        answer_mode = ARMS[arm]
        recorded_arm = label if label and len(_plan()) == 1 else arm
        client.app.dependency_overrides[get_settings] = lambda m=answer_mode: (  # type: ignore[attr-defined]
            get_settings().model_copy(update={"answer_mode": m})
        )
        for key, runs in questions.items():
            question, document = QUESTIONS[key]
            for run in range(1, runs + 1):
                conversation = client.post("/api/v1/conversations", json={}).json()["id"]
                before = db.execute("SELECT count(*) FROM llm_calls").fetchone()[0]
                started = time.perf_counter()
                response = client.post(
                    f"/api/v1/conversations/{conversation}/messages",
                    json={"question": question, "document_ids": [documents[document]]},
                )
                elapsed = time.perf_counter() - started
                assert response.status_code == 200, response.text
                stream = _events(response.text)
                by_name = dict(stream)
                answer = "".join(d["text"] for n, d in stream if n == "delta")
                calls = db.execute(
                    "SELECT purpose, status, prompt_tokens, completion_tokens, "
                    "estimated_prompt_tokens, finish_reason, duration_ms "
                    "FROM llm_calls ORDER BY created_at OFFSET %s",
                    (before,),
                ).fetchall()
                record = {
                    "arm": recorded_arm,
                    "answer_mode": answer_mode,
                    "question": key,
                    "question_text": question,
                    "document": document,
                    "run": run,
                    "settings": {
                        "model": settings.llm_model,
                        "embed_model": settings.embed_model,
                        "top_k": settings.top_k,
                        "chunk_size": settings.chunk_size,
                        "chunk_overlap": settings.chunk_overlap,
                        "min_similarity": settings.min_similarity,
                    },
                    "elapsed_seconds": round(elapsed, 1),
                    "stages": [d["stage"] for n, d in stream if n == "stage"],
                    "route": by_name.get("route"),
                    "sources": by_name.get("sources", []),  # full text, for coverage
                    "final_answer": answer,
                    "usage": by_name.get("usage"),
                    "done": by_name.get("done"),
                    "error": by_name.get("error"),
                    "llm_calls": [
                        {
                            "purpose": c[0],
                            "status": c[1],
                            "prompt_tokens": c[2],
                            "completion_tokens": c[3],
                            "estimated_prompt_tokens": c[4],
                            "finish_reason": c[5],
                            "duration_ms": c[6],
                        }
                        for c in calls
                    ],
                }
                (RUNS_DIR / f"{recorded_arm}-{key}-{run}.json").write_text(
                    json.dumps(record, indent=1, ensure_ascii=False) + "\n"
                )
                done = by_name.get("done") or {}
                navigation = done.get("navigation") or {}
                print(
                    f"\n[{recorded_arm} {key} run {run}] {elapsed:.0f}s calls={len(calls)} "
                    f"route={(by_name.get('route') or {}).get('type')} "
                    f"status={done.get('status', by_name.get('error'))} "
                    "sources="
                    f"{[(s['page_start'], s['origin'][:4]) for s in by_name.get('sources', [])]} "
                    f"plan_located={navigation.get('located')}/{len(navigation.get('items', []))} "
                    f"kept={navigation.get('kept')} excluded={navigation.get('excluded_budget')}"
                )
                for c in calls:
                    assert c[2] + c[3] <= settings.llm_context_limit, c
                    assert c[4] >= c[2], c
        client.app.dependency_overrides.pop(get_settings, None)  # type: ignore[attr-defined]
    report = client.get("/api/v1/llm-calls").json()
    assert report["underestimate_events"] == 0
    assert report["measured"]["max_total_tokens"] <= settings.llm_context_limit
