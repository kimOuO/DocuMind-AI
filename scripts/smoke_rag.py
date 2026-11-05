#!/usr/bin/env python3
"""Minimal end-to-end check of the RAG building blocks (acceptance criterion AC-47).

    bge-m3 embeddings  ->  pgvector (temporary table)  ->  cosine top-k  ->  qwen3 answer

It proves early that Ollama, the embedding model and pgvector work together with
this project's database and settings. It is not part of the application: it
writes only to a temporary table that disappears when the connection closes.

Run with `make smoke`. Exits 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import httpx
import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app" / "backend"))
from app.core.env_loader import get_settings

PASSAGES = [
    (
        "LightRAG builds a graph of entities and relations from the text and retrieves at "
        "two levels: low-level retrieval for specific entities and high-level retrieval "
        "for themes."
    ),
    (
        "GraphRAG generates community reports over a knowledge graph. Answering a global "
        "question traverses many communities, which makes retrieval expensive in tokens "
        "and API calls."
    ),
    "Sourdough bread needs a starter that is fed with flour and water for several days.",
    "The Hubble Space Telescope was launched into low Earth orbit in 1990.",
    "PostgreSQL is a relational database; the pgvector extension adds a vector column type.",
]
QUESTION = "How does LightRAG retrieve information?"
EXPECTED_TOP = 0
TOP_K = 2

settings = get_settings()
failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f": {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def to_vector(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.7f}" for v in values) + "]"


def main() -> int:
    ollama = settings.ollama_base_url
    print(
        f"Ollama {ollama} | LLM {settings.llm_model} | embedding {settings.embed_model}"
    )
    print(f"Database {settings.db_host}:{settings.db_port}/{settings.db_name}\n")

    # 1. Embeddings
    started = time.time()
    response = httpx.post(
        f"{ollama}/api/embed",
        json={"model": settings.embed_model, "input": [*PASSAGES, QUESTION]},
        timeout=120,
    )
    response.raise_for_status()
    vectors = response.json()["embeddings"]
    dimensions = len(vectors[0])
    check(
        "embeddings",
        len(vectors) == len(PASSAGES) + 1 and dimensions == 1024,
        f"{len(vectors)} vectors, {dimensions} dimensions, {time.time() - started:.1f}s",
    )

    # 2. pgvector: store and search
    dsn = (
        f"host={settings.db_host} port={settings.db_port} dbname={settings.db_name} "
        f"user={settings.db_user} password={settings.db_password}"
    )
    with psycopg.connect(dsn) as conn:
        version = conn.execute(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        ).fetchone()
        check(
            "pgvector extension",
            version is not None,
            f"version {version[0] if version else '-'}",
        )

        conn.execute(
            f"CREATE TEMP TABLE smoke_chunks (id int, body text, embedding vector({dimensions}))"
        )
        for index, (passage, vector) in enumerate(zip(PASSAGES, vectors, strict=False)):
            conn.execute(
                "INSERT INTO smoke_chunks VALUES (%s, %s, %s::vector)",
                (index, passage, to_vector(vector)),
            )
        rows = conn.execute(
            "SELECT id, body, 1 - (embedding <=> %s::vector) AS similarity "
            "FROM smoke_chunks ORDER BY embedding <=> %s::vector LIMIT %s",
            (to_vector(vectors[-1]), to_vector(vectors[-1]), TOP_K),
        ).fetchall()
    for row in rows:
        print(f"       #{row[0]} similarity={row[2]:.3f}  {row[1][:60]}...")
    check(
        "retrieval",
        bool(rows) and rows[0][0] == EXPECTED_TOP,
        f"top-1 is passage #{rows[0][0]}, expected #{EXPECTED_TOP}",
    )

    # 3. Generation from the retrieved evidence
    evidence = "\n".join(f"[{i + 1}] {row[1]}" for i, row in enumerate(rows))
    prompt = (
        "Answer the question using only the evidence. Cite the evidence number in brackets.\n\n"
        f"Evidence:\n{evidence}\n\nQuestion: {QUESTION}\nAnswer in one sentence."
    )
    started = time.time()
    response = httpx.post(
        f"{ollama}/api/generate",
        json={
            "model": settings.llm_model,
            "prompt": prompt,
            "stream": False,
            "think": settings.llm_thinking,
            "options": {
                "num_ctx": settings.llm_context_limit,
                "num_predict": 200,
                "temperature": 0,
            },
        },
        timeout=600,
    )
    response.raise_for_status()
    result = response.json()
    answer = result.get("response", "").strip()
    prompt_tokens, completion_tokens = (
        result.get("prompt_eval_count"),
        result.get("eval_count"),
    )
    print(f"       answer: {answer}")
    check("generation", bool(answer), f"{time.time() - started:.1f}s")
    check("answer cites the evidence", "[1]" in answer or "[2]" in answer)
    measured = isinstance(prompt_tokens, int) and isinstance(completion_tokens, int)
    total = (prompt_tokens or 0) + (completion_tokens or 0)
    check(
        "token usage reported by Ollama",
        measured and total <= settings.llm_context_limit,
        f"prompt={prompt_tokens} completion={completion_tokens} total={total} "
        f"limit={settings.llm_context_limit}",
    )

    print(
        "\nResult:",
        "ALL CHECKS PASSED" if not failures else f"FAILED: {', '.join(failures)}",
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
