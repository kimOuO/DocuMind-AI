"""The one place that builds generation requests for Ollama and reads how they ended.

Every request must carry the same limits, so that the context window can never
be exceeded without notice:

- `options.num_ctx`      the context window, prompt and answer together
- `options.num_predict`  the most tokens the answer may use
- `truncate: false`      an input that does not fit is refused (HTTP 400) instead
                         of being cut to size
- `shift: false`         generation stops when the window is full instead of
                         discarding the beginning of the prompt

`truncate` and `shift` are request fields, not model options: placed under
`options`, Ollama ignores them. A unit test checks that no other module builds
a request of its own.

Behaviour verified against Ollama 0.24.0 by the tests marked `llm`. It must be
verified again whenever Ollama is upgraded.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.core.env_loader import Settings
from app.llm.chat_template import ChatMessage

INPUT_TOO_LONG_MESSAGE = "the input length exceeds the context length"


@dataclass(frozen=True)
class OllamaRequest:
    path: str
    body: dict[str, Any]


class FinishReason(StrEnum):
    """Why generation ended. Only STOP means the model finished its answer."""

    STOP = "stop"
    OUTPUT_LIMIT = "output_limit"
    CONTEXT_EXHAUSTED = "context_exhausted"
    UNKNOWN = "unknown"

    @property
    def is_complete(self) -> bool:
        return self is FinishReason.STOP


def _limits(
    settings: Settings, max_output_tokens: int, stream: bool, temperature: float | None
) -> dict[str, Any]:
    if max_output_tokens <= 0:
        raise ValueError("max_output_tokens must be positive: every call needs an output limit.")
    if max_output_tokens >= settings.llm_context_limit:
        raise ValueError("max_output_tokens must leave room for the prompt in the context window.")
    options: dict[str, Any] = {
        "num_ctx": settings.llm_context_limit,
        "num_predict": max_output_tokens,
    }
    if temperature is not None:
        options["temperature"] = temperature
    return {
        "model": settings.llm_model,
        "stream": stream,
        "think": settings.llm_thinking,
        "truncate": False,
        "shift": False,
        "options": options,
    }


def generate_request(
    settings: Settings,
    *,
    prompt: str,
    system: str | None = None,
    max_output_tokens: int,
    stream: bool,
    temperature: float | None = None,
) -> OllamaRequest:
    """A request that answers a single prompt."""
    body = _limits(settings, max_output_tokens, stream, temperature)
    body["prompt"] = prompt
    if system:
        body["system"] = system
    return OllamaRequest("/api/generate", body)


def chat_request(
    settings: Settings,
    *,
    messages: list[ChatMessage],
    system: str | None = None,
    max_output_tokens: int,
    stream: bool,
    temperature: float | None = None,
) -> OllamaRequest:
    """A request that answers the last user turn of a conversation."""
    body = _limits(settings, max_output_tokens, stream, temperature)
    turns = [{"role": message.role, "content": message.content} for message in messages]
    if system:
        turns.insert(0, {"role": "system", "content": system})
    body["messages"] = turns
    return OllamaRequest("/api/chat", body)


def read_finish_reason(final: dict[str, Any], *, max_output_tokens: int) -> FinishReason:
    """Classify the last object of a response (the one with `done: true`).

    Ollama reports `length` both when the output limit is reached and when the
    context window is full. The two are told apart by the number of tokens
    generated: fewer than the limit means the window ran out first.
    """
    if not final.get("done"):
        return FinishReason.UNKNOWN
    reason = final.get("done_reason")
    if reason == "stop":
        return FinishReason.STOP
    if reason == "length":
        generated = final.get("eval_count")
        if not isinstance(generated, int):
            return FinishReason.UNKNOWN
        if generated >= max_output_tokens:
            return FinishReason.OUTPUT_LIMIT
        return FinishReason.CONTEXT_EXHAUSTED
    return FinishReason.UNKNOWN


def is_input_too_long(status_code: int, body: str) -> bool:
    """Whether a response is Ollama refusing an input that exceeds the context window."""
    return status_code == 400 and INPUT_TOO_LONG_MESSAGE in body
