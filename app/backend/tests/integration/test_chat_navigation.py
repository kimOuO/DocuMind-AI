"""D71: the experimental "roles" and "navigate" answer modes through the API.

"roles" changes only the prompt (one call, same evidence). "navigate" makes a navigation
call first, reads the plan back, keeps only the items it can locate on the document map,
fetches their chunks behind the retrieved ones and then answers; both calls are in the
ledger, and `done.navigation` says what happened to every item and chunk.
"""

import json

import httpx
import psycopg
from fastapi.testclient import TestClient

from app.core.env_loader import get_settings
from app.llm.tokenizer import Qwen3TokenCounter
from tests.integration import test_chat as chat_tests
from tests.integration.test_chat import (
    ABLATION_TABLE,
    add_document,
    ask,
    events,
    new_conversation,
    one,
    use_model,
)

kim = chat_tests.kim
tokenizer = chat_tests.tokenizer

ANSWER = "In Mix, the Comprehensiveness score of LightRAG falls from 61.2% to 59.6% for -High [1]."


class NavigatingOllama:
    """Plays the model: a reading plan for the navigation prompt, an answer otherwise."""

    def __init__(self, plan: str, answer: str = ANSWER) -> None:
        self.plan = plan
        self.answer = answer
        self.prompts: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.prompts.append(body["prompt"])
        if "Reading plan:" in body["prompt"]:
            assert not body["stream"]
            return httpx.Response(
                200,
                json={
                    "response": self.plan,
                    "done": True,
                    "done_reason": "stop",
                    "prompt_eval_count": 300,
                    "eval_count": 30,
                },
            )
        assert body["stream"]  # the answer is still streamed in these modes

        def lines():  # type: ignore[no-untyped-def]
            yield (json.dumps({"response": self.answer, "done": False}) + "\n").encode()
            yield (
                json.dumps(
                    {
                        "response": "",
                        "done": True,
                        "done_reason": "stop",
                        "prompt_eval_count": 400,
                        "eval_count": 40,
                    }
                )
                + "\n"
            ).encode()

        return httpx.Response(200, content=b"".join(lines()))


def mode(client: TestClient, answer_mode: str) -> None:
    settings = get_settings().model_copy(update={"answer_mode": answer_mode})
    client.app.dependency_overrides[get_settings] = lambda: settings  # type: ignore[attr-defined]


async def test_roles_mode_adds_the_two_roles_and_the_map_to_the_one_prompt(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = NavigatingOllama("unused")
    use_model(kim, tokenizer, model)
    mode(kim, "roles")

    stream = events(ask(kim, new_conversation(kim)))

    by_name = dict(stream)
    assert [n for n, _ in stream if n == "stage"] == []  # one streamed call, as in single mode
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    assert len(model.prompts) == 1
    prompt = model.prompts[0]
    assert prompt.index("Navigator") < prompt.index("Analyst") < prompt.index("Sources:")
    assert "Table 2 (page 1): Win rates of the variants." in prompt  # the map, from the caption
    assert by_name["done"]["navigation"] is None
    assert one(db, "SELECT count(*) FROM llm_calls") == (1,)


async def test_navigate_mode_plans_locates_fetches_and_then_answers(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = NavigatingOllama(
        "Reading plan:\n- Table 2 (page 1): the ablation results\n- Table 9\n- page 1"
    )
    use_model(kim, tokenizer, model)
    mode(kim, "navigate")

    stream = events(ask(kim, new_conversation(kim)))

    by_name = dict(stream)
    names = [n for n, _ in stream]
    assert names.index("stage") < names.index("sources") < names.index("delta")
    assert [d["stage"] for n, d in stream if n == "stage"] == ["navigating"]
    navigation = by_name["done"]["navigation"]
    assert navigation["plan"].startswith("Reading plan:")
    assert [(i["text"], i["located"]) for i in navigation["items"]] == [
        ("Table 2 (page 1): the ablation results", True),
        ("Table 9", False),
        ("page 1", True),
    ]
    assert navigation["located"] == 2
    # Every located place is the one page of this document, whose chunks the retrieval
    # already had: fetched (per item) but not added, and nothing fell to the budget.
    assert navigation["fetched"] == 2 * 2 and navigation["kept"] == 0
    assert all(
        e["reason"] == "already among the retrieved sources"
        for e in navigation["log"]
        if not e["kept"]
    )
    assert navigation["excluded_budget"] == 0
    assert all(s["origin"] == "retrieval" for s in by_name["sources"])
    # The analyst saw the plan as candidates, and answered from the sources.
    assert "A Navigator proposed where to look (candidates, not verified)" in model.prompts[1]
    assert "Table 9 (not found in the document)" in model.prompts[1]
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    purposes = db.execute("SELECT purpose FROM llm_calls ORDER BY created_at").fetchall()
    assert [p for (p,) in purposes] == ["navigate", "answer"]
    usage = by_name["usage"]
    assert usage["calls"] == 2 and usage["prompt_tokens"] == 700 and usage["limit"] is None


async def test_a_plan_that_locates_nothing_leaves_the_evidence_as_retrieved(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = NavigatingOllama("- Table 9\n- the appendix on prompts")
    use_model(kim, tokenizer, model)
    mode(kim, "navigate")

    stream = events(ask(kim, new_conversation(kim)))

    navigation = dict(stream)["done"]["navigation"]
    assert navigation["located"] == 0 and navigation["fetched"] == 0
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    assert one(db, "SELECT count(*) FROM llm_calls") == (2,)
