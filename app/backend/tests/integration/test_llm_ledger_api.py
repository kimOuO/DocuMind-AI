"""GET /llm-calls: the ledger as its owner sees it (AC-08, and the ledger part of AC-33).

Calls are produced through the real gateway with a stubbed Ollama, so the
ledger holds exactly the kinds of rows the report must keep apart.
"""

import contextlib
import json
import uuid
from collections.abc import AsyncIterator, Callable

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.llm.gateway import CallContext, LLMCallFailed, OllamaGateway
from app.llm.ledger import RESTART_REASON, LedgerRepository
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

LEDGER = "/api/v1/llm-calls"
PROMPT = "Answer briefly: what does LightRAG combine?"


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def kim(client: TestClient) -> tuple[TestClient, uuid.UUID]:
    return client, uuid.UUID(register_and_login(client, "kim")["id"])


@pytest.fixture()
def lee(make_client: Callable[..., TestClient]) -> tuple[TestClient, uuid.UUID]:
    client = make_client()
    return client, uuid.UUID(register_and_login(client, "lee")["id"])


def gateway(counter: Qwen3TokenCounter, handler) -> OllamaGateway:  # type: ignore[no-untyped-def]
    return OllamaGateway(
        settings=get_settings(),
        sessions=get_sessionmaker(),
        counter=counter,
        transport=httpx.MockTransport(handler),
    )


def completed(prompt_tokens: int, completion_tokens: int):  # type: ignore[no-untyped-def]
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "response": "ok",
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": prompt_tokens,
                "eval_count": completion_tokens,
            },
        )

    return handler


def refused(request: httpx.Request) -> httpx.Response:
    return httpx.Response(400, json={"error": "the input length exceeds the context length"})


def unavailable(request: httpx.Request) -> httpx.Response:
    return httpx.Response(500, json={"error": "model failed to load"})


def streaming(request: httpx.Request) -> httpx.Response:
    async def lines() -> AsyncIterator[bytes]:
        for part in ("Graphs", " and", " retrieval."):
            yield (json.dumps({"response": part, "done": False}) + "\n").encode()

    return httpx.Response(200, content=lines())


async def call(counter: Qwen3TokenCounter, handler, owner: uuid.UUID, **context: uuid.UUID) -> None:  # type: ignore[no-untyped-def]
    # A failed call is still recorded; the failure itself is not what is tested here.
    with contextlib.suppress(LLMCallFailed):
        await gateway(counter, handler).generate(
            PROMPT,
            purpose="answer",
            max_output_tokens=200,
            context=CallContext(owner_id=owner, **context),
        )


async def test_measured_and_unmeasured_calls_are_reported_separately(
    kim: tuple[TestClient, uuid.UUID], db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    """AC-08: a call without measured values is never counted as measured compliance."""
    client, owner = kim
    await call(counter, completed(31, 6), owner)
    await call(counter, completed(31, 150), owner)
    await call(counter, unavailable, owner)
    await call(counter, refused, owner)
    stream = gateway(counter, streaming).stream(
        PROMPT, purpose="answer", max_output_tokens=2_500, context=CallContext(owner_id=owner)
    )
    await anext(stream)
    await stream.aclose()

    report = client.get(LEDGER).json()

    estimate = report["calls"][0]["estimated_prompt_tokens"]
    assert report["limit"] == 10_000
    assert report["measured"] == {"count": 2, "max_total_tokens": 181}
    # Three calls have no measured values; the largest budget they were sent with is reported.
    assert report["unmeasured"] == {"count": 3, "max_budget_upper_bound": estimate + 2_500}
    assert [c["status"] for c in report["calls"]] == [
        "interrupted",
        "failed",
        "failed",
        "completed",
        "completed",
    ]
    interrupted, rejected, failed, second, first = report["calls"]
    assert (first["prompt_tokens"], first["completion_tokens"], first["total_tokens"]) == (
        31,
        6,
        37,
    )
    assert first["budget_upper_bound"] == first["estimated_prompt_tokens"] + 200
    assert (first["finish_reason"], second["total_tokens"]) == ("stop", 181)
    for unmeasured in (interrupted, rejected, failed):
        assert unmeasured["prompt_tokens"] is None
        assert unmeasured["completion_tokens"] is None
        assert unmeasured["total_tokens"] is None
        assert unmeasured["budget_upper_bound"] is not None
    assert rejected["error"].startswith("INPUT_EXCEEDS_CONTEXT")
    assert interrupted["finish_reason"] == "client_disconnect"
    assert interrupted["received_output_tokens_estimated"] == counter.count("Graphs")


async def test_underestimates_are_counted(
    kim: tuple[TestClient, uuid.UUID], db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    """AC-25 at run time: a prompt that turned out larger than estimated is flagged."""
    client, owner = kim
    await call(counter, completed(31, 6), owner)
    assert client.get(LEDGER).json()["underestimate_events"] == 0

    estimate = client.get(LEDGER).json()["calls"][0]["estimated_prompt_tokens"]
    await call(counter, completed(estimate + 1, 6), owner)
    await call(counter, completed(estimate, 6), owner)  # equal is not an underestimate
    # Ollama refusing an input means the local count let through too much.
    await call(counter, refused, owner)

    assert client.get(LEDGER).json()["underestimate_events"] == 2


async def test_an_empty_ledger_reports_nothing_measured(kim: tuple[TestClient, uuid.UUID]) -> None:
    client, _ = kim

    assert client.get(LEDGER).json() == {
        "limit": 10_000,
        "measured": {"count": 0, "max_total_tokens": None},
        "unmeasured": {"count": 0, "max_budget_upper_bound": None},
        "underestimate_events": 0,
        "calls": [],
    }


async def test_the_ledger_only_shows_the_callers_own_calls(
    kim: tuple[TestClient, uuid.UUID],
    lee: tuple[TestClient, uuid.UUID],
    db: psycopg.Connection,
    counter: Qwen3TokenCounter,
) -> None:
    """AC-33 (ledger): another user's calls are invisible, also in the totals."""
    kim_client, kim_id = kim
    lee_client, lee_id = lee
    await call(counter, completed(31, 6), kim_id)
    await call(counter, completed(5_000, 2_000), lee_id)

    mine = kim_client.get(LEDGER).json()
    theirs = lee_client.get(LEDGER).json()

    assert mine["measured"] == {"count": 1, "max_total_tokens": 37}
    assert theirs["measured"] == {"count": 1, "max_total_tokens": 7_000}
    assert len(mine["calls"]) == len(theirs["calls"]) == 1
    assert mine["calls"][0]["id"] != theirs["calls"][0]["id"]


async def test_calls_can_be_filtered_by_document_and_limited(
    kim: tuple[TestClient, uuid.UUID],
    lee: tuple[TestClient, uuid.UUID],
    db: psycopg.Connection,
    counter: Qwen3TokenCounter,
) -> None:
    client, owner = kim
    document = client.post("/api/v1/documents", files={"file": ("a.txt", b"text\n")}).json()["id"]
    await call(counter, completed(31, 6), owner, document_id=uuid.UUID(document))
    await call(counter, completed(31, 7), owner)
    await call(counter, completed(31, 8), owner)

    filtered = client.get(LEDGER, params={"document_id": document}).json()
    limited = client.get(LEDGER, params={"limit": 2}).json()
    # Someone else filtering on this document sees nothing.
    stranger = lee[0].get(LEDGER, params={"document_id": document}).json()

    assert [c["completion_tokens"] for c in filtered["calls"]] == [6]
    assert filtered["measured"]["count"] == 1
    # The limit shortens the list, not the totals.
    assert [c["completion_tokens"] for c in limited["calls"]] == [8, 7]
    assert limited["measured"]["count"] == 3
    assert stranger["calls"] == [] and stranger["measured"]["count"] == 0
    assert client.get(LEDGER, params={"limit": 0}).status_code == 422


async def test_calls_left_pending_by_a_shutdown_are_failed_at_startup(
    kim: tuple[TestClient, uuid.UUID], db: psycopg.Connection, counter: Qwen3TokenCounter
) -> None:
    """AC-50 (ledger): they become failed, with no measured values."""
    client, owner = kim
    await call(counter, completed(31, 6), owner)
    async with get_sessionmaker()() as session, session.begin():
        await LedgerRepository(session).open(
            CallContext(owner_id=owner),
            purpose="answer",
            model="qwen3:32b",
            estimated_prompt_tokens=100,
            max_output_tokens=200,
        )

    async with get_sessionmaker()() as session, session.begin():
        assert await LedgerRepository(session).fail_pending(RESTART_REASON) == 1

    report = client.get(LEDGER).json()
    assert [(c["status"], c["prompt_tokens"], c["error"]) for c in report["calls"]] == [
        ("failed", None, RESTART_REASON),
        ("completed", 31, None),
    ]
    assert report["unmeasured"] == {"count": 1, "max_budget_upper_bound": 300}
