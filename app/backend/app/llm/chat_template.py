"""The prompt Ollama actually sends to the model for a text-only conversation.

Ollama wraps messages in the model's chat template before tokenizing them, and
the wrapper counts towards the context limit. This module reproduces the
template of `qwen3:32b` (as returned by /api/show) for the cases this project
uses: an optional system instruction, user and assistant turns, no tools.

It exists for counting only. Requests still send plain messages to Ollama,
which applies its own template; tests marked `llm` check that the token count
of this rendering equals the prompt_eval_count Ollama reports (AC-25).
"""

from dataclasses import dataclass
from typing import Literal

Role = Literal["user", "assistant"]


@dataclass(frozen=True)
class ChatMessage:
    role: Role
    content: str


def render_chat(messages: list[ChatMessage], *, system: str | None = None, thinking: bool) -> str:
    """Render a conversation that ends with a user turn, ready for the model to answer.

    `thinking` mirrors the `think` request option, which this project always
    sets: Ollama then appends a switch to the last user turn and, when thinking
    is off, pre-fills an empty think block in the assistant turn.
    """
    if not messages or messages[-1].role != "user":
        raise ValueError("The conversation must end with a user turn.")

    parts: list[str] = []
    if system:
        parts.append(f"<|im_start|>system\n\n{system}<|im_end|>\n")

    last_index = len(messages) - 1
    for index, message in enumerate(messages):
        if message.role == "user":
            switch = (" /think" if thinking else " /no_think") if index == last_index else ""
            parts.append(f"<|im_start|>user\n{message.content}{switch}<|im_end|>\n")
        else:
            parts.append(f"<|im_start|>assistant\n{message.content}<|im_end|>\n")

    parts.append("<|im_start|>assistant\n")
    if not thinking:
        parts.append("<think>\n\n</think>\n\n")
    return "".join(parts)


def render_prompt(prompt: str, *, system: str | None = None, thinking: bool) -> str:
    """Render a single prompt, as Ollama does for a request without a conversation."""
    return render_chat([ChatMessage("user", prompt)], system=system, thinking=thinking)
