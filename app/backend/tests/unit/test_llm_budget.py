"""The check made before any prompt is sent to the model (AC-07)."""

import pytest

from app.core.env_loader import Settings
from app.llm.chat_template import render_prompt
from app.llm.gateway import ContextBudgetExceeded, check_budget, estimate_prompt_tokens
from app.llm.tokenizer import Qwen3TokenCounter

SETTINGS = Settings(llm_context_limit=10_000, token_safety_buffer=16, llm_thinking=False)


@pytest.fixture(scope="module")
def counter() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


def test_the_estimate_counts_the_chat_template_and_adds_the_safety_buffer(
    counter: Qwen3TokenCounter,
) -> None:
    prompt = "Retrieval-Augmented Generation (RAG) systems enhance large language models."

    estimate = estimate_prompt_tokens(counter, SETTINGS, prompt)

    # 32 tokens once Ollama's template is applied (measured), plus the buffer of 16.
    assert counter.count(render_prompt(prompt, thinking=False)) == 32
    assert estimate == 32 + 16


def test_a_call_that_fits_exactly_is_allowed() -> None:
    check_budget(estimated_prompt_tokens=7_500, max_output_tokens=2_500, limit=10_000)


def test_a_call_one_token_over_the_limit_is_refused_before_it_is_sent() -> None:
    with pytest.raises(ContextBudgetExceeded) as raised:
        check_budget(estimated_prompt_tokens=7_501, max_output_tokens=2_500, limit=10_000)

    error = raised.value
    assert (error.estimated_prompt_tokens, error.max_output_tokens, error.limit) == (
        7_501,
        2_500,
        10_000,
    )
    assert "10001" in str(error) and "10000" in str(error)


def test_the_reserved_output_counts_towards_the_limit() -> None:
    # The prompt alone fits, but not together with the room kept for the answer.
    with pytest.raises(ContextBudgetExceeded):
        check_budget(estimated_prompt_tokens=9_000, max_output_tokens=2_500, limit=10_000)


def test_a_long_prompt_is_refused_whatever_its_content(counter: Qwen3TokenCounter) -> None:
    prompt = "The quick brown fox jumps over the lazy dog. " * 1_200  # about 12,000 tokens

    estimate = estimate_prompt_tokens(counter, SETTINGS, prompt)

    with pytest.raises(ContextBudgetExceeded):
        check_budget(
            estimated_prompt_tokens=estimate,
            max_output_tokens=200,
            limit=SETTINGS.llm_context_limit,
        )


def test_an_empty_answer_temperature_means_the_models_default() -> None:
    """D86: ANSWER_TEMPERATURE= keeps the default; a value is a float."""
    assert Settings(answer_temperature="").answer_temperature is None  # type: ignore[arg-type]
    assert Settings(answer_temperature="0").answer_temperature == 0.0  # type: ignore[arg-type]
    assert Settings().answer_temperature is None
