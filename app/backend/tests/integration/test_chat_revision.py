"""D69: the experimental two-call mode (ANSWER_REVISION=true) through the API.

The draft is not streamed. Stage events show progress; the deterministic checks run
on the draft; when they fault it and the budget allows, one revision call is made and
checked in turn; the chosen text is then sent as deltas. Both calls are in the ledger.
"""

import json
import uuid

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

# Fixtures are registered under the module attribute's name: re-export them as such.
kim = chat_tests.kim
tokenizer = chat_tests.tokenizer

WRONG_DRAFT = "In Mix, the Overall score of LightRAG falls from 60.0% to 59.6% for -High [1]."
RIGHT_REVISION = (
    "In Mix, the Comprehensiveness score of LightRAG falls from 61.2% to 59.6% for -High [1]."
)
STILL_WRONG = "In Agriculture, the Overall score of LightRAG is 67.6% and 65.2% for -High [1]."


class TwoCallOllama:
    """Plays the model for the two-call mode: one answer for the draft prompt, one for
    the revision prompt (told apart by the draft it quotes)."""

    def __init__(self, draft: str, revision: str) -> None:
        self.draft = draft
        self.revision = revision
        self.prompts: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert (body["truncate"], body["shift"]) == (False, False)
        self.prompts.append(body["prompt"])
        text = self.revision if "Draft answer:" in body["prompt"] else self.draft
        if body["stream"]:  # the two-call mode never streams
            raise AssertionError("the two-call mode must not stream the draft")
        return httpx.Response(
            200,
            json={
                "response": text,
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 321,
                "eval_count": 40,
            },
        )


def two_call_mode(client: TestClient, **overrides: object) -> None:
    settings = get_settings().model_copy(update={"answer_revision": True, **overrides})
    client.app.dependency_overrides[get_settings] = lambda: settings  # type: ignore[attr-defined]


async def test_a_faulted_draft_is_revised_and_the_revision_is_checked_and_chosen(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = TwoCallOllama(WRONG_DRAFT, RIGHT_REVISION)
    use_model(kim, tokenizer, model)
    two_call_mode(kim)

    stream = events(ask(kim, new_conversation(kim)))

    names = [name for name, _ in stream]
    stages = [data["stage"] for name, data in stream if name == "stage"]
    assert stages == ["generating", "verifying", "revising", "verifying", "finalizing"]
    # The draft never reaches the client; only the chosen text does, after finalizing.
    finalizing = next(
        i for i, (n, d) in enumerate(stream) if n == "stage" and d["stage"] == "finalizing"
    )
    assert finalizing < names.index("delta")
    deltas = "".join(data["text"] for name, data in stream if name == "delta")
    assert deltas == RIGHT_REVISION
    by_name = dict(stream)
    revision = by_name["done"]["revision"]
    assert revision["mode"] == "conditional" and revision["triggered"] is True
    assert [t["kind"] for t in revision["draft_triggers"]] == ["mislabelled_number"]
    assert revision["revision_triggers"] == []
    assert (revision["chosen"], revision["status"]) == ("revision", "verified")
    assert by_name["done"]["mislabelled_numbers"] == []
    # The revision prompt carried the question, the sources, the draft and the finding.
    assert len(model.prompts) == 2
    assert "Draft answer:\n" + WRONG_DRAFT in model.prompts[1]
    assert "59.6%" in model.prompts[1] and "Comprehensiveness" in model.prompts[1]
    # Two calls in the ledger, both completed, on the same message.
    purposes = db.execute(
        "SELECT purpose, status, message_id FROM llm_calls ORDER BY created_at"
    ).fetchall()
    assert [(p, s) for p, s, _ in purposes] == [("answer", "completed"), ("revise", "completed")]
    assert purposes[0][2] == purposes[1][2] == uuid.UUID(by_name["start"]["assistant_message_id"])
    assert one(db, "SELECT content FROM messages WHERE role = 'assistant'") == (RIGHT_REVISION,)


async def test_a_revision_with_a_new_hard_fault_is_rejected_and_the_draft_stays_flagged(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    use_model(kim, tokenizer, TwoCallOllama(WRONG_DRAFT, STILL_WRONG))
    two_call_mode(kim)

    stream = events(ask(kim, new_conversation(kim)))

    by_name = dict(stream)
    revision = by_name["done"]["revision"]
    assert (revision["chosen"], revision["status"]) == ("draft", "unverified")
    assert [t["kind"] for t in revision["revision_triggers"]] == ["mislabelled_number"]
    deltas = [data["text"] for name, data in stream if name == "delta"]
    assert deltas[0] == WRONG_DRAFT
    # The draft's own check result is what the client gets, note included.
    assert deltas[-1].startswith("\n\nFigures whose labels differ from the source table: 59.6%")
    assert [m["number"] for m in by_name["done"]["mislabelled_numbers"]] == ["59.6%"]


async def test_a_clean_draft_is_final_after_one_call(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = TwoCallOllama(RIGHT_REVISION, "never used")
    use_model(kim, tokenizer, model)
    two_call_mode(kim)

    stream = events(ask(kim, new_conversation(kim)))

    stages = [data["stage"] for name, data in stream if name == "stage"]
    assert stages == ["generating", "verifying", "finalizing"]
    by_name = dict(stream)
    revision = by_name["done"]["revision"]
    assert revision["triggered"] is False and revision["chosen"] == "draft"
    assert revision["status"] == "verified"
    assert len(model.prompts) == 1
    assert one(db, "SELECT count(*) FROM llm_calls") == (1,)


async def test_a_revision_that_would_not_fit_the_budget_is_skipped_safely(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    long_wrong_draft = WRONG_DRAFT + " More words follow here." * 500
    model = TwoCallOllama(long_wrong_draft, RIGHT_REVISION)
    use_model(kim, tokenizer, model)
    # The first call fits (short prompt + 2,500 for the answer); a prompt that also
    # carries the long draft does not leave room for a revision.
    two_call_mode(kim, llm_context_limit=3_400)

    stream = events(ask(kim, new_conversation(kim)))

    by_name = dict(stream)
    revision = by_name["done"]["revision"]
    assert revision["triggered"] is True and revision["skipped"] == "budget"
    assert (revision["chosen"], revision["status"]) == ("draft", "unverified")
    assert len(model.prompts) == 1
    assert one(db, "SELECT count(*) FROM llm_calls") == (1,)


async def test_always_revise_calls_twice_even_without_a_fault(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = TwoCallOllama(RIGHT_REVISION, RIGHT_REVISION)
    use_model(kim, tokenizer, model)
    two_call_mode(kim, revision_always=True)

    stream = events(ask(kim, new_conversation(kim)))

    revision = dict(stream)["done"]["revision"]
    assert revision["mode"] == "always" and revision["triggered"] is False
    assert len(model.prompts) == 2
    # Nothing to choose between: the revision brought no change in checks, the draft stays.
    assert (revision["chosen"], revision["status"]) == ("draft", "verified")
