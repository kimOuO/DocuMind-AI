"""The gateway against the real model: the ledger holds what Ollama measured.

Run with:  pytest -m llm tests/integration/test_llm_gateway_real.py
"""

import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.llm.gateway import CallContext, OllamaGateway
from app.llm.ollama_api import FinishReason
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.conftest import register_and_login

pytestmark = [pytest.mark.llm, pytest.mark.db]

PROMPT = "Reply with exactly one word: hello"


def gateway() -> OllamaGateway:
    return OllamaGateway(
        settings=get_settings(), sessions=get_sessionmaker(), counter=Qwen3TokenCounter()
    )


@pytest.fixture()
def owner(client: TestClient) -> uuid.UUID:
    return uuid.UUID(register_and_login(client, "kim")["id"])


async def test_a_real_answer_is_recorded_with_measured_tokens_within_the_estimate(
    owner: uuid.UUID, db: psycopg.Connection
) -> None:
    result = await gateway().generate(
        PROMPT, purpose="answer", max_output_tokens=50, context=CallContext(owner_id=owner)
    )

    assert result.text.strip()
    assert result.finish_reason is FinishReason.STOP
    row = db.execute(
        "SELECT status, estimated_prompt_tokens, prompt_tokens, completion_tokens, finish_reason "
        "FROM llm_calls"
    ).fetchone()
    assert row is not None
    status, estimated, prompt_tokens, completion_tokens, finish_reason = row
    assert (status, finish_reason) == ("completed", "stop")
    # The local count plus the buffer is the estimate; here the count is exact.
    assert prompt_tokens == estimated - get_settings().token_safety_buffer
    assert prompt_tokens + completion_tokens <= get_settings().llm_context_limit


async def test_a_real_stream_arrives_in_pieces_and_is_recorded(
    owner: uuid.UUID, db: psycopg.Connection
) -> None:
    pieces: list[str] = []
    final = None
    async for chunk in gateway().stream(
        "Count from one to five in words, separated by commas.",
        purpose="answer",
        max_output_tokens=60,
        context=CallContext(owner_id=owner),
    ):
        if chunk.result is None:
            pieces.append(chunk.text)
        else:
            final = chunk.result

    assert len(pieces) > 1
    assert final is not None and final.text == "".join(pieces)
    row = db.execute("SELECT status, prompt_tokens, completion_tokens FROM llm_calls").fetchone()
    assert row == ("completed", final.prompt_tokens, final.completion_tokens)
    assert final.prompt_tokens is not None and final.completion_tokens is not None


async def test_a_real_answer_cut_by_the_output_limit_is_not_complete(
    owner: uuid.UUID, db: psycopg.Connection
) -> None:
    result = await gateway().generate(
        "Write a very long and detailed essay about foxes.",
        purpose="answer",
        max_output_tokens=20,
        context=CallContext(owner_id=owner),
    )

    assert result.finish_reason is FinishReason.OUTPUT_LIMIT
    assert result.completion_tokens == 20
    assert db.execute("SELECT status, finish_reason FROM llm_calls").fetchone() == (
        "completed",
        "output_limit",
    )
