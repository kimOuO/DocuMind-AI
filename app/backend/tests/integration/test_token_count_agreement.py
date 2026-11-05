"""AC-25: the local token count must agree with what Ollama actually evaluates.

Five kinds of content (Chinese, English, mixed, code, multi-turn conversation),
each at three lengths (about 200, 2,000 and 8,000 tokens). For every case the
count of the full prompt, chat template included, is compared with the
`prompt_eval_count` Ollama reports.

- Never an undercount: local + safety buffer >= measured.
- A bounded overcount: local + safety buffer - measured <= max(32, 2% of measured).

Run with:  pytest -m llm tests/integration/test_token_count_agreement.py -s
"""

import re
from dataclasses import dataclass
from pathlib import Path

import httpx
import pytest

from app.core.env_loader import get_settings
from app.llm.chat_template import ChatMessage, render_chat
from app.llm.ollama_api import chat_request, generate_request
from app.llm.tokenizer import TOKENIZER_PATH, Qwen3TokenCounter

pytestmark = pytest.mark.llm

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
BACKEND_ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"short": 200, "medium": 2_000, "long": 8_000}
SYSTEM = "Answer only from the provided context and cite the source of every statement."
# Kind of content, and the system instruction sent with it.
SINGLE_PROMPT_KINDS = (("chinese", None), ("english", None), ("mixed", SYSTEM), ("code", SYSTEM))
CJK = re.compile(r"[一-鿿，。、；：「」（）！？]+")


@dataclass
class Case:
    name: str
    system: str | None
    messages: list[ChatMessage]


@dataclass
class Row:
    case: str
    local: int
    measured: int

    @property
    def difference(self) -> int:
        return self.local - self.measured


def _cycled(text: str, characters: int) -> str:
    """At least `characters` of text, repeating the source with a marker when it runs out."""
    parts: list[str] = []
    size = 0
    round_number = 0
    while size < characters:
        round_number += 1
        parts.append(f"\n[part {round_number}]\n{text}")
        size += len(parts[-1])
    return "".join(parts)


def _sources() -> dict[str, str]:
    specs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((REPOSITORY_ROOT / "docs" / "02-specs").glob("0*.md"))
    )
    code = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted((BACKEND_ROOT / "app").rglob("*.py"))
    )
    return {
        "chinese": "".join(CJK.findall(specs)),
        "english": (TOKENIZER_PATH.parent / "LICENSE").read_text(encoding="utf-8"),
        "mixed": specs,
        "code": code,
    }


def _fit(build, counter: Qwen3TokenCounter, target: int, upper: int) -> Case:
    """The largest case `build(size)` whose full prompt stays within `target` tokens."""
    low, high = 1, upper
    while low < high:
        middle = (low + high + 1) // 2
        case = build(middle)
        if _local_count(case, counter) <= target:
            low = middle
        else:
            high = middle - 1
    return build(low)


def _local_count(case: Case, counter: Qwen3TokenCounter) -> int:
    thinking = get_settings().llm_thinking
    return counter.count(render_chat(case.messages, system=case.system, thinking=thinking))


def _single_prompt_case(name: str, source: str, system: str | None, characters: int) -> Case:
    return Case(name, system, [ChatMessage("user", _cycled(source, characters)[:characters])])


def _conversation_case(name: str, sources: dict[str, str], turns: int, characters: int) -> Case:
    """Alternating user and assistant turns drawn from different kinds of content."""
    kinds = ["mixed", "english", "chinese", "code"]
    messages = []
    for index in range(turns):
        source = _cycled(sources[kinds[index % len(kinds)]], characters * (index + 2))
        start = characters * index
        role = "user" if index % 2 == 0 else "assistant"
        messages.append(ChatMessage(role, source[start : start + characters]))  # type: ignore[arg-type]
    return Case(name, SYSTEM, messages)


def _cases(counter: Qwen3TokenCounter) -> list[Case]:
    sources = _sources()
    cases = []
    for length, target in TARGETS.items():
        limit = target * 8  # no content here is denser than 8 characters per token
        for kind, system in SINGLE_PROMPT_KINDS:
            cases.append(
                _fit(
                    lambda size, kind=kind, system=system, length=length: _single_prompt_case(
                        f"{kind}/{length}", sources[kind], system, size
                    ),
                    counter,
                    target,
                    limit,
                )
            )
        turns = {"short": 5, "medium": 9, "long": 13}[length]
        cases.append(
            _fit(
                lambda size, turns=turns, length=length: _conversation_case(
                    f"conversation/{length}", sources, turns, size
                ),
                counter,
                target,
                limit // turns,
            )
        )
    return cases


def _measure(case: Case) -> int:
    """Send the case to Ollama and return the number of prompt tokens it evaluated."""
    settings = get_settings()
    if len(case.messages) == 1:
        request = generate_request(
            settings,
            prompt=case.messages[0].content,
            system=case.system,
            max_output_tokens=1,
            stream=False,
            temperature=0,
        )
    else:
        request = chat_request(
            settings,
            messages=case.messages,
            system=case.system,
            max_output_tokens=1,
            stream=False,
            temperature=0,
        )
    response = httpx.post(
        f"{settings.ollama_base_url}{request.path}", json=request.body, timeout=600
    )
    response.raise_for_status()
    return int(response.json()["prompt_eval_count"])


def test_local_counts_agree_with_ollama_for_every_kind_and_length() -> None:
    counter = Qwen3TokenCounter()
    buffer = get_settings().token_safety_buffer
    rows = [Row(case.name, _local_count(case, counter), _measure(case)) for case in _cases(counter)]

    print(f"\n{'case':24} {'local':>7} {'ollama':>7} {'diff':>5}   (safety buffer {buffer})")
    for row in rows:
        print(f"{row.case:24} {row.local:>7} {row.measured:>7} {row.difference:>+5}")

    assert len(rows) == 15
    # The cases really cover the three lengths, up to close to the limit.
    for row in rows:
        target = TARGETS[row.case.split("/")[1]]
        assert target * 0.9 <= row.local <= target, row
    undercounts = [row for row in rows if row.local + buffer < row.measured]
    assert not undercounts, f"local count is below what Ollama evaluated: {undercounts}"
    overcounts = [
        row for row in rows if row.local + buffer - row.measured > max(32, 0.02 * row.measured)
    ]
    assert not overcounts, f"local count overestimates by more than allowed: {overcounts}"
