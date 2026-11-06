"""D71: the Navigator/Analyst experiment — the parts without a model or a database.

The document map, the reading plan read back from the Navigator's text and checked
against the map, the merge of plan-fetched chunks behind the original Top-K within
the budget, and the prompts of the two arms.
"""

import uuid

from app.chat.navigation import (
    build_map,
    build_navigation_prompt,
    map_text,
    merge_evidence,
    parse_plan,
    roles_preamble,
)
from app.chat.prompting import build_answer_prompt
from app.llm.tokenizer import Qwen3TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary

DOC = uuid.uuid4()


def summary(level: str, ordinal: int, title: str | None, start: int, end: int) -> StoredSummary:
    return StoredSummary(DOC, "paper.pdf", level, ordinal, title, start, end, "text", 10)


def chunk(
    ordinal: int, page: int, text: str, tokens: int, origin: str = "retrieval"
) -> RetrievedChunk:
    return RetrievedChunk(uuid.uuid4(), DOC, "paper.pdf", page, ordinal, text, tokens, 0.5, origin)


SUMMARIES = [
    summary("document", 0, None, 1, 16),
    summary("section", 1, "INTRODUCTION", 1, 2),
    summary("section", 2, "EVALUATION", 5, 10),
    summary("section", 3, "CONCLUSION", 10, 10),
]
CAPTIONS = [
    (
        DOC,
        "paper.pdf",
        7,
        "Table 1: Win rates (%) of baselines v.s. LightRAG across four datasets.",
    ),
    (
        DOC,
        "paper.pdf",
        8,
        "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.",
    ),
    (DOC, "paper.pdf", 9, "Figure 2: Comparison of Cost in Terms of Tokens and API Calls."),
]


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


# --- the document map -----------------------------------------------------------------


def test_the_map_lists_sections_tables_and_figures_with_their_pages_in_page_order() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)

    assert [(e.kind, e.label, e.page_start, e.page_end) for e in entries] == [
        ("section", "INTRODUCTION", 1, 2),
        ("section", "EVALUATION", 5, 10),
        ("table", "Table 1", 7, 7),
        ("table", "Table 2", 8, 8),
        ("figure", "Figure 2", 9, 9),
        ("section", "CONCLUSION", 10, 10),
    ]
    assert entries[3].caption.startswith("Performance of ablated versions")
    # The whole-document summary is not a place to look.
    assert all(e.label != "None" for e in entries)


def test_the_map_text_is_compact_and_names_every_entry_with_its_pages() -> None:
    text = map_text(build_map(SUMMARIES, CAPTIONS))

    assert "Section: EVALUATION (pages 5-10)" in text
    assert "Table 2 (page 8): Performance of ablated versions of LightRAG" in text
    assert "Figure 2 (page 9)" in text
    assert WordCounter().count(text) < 120


# --- the reading plan ------------------------------------------------------------------


def test_plan_lines_are_located_on_the_map_or_marked_as_not_found() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)
    plan = (
        "Reading plan:\n"
        "- Table 2 (page 8): the ablation results\n"
        "- Section EVALUATION, the paragraph after the table\n"
        "- page 9 for the cost comparison\n"
        "- Table 9: does not exist in this paper\n"
        "- The appendix on prompts\n"
    )

    items = parse_plan(plan, entries)

    assert [item.text for item in items] == [
        "Table 2 (page 8): the ablation results",
        "Section EVALUATION, the paragraph after the table",
        "page 9 for the cost comparison",
        "Table 9: does not exist in this paper",
        "The appendix on prompts",
    ]
    assert items[0].entry is not None and items[0].entry.label == "Table 2"
    assert items[0].pages == [8]
    assert items[1].entry is not None and items[1].entry.label == "EVALUATION"
    assert items[1].pages == [5, 6, 7, 8, 9, 10]
    assert items[2].entry is None and items[2].pages == [9]  # an explicit page counts
    assert items[3].entry is None and items[3].pages == []
    assert items[4].entry is None and items[4].pages == []
    assert [item.located for item in items] == [True, True, True, False, False]


def test_a_page_beyond_the_document_is_not_located() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)

    [item] = parse_plan("- page 40", entries)

    assert item.located is False and item.pages == []


def test_a_section_is_found_by_its_number_or_enough_of_its_title() -> None:
    entries = build_map([summary("section", 1, "4.3 ABLATION STUDIES (RQ2)", 7, 8)], [])

    assert parse_plan("- Section 4.3", entries)[0].entry is not None
    assert parse_plan("- the ablation studies section", entries)[0].entry is not None
    assert parse_plan("- the related work section", entries)[0].entry is None


# --- merging the evidence ------------------------------------------------------------


def test_the_top_k_is_kept_whole_and_plan_chunks_fill_the_rest_of_the_budget() -> None:
    base = [chunk(10, 7, "top one", 300), chunk(20, 8, "top two", 300)]
    entries = build_map(SUMMARIES, CAPTIONS)
    [table, cost] = parse_plan("- Table 2\n- page 9", entries)
    fetched = [
        (table, [chunk(21, 8, "table two", 400), base[1]]),  # the second is already in
        (cost, [chunk(30, 9, "cost one", 500), chunk(31, 9, "cost two", 900)]),
    ]

    used, log = merge_evidence(base, fetched, WordCounter(), budget=1_600)

    assert [c.ordinal for c in used] == [10, 20, 21, 30]
    assert [c.origin for c in used] == ["retrieval", "retrieval", "navigation", "navigation"]
    assert [(e["ordinal"], e["kept"], e["reason"]) for e in log] == [
        (10, True, "retrieval"),
        (20, True, "retrieval"),
        (21, True, "plan: Table 2"),
        (20, False, "already among the retrieved sources"),
        (30, True, "plan: page 9"),
        (31, False, "over the evidence budget"),
    ]


def test_without_a_plan_the_evidence_is_the_top_k_unchanged() -> None:
    base = [chunk(10, 7, "top one", 300)]

    used, log = merge_evidence(base, [], WordCounter(), budget=1_000)

    assert used == base and [e["kept"] for e in log] == [True]


# --- the prompts -----------------------------------------------------------------------


def test_the_navigation_prompt_asks_for_places_not_facts() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)
    headers = [
        "[1] paper.pdf, page 8: Table 2: Performance of ablated…",
        "[2] paper.pdf, page 7: outperforms GraphRAG…",
    ]

    prompt, max_output = build_navigation_prompt(
        "Performance of ablated versions of LightRAG", entries, headers, Qwen3TokenCounter(), 10_000
    )

    assert "Question: Performance of ablated versions of LightRAG" in prompt
    assert "Table 2 (page 8)" in prompt and "Section: EVALUATION (pages 5-10)" in prompt
    assert headers[0] in prompt
    assert "Do not answer the question" in prompt and "do not state" in prompt.lower()
    assert prompt.endswith("Reading plan:")
    assert 200 <= max_output <= 600
    assert Qwen3TokenCounter().count(prompt) + max_output <= 10_000


def test_the_roles_preamble_puts_the_navigator_before_the_analyst_and_shows_the_map() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)
    preamble = roles_preamble(entries)
    prompt, _ = build_answer_prompt(
        "q", [chunk(1, 8, "Table 2 text", 10)], WordCounter(), 5_500, preamble=preamble
    )

    assert prompt.index("Navigator") < prompt.index("Analyst") < prompt.index("Sources:")
    assert "Table 2 (page 8)" in prompt
    assert "candidates, not facts" in prompt.lower() or "not state any fact" in prompt.lower()
    # The default prompt is unchanged without a preamble.
    plain, _ = build_answer_prompt("q", [chunk(1, 8, "Table 2 text", 10)], WordCounter(), 5_500)
    assert "Navigator" not in plain
