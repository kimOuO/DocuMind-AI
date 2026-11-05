"""Asking a question: POST /conversations/{id}/messages.

Ollama is replaced by a stub transport and the embedder by a fake, so each
outcome can be produced on demand. Covers AC-05, AC-06, AC-33, AC-34, AC-41,
AC-48, AC-49, AC-50 and AC-57.
"""

import json
import uuid
from collections.abc import AsyncIterator, Callable
from pathlib import Path

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.chat.repository import ChatRepository
from app.chat.router import get_embedder, get_llm_gateway
from app.chat.service import ChatService
from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner
from app.ingestion.parsing import parse_document
from app.llm.embedding import EmbeddingError
from app.llm.gateway import OllamaGateway
from app.llm.tokenizer import Qwen3TokenCounter
from app.models import User
from tests.fakes import FakeEmbedder
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
CONVERSATIONS = "/api/v1/conversations"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
GRAPH = "LightRAG builds a graph of entities and relations."
BREAD = "Sourdough bread needs a long, slow fermentation."
QUESTION = "What does LightRAG build?"


class StubOllama:
    """Plays the model: streams the given pieces, then reports how it ended."""

    def __init__(
        self,
        pieces: list[str],
        *,
        done_reason: str = "stop",
        completion_tokens: int | None = None,
        status_code: int = 200,
        error: str = "",
    ) -> None:
        self.pieces = pieces
        self.done_reason = done_reason
        self.completion_tokens = len(pieces) if completion_tokens is None else completion_tokens
        self.status_code = status_code
        self.error = error
        self.prompts: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.prompts.append(body["prompt"])
        assert (body["truncate"], body["shift"], body["stream"]) == (False, False, True)
        assert body["options"] == {"num_ctx": 10_000, "num_predict": 2_500}
        if self.status_code != 200:
            return httpx.Response(self.status_code, json={"error": self.error})

        async def lines() -> AsyncIterator[bytes]:
            for piece in self.pieces:
                yield (json.dumps({"response": piece, "done": False}) + "\n").encode()
            final = {
                "response": "",
                "done": True,
                "done_reason": self.done_reason,
                "prompt_eval_count": 321,
                "eval_count": self.completion_tokens,
            }
            yield (json.dumps(final) + "\n").encode()

        return httpx.Response(200, content=lines())


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


def use_model(client: TestClient, tokenizer: Qwen3TokenCounter, model: StubOllama) -> None:
    client.app.dependency_overrides[get_llm_gateway] = lambda: OllamaGateway(  # type: ignore[attr-defined]
        settings=get_settings(),
        sessions=get_sessionmaker(),
        counter=tokenizer,
        transport=httpx.MockTransport(model),
    )


def login(client: TestClient, username: str) -> TestClient:
    client.app.dependency_overrides[get_embedder] = lambda: FakeEmbedder()  # type: ignore[attr-defined]
    register_and_login(client, username)
    return client


@pytest.fixture()
def kim(client: TestClient) -> TestClient:
    return login(client, "kim")


@pytest.fixture()
def lee(make_client: Callable[..., TestClient]) -> TestClient:
    return login(make_client(), "lee")


async def add_document(
    client: TestClient,
    tokenizer: Qwen3TokenCounter,
    name: str,
    content: bytes,
    *,
    index: bool = True,
) -> str:
    body = client.post(DOCUMENTS, files={"file": (name, content)}).json()
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


def new_conversation(client: TestClient, title: str | None = None) -> str:
    return str(client.post(CONVERSATIONS, json={"title": title}).json()["id"])


def ask(client: TestClient, conversation: str, question: str = QUESTION, **body: object):  # type: ignore[no-untyped-def]
    return client.post(
        f"{CONVERSATIONS}/{conversation}/messages", json={"question": question, **body}
    )


def events(response) -> list[tuple[str, object]]:  # type: ignore[no-untyped-def]
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    parsed = []
    for block in response.text.strip().split("\n\n"):
        name, data = block.split("\n", 1)
        parsed.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    return parsed


def one(db: psycopg.Connection, query: str, *params: object) -> tuple:
    row = db.execute(query, params).fetchone()
    assert row is not None
    return row


def counts(db: psycopg.Connection) -> tuple[int, int]:
    return one(db, "SELECT count(*) FROM messages")[0], one(db, "SELECT count(*) FROM llm_calls")[0]


async def test_an_answer_is_streamed_with_its_sources_and_stored(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    graph = await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = StubOllama(["LightRAG builds", " a graph", " [1]."])
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    stream = events(ask(kim, conversation))

    names = [name for name, _ in stream]
    assert names == ["start", "route", "sources", "delta", "delta", "delta", "usage", "done"]
    by_name = dict(stream)
    assert by_name["start"]["scope"] == {"mode": "all", "document_ids": [graph]}
    assert by_name["route"] == {"type": "retrieval", "standalone_question": QUESTION}
    [source] = by_name["sources"]
    assert (source["index"], source["kind"], source["filename"]) == (1, "chunk", "graph.txt")
    assert (source["document_id"], source["page_start"], source["page_end"]) == (graph, 1, 1)
    assert source["snippet"] == GRAPH
    assert [data["text"] for name, data in stream if name == "delta"] == [
        "LightRAG builds",
        " a graph",
        " [1].",
    ]
    assert by_name["usage"] == {"prompt_tokens": 321, "completion_tokens": 3, "limit": 10_000}
    assert by_name["done"] == {
        "status": "completed",
        "answered": True,
        "cited": [1],
        "unverified_numbers": [],
        "finish_reason": "stop",
    }
    # What the model was given: the rules, the numbered source, the question.
    [prompt] = model.prompts
    assert f"[1] graph.txt, page 1\n{GRAPH}" in prompt
    assert prompt.rstrip().endswith(f"Question: {QUESTION}\nAnswer:")

    # Both messages are stored, in order, and the conversation is titled after the question.
    stored = kim.get(f"{CONVERSATIONS}/{conversation}").json()
    assert stored["title"] == QUESTION
    question, answer = stored["messages"]
    assert (question["role"], question["content"], question["status"]) == (
        "user",
        QUESTION,
        "completed",
    )
    assert (answer["id"], question["id"]) == (
        by_name["start"]["assistant_message_id"],
        by_name["start"]["user_message_id"],
    )
    assert (answer["role"], answer["content"]) == ("assistant", "LightRAG builds a graph [1].")
    assert (answer["status"], answer["answered"]) == ("completed", True)
    assert answer["sources"] == by_name["sources"]
    # The call is in the ledger, linked to the conversation and the answer.
    call = one(
        db, "SELECT status, purpose, conversation_id, message_id, prompt_tokens FROM llm_calls"
    )
    assert call == ("completed", "answer", uuid.UUID(conversation), uuid.UUID(answer["id"]), 321)


async def test_every_source_snippet_is_on_the_cited_page_of_the_paper(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-05: file name, page and a snippet that really is on that page."""
    paper = await add_document(kim, tokenizer, "2410.05779v3.pdf", SAMPLE_PDF.read_bytes())
    use_model(kim, tokenizer, StubOllama(["The ablated versions perform worse [1][2]."]))

    stream = dict(
        events(ask(kim, new_conversation(kim), "Performance of ablated versions of LightRAG"))
    )

    sources = stream["sources"]
    assert len(sources) == get_settings().top_k
    pages = {page.number: page.text for page in parse_document(SAMPLE_PDF, "pdf")}
    for source in sources:
        assert source["filename"] == "2410.05779v3.pdf"
        assert source["document_id"] == paper
        assert source["page_start"] == source["page_end"]
        assert source["snippet"] and source["snippet"] in pages[source["page_start"]]
    assert stream["done"]["cited"] == [1, 2]


async def test_only_the_selected_document_is_used(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-06 and AC-48: the scope is what was selected, or everything that is ready."""
    graph = await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    bread = await add_document(kim, tokenizer, "bread.md", BREAD.encode())
    model = StubOllama(["Not in the documents."])
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    selected = dict(events(ask(kim, conversation, document_ids=[bread])))
    everything = dict(events(ask(kim, conversation)))
    empty_list = dict(events(ask(kim, conversation, document_ids=[])))

    assert selected["start"]["scope"] == {"mode": "selected", "document_ids": [bread]}
    assert [s["filename"] for s in selected["sources"]] == ["bread.md"]
    assert GRAPH not in model.prompts[0]
    assert everything["start"]["scope"]["mode"] == empty_list["start"]["scope"]["mode"] == "all"
    assert sorted(everything["start"]["scope"]["document_ids"]) == sorted([graph, bread])
    assert {s["filename"] for s in everything["sources"]} == {"graph.txt", "bread.md"}


async def test_an_answer_without_a_citation_counts_as_not_answered(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "bread.md", BREAD.encode())
    use_model(kim, tokenizer, StubOllama(["The documents do not contain this. See [7]."]))
    conversation = new_conversation(kim, "kept title")

    done = dict(events(ask(kim, conversation)))["done"]

    # [7] is not one of the sources, so nothing was cited.
    assert (done["status"], done["answered"], done["cited"]) == ("completed", False, [])
    stored = kim.get(f"{CONVERSATIONS}/{conversation}").json()
    assert stored["title"] == "kept title"
    assert stored["messages"][1]["answered"] is False


async def test_a_question_that_is_too_long_is_refused_and_leaves_nothing(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-49: refused, not truncated; the limit follows the setting."""
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = StubOllama(["ok [1]"])
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)
    long_question = "What does LightRAG build, and why? " * 30
    assert tokenizer.count(long_question.strip()) > 200

    refused = ask(kim, conversation, long_question)

    assert refused.status_code == 422
    assert refused.json()["code"] == "QUESTION_TOO_LONG"
    assert counts(db) == (0, 0)
    assert model.prompts == []
    assert kim.get(f"{CONVERSATIONS}/{conversation}").json()["title"] == ""

    # With a larger budget the same question is accepted, whole.
    from app.core.env_loader import get_settings as settings_dependency

    larger = get_settings().model_copy(update={"question_token_budget": 400})
    kim.app.dependency_overrides[settings_dependency] = lambda: larger  # type: ignore[attr-defined]
    accepted = dict(events(ask(kim, conversation, long_question)))
    assert accepted["done"]["status"] == "completed"
    assert f"Question: {long_question.strip()}\nAnswer:" in model.prompts[0]


async def test_a_blank_question_is_refused(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    conversation = new_conversation(kim)

    assert ask(kim, conversation, "   ").status_code == 422
    assert ask(kim, conversation, "").status_code == 422
    assert counts(db) == (0, 0)


async def test_asking_without_a_ready_document_is_refused_and_leaves_nothing(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    waiting = await add_document(kim, tokenizer, "waiting.txt", GRAPH.encode(), index=False)
    conversation = new_conversation(kim)

    nothing_ready = ask(kim, conversation)
    not_ready = ask(kim, conversation, document_ids=[waiting])

    assert (nothing_ready.status_code, nothing_ready.json()["code"]) == (409, "NO_READY_DOCUMENT")
    assert (not_ready.status_code, not_ready.json()["code"]) == (409, "DOCUMENT_NOT_READY")
    assert "waiting.txt" in not_ready.json()["detail"]
    assert counts(db) == (0, 0)


async def test_another_users_conversation_and_documents_are_out_of_reach(
    kim: TestClient, lee: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-33 (asking) and AC-34."""
    await add_document(kim, tokenizer, "bread.md", BREAD.encode())
    lees_document = await add_document(lee, tokenizer, "graph.txt", GRAPH.encode())
    lees_conversation = new_conversation(lee)
    model = StubOllama(["Bread [1]."])
    use_model(kim, tokenizer, model)
    mine = new_conversation(kim)

    in_their_conversation = ask(kim, lees_conversation)
    in_no_conversation = ask(kim, str(uuid.uuid4()))
    with_their_document = ask(kim, mine, document_ids=[lees_document])
    with_no_document = ask(kim, mine, document_ids=[str(uuid.uuid4())])

    assert in_their_conversation.status_code == in_no_conversation.status_code == 404
    assert in_their_conversation.json() == in_no_conversation.json()
    assert with_their_document.status_code == with_no_document.status_code == 404
    assert with_their_document.json() == with_no_document.json()
    assert counts(db) == (0, 0)
    assert lee.get(f"{CONVERSATIONS}/{lees_conversation}").json()["messages"] == []

    # Asking over everything of one's own never brings in the other user's text,
    # although it matches the question exactly.
    answer = dict(events(ask(kim, mine, GRAPH)))
    assert [s["filename"] for s in answer["sources"]] == ["bread.md"]
    assert GRAPH not in model.prompts[0].split("Question:")[0]
    # And the other user's ledger does not show this call.
    assert lee.get("/api/v1/llm-calls").json()["calls"] == []
    assert len(kim.get("/api/v1/llm-calls").json()["calls"]) == 1


@pytest.mark.parametrize(
    ("completion_tokens", "finish_reason"), [(2_500, "output_limit"), (40, "context_exhausted")]
)
async def test_an_answer_that_was_cut_short_is_not_marked_completed(
    kim: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    completion_tokens: int,
    finish_reason: str,
) -> None:
    """AC-57: the stream ended normally, but the answer is not whole."""
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = StubOllama(
        ["LightRAG builds", " a graph [1] and"],
        done_reason="length",
        completion_tokens=completion_tokens,
    )
    use_model(kim, tokenizer, model)
    conversation = new_conversation(kim)

    done = dict(events(ask(kim, conversation)))["done"]

    assert (done["status"], done["finish_reason"], done["answered"]) == (
        "interrupted",
        finish_reason,
        None,
    )
    answer = kim.get(f"{CONVERSATIONS}/{conversation}").json()["messages"][1]
    # What was produced is kept, marked as unfinished.
    assert (answer["status"], answer["content"]) == (
        "interrupted",
        "LightRAG builds a graph [1] and",
    )
    # The call itself completed and was measured; the reason is on record.
    call = one(db, "SELECT status, finish_reason, prompt_tokens, completion_tokens FROM llm_calls")
    assert call == ("completed", finish_reason, 321, completion_tokens)


@pytest.mark.parametrize(
    ("status_code", "error", "code"),
    [
        (400, "the input length exceeds the context length", "INPUT_EXCEEDS_CONTEXT"),
        (500, "model failed to load", "LLM_UNAVAILABLE"),
    ],
)
async def test_a_call_that_ollama_refuses_or_fails_makes_the_answer_failed(
    kim: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    status_code: int,
    error: str,
    code: str,
) -> None:
    """AC-57: a refused call is failed in the ledger, without measured values."""
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    use_model(kim, tokenizer, StubOllama([], status_code=status_code, error=error))
    conversation = new_conversation(kim)

    stream = events(ask(kim, conversation))

    assert [name for name, _ in stream] == ["start", "route", "sources", "error"]
    assert stream[-1][1]["code"] == code
    answer = kim.get(f"{CONVERSATIONS}/{conversation}").json()["messages"][1]
    assert (answer["status"], answer["content"], answer["answered"]) == ("failed", "", None)
    call = one(
        db, "SELECT status, prompt_tokens, completion_tokens, finish_reason, error FROM llm_calls"
    )
    assert call[:4] == ("failed", None, None, None)
    assert call[4].startswith(code)


async def test_a_failing_embedding_service_makes_the_answer_failed_without_an_llm_call(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    use_model(kim, tokenizer, StubOllama(["unused"]))

    class BrokenEmbedder:
        async def embed(self, texts: list[str]) -> list[list[float]]:
            raise EmbeddingError("The embedding service could not be reached: refused")

    kim.app.dependency_overrides[get_embedder] = lambda: BrokenEmbedder()  # type: ignore[attr-defined]
    conversation = new_conversation(kim)

    stream = events(ask(kim, conversation))

    assert [name for name, _ in stream] == ["start", "route", "error"]
    assert stream[-1][1]["code"] == "EMBEDDING_UNAVAILABLE"
    assert kim.get(f"{CONVERSATIONS}/{conversation}").json()["messages"][1]["status"] == "failed"
    assert one(db, "SELECT count(*) FROM llm_calls")[0] == 0


async def test_a_client_that_disconnects_leaves_an_interrupted_answer(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-41 and AC-57: interrupted, not completed, and the reason is the client."""
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    conversation = new_conversation(kim)
    settings = get_settings()
    gateway = OllamaGateway(
        settings=settings,
        sessions=get_sessionmaker(),
        counter=tokenizer,
        transport=httpx.MockTransport(StubOllama(["LightRAG builds", " a graph", " [1]."])),
    )
    async with get_sessionmaker()() as session:
        actor = await session.scalar(select(User).where(User.username == "kim"))
        assert actor is not None
        service = ChatService(
            session,
            sessions=get_sessionmaker(),
            settings=settings,
            counter=tokenizer,
            embedder=FakeEmbedder(),
            gateway=gateway,
        )
        prepared = await service.prepare(actor, uuid.UUID(conversation), QUESTION, None)

    stream = service.answer(prepared)
    seen = []
    async for event in stream:
        seen.append(event.name)
        if event.name == "delta":
            break
    await stream.aclose()  # the browser closed the connection after the first piece

    assert seen == ["start", "route", "sources", "delta"]
    answer = kim.get(f"{CONVERSATIONS}/{conversation}").json()["messages"][1]
    assert (answer["status"], answer["content"], answer["answered"]) == (
        "interrupted",
        "LightRAG builds",
        None,
    )
    call = one(
        db,
        "SELECT status, finish_reason, prompt_tokens, received_output_tokens_estimated "
        "FROM llm_calls",
    )
    assert call == ("interrupted", "client_disconnect", None, tokenizer.count("LightRAG builds"))


async def test_answers_left_unfinished_by_a_shutdown_are_interrupted_at_startup(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """AC-50 (messages)."""
    conversation = new_conversation(kim)
    for status in ("pending", "streaming", "completed", "failed"):
        db.execute(
            "INSERT INTO messages (id, conversation_id, role, content, status, created_at) "
            "VALUES (gen_random_uuid(), %s, 'assistant', %s, %s, clock_timestamp())",
            (conversation, f"was {status}", status),
        )

    async with get_sessionmaker()() as session, session.begin():
        assert await ChatRepository(session).interrupt_unfinished() == 2

    messages = kim.get(f"{CONVERSATIONS}/{conversation}").json()["messages"]
    assert [(m["content"], m["status"]) for m in messages] == [
        ("was pending", "interrupted"),
        ("was streaming", "interrupted"),
        ("was completed", "completed"),
        ("was failed", "failed"),
    ]
