"""The shape of every generation request sent to Ollama, and how its answer is read.

No test here calls Ollama. What Ollama actually does with these requests is
checked by tests/integration/test_ollama_context_limits.py (marked `llm`).
"""

from pathlib import Path

import pytest

from app.core.env_loader import Settings
from app.llm.chat_template import ChatMessage
from app.llm.ollama_api import (
    FinishReason,
    chat_request,
    generate_request,
    is_input_too_long,
    read_finish_reason,
)

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = BACKEND_ROOT.parents[1]
SETTINGS = Settings(llm_model="qwen3:32b", llm_context_limit=10_000, llm_thinking=False)


def _assert_limits(body: dict, max_output_tokens: int) -> None:
    # Model options live under "options" ...
    assert body["options"]["num_ctx"] == 10_000
    assert body["options"]["num_predict"] == max_output_tokens
    # ... while these two are request fields. In the wrong place Ollama ignores them.
    assert body["truncate"] is False
    assert body["shift"] is False
    assert "truncate" not in body["options"]
    assert "shift" not in body["options"]
    assert "num_ctx" not in body
    assert "num_predict" not in body


def test_a_single_prompt_request_carries_every_limit() -> None:
    request = generate_request(SETTINGS, prompt="Hi", max_output_tokens=200, stream=False)

    assert request.path == "/api/generate"
    assert request.body["model"] == "qwen3:32b"
    assert request.body["prompt"] == "Hi"
    assert request.body["stream"] is False
    assert request.body["think"] is False
    assert "system" not in request.body
    _assert_limits(request.body, 200)


def test_a_conversation_request_carries_every_limit() -> None:
    messages = [
        ChatMessage("user", "one"),
        ChatMessage("assistant", "two"),
        ChatMessage("user", "three"),
    ]

    request = chat_request(
        SETTINGS, messages=messages, system="Be brief.", max_output_tokens=2_500, stream=True
    )

    assert request.path == "/api/chat"
    assert request.body["stream"] is True
    assert request.body["messages"] == [
        {"role": "system", "content": "Be brief."},
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
    ]
    _assert_limits(request.body, 2_500)


def test_the_system_instruction_and_thinking_follow_the_caller_and_the_settings() -> None:
    thinking = Settings(llm_thinking=True)

    request = generate_request(
        thinking, prompt="Hi", system="Be brief.", max_output_tokens=10, stream=False
    )

    assert request.body["system"] == "Be brief."
    assert request.body["think"] is True


def test_temperature_is_sent_only_when_asked_for() -> None:
    default = generate_request(SETTINGS, prompt="Hi", max_output_tokens=10, stream=False)
    fixed = generate_request(
        SETTINGS, prompt="Hi", max_output_tokens=10, stream=False, temperature=0
    )

    assert "temperature" not in default.body["options"]
    assert fixed.body["options"]["temperature"] == 0
    _assert_limits(fixed.body, 10)


def test_the_context_limit_comes_from_the_settings() -> None:
    small = Settings(llm_context_limit=2_000)

    request = generate_request(small, prompt="Hi", max_output_tokens=10, stream=False)

    assert request.body["options"]["num_ctx"] == 2_000


@pytest.mark.parametrize("max_output_tokens", [0, -1, 10_000, 20_000])
def test_an_output_limit_must_be_set_and_leave_room_for_the_prompt(max_output_tokens: int) -> None:
    with pytest.raises(ValueError):
        generate_request(SETTINGS, prompt="Hi", max_output_tokens=max_output_tokens, stream=False)
    with pytest.raises(ValueError):
        chat_request(
            SETTINGS,
            messages=[ChatMessage("user", "Hi")],
            max_output_tokens=max_output_tokens,
            stream=False,
        )


@pytest.mark.parametrize(
    ("done_reason", "completion_tokens", "expected"),
    [
        ("stop", 12, FinishReason.STOP),
        # Stopped by the output limit: exactly as many tokens as allowed.
        ("length", 400, FinishReason.OUTPUT_LIMIT),
        # Stopped early although more output was allowed: the context window was full.
        ("length", 76, FinishReason.CONTEXT_EXHAUSTED),
        ("length", None, FinishReason.UNKNOWN),
        (None, 12, FinishReason.UNKNOWN),
        ("load", 0, FinishReason.UNKNOWN),
    ],
)
def test_finish_reason(
    done_reason: str | None, completion_tokens: int | None, expected: FinishReason
) -> None:
    final = {"done": True, "done_reason": done_reason, "eval_count": completion_tokens}
    final = {key: value for key, value in final.items() if value is not None}

    assert read_finish_reason(final, max_output_tokens=400) is expected


def test_only_a_natural_stop_is_a_complete_answer() -> None:
    assert FinishReason.STOP.is_complete
    assert not FinishReason.OUTPUT_LIMIT.is_complete
    assert not FinishReason.CONTEXT_EXHAUSTED.is_complete
    assert not FinishReason.UNKNOWN.is_complete


def test_a_response_that_is_not_finished_has_no_finish_reason() -> None:
    assert (
        read_finish_reason({"done": False, "response": "partial"}, max_output_tokens=400)
        is FinishReason.UNKNOWN
    )


def test_the_refusal_of_an_over_long_input_is_recognised() -> None:
    refusal = '{"error":"the input length exceeds the context length"}'

    assert is_input_too_long(400, refusal)
    assert not is_input_too_long(400, '{"error":"model is required"}')
    assert not is_input_too_long(500, refusal)
    assert not is_input_too_long(200, "{}")


def test_generation_requests_are_built_in_one_place_only() -> None:
    """Every call must carry the limits, so no other code may assemble a request itself."""
    forbidden = (
        "/api/generate",
        "/api/chat",
        "/api/embed",
        '"num_ctx"',
        '"num_predict"',
        '"truncate"',
        '"shift"',
    )
    allowed = BACKEND_ROOT / "app" / "llm" / "ollama_api.py"
    sources = [*(BACKEND_ROOT / "app").rglob("*.py"), *(REPOSITORY_ROOT / "scripts").glob("*.py")]

    offenders = [
        f"{path.relative_to(REPOSITORY_ROOT)}: {needle}"
        for path in sources
        if path != allowed
        for needle in forbidden
        if needle in path.read_text(encoding="utf-8")
    ]

    assert sources
    assert offenders == []
