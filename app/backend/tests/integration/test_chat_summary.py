"""Summary questions: answered from the stored summaries, not from retrieved chunks.

Covers the routing rule (architecture section 8, step 4), the sources of a
summary answer (AC-26: file name, section title, page range), one part per
document (D32) and the behaviour when a summary is not ready (AC-42).
"""

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
from app.ingestion.indexing import IndexJobRunner
from app.llm.gateway import OllamaGateway
from app.llm.tokenizer import Qwen3TokenCounter
from app.summarization.service import SummaryJobRunner
from tests.fakes import FakeEmbedder, StubSummariser
from tests.integration.test_chat import (
    DOCUMENTS,
    StubOllama,
    ask,
    counts,
    events,
    login,
    new_conversation,
    one,
    use_model,
)

pytestmark = pytest.mark.db

SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
NOTE = (
    b"# Notes on LightRAG\n\nGraphs help retrieval.\n\n## Indexing\n\nEntities become nodes. "
    b"Win rate 67.6%.\n\n## Retrieval\n\nTwo levels.\n"
)
ANSWER = ["LightRAG builds a graph [1]", " and wins 67.6% (p. 8) [2]."]


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def kim(client: TestClient) -> TestClient:
    return login(client, "kim")


async def add_document(
    client: TestClient,
    tokenizer: Qwen3TokenCounter,
    name: str,
    content: bytes,
    *,
    summarise: bool | None = True,
) -> str:
    """Upload and index a document; summarise it too (True), fail its summary (False) or
    leave the summary not started (None)."""
    body = client.post(DOCUMENTS, files={"file": (name, content)}).json()
    settings = get_settings()
    storage = FileStorage(settings.data_dir)
    index = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        tokenizer=tokenizer,
        embedder=FakeEmbedder(),
        settings=settings,
    )
    job_id = uuid.UUID(body["jobs"][0]["id"])
    if summarise is None:
        await index.run(job_id)
        return str(body["id"])
    summary = SummaryJobRunner(
        sessions=get_sessionmaker(),
        storage=storage,
        counter=tokenizer,
        gateway=OllamaGateway(
            settings=settings,
            sessions=get_sessionmaker(),
            counter=tokenizer,
            transport=httpx.MockTransport(StubSummariser(fail_on_call=None if summarise else 0)),
        ),
    )
    dispatcher = JobDispatcher(
        sessions=get_sessionmaker(), index_runner=index, summary_runner=summary
    )
    await dispatcher.run(job_id)
    return str(body["id"])


def message(db: psycopg.Connection, message_id: str) -> tuple:
    return one(
        db, "SELECT status, answered, content, sources FROM messages WHERE id = %s", message_id
    )


async def test_a_summary_question_is_answered_from_the_stored_summaries(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    document_id = await add_document(kim, tokenizer, "paper.pdf", SAMPLE_PDF.read_bytes())
    model = StubOllama(ANSWER)
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    received = events(ask(kim, conversation, "summary this document."))

    names = [name for name, _ in received]
    assert names[:3] == ["start", "route", "sources"]
    assert names[-2:] == ["usage", "done"]
    assert received[1][1] == {"type": "summary", "standalone_question": "summary this document."}
    sources = received[2][1]
    assert isinstance(sources, list) and len(sources) >= 3
    assert {s["kind"] for s in sources} == {"summary"}
    assert {s["filename"] for s in sources} == {"paper.pdf"}
    assert {s["document_id"] for s in sources} == {document_id}
    assert all(s["score"] is None for s in sources)
    # The whole-document summary comes first, then the sections in document order.
    assert sources[0]["section_title"] is None
    assert (sources[0]["page_start"], sources[0]["page_end"]) == (1, 16)
    assert [s["section_title"] for s in sources[1:4]] == [
        "Front matter",
        "INTRODUCTION",
        "RETRIEVAL-AUGMENTED GENERATION",
    ]
    assert [(s["page_start"], s["page_end"]) for s in sources[1:4]] == [(1, 1), (1, 2), (2, 3)]
    assert all(s["index"] == i for i, s in enumerate(sources, start=1))
    # The model saw the summaries, not the raw text, and the answer came back with its usage.
    [prompt] = model.prompts
    assert "whole document" in prompt and "section: EVALUATION" in prompt
    assert "Question: summary this document." in prompt
    assert "".join(d["text"] for n, d in received if n == "delta") == "".join(ANSWER)
    assert received[-1][1]["status"] == "completed"
    assert received[-1][1]["answered"] is True
    assert received[-1][1]["cited"] == [1, 2]

    start = received[0][1]
    assert isinstance(start, dict)
    status, answered, content, stored = message(db, start["assistant_message_id"])
    assert (status, answered, content) == ("completed", True, "".join(ANSWER))
    assert stored == sources
    assert one(db, "SELECT purpose, status FROM llm_calls WHERE purpose = 'answer'") == (
        "answer",
        "completed",
    )


async def test_a_summary_question_while_the_summary_is_not_ready_calls_no_model(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "notes.md", NOTE, summarise=None)
    model = StubOllama(ANSWER)
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)
    _, calls_before = counts(db)

    received = events(ask(kim, conversation, "Summarize this document"))

    # The explanation is streamed like an answer, so the client shows it; no usage event.
    assert [name for name, _ in received] == ["start", "route", "sources", "delta", "done"]
    assert received[1][1] == {"type": "summary", "standalone_question": "Summarize this document"}
    assert received[2][1] == []
    assert received[4][1]["status"] == "completed"
    assert received[4][1]["answered"] is False
    assert model.prompts == []
    assert counts(db)[1] == calls_before  # nothing was sent, so nothing is in the ledger
    start = received[0][1]
    assert isinstance(start, dict)
    status, answered, content, stored = message(db, start["assistant_message_id"])
    assert (status, answered, stored) == ("completed", False, [])
    assert '"notes.md"' in content and "not available" in content and "not started" in content
    assert received[3][1] == {"text": content}


async def test_a_failed_summary_is_reported_and_ordinary_questions_still_work(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-42: the document stays usable; a summary question says the summary failed."""
    document_id = await add_document(kim, tokenizer, "notes.md", NOTE, summarise=False)
    assert kim.get(f"{DOCUMENTS}/{document_id}").json()["summary_status"] == "failed"
    model = StubOllama(ANSWER)
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    summary = events(ask(kim, conversation, "請摘要這份文件"))
    ordinary = events(ask(kim, conversation, "What does LightRAG build?"))

    assert summary[-1][1]["answered"] is False
    start = summary[0][1]
    assert isinstance(start, dict)
    content = message(db, start["assistant_message_id"])[2]
    assert "「notes.md」" in content and "尚未就緒" in content and "失敗" in content
    # The ordinary question went through retrieval as before.
    assert ordinary[1][1]["type"] == "retrieval"
    assert {s["kind"] for s in ordinary[2][1]} == {"chunk"}
    assert ordinary[-1][1]["answered"] is True
    assert len(model.prompts) == 1


async def test_each_document_gets_its_own_part_and_missing_summaries_are_named(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """D32: one part per document, never mixed; a document without a summary is named."""
    notes = await add_document(kim, tokenizer, "notes.md", NOTE)
    plan = await add_document(kim, tokenizer, "plan.txt", b"Index first, then summarise.\n")
    await add_document(kim, tokenizer, "later.txt", b"Still being processed.\n", summarise=None)
    model = StubOllama(ANSWER)
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    received = events(ask(kim, conversation, "Give me a summary of my documents"))

    sources = received[2][1]
    assert isinstance(sources, list)
    assert {s["document_id"] for s in sources} == {notes, plan}
    assert [s["filename"] for s in sources if s["section_title"] is None] == [
        "notes.md",
        "plan.txt",
    ]
    [prompt] = model.prompts
    assert "sources come from 2 documents" in prompt
    assert "later.txt" not in prompt
    start = received[0][1]
    assert isinstance(start, dict)
    status, answered, content, _ = message(db, start["assistant_message_id"])
    assert (status, answered) == ("completed", True)
    assert content.startswith("".join(ANSWER))
    assert '"later.txt"' in content and "not available" in content
    # The note is part of the answer the client received, too.
    assert "later.txt" in "".join(d["text"] for n, d in received if n == "delta")
