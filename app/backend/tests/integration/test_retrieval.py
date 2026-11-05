"""Retrieval: the most similar chunks, only from the asker's own ready documents.

Covers AC-06 (a selected document excludes the others), AC-34 (another user's
documents are never searched or returned) and AC-48 (no selection means all of
the asker's ready documents, sharing one Top-K). Uses a fake embedder: a
question that equals a chunk's text has similarity 1 with it.
"""

import uuid
from collections.abc import Callable

import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.core.errors import ApiError
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner
from app.llm.tokenizer import Qwen3TokenCounter
from app.models import User
from app.retrieval.service import RetrievalService, RetrievedChunk, SearchScope
from tests.fakes import FakeEmbedder
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
GRAPH = "LightRAG builds a graph of entities and relations."
BREAD = "Sourdough bread needs a long, slow fermentation."


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def kim(client: TestClient) -> TestClient:
    register_and_login(client, "kim")
    return client


@pytest.fixture()
def lee(make_client: Callable[..., TestClient]) -> TestClient:
    client = make_client()
    register_and_login(client, "lee")
    return client


async def add_document(
    client: TestClient, tokenizer: Qwen3TokenCounter, name: str, text: str, *, index: bool = True
) -> str:
    """Upload a one-chunk text document and, unless told otherwise, index it."""
    body = client.post(DOCUMENTS, files={"file": (name, text.encode())}).json()
    if index:
        settings = get_settings()
        runner = IndexJobRunner(
            sessions=get_sessionmaker(),
            storage=FileStorage(settings.data_dir),
            tokenizer=tokenizer,
            embedder=FakeEmbedder(),
            settings=settings,
        )
        await runner.run(uuid.UUID(body["jobs"][0]["id"]))
    return str(body["id"])


async def search(
    username: str, question: str, document_ids: list[str] | None = None, *, top_k: int | None = None
) -> tuple[SearchScope, list[RetrievedChunk]]:
    settings = get_settings()
    if top_k is not None:
        settings = settings.model_copy(update={"top_k": top_k})
    async with get_sessionmaker()() as session:
        actor = await session.scalar(select(User).where(User.username == username))
        assert actor is not None
        service = RetrievalService(session, FakeEmbedder(), settings)
        ids = None if document_ids is None else [uuid.UUID(i) for i in document_ids]
        scope = await service.resolve_scope(actor, ids)
        return scope, await service.search(actor, scope, question)


async def test_the_most_similar_chunk_comes_first_with_what_a_citation_needs(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    graph = await add_document(kim, tokenizer, "graph.txt", GRAPH)
    await add_document(kim, tokenizer, "bread.md", BREAD)

    _, chunks = await search("kim", GRAPH)

    top = chunks[0]
    assert (str(top.document_id), top.filename, top.page, top.text) == (
        graph,
        "graph.txt",
        1,
        GRAPH,
    )
    assert top.score == pytest.approx(1.0, abs=1e-4)
    assert [c.score for c in chunks] == sorted((c.score for c in chunks), reverse=True)
    assert {c.filename for c in chunks} == {"graph.txt", "bread.md"}


async def test_selecting_one_document_excludes_the_others(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-06."""
    await add_document(kim, tokenizer, "graph.txt", GRAPH)
    bread = await add_document(kim, tokenizer, "bread.md", BREAD)

    # The question matches the document that was left out.
    scope, chunks = await search("kim", GRAPH, [bread])

    assert (scope.mode, [str(i) for i in scope.document_ids]) == ("selected", [bread])
    assert [c.filename for c in chunks] == ["bread.md"]


async def test_without_a_selection_all_ready_documents_share_one_top_k(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-48."""
    ready = [
        await add_document(kim, tokenizer, f"note-{i}.txt", f"Note number {i} about LightRAG.")
        for i in range(7)
    ]
    waiting = await add_document(kim, tokenizer, "waiting.txt", GRAPH, index=False)

    scope, chunks = await search("kim", GRAPH)

    assert scope.mode == "all"
    assert sorted(str(i) for i in scope.document_ids) == sorted(ready)
    # Seven documents, one Top-K of five in total: no quota per document.
    assert len(chunks) == get_settings().top_k == 5
    assert len({c.document_id for c in chunks}) == 5
    # A document that is not ready is not searched, even though it matches exactly.
    assert waiting not in {str(c.document_id) for c in chunks}


async def test_top_k_follows_the_setting(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    for i in range(4):
        await add_document(kim, tokenizer, f"note-{i}.txt", f"Note number {i} about LightRAG.")

    _, chunks = await search("kim", GRAPH, top_k=3)

    assert len(chunks) == 3


async def test_another_users_documents_are_never_returned(
    kim: TestClient, lee: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-34: even when they match the question better than anything of one's own."""
    mine = await add_document(kim, tokenizer, "bread.md", BREAD)
    for i in range(8):
        # Lee's documents contain the question itself; several of them.
        await add_document(lee, tokenizer, f"graph-{i}.txt", f"{GRAPH} Copy {i}.")
    theirs = await add_document(lee, tokenizer, "graph.txt", GRAPH)

    scope, chunks = await search("kim", GRAPH)

    assert [str(i) for i in scope.document_ids] == [mine]
    assert [(c.filename, str(c.document_id)) for c in chunks] == [("bread.md", mine)]
    # Naming someone else's document is the same as naming one that does not exist.
    with pytest.raises(ApiError) as stranger:
        await search("kim", GRAPH, [theirs])
    with pytest.raises(ApiError) as missing:
        await search("kim", GRAPH, [str(uuid.uuid4())])
    assert (stranger.value.status_code, stranger.value.code) == (404, "DOCUMENT_NOT_FOUND")
    assert (missing.value.status_code, missing.value.detail) == (404, stranger.value.detail)
    # One foreign id among valid ones fails the whole request.
    with pytest.raises(ApiError):
        await search("kim", GRAPH, [mine, theirs])


async def test_a_selected_document_that_is_not_ready_is_named_in_the_refusal(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    ready = await add_document(kim, tokenizer, "bread.md", BREAD)
    waiting = await add_document(kim, tokenizer, "waiting.txt", GRAPH, index=False)

    with pytest.raises(ApiError) as refused:
        await search("kim", GRAPH, [ready, waiting])

    assert (refused.value.status_code, refused.value.code) == (409, "DOCUMENT_NOT_READY")
    assert "waiting.txt" in refused.value.detail
    assert "bread.md" not in refused.value.detail


async def test_asking_without_any_ready_document_is_refused(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "waiting.txt", GRAPH, index=False)

    with pytest.raises(ApiError) as refused:
        await search("kim", GRAPH)

    assert (refused.value.status_code, refused.value.code) == (409, "NO_READY_DOCUMENT")


async def test_repeating_a_document_in_the_selection_changes_nothing(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    graph = await add_document(kim, tokenizer, "graph.txt", GRAPH)

    scope, chunks = await search("kim", GRAPH, [graph, graph])

    assert [str(i) for i in scope.document_ids] == [graph]
    assert len(chunks) == 1
