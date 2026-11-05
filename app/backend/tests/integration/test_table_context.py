"""Table-aware context expansion end to end (D62).

A question whose search results include a table also gets the discussion that
follows the table, within the same section, marked as added context. Ordinary
questions and tables at the end of a section get nothing extra.
"""

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.env_loader import get_settings
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration.test_chat import (
    StubOllama,
    add_document,
    ask,
    events,
    login,
    new_conversation,
    use_model,
)

pytestmark = pytest.mark.db

TABLE_THEN_DISCUSSION = (
    "# Results\n\n"
    "Table 1: Win rates of the variants.\n"
    "Agriculture Legal\n"
    "Full -High Full -High\n"
    "Overall 67.6% 64.8% 84.8% 78.0%\n"
    "\n"
    "The -High variant removes high-level retrieval, which costs it a few points.\n\n"
    "# Methods\n\n"
    "The methods section describes the indexing pipeline in detail.\n"
)
TABLE_THEN_SECTION = (
    "# Results\n\n"
    "Table 1: Win rates of the variants.\n"
    "Agriculture Legal\n"
    "Full -High Full -High\n"
    "Overall 67.6% 64.8% 84.8% 78.0%\n"
    "\n"
    "# Methods\n\n"
    "The methods section describes the indexing pipeline in detail.\n"
)


@pytest.fixture(scope="module")
def tokenizer() -> Qwen3TokenCounter:
    return Qwen3TokenCounter()


TABLE_CHUNK = (
    "Table 1: Win rates of the variants.\nAgriculture Legal\nFull -High Full -High\n"
    "Overall — Agriculture: Full 67.6%, -High 64.8%; Legal: Full 84.8%, -High 78.0%"
)


@pytest.fixture()
def kim(client: TestClient) -> TestClient:
    # Top-K 1 and a question identical to the table chunk (fake vectors give identical
    # texts 1.0, different ones about 0.75): the search returns the table and nothing else,
    # so whatever else appears can only come from the expansion.
    client.app.dependency_overrides[get_settings] = lambda: get_settings().model_copy(  # type: ignore[attr-defined]
        update={"top_k": 1}
    )
    return login(client, "kim")


async def test_the_discussion_after_a_retrieved_table_is_added_as_separate_context(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "results.md", TABLE_THEN_DISCUSSION.encode())
    model = StubOllama(["Full wins 67.6% [1], -High 64.8% [1]; it removes high-level [2]."])
    use_model(kim, tokenizer, model)

    received = dict(events(ask(kim, new_conversation(kim), TABLE_CHUNK)))

    sources = received["sources"]
    assert [s["origin"] for s in sources] == ["retrieval", "table_context"]
    table, context = sources
    assert table["snippet"] == TABLE_CHUNK and table["score"] == pytest.approx(1.0, abs=1e-4)
    assert context["score"] is None and context["page_start"] == 1
    assert context["snippet"].startswith("The -High variant removes high-level retrieval")
    # The next section's heading ends the expansion; it is inside this chunk, so the
    # chunk is still added, but nothing after it.
    assert "# Methods" in context["snippet"]
    [prompt] = model.prompts
    assert "(the text that follows the table above)" in prompt
    assert received["done"]["answered"] is True


async def test_a_table_at_the_end_of_its_section_gets_no_added_context(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "results.md", TABLE_THEN_SECTION.encode())
    use_model(kim, tokenizer, StubOllama(["Full wins 67.6% [1]."]))

    received = dict(events(ask(kim, new_conversation(kim), TABLE_CHUNK)))

    # Only the table itself: the chunk after it starts with the next section's heading.
    origins = [(s["origin"], s["snippet"][:8]) for s in received["sources"]]
    assert origins == [("retrieval", "Table 1:")]


async def test_a_question_without_a_table_among_its_results_is_unchanged(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "graph.txt", b"LightRAG builds a graph of entities.")
    use_model(kim, tokenizer, StubOllama(["LightRAG builds a graph [1]."]))

    received = dict(events(ask(kim, new_conversation(kim), "What does LightRAG build?")))

    assert [s["origin"] for s in received["sources"]] == ["retrieval"]
