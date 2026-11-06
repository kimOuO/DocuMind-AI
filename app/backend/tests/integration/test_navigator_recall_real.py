"""Navigator-only experiment (D76 follow-up): how often the first call of the navigate mode
names the table a question needs. Only the Navigator call is made — no answer — so one run
costs a few seconds. Real Ollama and PostgreSQL; not run in CI.

    NAV_QUESTIONS=Q2,G2 NAV_RUNS=10 NAV_LABEL=N1 \\
      pytest tests/integration/test_navigator_recall_real.py -m "llm and db" -s

Variants: NAV_TEMPERATURE fixes the sampling of the Navigator call ("-" = the model's
default); NAV_PROMPT=b3 drops the tables rule that is now part of the prompt.
Writes evaluation/navigator-abc/runs/<label>-navigator.json with every plan.
"""

from __future__ import annotations

import json
import os
import re
import uuid

import pytest
from fastapi.testclient import TestClient

import app.chat.navigation as navigation
from app.chat.navigation import build_navigation_prompt, describe_retrieved, parse_plan
from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.llm.embedding import OllamaEmbedder
from app.llm.gateway import OllamaGateway
from app.llm.ledger import CallContext
from app.llm.tokenizer import get_token_counter
from app.retrieval.service import RetrievalService, SearchScope
from app.summarization.service import SummaryJobRunner, SummaryOutcome
from tests.integration.conftest import register_and_login
from tests.integration.test_navigator_abc_real import GRAPHRAG, LIGHTRAG, QUESTIONS, RUNS_DIR

pytestmark = [pytest.mark.llm, pytest.mark.db]

# The table each question's key facts need (evaluation/ground-truth/evidence-locations.json).
REQUIRED_TABLE = {"Q2": "Table 1", "Q3": "Table 2", "G1": "Table 2", "G2": "Table 6"}


class _Actor:
    def __init__(self, user_id: uuid.UUID) -> None:
        self.id = user_id


async def test_navigator_recall(client: TestClient, db) -> None:  # type: ignore[no-untyped-def]
    questions = os.environ.get("NAV_QUESTIONS", "Q2,G2").split(",")
    runs = int(os.environ.get("NAV_RUNS", "10"))
    # NAV_VARIANTS: comma-separated "<label>:<temperature or ->:<prompt or ->", e.g.
    # "N2:0:-,N3:-:tables,N4:0:tables". Default: one variant from NAV_LABEL, NAV_TEMPERATURE,
    # NAV_PROMPT.
    variants_env = os.environ.get("NAV_VARIANTS")
    if variants_env:
        variants = [tuple(v.split(":")) for v in variants_env.split(",")]
    else:
        variants = [
            (
                os.environ.get("NAV_LABEL", "N"),
                os.environ.get("NAV_TEMPERATURE") or "-",
                os.environ.get("NAV_PROMPT") or "-",
            )
        ]
    original_instructions = navigation.NAVIGATION_INSTRUCTIONS
    register_and_login(client, "kim")
    owner_id = uuid.UUID(db.execute("SELECT id FROM users").fetchone()[0].__str__())
    settings = get_settings()
    counter = get_token_counter()
    storage = FileStorage(settings.data_dir)
    sessions = get_sessionmaker()
    embedder = OllamaEmbedder(settings)
    gateway = OllamaGateway(settings=settings, sessions=sessions, counter=counter)
    index = IndexJobRunner(
        sessions=sessions, storage=storage, tokenizer=counter, embedder=embedder, settings=settings
    )
    summary = SummaryJobRunner(sessions=sessions, storage=storage, counter=counter, gateway=gateway)
    documents: dict[str, uuid.UUID] = {}
    needed = {QUESTIONS[q][1] for q in questions}
    for key, path in (("lightrag", LIGHTRAG), ("graphrag", GRAPHRAG)):
        if key not in needed:
            continue
        uploaded = client.post(
            "/api/v1/documents", files={"file": (path.name, path.read_bytes())}
        ).json()
        job = uuid.UUID(uploaded["jobs"][0]["id"])
        assert await index.run(job) is JobOutcome.COMPLETED
        documents[key] = uuid.UUID(uploaded["id"])
        assert await summary.run(index.queued_summary_jobs[job]) is SummaryOutcome.COMPLETED

    for label, temperature_text, prompt_variant in variants:
        temperature = None if temperature_text == "-" else float(temperature_text)
        navigation.NAVIGATION_INSTRUCTIONS = original_instructions
        if prompt_variant == "b3":  # the prompt before the tables rule
            navigation.NAVIGATION_INSTRUCTIONS = original_instructions.replace("{tables_rule}", "")
        await _run_variant(
            label,
            temperature,
            prompt_variant,
            questions,
            runs,
            documents,
            owner_id,
            sessions,
            embedder,
            settings,
            counter,
            gateway,
        )
    navigation.NAVIGATION_INSTRUCTIONS = original_instructions


async def _run_variant(  # type: ignore[no-untyped-def]
    label,
    temperature,
    prompt_variant,
    questions,
    runs,
    documents,
    owner_id,
    sessions,
    embedder,
    settings,
    counter,
    gateway,
) -> None:
    from app.chat.service import ChatService  # the map builder lives on the service

    records = []
    for q in questions:
        question, document = QUESTIONS[q]
        scope = SearchScope(mode="selected", document_ids=[documents[document]])
        actor = _Actor(owner_id)
        async with sessions() as session:
            retrieval = RetrievalService(session, embedder, settings)
            embedding = await retrieval.embed(question)
            chunks = await retrieval.search(actor, scope, question, embedding)  # type: ignore[arg-type]
            chunks = await retrieval.with_table_context(actor, chunks)  # type: ignore[arg-type]
        service = ChatService.__new__(ChatService)
        service._sessions = sessions  # type: ignore[attr-defined]

        class _Prepared:
            pass

        prepared = _Prepared()
        prepared.actor = actor  # type: ignore[attr-defined]
        prepared.scope = scope  # type: ignore[attr-defined]
        entries, _ = await service._document_map(prepared)  # type: ignore[arg-type]
        prompt, max_output = build_navigation_prompt(
            question,
            entries,
            describe_retrieved(chunks, entries),
            counter,
            settings.llm_context_limit,
        )
        table = REQUIRED_TABLE.get(q)
        for run in range(1, runs + 1):
            result = await gateway.generate(
                prompt,
                purpose="navigate",
                max_output_tokens=max_output,
                context=CallContext(owner_id=owner_id),
                temperature=temperature,
            )
            items = parse_plan(result.text, entries)
            listed = bool(table and re.search(re.escape(table) + r"\b", result.text, re.I))
            records.append(
                {
                    "label": label,
                    "temperature": temperature,
                    "prompt_variant": prompt_variant,
                    "question": q,
                    "run": run,
                    "required_table": table,
                    "listed": listed,
                    "targets": len(items),
                    "located": sum(1 for i in items if i.located),
                    "tables_named": sorted(
                        {m.group(0) for m in re.finditer(r"Table \d+", result.text)}
                    ),
                    "prompt_tokens": result.prompt_tokens,
                    "completion_tokens": result.completion_tokens,
                    "plan": result.text,
                }
            )
            print(f"{label}-{q}-{run}: listed={listed} tables={records[-1]['tables_named']}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{label}-navigator.json").write_text(
        json.dumps(records, indent=1, ensure_ascii=False) + "\n"
    )
    for q in questions:
        hits = sum(1 for r in records if r["question"] == q and r["listed"])
        print(f"{q}: required {REQUIRED_TABLE.get(q)} listed in {hits}/{runs}")
