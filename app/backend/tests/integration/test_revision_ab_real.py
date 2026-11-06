"""D69 A/B experiment with the real models: single call (A), conditional revision (B),
always revise (C, Q3 only), on the same questions, the same documents and the same
settings, in one run. Every candidate answer is written to
evaluation/revision-ab/runs/<arm>-<question>-<run>.json for the independent, hand-made
evaluation against the key facts; the key facts never reach the model.

Run with:  pytest -m llm tests/integration/test_revision_ab_real.py -s
Narrow it:  AB_ARMS=A,B AB_QUESTIONS=Q2,Q3 AB_RUNS=1 (read through get_settings' environment
is not used here: these are read with os.environ by the test only).
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
RUNS_DIR = ROOT / "evaluation" / "revision-ab" / "runs"

QUESTIONS = {
    "Q1": ("summary this document.", "lightrag"),
    "Q2": ("compare lightRAG with GraphRAG", "lightrag"),
    "Q3": ("Performance of ablated versions of LightRAG", "lightrag"),
    "FACT": (
        "How many tokens does GraphRAG consume in the retrieval phase on the Legal dataset?",
        "lightrag",
    ),
    "NOANS": ("What is the capital of France?", "lightrag"),
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
ARMS = {
    "A": {"answer_revision": False},
    "B": {"answer_revision": True},
    "C": {"answer_revision": True, "revision_always": True},
}
DEFAULT_PLAN = {  # arm -> question -> runs
    "A": {"Q1": 3, "Q2": 3, "Q3": 3, "FACT": 1, "NOANS": 1, "G1": 2, "G2": 2},
    "B": {"Q1": 3, "Q2": 3, "Q3": 3, "FACT": 1, "NOANS": 1, "G1": 2, "G2": 2},
    "C": {"Q3": 3},
}


def _plan() -> dict[str, dict[str, int]]:
    arms = os.environ.get("AB_ARMS", "A,B,C").split(",")
    questions = os.environ.get("AB_QUESTIONS")
    runs = os.environ.get("AB_RUNS")
    plan: dict[str, dict[str, int]] = {}
    for arm in arms:
        chosen = DEFAULT_PLAN[arm]
        if questions:
            chosen = {q: n for q, n in chosen.items() if q in questions.split(",")}
        plan[arm] = {q: (int(runs) if runs else n) for q, n in chosen.items()}
    return plan


def _events(text: str) -> list[tuple[str, dict]]:
    stream = []
    for block in text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        stream.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    return stream


async def test_ab_experiment(client: TestClient, db: psycopg.Connection) -> None:
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
    documents: dict[str, str] = {}
    for key, path in (("lightrag", LIGHTRAG), ("graphrag", GRAPHRAG)):
        uploaded = client.post(
            "/api/v1/documents", files={"file": (path.name, path.read_bytes())}
        ).json()
        job = uuid.UUID(uploaded["jobs"][0]["id"])
        assert await index.run(job) is JobOutcome.COMPLETED
        documents[key] = uploaded["id"]
        if key == "lightrag":  # Q1 needs the stored summaries
            summary = SummaryJobRunner(
                sessions=sessions,
                storage=storage,
                counter=counter,
                gateway=OllamaGateway(settings=settings, sessions=sessions, counter=counter),
            )
            assert await summary.run(index.queued_summary_jobs[job]) is SummaryOutcome.COMPLETED
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    for arm, questions in _plan().items():
        overrides = ARMS[arm]
        client.app.dependency_overrides[get_settings] = lambda o=overrides: (  # type: ignore[attr-defined]
            get_settings().model_copy(update=o)
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
                    "arm": arm,
                    "question": key,
                    "question_text": question,
                    "document": document,
                    "run": run,
                    "settings": {
                        "model": settings.llm_model,
                        "top_k": settings.top_k,
                        "chunk_size": settings.chunk_size,
                        "overrides": overrides,
                    },
                    "elapsed_seconds": round(elapsed, 1),
                    "stages": [d["stage"] for n, d in stream if n == "stage"],
                    "route": by_name.get("route"),
                    "sources": [
                        {
                            k: s[k]
                            for k in ("index", "kind", "page_start", "page_end", "origin", "score")
                        }
                        | {"snippet": s["snippet"][:80]}
                        for s in by_name.get("sources", [])
                    ],
                    "final_answer": answer,
                    "usage": by_name.get("usage"),
                    "done": by_name.get("done"),
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
                (RUNS_DIR / f"{arm}-{key}-{run}.json").write_text(
                    json.dumps(record, indent=1, ensure_ascii=False) + "\n"
                )
                done = by_name["done"]
                revision = done.get("revision") or {}
                print(
                    f"\n[{arm} {key} run {run}] {elapsed:.0f}s calls={len(calls)} "
                    f"status={done['status']} chosen={revision.get('chosen')} "
                    f"rev_status={revision.get('status')} skipped={revision.get('skipped')} "
                    f"draft_triggers={[t['kind'] for t in revision.get('draft_triggers', [])]} "
                    "revision_triggers="
                    f"{[t['kind'] for t in revision.get('revision_triggers', [])]} "
                    f"mislabelled={len(done['mislabelled_numbers'])} "
                    f"overstated={len(done['overstated_claims'])} "
                    f"doubtful={len(done['doubtful_citations'])}"
                )
                for c in calls:
                    assert c[2] + c[3] <= settings.llm_context_limit, c
                    assert c[4] >= c[2], c  # the estimate was never below the measure
        client.app.dependency_overrides.pop(get_settings, None)  # type: ignore[attr-defined]
    report = client.get("/api/v1/llm-calls").json()
    assert report["underestimate_events"] == 0
    assert report["measured"]["max_total_tokens"] <= settings.llm_context_limit
