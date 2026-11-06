"""D71/D73: the experimental "roles" and "navigate" answer modes through the API.

"roles" changes only the prompt (one call, same evidence). "navigate" makes a navigation
call first, reads the targets back (place, need, priority), locates each on the document
map — sections and subsections from the heading lines of the chunks, tables and figures
from caption lines — ranks the candidate chunks of each located place by similarity to
the question and to the need, lets the targets take turns at the remaining budget behind
the retrieved sources, and then answers; both calls are in the ledger, and
`done.navigation` says what happened to every target and chunk.
"""

import json
import uuid

import httpx
import psycopg
from fastapi.testclient import TestClient

from app.chat.router import get_embedder
from app.core.database import get_sessionmaker
from app.core.env_loader import get_settings
from app.documents.storage import FileStorage
from app.ingestion.indexing import IndexJobRunner
from app.llm.embedding import EmbeddingError
from app.llm.tokenizer import Qwen3TokenCounter
from app.models import EMBEDDING_DIMENSIONS
from tests.integration import test_chat as chat_tests
from tests.integration import test_chat_summary as summary_tests
from tests.integration.test_chat import (
    ABLATION_TABLE,
    DOCUMENTS,
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
QUESTION = "Performance of the ablated variants"

# A paper-like text file: numbered sections and subsections, long enough for several
# chunks, with the ablation material inside subsection 4.2 and a table at its end.
_FILLER = (
    "The weather station on the hill records temperature, humidity and wind every "
    "minute, and the readings are averaged over the hour before they are written to the "
    "log. Visitors often ask why the readings differ from the valley; the answer is the "
    "altitude and the exposure of the ridge. "
)
PAPER = (
    "1 INTRODUCTION\n"
    + _FILLER * 12
    + "\n4 EVALUATION\n"
    + "4.1 EXPERIMENTAL SETTINGS\n"
    + "We use four datasets of documents and generate questions for each. " * 20
    + _FILLER * 10
    + "\n4.2 ABLATION STUDIES\n"
    + "The -High variant removes high-level retrieval and keeps only the low level. " * 12
    + _FILLER * 14
    + "The -Low variant removes low-level retrieval and keeps only the high level. " * 12
    + _FILLER * 14
    + "\n"
    + ABLATION_TABLE
    + "\n5 CONCLUSION\n"
    + _FILLER * 12
)
KEYWORDS = ("ablat", "variant")
DATASET_WORDS = ("dataset",)


def kind_of(text: str) -> int:
    lowered = text.lower()
    if any(k in lowered for k in KEYWORDS):
        return 0
    if any(k in lowered for k in DATASET_WORDS):
        return 1
    return 2


class KeywordEmbedder:
    """Three vectors only: texts about the ablation variants, texts about the datasets,
    and the rest, so that similarity is 1 within a kind and 0 across kinds. Can fail on a
    chosen call."""

    def __init__(self, *, fail_on_call: int | None = None) -> None:
        self.calls: list[list[str]] = []
        self._fail_on_call = fail_on_call

    async def embed(self, texts: list[str]) -> list[list[float]]:
        index = len(self.calls)
        self.calls.append(list(texts))
        if self._fail_on_call == index:
            raise EmbeddingError("The embedding service answered 500: simulated failure")
        vectors = []
        for text in texts:
            vector = [0.0] * EMBEDDING_DIMENSIONS
            vector[kind_of(text)] = 1.0
            vectors.append(vector)
        return vectors


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


def mode(client: TestClient, answer_mode: str, **settings: object) -> None:
    updated = get_settings().model_copy(update={"answer_mode": answer_mode, **settings})
    client.app.dependency_overrides[get_settings] = lambda: updated  # type: ignore[attr-defined]


async def add_paper(
    client: TestClient, tokenizer: Qwen3TokenCounter, embedder: KeywordEmbedder
) -> str:
    """Index the paper-like text with the keyword embedder, which the chat then uses too."""
    client.app.dependency_overrides[get_embedder] = lambda: embedder  # type: ignore[attr-defined]
    body = client.post(DOCUMENTS, files={"file": ("paper.txt", PAPER.encode())}).json()
    settings = get_settings()
    runner = IndexJobRunner(
        sessions=get_sessionmaker(),
        storage=FileStorage(settings.data_dir),
        tokenizer=tokenizer,
        embedder=embedder,
        settings=settings,
    )
    await runner.run(uuid.UUID(body["jobs"][0]["id"]))
    return str(body["id"])


def chunks_of(db: psycopg.Connection) -> list[tuple[int, str]]:
    return db.execute("SELECT ordinal, text FROM chunks ORDER BY ordinal").fetchall()


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


async def test_navigate_mode_plans_locates_and_then_answers_without_repeating_sources(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """The one-page document is already the retrieval: every located place is found to be
    among the retrieved sources, nothing is added, and the answer still follows."""
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = NavigatingOllama(
        "Reading plan:\n"
        "- Table 2 (page 1) | need: the ablation results | priority: required | status: covered\n"
        "- Table 9 | need: nothing\n"
        "- page 1 | need: the rest"
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
    assert [
        (i["location"], i["need"], i["priority"], i["status"], i["located"])
        for i in navigation["items"]
    ] == [
        ("Table 2 (page 1)", "the ablation results", "required", "covered", True),
        ("Table 9", "nothing", "required", None, False),
        ("page 1", "the rest", "required", None, True),
    ]
    assert navigation["items"][0]["label"] == "Table 2" and navigation["items"][1]["label"] is None
    assert navigation["located"] == 2
    assert navigation["fetched"] >= 2 and navigation["kept"] == 0
    assert all(
        e["reason"] == "already among the retrieved sources"
        for e in navigation["log"]
        if not e["kept"]
    )
    assert navigation["excluded_budget"] == 0
    assert navigation["embedding"] == {"texts": 2, "failed": None}
    assert all(s["origin"] == "retrieval" for s in by_name["sources"])
    # The analyst saw the targets as candidates, and answered from the sources.
    assert "A Navigator proposed where to look and what is needed there" in model.prompts[1]
    assert "- Table 9: nothing (not found in the document)" in model.prompts[1]
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    purposes = db.execute("SELECT purpose FROM llm_calls ORDER BY created_at").fetchall()
    assert [p for (p,) in purposes] == ["navigate", "answer"]
    usage = by_name["usage"]
    assert usage["calls"] == 2 and usage["prompt_tokens"] == 700 and usage["limit"] is None


async def test_the_map_has_subsections_with_chunk_ranges_and_the_navigator_sees_what_is_covered(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_paper(kim, tokenizer, KeywordEmbedder())
    model = NavigatingOllama("- Table 9 | need: nothing")
    use_model(kim, tokenizer, model)
    mode(kim, "navigate", top_k=1)

    events(ask(kim, new_conversation(kim), QUESTION))

    prompt = model.prompts[0]
    assert "- Section 1 INTRODUCTION (page 1)" in prompt
    assert "- Section 4 EVALUATION (page 1)" in prompt
    assert "  - Section 4.1 EXPERIMENTAL SETTINGS (page 1)" in prompt
    assert "  - Section 4.2 ABLATION STUDIES (page 1)" in prompt
    assert "- Table 2 (page 1): Win rates of the variants." in prompt
    # The retrieved source is described with its section, not just a header.
    assert "[1] paper.txt, page 1, Section 4.2 ABLATION STUDIES" in prompt
    assert "| need:" in prompt and "status: covered or missing" in prompt


async def test_targets_rank_the_chunks_of_their_subsection_by_the_need_and_take_turns(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    """Subsection 4.2 holds chunks about the variants and chunks of filler: only the former
    clear the relevance floor; the table named last still gets in first (structure); the
    supplementary target about 4.1 gets nothing because nothing there is relevant."""
    embedder = KeywordEmbedder()
    await add_paper(kim, tokenizer, embedder)
    model = NavigatingOllama(
        "- Section 4.1 | need: the datasets used | priority: supplementary | status: missing\n"
        "- Section 4.2 ABLATION STUDIES | need: definitions of the ablation variants"
        " | priority: required | status: missing\n"
        "- Table 2 | need: the win rates of the variants | priority: required | status: missing"
    )
    use_model(kim, tokenizer, model)
    mode(kim, "navigate", top_k=1)

    stream = events(ask(kim, new_conversation(kim), QUESTION))

    by_name = dict(stream)
    navigation = by_name["done"]["navigation"]
    chunks = dict(chunks_of(db))
    about = {o for o, text in chunks.items() if kind_of(text) == 0}
    datasets = {o for o, text in chunks.items() if kind_of(text) == 1}
    sources = by_name["sources"]
    assert sources[0]["origin"] == "retrieval" and len(sources) > 1
    added = [s for s in sources if s["origin"] == "navigation"]
    settings_items = navigation["items"]
    section, table = settings_items[1], settings_items[2]
    assert [i["located"] for i in settings_items] == [True, True, True]
    assert section["label"] == "4.2 ABLATION STUDIES" and table["label"] == "Table 2"
    # The table came first (structural), then the subsection's relevant chunks.
    table_ordinal = next(o for o, text in chunks.items() if text.startswith("Table 2:"))
    kept = [e for e in navigation["log"] if e["kept"] and e["target"] is not None]
    assert kept[0]["ordinal"] == table_ordinal or table_ordinal in {
        e["ordinal"]
        for e in navigation["log"]
        if e["reason"] == "already among the retrieved sources"
    }
    assert section["selected"] and all(o in about for o in section["selected"])
    assert len(section["selected"]) <= 3
    low = [e for e in navigation["log"] if e["reason"] == "low relevance"]
    assert low and all(e["ordinal"] not in about for e in low)
    assert all(e["score"] is not None and e["score"] < 0.45 for e in low)
    # 4.1: its need (the datasets) picked the chunks about the datasets, not the filler
    # before them, and the supplementary target went after the required ones each round.
    assert settings_items[0]["selected"] and all(
        o in datasets for o in settings_items[0]["selected"]
    )
    assert any(x["reason"] == "low relevance" for x in settings_items[0]["excluded"])
    first = {t: next(i for i, e in enumerate(kept) if e["target"] == t) for t in (0, 1, 2)}
    assert first[0] > first[1] and first[0] > first[2]
    assert len(added) == navigation["kept"] == sum(len(i["selected"]) for i in settings_items)
    # The question's embedding was reused; the two distinct needs cost one batched call.
    assert navigation["embedding"] == {"texts": 3, "failed": None}
    assert [len(call) for call in embedder.calls[-2:]] == [1, 3]
    assert navigation["evidence_tokens"] <= 5_500 and navigation["budget"] > 0
    assert (
        "- Section 4.2 ABLATION STUDIES: definitions of the ablation variants" in model.prompts[1]
    )


async def test_when_the_need_embeddings_fail_the_question_alone_ranks_the_candidates(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    # Calls: the indexing (several), the question (one), then the needs — that one fails.
    embedder = KeywordEmbedder()
    await add_paper(kim, tokenizer, embedder)
    embedder._fail_on_call = len(embedder.calls) + 1
    model = NavigatingOllama(
        "- Section 4.2 ABLATION STUDIES | need: definitions of the ablation variants"
        " | priority: required"
    )
    use_model(kim, tokenizer, model)
    mode(kim, "navigate", top_k=1)

    stream = events(ask(kim, new_conversation(kim), QUESTION))

    by_name = dict(stream)
    navigation = by_name["done"]["navigation"]
    assert navigation["embedding"] == {"texts": 1, "failed": "EMBEDDING_UNAVAILABLE"}
    assert navigation["kept"] >= 1  # ranked by the question's embedding alone
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    assert one(db, "SELECT count(*) FROM llm_calls") == (2,)


async def test_a_plan_that_locates_nothing_leaves_the_evidence_as_retrieved(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await add_document(kim, tokenizer, "ablation.txt", ABLATION_TABLE.encode())
    model = NavigatingOllama("- Table 9\n- the appendix on prompts")
    use_model(kim, tokenizer, model)
    mode(kim, "navigate")

    stream = events(ask(kim, new_conversation(kim)))

    navigation = dict(stream)["done"]["navigation"]
    assert navigation["located"] == 0 and navigation["fetched"] == 0 and navigation["kept"] == 0
    assert navigation["embedding"] == {"texts": 0, "failed": None}
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    assert one(db, "SELECT count(*) FROM llm_calls") == (2,)


async def test_the_summary_route_keeps_the_summaries_first_and_adds_targets_behind_them(
    kim: TestClient, db: psycopg.Connection, tokenizer: Qwen3TokenCounter
) -> None:
    await summary_tests.add_document(kim, tokenizer, "notes.md", summary_tests.NOTE)
    model = NavigatingOllama(
        "- Section Indexing | need: how the graph is built | priority: required"
    )
    use_model(kim, tokenizer, model)
    mode(kim, "navigate")

    stream = events(ask(kim, new_conversation(kim), "summary this document."))

    by_name = dict(stream)
    assert by_name["route"]["type"] == "summary"
    sources = by_name["sources"]
    assert sources and sources[0]["kind"] == "summary"
    navigation = by_name["done"]["navigation"]
    assert navigation is not None and navigation["skipped"] is None
    kinds = [s["kind"] for s in sources]
    assert kinds == sorted(kinds, key=lambda k: k != "summary")  # summaries first, chunks after
    assert "".join(d["text"] for n, d in stream if n == "delta").startswith(ANSWER)
    purposes = db.execute("SELECT purpose FROM llm_calls ORDER BY created_at").fetchall()
    assert [p for (p,) in purposes][-2:] == ["navigate", "answer"]
