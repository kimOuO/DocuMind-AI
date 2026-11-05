"""The LLM gateway and its ledger, against the real database.

Ollama is replaced by a stub HTTP transport, so every outcome can be produced
on demand: success, refusal, failure, a stream that breaks, a client that
leaves. Covers AC-07 (nothing is sent or recorded when over budget), AC-08
(every call that was sent is in the ledger, measured values only when Ollama
reported them) and the ledger part of AC-57 (why a call ended).
"""

import json
import uuid
from collections.abc import AsyncIterator

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.llm.chat_template import render_prompt
from app.llm.gateway import (
    CallContext,
    ContextBudgetExceeded,
    LLMCallFailed,
    OllamaGateway,
)
from app.llm.ollama_api import FinishReason
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

PROMPT = "Answer briefly: what does LightRAG combine?"
COLUMNS = (
    "status, purpose, model, estimated_prompt_tokens, max_output_tokens, prompt_tokens, "
    "completion_tokens, received_output_tokens_estimated, finish_reason, error, duration_ms"
)


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def owner(client: TestClient) -> uuid.UUID:
    return uuid.UUID(register_and_login(client, "kim")["id"])


def gateway(counter: Qwen3TokenCounter, handler) -> OllamaGateway:  # type: ignore[no-untyped-def]
    return OllamaGateway(
        settings=get_settings(),
        sessions=get_sessionmaker(),
        counter=counter,
        transport=httpx.MockTransport(handler),
    )


def ledger(db: psycopg.Connection) -> list[dict]:
    names = [name.strip() for name in COLUMNS.split(",")]
    rows = db.execute(f"SELECT {COLUMNS} FROM llm_calls ORDER BY created_at").fetchall()
    return [dict(zip(names, row, strict=True)) for row in rows]


def estimate(counter: Qwen3TokenCounter, prompt: str = PROMPT) -> int:
    settings = get_settings()
    return (
        counter.count(render_prompt(prompt, thinking=settings.llm_thinking))
        + settings.token_safety_buffer
    )


def answer(
    text: str, *, prompt_tokens: int, completion_tokens: int, done_reason: str = "stop"
) -> dict:
    return {
        "response": text,
        "done": True,
        "done_reason": done_reason,
        "prompt_eval_count": prompt_tokens,
        "eval_count": completion_tokens,
    }


def stream_body(parts: list[str], final: dict | None, *, break_after: int | None = None):  # type: ignore[no-untyped-def]
    async def lines() -> AsyncIterator[bytes]:
        for index, part in enumerate(parts):
            if break_after is not None and index == break_after:
                raise httpx.ReadError("connection lost")
            yield (json.dumps({"response": part, "done": False}) + "\n").encode()
        if final is not None:
            yield (json.dumps(final) + "\n").encode()

    return lines()


async def test_a_completed_call_is_recorded_with_what_ollama_measured(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append({"path": request.url.path, **json.loads(request.content)})
        return httpx.Response(
            200, json=answer("Graphs and retrieval.", prompt_tokens=31, completion_tokens=6)
        )

    result = await gateway(counter, handler).generate(
        PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
    )

    assert (result.text, result.prompt_tokens, result.completion_tokens) == (
        "Graphs and retrieval.",
        31,
        6,
    )
    assert result.finish_reason is FinishReason.STOP
    # The request went through the one request builder: every limit is set.
    assert sent[0]["path"] == "/api/generate"
    assert sent[0]["prompt"] == PROMPT
    assert sent[0]["options"] == {"num_ctx": 10_000, "num_predict": 200}
    assert (sent[0]["truncate"], sent[0]["shift"], sent[0]["stream"]) == (False, False, False)
    [row] = ledger(db)
    assert row["status"] == "completed"
    assert (row["purpose"], row["model"]) == ("answer", get_settings().llm_model)
    assert (row["estimated_prompt_tokens"], row["max_output_tokens"]) == (estimate(counter), 200)
    assert (row["prompt_tokens"], row["completion_tokens"]) == (31, 6)
    assert (row["finish_reason"], row["error"]) == ("stop", None)
    assert row["received_output_tokens_estimated"] is None
    assert row["duration_ms"] is not None


async def test_a_call_over_the_budget_is_neither_sent_nor_recorded(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    """AC-07, and the rule that a request stopped locally is not an LLM call."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("nothing may be sent")

    too_long = "The quick brown fox jumps over the lazy dog. " * 1_200

    with pytest.raises(ContextBudgetExceeded):
        await gateway(counter, handler).generate(
            too_long, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        )
    # The prompt fits, but not with the room reserved for the answer.
    with pytest.raises(ContextBudgetExceeded):
        await gateway(counter, handler).generate(
            PROMPT, purpose="answer", max_output_tokens=9_990, context=CallContext(owner_id=owner)
        )

    assert ledger(db) == []


async def test_an_input_refused_by_ollama_is_a_failed_call_with_unknown_usage(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"error": "the input length exceeds the context length"})

    with pytest.raises(LLMCallFailed) as raised:
        await gateway(counter, handler).generate(
            PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        )

    assert raised.value.code == "INPUT_EXCEEDS_CONTEXT"
    [row] = ledger(db)
    assert row["status"] == "failed"
    assert row["error"].startswith("INPUT_EXCEEDS_CONTEXT")
    # Not measured: the fields stay empty, the estimate is kept.
    assert (row["prompt_tokens"], row["completion_tokens"], row["finish_reason"]) == (
        None,
        None,
        None,
    )
    assert row["estimated_prompt_tokens"] == estimate(counter)


@pytest.mark.parametrize("failure", ["http_500", "unreachable", "garbage"])
async def test_a_failed_call_is_recorded_without_measured_values(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter, failure: str
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if failure == "http_500":
            return httpx.Response(500, json={"error": "model failed to load"})
        if failure == "unreachable":
            raise httpx.ConnectError("connection refused", request=request)
        return httpx.Response(200, content=b"not json")

    with pytest.raises(LLMCallFailed) as raised:
        await gateway(counter, handler).generate(
            PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        )

    assert raised.value.code == "LLM_UNAVAILABLE"
    [row] = ledger(db)
    assert row["status"] == "failed"
    assert row["error"]
    assert (row["prompt_tokens"], row["completion_tokens"], row["finish_reason"]) == (
        None,
        None,
        None,
    )


@pytest.mark.parametrize(
    ("completion_tokens", "expected"),
    [(200, FinishReason.OUTPUT_LIMIT), (57, FinishReason.CONTEXT_EXHAUSTED)],
)
async def test_an_answer_cut_short_is_measured_but_marked_with_the_reason(
    owner: uuid.UUID,
    db: psycopg.Connection,
    counter: Qwen3TokenCounter,
    completion_tokens: int,
    expected: FinishReason,
) -> None:
    """AC-57 (ledger): output limit and exhausted context are told apart."""

    def handler(request: httpx.Request) -> httpx.Response:
        body = answer(
            "An unfinished",
            prompt_tokens=31,
            completion_tokens=completion_tokens,
            done_reason="length",
        )
        return httpx.Response(200, json=body)

    result = await gateway(counter, handler).generate(
        PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
    )

    assert result.finish_reason is expected
    assert not result.finish_reason.is_complete
    [row] = ledger(db)
    # The call itself finished and was measured; the reason says the answer is not whole.
    assert (row["status"], row["finish_reason"]) == ("completed", expected.value)
    assert (row["prompt_tokens"], row["completion_tokens"]) == (31, completion_tokens)


async def test_a_stream_delivers_text_as_it_arrives_and_is_recorded_at_the_end(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content)["stream"] is True
        final = answer("", prompt_tokens=31, completion_tokens=3)
        return httpx.Response(200, content=stream_body(["Graphs", " and", " retrieval."], final))

    pieces: list[str] = []
    statuses_during: list[str] = []
    final = None
    stream = gateway(counter, handler).stream(
        PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
    )
    async for chunk in stream:
        if chunk.result is None:
            pieces.append(chunk.text)
            statuses_during.append(ledger(db)[0]["status"])
        else:
            final = chunk.result

    assert pieces == ["Graphs", " and", " retrieval."]
    # The ledger row exists before the answer starts, as pending.
    assert set(statuses_during) == {"pending"}
    assert final is not None
    assert (final.text, final.prompt_tokens, final.completion_tokens) == (
        "Graphs and retrieval.",
        31,
        3,
    )
    assert final.finish_reason is FinishReason.STOP
    [row] = ledger(db)
    assert (row["status"], row["finish_reason"]) == ("completed", "stop")
    assert (row["prompt_tokens"], row["completion_tokens"]) == (31, 3)


async def test_a_stream_that_breaks_is_a_failed_call_with_an_estimate_of_what_arrived(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = stream_body(["Graphs", " and", " retrieval."], None, break_after=2)
        return httpx.Response(200, content=body)

    received: list[str] = []
    with pytest.raises(LLMCallFailed):
        async for chunk in gateway(counter, handler).stream(
            PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        ):
            received.append(chunk.text)

    assert received == ["Graphs", " and"]
    [row] = ledger(db)
    assert row["status"] == "failed"
    assert (row["prompt_tokens"], row["completion_tokens"], row["finish_reason"]) == (
        None,
        None,
        None,
    )
    # An estimate, kept apart from the measured fields.
    assert row["received_output_tokens_estimated"] == counter.count("Graphs and")


async def test_a_stream_that_ends_without_a_final_report_is_a_failed_call(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=stream_body(["Graphs"], None))

    with pytest.raises(LLMCallFailed):
        async for _ in gateway(counter, handler).stream(
            PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        ):
            pass

    [row] = ledger(db)
    assert (row["status"], row["prompt_tokens"]) == ("failed", None)


async def test_a_reader_that_leaves_makes_the_call_interrupted(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    """AC-08 and AC-57: a client that disconnects is distinguishable from a cut-off answer."""

    def handler(request: httpx.Request) -> httpx.Response:
        final = answer("", prompt_tokens=31, completion_tokens=3)
        return httpx.Response(200, content=stream_body(["Graphs", " and", " retrieval."], final))

    stream = gateway(counter, handler).stream(
        PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
    )
    first = await anext(stream)
    await stream.aclose()  # what happens when the browser closes the connection

    assert first.text == "Graphs"
    [row] = ledger(db)
    assert (row["status"], row["finish_reason"]) == ("interrupted", "client_disconnect")
    assert (row["prompt_tokens"], row["completion_tokens"]) == (None, None)
    assert row["received_output_tokens_estimated"] == counter.count("Graphs")


async def test_a_refused_stream_is_a_failed_call_before_any_text(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"error": "the input length exceeds the context length"})

    with pytest.raises(LLMCallFailed) as raised:
        async for _ in gateway(counter, handler).stream(
            PROMPT, purpose="answer", max_output_tokens=200, context=CallContext(owner_id=owner)
        ):
            raise AssertionError("no text expected")

    assert raised.value.code == "INPUT_EXCEEDS_CONTEXT"
    assert ledger(db)[0]["status"] == "failed"


async def test_a_call_is_linked_to_its_owner_and_document(
    owner: uuid.UUID, db: psycopg.Connection, counter: Qwen3TokenCounter, client: TestClient
) -> None:
    document = client.post(
        "/api/v1/documents", files={"file": ("notes.txt", b"some text\n")}
    ).json()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=answer("ok", prompt_tokens=31, completion_tokens=1))

    context = CallContext(owner_id=owner, document_id=uuid.UUID(document["id"]))
    await gateway(counter, handler).generate(
        PROMPT, purpose="section_summary", max_output_tokens=200, context=context
    )

    row = db.execute(
        "SELECT owner_id, document_id, conversation_id, message_id, purpose FROM llm_calls"
    ).fetchone()
    assert row == (owner, uuid.UUID(document["id"]), None, None, "section_summary")
    # Deleting the document keeps the record and clears the reference.
    client.delete(f"/api/v1/documents/{document['id']}")
    assert db.execute("SELECT document_id FROM llm_calls").fetchone() == (None,)
