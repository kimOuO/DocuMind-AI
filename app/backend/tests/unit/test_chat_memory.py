"""Conversation memory for follow-up questions (AC-16).

The memory given to the rewrite call keeps the most recent turns verbatim and
reduces earlier ones to their questions, within 800 tokens. Answers that did
not complete are left out.
"""

from app.chat.memory import (
    MEMORY_TOKEN_BUDGET,
    HistoryMessage,
    build_memory,
    clean_rewrite,
    rewrite_prompt,
)
from app.llm.tokenizer import Qwen3TokenCounter


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


def exchange(question: str, answer: str, status: str = "completed") -> list[HistoryMessage]:
    return [
        HistoryMessage("user", question, "completed"),
        HistoryMessage("assistant", answer, status),
    ]


def test_recent_turns_are_kept_verbatim_oldest_first() -> None:
    history = exchange("What does LightRAG build?", "A graph of entities [1].") + exchange(
        "How is it retrieved?", "At two levels [2]."
    )

    memory = build_memory(history, WordCounter(), budget_tokens=100)

    assert memory == (
        "User: What does LightRAG build?\n"
        "Assistant: A graph of entities [1].\n"
        "User: How is it retrieved?\n"
        "Assistant: At two levels [2]."
    )


def test_earlier_turns_keep_only_their_questions_when_the_budget_is_tight() -> None:
    history = (
        exchange("First question here?", "A long first answer with many many words in it.")
        + exchange("Second question here?", "A long second answer with many many words in it.")
        + exchange("Third question here?", "Short third answer.")
    )
    # Room for the last turn whole (9 words) and the earlier questions (4+4), not their answers.
    memory = build_memory(history, WordCounter(), budget_tokens=18)

    assert memory == (
        "User: First question here?\n"
        "User: Second question here?\n"
        "User: Third question here?\n"
        "Assistant: Short third answer."
    )


def test_the_oldest_questions_are_dropped_when_even_they_do_not_fit() -> None:
    history = (
        exchange("Q1 one?", "A1.")
        + exchange("Q2 two?", "A2 is a long answer.")
        + exchange("Q3 three?", "A3.")
    )
    # 8 words: the last turn (5), then the second question (3); the first question no longer fits.
    memory = build_memory(history, WordCounter(), budget_tokens=8)

    assert memory == "User: Q2 two?\nUser: Q3 three?\nAssistant: A3."


def test_answers_that_did_not_complete_are_left_out() -> None:
    history = (
        exchange("What does LightRAG build?", "A graph [1].")
        + exchange("And GraphRAG?", "GraphRAG bui", status="interrupted")
        + exchange("Any cost figures?", "", status="failed")
    )

    memory = build_memory(history, WordCounter(), budget_tokens=100)

    assert memory == (
        "User: What does LightRAG build?\nAssistant: A graph [1].\n"
        "User: And GraphRAG?\nUser: Any cost figures?"
    )


def test_no_history_means_no_memory() -> None:
    assert build_memory([], WordCounter(), budget_tokens=100) == ""


def test_the_rewrite_prompt_holds_the_memory_and_the_question_and_fits_its_budget() -> None:
    counter = Qwen3TokenCounter()
    memory = "User: What does LightRAG build?\nAssistant: A graph of entities [1]."

    prompt = rewrite_prompt(memory, "那它的缺點呢？")

    assert memory in prompt
    assert prompt.endswith("Latest question: 那它的缺點呢？\nStandalone question:")
    assert "same language" in prompt
    assert "Do not answer" in prompt
    # Instructions alone stay small; memory (800) and the question (200) come on top.
    assert counter.count(rewrite_prompt("", "")) <= 300
    assert MEMORY_TOKEN_BUDGET == 800


def test_the_rewritten_question_is_cleaned_or_rejected() -> None:
    assert clean_rewrite('  "What are the drawbacks of LightRAG?"  \n') == (
        "What are the drawbacks of LightRAG?"
    )
    assert clean_rewrite("Standalone question: What is LightRAG?") == "What is LightRAG?"
    assert clean_rewrite("「LightRAG 的缺點是什麼？」") == "LightRAG 的缺點是什麼？"
    assert clean_rewrite("   ") is None
    assert clean_rewrite("First line?\nSecond line explaining.") is None  # not a single question


def test_the_follow_up_judgement_is_asked_without_any_word_of_the_documents() -> None:
    """D99: the model decides whether a question leans on the conversation; the prompt's
    examples are about an unrelated report, and "same topic" is explicitly not enough."""
    from app.chat.memory import FOLLOW_UP_MAX_OUTPUT_TOKENS, follow_up_prompt, parse_follow_up

    prompt = follow_up_prompt(
        "User: What does LightRAG build?\nAssistant: A graph [1].", "那它的缺點呢？"
    )
    assert prompt.endswith("Message: 那它的缺點呢？\nAnswer:")
    assert "same topic" in prompt and "NEW or FOLLOW-UP" in prompt
    assert "solar" in prompt and "LightRAG" not in prompt.split("Conversation:")[0]
    assert FOLLOW_UP_MAX_OUTPUT_TOKENS <= 16
    assert parse_follow_up(" FOLLOW-UP\n") is True
    assert parse_follow_up("New") is False
    assert parse_follow_up("I am not sure") is None
