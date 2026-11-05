"""What Ollama does at the edge of the context window, with this project's request settings.

These tests are about the server, not about local counting (that is AC-25,
tests/integration/test_token_count_agreement.py). They check that the limits
sent with every request make Ollama itself keep prompt + answer within the
context window:

- AC-55: an input that does not fit is refused, not truncated.
- AC-56: generation stops when the window is full; the prompt is never shifted
         out, and the output never exceeds its limit.
- The reason generation ended can be told apart, so that an answer that was
  cut short is not taken for a complete one.

Verified against Ollama 0.24.0. Run again after every Ollama upgrade:
    pytest -m llm tests/integration/test_ollama_context_limits.py -s
"""

import json
from dataclasses import dataclass

import httpx
import pytest

from app.core.env_loader import Settings, get_settings
from app.llm.chat_template import ChatMessage, render_prompt
from app.llm.ollama_api import (
    FinishReason,
    OllamaRequest,
    chat_request,
    generate_request,
    is_input_too_long,
    read_finish_reason,
)
from app.llm.tokenizer import Qwen3TokenCounter

pytestmark = pytest.mark.llm

SENTENCE = "The quick brown fox jumps over the lazy dog. "
ESSAY = "Write a very long and detailed essay about foxes."


@dataclass
class Outcome:
    status_code: int
    body: str
    chunks: int
    text: str
    final: dict

    @property
    def prompt_tokens(self) -> int:
        return int(self.final["prompt_eval_count"])

    @property
    def completion_tokens(self) -> int:
        return int(self.final["eval_count"])


def _send(settings: Settings, request: OllamaRequest) -> Outcome:
    """Send a request built by the application and collect the whole response."""
    response = httpx.post(
        f"{settings.ollama_base_url}{request.path}", json=request.body, timeout=900
    )
    if response.status_code != 200:
        return Outcome(response.status_code, response.text, 0, "", {})
    objects = [json.loads(line) for line in response.text.splitlines() if line.strip()]
    text = "".join(o.get("response") or o.get("message", {}).get("content") or "" for o in objects)
    return Outcome(200, response.text, len(objects), text, objects[-1])


def _filler(
    counter: Qwen3TokenCounter, settings: Settings, prompt_tokens: int, ending: str = ""
) -> str:
    """The longest prompt whose full rendering does not exceed `prompt_tokens`."""
    low, high = 1, prompt_tokens
    while low < high:
        middle = (low + high + 1) // 2
        rendered = render_prompt(SENTENCE * middle + ending, thinking=settings.llm_thinking)
        if counter.count(rendered) <= prompt_tokens:
            low = middle
        else:
            high = middle - 1
    return SENTENCE * low + ending


@pytest.fixture(scope="module")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


@pytest.mark.parametrize("stream", [False, True])
def test_an_input_over_the_context_limit_is_refused_not_truncated(
    settings: Settings, counter: Qwen3TokenCounter, stream: bool
) -> None:
    too_long = _filler(counter, settings, settings.llm_context_limit + 2_000)
    requests = [
        generate_request(settings, prompt=too_long, max_output_tokens=50, stream=stream),
        chat_request(
            settings, messages=[ChatMessage("user", too_long)], max_output_tokens=50, stream=stream
        ),
    ]

    for request in requests:
        outcome = _send(settings, request)

        # Refused before anything is generated: no partial answer to mistake for a real one.
        assert outcome.status_code == 400, request.path
        assert is_input_too_long(outcome.status_code, outcome.body)
        assert outcome.chunks == 0


def test_an_input_just_within_the_limit_is_accepted_in_full(
    settings: Settings, counter: Qwen3TokenCounter
) -> None:
    limit = settings.llm_context_limit
    prompt = _filler(counter, settings, limit - 200)

    outcome = _send(
        settings, generate_request(settings, prompt=prompt, max_output_tokens=20, stream=False)
    )

    assert outcome.status_code == 200
    # Nothing was cut off: Ollama evaluated the whole prompt.
    local = counter.count(render_prompt(prompt, thinking=settings.llm_thinking))
    assert outcome.prompt_tokens == local
    assert outcome.prompt_tokens + outcome.completion_tokens <= limit


@pytest.mark.parametrize("stream", [False, True])
def test_generation_stops_when_the_context_is_full_instead_of_shifting(
    settings: Settings, counter: Qwen3TokenCounter, stream: bool
) -> None:
    limit = settings.llm_context_limit
    allowed_output = 400
    # Leaves room for about 60 tokens of answer although 400 are allowed.
    prompt = _filler(counter, settings, limit - 60, ending=ESSAY)

    outcome = _send(
        settings,
        generate_request(
            settings, prompt=prompt, max_output_tokens=allowed_output, stream=stream, temperature=0
        ),
    )

    assert outcome.status_code == 200
    # The window is used up to the limit and not beyond: nothing was discarded to make room.
    assert outcome.prompt_tokens + outcome.completion_tokens == limit
    assert 0 < outcome.completion_tokens < allowed_output
    reason = read_finish_reason(outcome.final, max_output_tokens=allowed_output)
    assert reason is FinishReason.CONTEXT_EXHAUSTED
    assert not reason.is_complete


@pytest.mark.parametrize("stream", [False, True])
def test_the_output_never_exceeds_its_limit(settings: Settings, stream: bool) -> None:
    allowed_output = 40

    outcome = _send(
        settings,
        generate_request(
            settings, prompt=ESSAY, max_output_tokens=allowed_output, stream=stream, temperature=0
        ),
    )

    assert outcome.status_code == 200
    assert outcome.completion_tokens == allowed_output
    reason = read_finish_reason(outcome.final, max_output_tokens=allowed_output)
    assert reason is FinishReason.OUTPUT_LIMIT
    # The stream ended normally, yet the answer is not complete.
    assert outcome.final["done"] is True
    assert not reason.is_complete


@pytest.mark.parametrize("stream", [False, True])
def test_a_natural_end_is_the_only_complete_answer(settings: Settings, stream: bool) -> None:
    request = chat_request(
        settings,
        messages=[ChatMessage("user", "Reply with exactly one word: hello")],
        max_output_tokens=300,
        stream=stream,
        temperature=0,
    )

    outcome = _send(settings, request)

    assert outcome.status_code == 200
    assert outcome.completion_tokens < 300
    reason = read_finish_reason(outcome.final, max_output_tokens=300)
    assert reason is FinishReason.STOP
    assert reason.is_complete
    assert outcome.text.strip()
