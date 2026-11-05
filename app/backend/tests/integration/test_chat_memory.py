"""Follow-up questions (AC-16): rewritten from the conversation before retrieval.

The first question of a conversation is used as asked. A later one is first
rewritten by one LLM call (purpose `rewrite`) so that it stands on its own;
retrieval and the answer work from the rewritten question. A rewrite that
fails or is cut short is not used, and the question is answered as asked.
"""

import json
import uuid
from collections.abc import AsyncIterator

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient

from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.test_chat import (
    GRAPH,
    add_document,
    ask,
    events,
    login,
    new_conversation,
    use_model,
)

pytestmark = pytest.mark.db

FIRST = "What does LightRAG build?"
FOLLOW_UP = "What are its drawbacks?"
REWRITTEN = "What are the drawbacks of LightRAG?"


class RewritingModel:
    """Plays the model for both calls: the one-shot rewrite and the streamed answer."""

    def __init__(
        self,
        *,
        rewrite: str = REWRITTEN,
        rewrite_status: int = 200,
        rewrite_done_reason: str = "stop",
        fail_answers: int = 0,
    ) -> None:
        self.rewrite = rewrite
        self.rewrite_status = rewrite_status
        self.rewrite_done_reason = rewrite_done_reason
        self.fail_answers = fail_answers
        self.rewrite_prompts: list[str] = []
        self.answer_prompts: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert (body["truncate"], body["shift"]) == (False, False)
        if not body["stream"]:
            # The rewrite: bounded by the question budget, not the answer's.
            assert body["options"] == {"num_ctx": 10_000, "num_predict": 200}
            self.rewrite_prompts.append(body["prompt"])
            if self.rewrite_status != 200:
                return httpx.Response(self.rewrite_status, json={"error": "model failed to load"})
            return httpx.Response(
                200,
                json={
                    "response": self.rewrite,
                    "done": True,
                    "done_reason": self.rewrite_done_reason,
                    "prompt_eval_count": 150,
                    "eval_count": 200 if self.rewrite_done_reason == "length" else 9,
                },
            )
        assert body["options"] == {"num_ctx": 10_000, "num_predict": 2_500}
        self.answer_prompts.append(body["prompt"])
        if len(self.answer_prompts) <= self.fail_answers:
            return httpx.Response(500, json={"error": "model failed to load"})

        async def lines() -> AsyncIterator[bytes]:
            for piece in ["LightRAG builds", " a graph", " [1]."]:
                yield (json.dumps({"response": piece, "done": False}) + "\n").encode()
            final = {
                "response": "",
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 321,
                "eval_count": 3,
            }
            yield (json.dumps(final) + "\n").encode()

        return httpx.Response(200, content=lines())


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.fixture()
def kim(client: TestClient) -> TestClient:
    return login(client, "kim")


def calls(db: psycopg.Connection) -> list[tuple]:
    return db.execute(
        "SELECT purpose, status, finish_reason FROM llm_calls ORDER BY created_at"
    ).fetchall()


async def test_the_first_question_of_a_conversation_is_used_as_asked(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = RewritingModel()
    use_model(kim, tokenizer, model)  # type: ignore[arg-type]
    conversation = new_conversation(kim)

    received = dict(events(ask(kim, conversation, FIRST)))

    assert received["route"] == {"type": "retrieval", "standalone_question": FIRST}
    assert model.rewrite_prompts == []
    assert calls(db) == [("answer", "completed", "stop")]


async def test_a_follow_up_is_rewritten_from_the_conversation_before_retrieval(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = RewritingModel()
    use_model(kim, tokenizer, model)  # type: ignore[arg-type]
    conversation = new_conversation(kim)
    events(ask(kim, conversation, FIRST))

    received = dict(events(ask(kim, conversation, FOLLOW_UP)))

    assert received["route"] == {"type": "retrieval", "standalone_question": REWRITTEN}
    # The rewrite saw the earlier turn and the follow-up as asked.
    [rewrite_prompt] = model.rewrite_prompts
    earlier_turn = "User: What does LightRAG build?\nAssistant: LightRAG builds a graph [1]."
    assert earlier_turn in rewrite_prompt
    assert rewrite_prompt.endswith(f"Latest question: {FOLLOW_UP}\nStandalone question:")
    # Retrieval and the answer worked from the rewritten question.
    assert f"Question: {REWRITTEN}\nAnswer:" in model.answer_prompts[1]
    assert received["done"]["answered"] is True
    assert calls(db) == [
        ("answer", "completed", "stop"),
        ("rewrite", "completed", "stop"),
        ("answer", "completed", "stop"),
    ]
    # The user's message is stored as typed; the rewrite is only a working form.
    stored = kim.get(f"/api/v1/conversations/{conversation}").json()["messages"]
    assert [m["content"] for m in stored if m["role"] == "user"] == [FIRST, FOLLOW_UP]
    # The rewrite call is tied to this conversation and the answer message.
    row = db.execute(
        "SELECT conversation_id, message_id FROM llm_calls WHERE purpose = 'rewrite'"
    ).fetchone()
    assert row == (uuid.UUID(conversation), uuid.UUID(received["start"]["assistant_message_id"]))


@pytest.mark.parametrize(
    ("model", "expected_call"),
    [
        (RewritingModel(rewrite_status=500), ("rewrite", "failed", None)),
        (RewritingModel(rewrite_done_reason="length"), ("rewrite", "completed", "output_limit")),
        (RewritingModel(rewrite="Line one?\nLine two."), ("rewrite", "completed", "stop")),
    ],
    ids=["failed", "cut-short", "not-one-line"],
)
async def test_an_unusable_rewrite_leaves_the_question_as_asked(
    kim: TestClient,
    db: psycopg.Connection,
    tokenizer: Qwen3TokenCounter,
    model: RewritingModel,
    expected_call: tuple,
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    use_model(kim, tokenizer, model)  # type: ignore[arg-type]
    conversation = new_conversation(kim)
    events(ask(kim, conversation, FIRST))

    received = dict(events(ask(kim, conversation, FOLLOW_UP)))

    assert received["route"]["standalone_question"] == FOLLOW_UP
    assert f"Question: {FOLLOW_UP}\nAnswer:" in model.answer_prompts[1]
    assert received["done"]["status"] == "completed"
    assert calls(db)[1:] == [expected_call, ("answer", "completed", "stop")]


async def test_answers_that_did_not_complete_are_not_in_the_memory(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", GRAPH.encode())
    model = RewritingModel(fail_answers=1)
    use_model(kim, tokenizer, model)  # type: ignore[arg-type]
    conversation = new_conversation(kim)
    first = dict(events(ask(kim, conversation, FIRST)))
    assert "error" in first  # the first answer failed

    events(ask(kim, conversation, FOLLOW_UP))

    [rewrite_prompt] = model.rewrite_prompts
    assert "User: What does LightRAG build?" in rewrite_prompt
    assert "Assistant:" not in rewrite_prompt.split("Conversation:")[1]
