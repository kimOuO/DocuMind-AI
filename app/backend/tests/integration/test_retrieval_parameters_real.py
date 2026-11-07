"""P4 retrieval-parameter experiment with the real embedding model (AC-19, spec 02 §9).

For each chunk size the two sample documents are ingested afresh (embeddings only, no
summaries); every question of evaluation/ground-truth/question-set.json is embedded once and
searched within its own documents; Recall@K, source hit rate and evidence tokens are computed
for K in 3, 5, 8 against the verbatim evidence (same document and page, text contained, or at
least half of its characters when a chunk boundary cuts it). Hybrid retrieval — PostgreSQL
full-text search fused with the vector ranking by Reciprocal Rank Fusion — is computed in this
harness from the same chunks, so that the production code changes only if it wins. The top-1
similarity of every question (including the no-answer ones) is recorded for the threshold
sweep. One result file per chunk size: evaluation/retrieval-parameters/runs/chunk<size>.json.

Run with:  make eval   (or: pytest -m llm tests/integration/test_retrieval_parameters_real.py -s)
Narrow it:  EVAL_CHUNK_SIZES=400 EVAL_QUESTIONS=Q2,T1
"""

import difflib
import json
import math
import os
import re
import time
import uuid
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text as sql_text

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.ingestion.tables import _CAPTION, _is_header_line, _is_prose_line, _is_row, header_lines
from app.llm.embedding import OllamaEmbedder
from app.llm.tokenizer import get_token_counter
from app.models import User
from app.retrieval.repository import RetrievalRepository
from app.retrieval.service import RetrievalService
from tests.integration.conftest import register_and_login

pytestmark = [pytest.mark.llm, pytest.mark.db]

ROOT = Path(__file__).resolve().parents[4]
QUESTION_SET = ROOT / "evaluation" / "ground-truth" / "question-set.json"
RUNS_DIR = ROOT / "evaluation" / "retrieval-parameters" / "runs"
DOCUMENTS = {
    "lightrag": ROOT / "sample-documents" / "2410.05779v3.pdf",
    "graphrag": ROOT / "sample-documents" / "2404.16130v2.pdf",
}
KS = (3, 5, 8)
CANDIDATES = 20  # each ranking's depth before fusion
RRF_K = 60


def _norm(text: str) -> str:
    return " ".join(text.split())


_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?%?")


def covers(chunk_text: str, evidence: str) -> bool:
    """Spec §9.1: the chunk contains the evidence text, or at least half of its characters
    when a chunk boundary cuts it (longest common block). A table's rows are rewritten cell
    by cell at ingestion (ADR 0007), so evidence that is mostly figures counts as covered
    when the chunk holds at least 90% of those figures."""
    chunk_text, evidence = _norm(chunk_text), _norm(evidence)
    if evidence in chunk_text:
        return True
    figures = _NUMBER.findall(evidence)
    if len(figures) >= 4:
        present = sum(1 for f in figures if f in chunk_text)
        if present >= 0.9 * len(figures):
            return True
    match = difflib.SequenceMatcher(None, chunk_text, evidence, autojunk=False).find_longest_match(
        0, len(chunk_text), 0, len(evidence)
    )
    return match.size >= len(evidence) / 2


def table_blocks(text: str) -> list[str]:
    """A linearised table chunk split at its block headers (the header lines between row
    groups, e.g. one per baseline); each block carries the caption and the group headers.
    One block (or none) means the chunk has nothing to split."""
    lines = text.splitlines()
    if not lines or not _CAPTION.match(lines[0].strip()):
        return []
    first_row = next((i for i, line in enumerate(lines) if _is_row(line)), None)
    if first_row is None:
        return []
    head = [lines[0], *header_lines(lines, first_row)]
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines[first_row:]:
        if not _is_row(line) and _is_header_line(line) and not _is_prose_line(line):
            if current:
                blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)
    if len(blocks) <= 1:
        return []
    # The first block's column header is the last header line; the later blocks each start
    # with their own, so they take the caption and the group header only.
    shared = head[:-1] if len(head) > 1 else head
    return ["\n".join([*head, *blocks[0]])] + ["\n".join([*shared, *block]) for block in blocks[1:]]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True)) / math.sqrt(
        sum(x * x for x in a) * sum(y * y for y in b)
    )


def _without_text(chunk: dict) -> dict:
    return {k: v for k, v in chunk.items() if k != "text"}


def rrf(*rankings: list[uuid.UUID]) -> list[uuid.UUID]:
    scores: dict[uuid.UUID, float] = {}
    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
    return sorted(scores, key=lambda c: (-scores[c], str(c)))


def _payload(ids: list[uuid.UUID], by_id: dict, doc_key: dict[str, str]) -> list[dict]:
    return [
        {
            "chunk_id": str(i),
            "document_id": str(by_id[i].document_id),
            "document": doc_key[str(by_id[i].document_id)],
            "page": by_id[i].page,
            "ordinal": by_id[i].ordinal,
            "token_count": by_id[i].token_count,
            "score": by_id[i].score,
            "text": by_id[i].text,
        }
        for i in ids
    ]


def _metrics(
    ranked: list[dict], evidence: list[dict], documents: dict[str, str], *, whole: bool = False
) -> dict:
    """Per K: recall (evidence items covered / all), hit (any covered), evidence tokens.
    `whole` scores the complete list under every K (a Top-K already expanded)."""
    out = {}
    for k in KS:
        top = ranked if whole else ranked[:k]
        covered = [
            any(
                c["document_id"] == documents[e["document"]]
                and c["page"] == e["page"]
                and covers(c["text"], e["text"])
                for c in top
            )
            for e in evidence
        ]
        out[str(k)] = {
            "recall": (sum(covered) / len(covered)) if covered else None,
            "hit": any(covered) if covered else None,
            "covered": [e["label"] for e, c in zip(evidence, covered, strict=True) if c],
            "evidence_tokens": sum(c["token_count"] for c in top),
            "pages": [(c["document"], c["page"]) for c in top],
        }
    return out


async def test_retrieval_parameters(client: TestClient, db: psycopg.Connection) -> None:
    register_and_login(client, "kim")
    owner_id = db.execute("SELECT id FROM users WHERE username = 'kim'").fetchone()[0]
    base = get_settings()
    question_set = json.loads(QUESTION_SET.read_text())
    wanted = os.environ.get("EVAL_QUESTIONS")
    questions = [
        q
        for q in question_set["questions"]
        if q["route"] != "summary" and (not wanted or q["id"] in wanted.split(","))
    ]
    sizes = [int(s) for s in os.environ.get("EVAL_CHUNK_SIZES", "256,400,600").split(",")]
    embedder = OllamaEmbedder(base)
    counter = get_token_counter()
    storage = FileStorage(base.data_dir)
    sessions = get_sessionmaker()
    # One embedding per question, shared by every chunk size (the question does not change).
    question_embeddings = {}
    for q in questions:
        [question_embeddings[q["id"]]] = await embedder.embed([q["question"]])

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    for size in sizes:
        overlap = size // 5  # the default 400/80 ratio, kept for every size
        settings = base.model_copy(update={"chunk_size": size, "chunk_overlap": overlap})
        index = IndexJobRunner(
            sessions=sessions,
            storage=storage,
            tokenizer=counter,
            embedder=embedder,
            settings=settings,
        )
        # Fresh documents for this chunk size (the previous size's are deleted first).
        for doc in client.get("/api/v1/documents").json():
            assert client.delete(f"/api/v1/documents/{doc['id']}").status_code == 204
        documents: dict[str, str] = {}
        started = time.perf_counter()
        for key, path in DOCUMENTS.items():
            uploaded = client.post(
                "/api/v1/documents", files={"file": (path.name, path.read_bytes())}
            ).json()
            assert await index.run(uuid.UUID(uploaded["jobs"][0]["id"])) is JobOutcome.COMPLETED
            documents[key] = uploaded["id"]
        ingest_seconds = time.perf_counter() - started
        chunk_count = db.execute("SELECT count(*) FROM chunks").fetchone()[0]

        # D82 (user's idea): besides the chunk's one vector — the average meaning of the
        # whole chunk — a table chunk gets one vector per block, and its score is the best of
        # them. Computed here from the stored chunks to measure the idea before any change
        # to the production code.
        all_chunks = db.execute(
            "SELECT c.id, c.document_id, c.page, c.ordinal, c.text, c.token_count, "
            "c.embedding::text FROM chunks c"
        ).fetchall()
        chunk_vectors = {row[0]: json.loads(row[6]) for row in all_chunks}
        chunk_rows = {row[0]: row for row in all_chunks}
        part_texts: list[tuple[uuid.UUID, str]] = []
        for row in all_chunks:
            for block in table_blocks(row[4]):
                part_texts.append((row[0], block))
        part_vectors: dict[uuid.UUID, list[list[float]]] = {}
        if part_texts:
            vectors = await embedder.embed([t for _, t in part_texts])
            for (chunk_id, _), vector in zip(part_texts, vectors, strict=True):
                part_vectors.setdefault(chunk_id, []).append(vector)
        print(f"  table blocks embedded: {len(part_texts)} parts of {len(part_vectors)} chunks")

        results = []
        async with sessions() as session:
            repo = RetrievalRepository(session)
            actor = await session.get(User, owner_id)
            retrieval = RetrievalService(session, embedder, settings)
            for q in questions:
                doc_ids = [uuid.UUID(documents[d]) for d in q["documents"]]
                embedding = question_embeddings[q["id"]]
                vector = await repo.search(owner_id, doc_ids, embedding, CANDIDATES)
                by_id = {c.chunk_id: c for c in vector}
                # Full-text ranking from the same chunks (PostgreSQL's ranking is not strict
                # BM25 — noted in the report). 'simple' config: the questions mix languages.
                # The question's Latin and numeric tokens, OR-ed: the AND semantics of
                # websearch_to_tsquery on the whole question returned nothing for 16 of
                # 18 questions in the first run, and PostgreSQL's 'simple' parser does not
                # segment Chinese. Leading hyphens are dropped ("-High" would mean NOT).
                tokens = [
                    t.lstrip("-")
                    for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9.%-]*", q["question"])
                    if len(t.lstrip("-")) >= 2
                ]
                fulltext_query = " OR ".join(dict.fromkeys(tokens)) or "zzzz"
                rows = (
                    await session.execute(
                        sql_text(
                            "SELECT c.id, c.document_id, d.filename, c.page, c.ordinal, c.text, "
                            "c.token_count, ts_rank_cd(to_tsvector('simple', c.text), "
                            "websearch_to_tsquery('simple', :q)) AS rank "
                            "FROM chunks c JOIN documents d ON d.id = c.document_id "
                            "WHERE d.owner_id = :owner AND d.id = ANY(:docs) "
                            "AND to_tsvector('simple', c.text) "
                            "@@ websearch_to_tsquery('simple', :q) "
                            "ORDER BY rank DESC, c.id LIMIT :n"
                        ),
                        {"q": fulltext_query, "owner": owner_id, "docs": doc_ids, "n": CANDIDATES},
                    )
                ).fetchall()
                fulltext_ids = []
                for row in rows:
                    fulltext_ids.append(row.id)
                    if row.id not in by_id:
                        by_id[row.id] = type(vector[0])(
                            chunk_id=row.id,
                            document_id=row.document_id,
                            filename=row.filename,
                            page=row.page,
                            ordinal=row.ordinal,
                            text=row.text,
                            token_count=row.token_count,
                            score=None,
                        )
                doc_key = {v: k for k, v in documents.items()}
                # Max over the chunk's vector and its block vectors, ranked over every chunk
                # of the question's documents.
                scored = []
                for chunk_id, row in chunk_rows.items():
                    if row[1] not in doc_ids:
                        continue
                    best = cosine(embedding, chunk_vectors[chunk_id])
                    for part in part_vectors.get(chunk_id, []):
                        best = max(best, cosine(embedding, part))
                    scored.append((best, chunk_id))
                scored.sort(key=lambda pair: (-pair[0], str(pair[1])))
                max_ids = [chunk_id for _, chunk_id in scored[:CANDIDATES]]
                for chunk_id in max_ids:
                    if chunk_id not in by_id:
                        row = chunk_rows[chunk_id]
                        by_id[chunk_id] = type(vector[0])(
                            chunk_id=row[0],
                            document_id=row[1],
                            filename="",
                            page=row[2],
                            ordinal=row[3],
                            text=row[4],
                            token_count=row[5],
                            score=None,
                        )
                max_scores = dict((cid, sc) for sc, cid in scored[:CANDIDATES])
                vector_ids = [c.chunk_id for c in vector]
                hybrid_ids = rrf(vector_ids, fulltext_ids)
                v_ranked = _payload(vector_ids, by_id, doc_key)
                h_ranked = _payload(hybrid_ids, by_id, doc_key)
                m_ranked = _payload(max_ids, by_id, doc_key)
                for c in m_ranked:
                    c["score"] = round(max_scores[uuid.UUID(c["chunk_id"])], 4)
                # The production path (D62): the Top-K, then the discussion that follows any
                # table among them. Measured per K, since the expansion depends on the Top-K.
                context_ranked = {}
                for k in KS:
                    with_context = await retrieval.with_table_context(actor, vector[:k])
                    for c in with_context:
                        by_id.setdefault(c.chunk_id, c)
                    context_ranked[k] = _payload([c.chunk_id for c in with_context], by_id, doc_key)
                results.append(
                    {
                        "id": q["id"],
                        "kind": q["kind"],
                        "keyword_type": q["keyword_type"],
                        "expect_refusal": q["expect_refusal"],
                        "documents": q["documents"],
                        "top1_similarity": vector[0].score if vector else None,
                        "fulltext_candidates": len(fulltext_ids),
                        "vector": _metrics(v_ranked, q["evidence"], documents),
                        "hybrid": _metrics(h_ranked, q["evidence"], documents),
                        "vector_max": _metrics(m_ranked, q["evidence"], documents),
                        "vector_max_top1": max_scores[max_ids[0]] if max_ids else None,
                        "vector_max_top8": [_without_text(c) for c in m_ranked[:8]],
                        "vector_context": {
                            str(k): _metrics(
                                context_ranked[k], q["evidence"], documents, whole=True
                            )[str(k)]
                            | {"added": len(context_ranked[k]) - k}
                            for k in KS
                        },
                        "vector_top8": [
                            {k: v for k, v in c.items() if k != "text"} for c in v_ranked[:8]
                        ],
                        "hybrid_top8": [
                            {k: v for k, v in c.items() if k != "text"} for c in h_ranked[:8]
                        ],
                    }
                )
        record = {
            "config": {
                "chunk_size": size,
                "chunk_overlap": overlap,
                "embed_model": base.embed_model,
                "candidates_per_ranking": CANDIDATES,
                "rrf_k": RRF_K,
                "fulltext_config": "simple; OR of the question's Latin/numeric tokens",
                "coverage_rule": (
                    "same document and page; evidence text contained, or longest common "
                    "block >= 50% of its characters"
                ),
            },
            "ingest_seconds": round(ingest_seconds, 1),
            "chunk_count": chunk_count,
            "questions": results,
        }
        (RUNS_DIR / f"chunk{size}.json").write_text(
            json.dumps(record, indent=1, ensure_ascii=False) + "\n"
        )
        print(
            f"\n[chunk {size}] chunks={chunk_count} ingest={ingest_seconds:.0f}s "
            f"questions={len(results)}"
        )
