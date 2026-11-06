"""Local token counting: the vendored tokenizer file and the chat template mirror.

These tests do not call Ollama. Agreement with Ollama's own count is checked by
tests/integration/test_token_count_agreement.py (marked `llm`, AC-25).
"""

import hashlib
import shutil
from pathlib import Path

import pytest

from app.llm.chat_template import ChatMessage, render_chat, render_prompt
from app.llm.tokenizer import (
    BACKEND_ROOT,
    TOKENIZER_PATH,
    TOKENIZER_SHA256,
    Qwen3TokenCounter,
    TokenCounter,
    TokenizerFileError,
)

ENGLISH = "Retrieval-Augmented Generation (RAG) systems enhance large language models."
CHINESE = "這是一個本地執行的文件問答平台，回答必須附上來源。"


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


def test_the_vendored_tokenizer_file_is_unmodified() -> None:
    digest = hashlib.sha256(TOKENIZER_PATH.read_bytes()).hexdigest()

    assert digest == TOKENIZER_SHA256


def test_the_recorded_checksum_matches_the_asset_readme() -> None:
    readme = (TOKENIZER_PATH.parent / "README.md").read_text(encoding="utf-8")

    assert TOKENIZER_SHA256 in readme


def test_a_modified_tokenizer_file_is_refused(tmp_path: Path) -> None:
    altered = tmp_path / "tokenizer.json"
    shutil.copy(TOKENIZER_PATH, altered)
    with altered.open("ab") as handle:
        handle.write(b"\n")

    with pytest.raises(TokenizerFileError):
        Qwen3TokenCounter(altered)


def test_a_missing_tokenizer_file_is_refused(tmp_path: Path) -> None:
    with pytest.raises(TokenizerFileError):
        Qwen3TokenCounter(tmp_path / "missing.json")


def test_counter_satisfies_the_protocol(counter: Qwen3TokenCounter) -> None:
    as_protocol: TokenCounter = counter

    assert as_protocol.count("") == 0


def test_counts_match_values_measured_against_ollama(counter: Qwen3TokenCounter) -> None:
    # Ollama reported the same numbers for these strings (2026-11-05, raw mode).
    assert counter.count(ENGLISH) == 16
    assert counter.count(CHINESE) == 17


def test_no_start_token_is_added(counter: Qwen3TokenCounter) -> None:
    assert counter.count("a") == 1


def test_a_special_token_counts_as_one(counter: Qwen3TokenCounter) -> None:
    assert counter.count("<|im_start|>") == 1
    assert counter.count("<|im_end|>") == 1


def test_a_single_prompt_is_wrapped_like_ollama_does() -> None:
    assert render_prompt("Hi", thinking=False) == (
        "<|im_start|>user\nHi /no_think<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )


def test_thinking_changes_the_switch_and_drops_the_empty_think_block() -> None:
    assert render_prompt("Hi", thinking=True) == (
        "<|im_start|>user\nHi /think<|im_end|>\n<|im_start|>assistant\n"
    )


def test_a_system_instruction_comes_first() -> None:
    rendered = render_prompt("Hi", system="Be brief.", thinking=False)

    assert rendered.startswith("<|im_start|>system\n\nBe brief.<|im_end|>\n<|im_start|>user\nHi")


def test_only_the_last_user_turn_carries_the_thinking_switch() -> None:
    messages = [
        ChatMessage("user", "one"),
        ChatMessage("assistant", "two"),
        ChatMessage("user", "three"),
    ]

    assert render_chat(messages, thinking=False) == (
        "<|im_start|>user\none<|im_end|>\n"
        "<|im_start|>assistant\ntwo<|im_end|>\n"
        "<|im_start|>user\nthree /no_think<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )


def test_a_conversation_must_end_with_a_user_turn() -> None:
    with pytest.raises(ValueError):
        render_chat([ChatMessage("user", "one"), ChatMessage("assistant", "two")], thinking=False)
    with pytest.raises(ValueError):
        render_chat([], thinking=False)


def test_the_templated_prompt_count_matches_the_value_measured_against_ollama(
    counter: Qwen3TokenCounter,
) -> None:
    # Ollama reported 32 for this prompt through /api/generate with think=false.
    assert counter.count(render_prompt(ENGLISH, thinking=False)) == 32
    # ... and 41 with this system instruction.
    assert counter.count(render_prompt(ENGLISH, system="You answer briefly.", thinking=False)) == 41


def test_the_qwen36_tokenizer_file_loads_and_counts_table_text_differently() -> None:
    """D77/M5: qwen3.6 has its own vocabulary (248,044 entries against Qwen3's 151,669);
    the Qwen3 file undercounted its table text by up to 3%, so a qwen3.6 run must point the
    settings at this file. The checksum is the one recorded in the folder's README."""
    path = BACKEND_ROOT / "third-party" / "qwen3.6-tokenizer" / "tokenizer.json"
    counter = Qwen3TokenCounter(
        path, "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"
    )
    table = "Comprehensiveness 32.4% 67.6% 38.4% 61.6% 16.4% 83.6% 38.8% 61.2%\n" * 8

    assert counter.count("LightRAG") >= 1
    assert counter.count(table) != Qwen3TokenCounter().count(table)
