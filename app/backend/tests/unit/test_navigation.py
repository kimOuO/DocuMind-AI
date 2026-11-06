"""D71/D73: the Navigator/Analyst experiment — the parts without a model or a database.

The document map (sections and subsections from the heading lines of the chunks, tables
and figures from caption lines), the Navigator's targets read back from its text and
checked against the map, the selection of evidence across targets within the budget,
and the prompts of the two arms.
"""

import uuid

from app.chat.navigation import (
    EvidenceCandidate,
    TargetCandidates,
    analyst_preamble,
    build_map,
    build_navigation_prompt,
    describe_retrieved,
    map_text,
    parse_plan,
    roles_preamble,
    select_evidence,
)
from app.chat.prompting import build_answer_prompt
from app.llm.tokenizer import Qwen3TokenCounter
from app.retrieval.repository import RetrievedChunk
from app.summarization.repository import StoredSummary

DOC = uuid.uuid4()
FILE = "paper.pdf"


def summary(level: str, ordinal: int, title: str | None, start: int, end: int) -> StoredSummary:
    return StoredSummary(DOC, FILE, level, ordinal, title, start, end, "text", 10)


def chunk(
    ordinal: int, page: int, text: str, tokens: int, origin: str = "retrieval"
) -> RetrievedChunk:
    return RetrievedChunk(uuid.uuid4(), DOC, FILE, page, ordinal, text, tokens, 0.5, origin)


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


SUMMARIES = [
    summary("document", 0, None, 1, 16),
    summary("section", 1, "INTRODUCTION", 1, 2),
    summary("section", 2, "EVALUATION", 5, 10),
    summary("section", 3, "CONCLUSION", 10, 10),
]
# (document id, filename, page, chunk ordinal, caption line)
CAPTIONS = [
    (DOC, FILE, 7, 20, "Table 1: Win rates (%) of baselines v.s. LightRAG across four datasets."),
    (
        DOC,
        FILE,
        8,
        23,
        "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.",
    ),
    (DOC, FILE, 9, 27, "Figure 2: Comparison of Cost in Terms of Tokens and API Calls."),
]
# Chunks 0-9: ordinals 0-2 on page 1, 3-5 on page 2, 6-9 on page 3.
CHUNK_PAGES = [(DOC, o, 1 + o // 3 if o < 6 else 3) for o in range(10)]
# (document id, filename, page, chunk ordinal, line index within the chunk, heading line)
HEADINGS = [
    (DOC, FILE, 1, 0, 0, "1 I NTRODUCTION"),
    (DOC, FILE, 2, 3, 0, "4 E VALUATION"),
    (DOC, FILE, 2, 3, 5, "4.1 E XPERIMENTAL S ETTINGS"),
    (DOC, FILE, 2, 5, 0, "4.2 R ESULTS"),
    (DOC, FILE, 3, 8, 2, "5 C ONCLUSION"),
]


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
    assert entries[3].ordinal_start == entries[3].ordinal_end == 23  # the caption's chunk
    # Sections from the summaries have no chunk range: they are fetched by page.
    assert entries[1].ordinal_start is None
    # The whole-document summary is not a place to look.
    assert all(e.label != "None" for e in entries)


def test_headings_in_the_chunks_give_subsections_with_chunk_ranges_and_parents() -> None:
    entries = build_map(SUMMARIES, [], HEADINGS, CHUNK_PAGES)

    sections = [
        (e.label, e.level, e.parent, e.ordinal_start, e.ordinal_end, e.page_start, e.page_end)
        for e in entries
    ]
    assert sections == [
        ("1 INTRODUCTION", 1, None, 0, 2, 1, 1),
        ("4 EVALUATION", 1, None, 3, 8, 2, 3),
        # 4.1 and 4.2 share page 2: the chunk ranges tell them apart. 4.2 starts at the
        # first line of chunk 5, so chunk 5 is not 4.1's.
        ("4.1 EXPERIMENTAL SETTINGS", 2, "4 EVALUATION", 3, 4, 2, 2),
        # Section 5 begins inside chunk 8, so chunk 8 still belongs to 4.2 (and to 4).
        ("4.2 RESULTS", 2, "4 EVALUATION", 5, 8, 2, 3),
        ("5 CONCLUSION", 1, None, 8, 9, 3, 3),
    ]
    assert [e.number for e in entries] == ["1", "4", "4.1", "4.2", "5"]
    # The section summaries of a document whose headings were found are not repeated.
    assert "EVALUATION" not in [e.label for e in entries]


def test_a_heading_repeated_by_the_chunk_overlap_counts_once() -> None:
    repeated = [
        *HEADINGS,
        (DOC, FILE, 2, 4, 0, "4 E VALUATION"),
        (DOC, FILE, 2, 4, 1, "4.1 E XPERIMENTAL S ETTINGS"),
    ]

    entries = build_map([], [], repeated, CHUNK_PAGES)

    assert [e.label for e in entries].count("4 EVALUATION") == 1
    assert [(e.label, e.ordinal_start, e.ordinal_end) for e in entries if e.number == "4.1"] == [
        ("4.1 EXPERIMENTAL SETTINGS", 3, 4)
    ]


def test_a_document_without_recognised_headings_falls_back_to_its_section_summaries() -> None:
    other = uuid.uuid4()
    summaries = [*SUMMARIES, StoredSummary(other, "notes.txt", "section", 1, "Notes", 1, 1, "t", 1)]

    entries = build_map(summaries, [], HEADINGS, CHUNK_PAGES)

    assert [e.label for e in entries if e.document_id == other] == ["Notes"]
    assert [e.label for e in entries if e.document_id == DOC][:2] == [
        "1 INTRODUCTION",
        "4 EVALUATION",
    ]


def test_the_map_text_is_compact_and_indents_subsections_under_their_section() -> None:
    text = map_text(build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES))

    assert "- Section 4 EVALUATION (pages 2-3)" in text
    assert "  - Section 4.1 EXPERIMENTAL SETTINGS (page 2)" in text
    assert "- Table 2 (page 8): Performance of ablated versions of LightRAG" in text
    assert "- Figure 2 (page 9)" in text
    assert WordCounter().count(text) < 150


def test_retrieved_sources_are_described_with_their_section_and_a_snippet() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    table = chunk(
        23, 8, "Table 2: Performance of ablated versions\nLightRAG -High\nOverall 67.6% 64.8%", 30
    )
    body = chunk(4, 2, "We run the experiments on four datasets " * 10, 80)

    lines = describe_retrieved([table, body], entries, snippet_chars=60)

    assert lines[0].startswith("[1] paper.pdf, page 8, Table 2 (a table): Table 2: Performance")
    assert lines[1].startswith(
        "[2] paper.pdf, page 2, Section 4.1 EXPERIMENTAL SETTINGS: We run the"
    )
    assert len(lines[1]) < 60 + 70


# --- the Navigator's targets -------------------------------------------------------------


def test_targets_are_read_with_their_need_and_priority_and_located_on_the_map() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    plan = (
        "Reading plan:\n"
        "- Table 2 (page 8) | need: the values of every variant | priority: required"
        " | status: covered\n"
        "- Section 4.2 RESULTS | need: how the variants are defined and discussed"
        " | priority: required | status: missing\n"
        "- page 3 | need: the closing remarks | priority: supplementary\n"
        "- Table 9 | need: does not exist in this paper\n"
        "- The appendix on prompts\n"
    )

    items = parse_plan(plan, entries)

    assert [(i.location, i.need, i.priority, i.status) for i in items] == [
        ("Table 2 (page 8)", "the values of every variant", "required", "covered"),
        (
            "Section 4.2 RESULTS",
            "how the variants are defined and discussed",
            "required",
            "missing",
        ),
        ("page 3", "the closing remarks", "supplementary", None),
        ("Table 9", "does not exist in this paper", "required", None),
        ("The appendix on prompts", "The appendix on prompts", "required", None),
    ]
    assert (
        items[0].entry is not None and items[0].entry.label == "Table 2" and items[0].pages == [8]
    )
    assert items[1].entry is not None and items[1].entry.label == "4.2 RESULTS"
    assert items[1].pages == [2, 3]
    assert items[2].entry is None and items[2].pages == [3]  # an explicit page counts
    assert [i.located for i in items] == [True, True, True, False, False]
    # The raw line is kept for the record.
    assert items[0].text.startswith("Table 2 (page 8) | need:")


def test_targets_may_also_come_as_the_json_the_brief_showed() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    plan = (
        '{"targets": [{"location": "Section 4.1", "need": "settings", "priority": "required"},'
        ' {"location": "Figure 2", "need": "the cost", "priority": "supplementary",'
        ' "reason": "x"}]}'
    )

    items = parse_plan(plan, entries)

    assert [(i.location, i.need, i.priority) for i in items] == [
        ("Section 4.1", "settings", "required"),
        ("Figure 2", "the cost", "supplementary"),
    ]
    assert items[0].entry is not None and items[0].entry.label == "4.1 EXPERIMENTAL SETTINGS"
    assert items[1].entry is not None and items[1].entry.label == "Figure 2"


def test_a_page_beyond_the_document_is_not_located() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)

    [item] = parse_plan("- page 40", entries)

    assert item.located is False and item.pages == []


def test_a_section_is_found_by_its_number_or_enough_of_its_title() -> None:
    entries = build_map([summary("section", 1, "4.3 ABLATION STUDIES (RQ2)", 7, 8)], [])

    assert parse_plan("- Section 4.3", entries)[0].entry is not None
    assert parse_plan("- the ablation studies section", entries)[0].entry is not None
    assert parse_plan("- the related work section", entries)[0].entry is None


# --- selecting the evidence ------------------------------------------------------------


def target(item_text: str, candidates: list[EvidenceCandidate], entries=None) -> TargetCandidates:  # type: ignore[no-untyped-def]
    [item] = parse_plan(f"- {item_text}", entries or [])
    return TargetCandidates(item, candidates)


def semantic(c: RetrievedChunk, question: float, need: float | None = None) -> EvidenceCandidate:
    return EvidenceCandidate(c, question, need, structural=False)


def structural(c: RetrievedChunk) -> EvidenceCandidate:
    return EvidenceCandidate(c, None, None, structural=True)


def test_targets_take_turns_and_a_required_table_named_last_is_not_starved() -> None:
    base = [chunk(10, 7, "top one", 300)]
    section = [chunk(o, 2, f"section {o}", 300) for o in range(1, 6)]
    table, discussion = chunk(23, 8, "Table 2: …", 300), chunk(24, 8, "The -High variant …", 300)
    targets = [
        target(
            "Section 4.2 | need: discussion | priority: required",
            [semantic(c, 0.9 - 0.1 * i, 0.8) for i, c in enumerate(section)],
        ),
        target(
            "Table 2 | need: the values | priority: required",
            [structural(table), structural(discussion)],
        ),
    ]

    selection = select_evidence(base, targets, budget=1_200, floor=0.45)

    # Round 1: the table (structural, so first) then the section's best; round 2: the
    # table's discussion, and the section's second chunk is over the budget.
    assert [c.ordinal for c in selection.chunks] == [10, 23, 1, 24]
    assert [c.origin for c in selection.chunks] == [
        "retrieval",
        "navigation",
        "navigation",
        "navigation",
    ]
    assert [
        (e["ordinal"], e["kept"], e["reason"]) for e in selection.log if e["ordinal"] in (2, 3)
    ] == [
        (2, False, "over the evidence budget"),
        (3, False, "over the evidence budget"),
    ]
    assert selection.targets[1]["selected"] == [23, 24] and selection.targets[0]["selected"] == [1]
    assert selection.evidence_tokens == 1_200


def test_a_supplementary_target_waits_until_the_required_ones_are_settled() -> None:
    required = [chunk(1, 2, "r1", 100), chunk(2, 2, "r2", 100)]
    extra = [chunk(5, 4, "e1", 100), chunk(6, 4, "e2", 100)]
    targets = [
        target("page 4 | need: more | priority: supplementary", [semantic(c, 0.95) for c in extra]),
        target("page 2 | need: core | priority: required", [semantic(c, 0.6) for c in required]),
    ]

    selection = select_evidence([], targets, budget=300, floor=0.45)

    # D74: the required targets are settled first; supplementary ones use what is left.
    assert [c.ordinal for c in selection.chunks] == [1, 2, 5]


def test_candidates_below_the_relevance_floor_get_no_share_of_the_budget() -> None:
    weak = [chunk(o, 5, f"w{o}", 100) for o in range(1, 4)]
    targets = [target("page 5 | need: anything", [semantic(c, 0.2, 0.3) for c in weak])]

    selection = select_evidence([], targets, budget=10_000, floor=0.45)

    assert selection.chunks == []
    assert {e["reason"] for e in selection.log} == {"low relevance"}
    assert selection.targets[0]["candidates"] == 3 and selection.targets[0]["selected"] == []


def test_each_target_adds_at_most_a_few_chunks_even_with_room() -> None:
    many = [chunk(o, 5, f"m{o}", 10) for o in range(1, 8)]
    targets = [target("page 5 | need: all of it", [semantic(c, 0.9) for c in many])]

    selection = select_evidence([], targets, budget=10_000, floor=0.45, per_target=3)

    assert [c.ordinal for c in selection.chunks] == [1, 2, 3]
    assert all(e["reason"] == "target quota reached" for e in selection.log if not e["kept"])


def test_chunks_are_deduplicated_against_the_retrieved_sources_and_across_targets() -> None:
    shared = chunk(7, 3, "shared", 100)
    base = [chunk(10, 7, "top", 100)]
    targets = [
        target("page 3 | need: a", [semantic(shared, 0.9), semantic(base[0], 0.9)]),
        target(
            "page 7 | need: b", [semantic(shared, 0.8), semantic(chunk(8, 3, "other", 100), 0.7)]
        ),
    ]

    selection = select_evidence(base, targets, budget=10_000, floor=0.45)

    assert [c.ordinal for c in selection.chunks] == [10, 7, 8]
    reasons = [(e["ordinal"], e["target"], e["reason"]) for e in selection.log if not e["kept"]]
    # Round 1: target 0 takes the shared chunk, target 1 finds it taken; round 2: target 0
    # finds its next one among the retrieved sources, target 1 adds its other chunk.
    assert reasons == [
        (7, 1, "already selected for another target"),
        (10, 0, "already among the retrieved sources"),
    ]


def test_a_chunk_that_does_not_fit_is_skipped_and_a_smaller_one_still_gets_in() -> None:
    big, small = chunk(1, 2, "big", 900), chunk(2, 2, "small", 100)
    targets = [target("page 2 | need: x", [semantic(big, 0.9), semantic(small, 0.8)])]

    selection = select_evidence([], targets, budget=500, floor=0.45)

    assert [c.ordinal for c in selection.chunks] == [2]
    assert [(e["ordinal"], e["reason"]) for e in selection.log if not e["kept"]] == [
        (1, "over the evidence budget")
    ]


def test_the_selected_chunks_carry_their_relevance_and_the_log_says_which_target() -> None:
    c = chunk(1, 2, "x", 100)
    selection = select_evidence(
        [], [target("page 2 | need: x", [semantic(c, 0.7, 0.9)])], budget=500, floor=0.45
    )

    [kept] = selection.chunks
    assert kept.origin == "navigation" and kept.score == 0.8
    assert selection.log == [
        {"ordinal": 1, "page": 2, "kept": True, "reason": "plan: page 2", "target": 0, "score": 0.8}
    ]


def test_without_targets_the_evidence_is_the_top_k_unchanged() -> None:
    base = [chunk(10, 7, "top one", 300)]

    selection = select_evidence(base, [], budget=1_000, floor=0.45)

    assert selection.chunks == base
    assert selection.log == [
        {
            "ordinal": 10,
            "page": 7,
            "kept": True,
            "reason": "retrieval",
            "target": None,
            "score": None,
        }
    ]


# --- the prompts -----------------------------------------------------------------------


def test_the_navigation_prompt_asks_for_places_and_needs_not_facts() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    retrieved = ["[1] paper.pdf, page 8, Table 2 (a table): Table 2: Performance of ablated…"]

    prompt, max_output = build_navigation_prompt(
        "Performance of ablated versions of LightRAG",
        entries,
        retrieved,
        Qwen3TokenCounter(),
        10_000,
    )

    assert "Question: Performance of ablated versions of LightRAG" in prompt
    assert "- Table 2 (page 8)" in prompt and "  - Section 4.1 EXPERIMENTAL SETTINGS" in prompt
    assert retrieved[0] in prompt
    assert "| need:" in prompt and "priority:" in prompt and "status:" in prompt
    assert "Do not answer the question" in prompt and "do not state" in prompt.lower()
    assert prompt.endswith("Reading plan:")
    assert 200 <= max_output <= 600
    assert Qwen3TokenCounter().count(prompt) + max_output <= 10_000


def test_the_analyst_preamble_lists_the_targets_with_their_needs_as_candidates() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    items = parse_plan("- Table 2 | need: the values\n- Table 9 | need: nothing", entries)

    preamble = analyst_preamble(items)

    assert "candidates, not verified" in preamble
    assert "- Table 2: the values" in preamble
    assert "- Table 9: nothing (not found in the document)" in preamble


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


# --- coverage (D74) --------------------------------------------------------------------

from app.chat.navigation import COVERED, MISSING, PARTIAL, UNKNOWN, coverage_of  # noqa: E402

TABLE_TEXT = "Table 2: Win rates of the variants.\nOverall — Agri: Naive 32.4%, Full 67.6%"


def test_a_table_is_covered_only_when_its_chunk_is_retrieved_with_its_rows() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    [table] = parse_plan("- Table 2 | need: the values", entries)
    table_chunk = RetrievedChunk(uuid.uuid4(), DOC, FILE, 8, 23, TABLE_TEXT, 50, 0.7, "retrieval")
    caption_only = RetrievedChunk(
        uuid.uuid4(), DOC, FILE, 8, 23, "Table 2: Win rates of the variants.\nSee below.", 20, 0.7
    )
    same_page_prose = chunk(22, 8, "prose on the same page", 30)

    assert coverage_of(table, [table_chunk]) == (
        COVERED,
        "the table's chunk, with its rows, is among the sources",
    )
    assert coverage_of(table, [caption_only])[0] == PARTIAL
    assert coverage_of(table, [same_page_prose])[0] == MISSING  # the page alone is not enough
    assert coverage_of(table, [])[0] == MISSING


def test_a_section_is_covered_by_its_chunk_range_not_its_pages() -> None:
    entries = build_map(SUMMARIES, CAPTIONS, HEADINGS, CHUNK_PAGES)
    [section] = parse_plan("- Section 4.1 | need: settings", entries)  # chunks 3-4

    assert coverage_of(section, [chunk(3, 2, "a", 10), chunk(4, 2, "b", 10)])[0] == COVERED
    assert coverage_of(section, [chunk(3, 2, "a", 10)])[0] == PARTIAL
    assert coverage_of(section, [chunk(5, 2, "same page, other section", 10)])[0] == MISSING


def test_a_place_known_only_by_its_pages_is_unknown_not_covered() -> None:
    entries = build_map(SUMMARIES, CAPTIONS)  # sections from summaries: pages only
    [section] = parse_plan("- Section EVALUATION | need: results", entries)
    [page] = parse_plan("- page 7 | need: anything", entries)

    assert coverage_of(section, [chunk(20, 7, "on page 7", 10)])[0] == UNKNOWN
    assert coverage_of(page, [chunk(20, 7, "on page 7", 10)])[0] == UNKNOWN
    assert coverage_of(section, [])[0] == MISSING


def test_a_target_that_is_not_located_has_no_coverage() -> None:
    [item] = parse_plan("- Table 9 | need: nothing", build_map(SUMMARIES, CAPTIONS))
    assert coverage_of(item, [])[0] == "not_located"


# --- selection with coverage and the supplementary cap (D74) ---------------------------


def covered_target(
    item_text: str, candidates: list[EvidenceCandidate], coverage: str
) -> TargetCandidates:
    [item] = parse_plan(f"- {item_text}", [])
    return TargetCandidates(item, candidates, coverage)


def test_a_required_target_already_covered_fetches_nothing_and_says_why() -> None:
    base = [chunk(23, 8, TABLE_TEXT, 100)]
    targets = [covered_target("Table 2 | need: the values | priority: required", [], COVERED)]

    selection = select_evidence(base, targets, budget=10_000, floor=0.45)

    assert selection.chunks == base
    assert selection.targets[0]["coverage"] == COVERED and selection.targets[0]["selected"] == []
    assert selection.unmet_required == []


def test_supplementary_is_capped_for_the_question_and_skipped_when_required_is_covered() -> None:
    extras = [chunk(o, 4, f"e{o}", 100) for o in range(1, 6)]
    supplementary = [
        covered_target(
            "page 4 | need: more | priority: supplementary",
            [semantic(c, 0.9) for c in extras[:3]],
            MISSING,
        ),
        covered_target(
            "page 5 | need: even more | priority: supplementary",
            [semantic(c, 0.9) for c in extras[3:]],
            MISSING,
        ),
    ]
    required_missing = covered_target(
        "Table 2 | need: the values | priority: required",
        [structural(chunk(23, 8, TABLE_TEXT, 100))],
        MISSING,
    )

    with_missing = select_evidence(
        [], [required_missing, *supplementary], budget=10_000, floor=0.45
    )
    assert [c.ordinal for c in with_missing.chunks] == [
        23,
        1,
        4,
    ]  # one per supplementary target, two in all
    assert with_missing.supplementary_used == 2
    assert {e["reason"] for e in with_missing.log if not e["kept"]} == {"supplementary cap reached"}

    required_covered = covered_target(
        "Table 2 | need: the values | priority: required", [], COVERED
    )
    all_covered = select_evidence([], [required_covered, *supplementary], budget=10_000, floor=0.45)
    assert all_covered.chunks == []
    assert {e["reason"] for e in all_covered.log} == {"all required evidence already covered"}


def test_supplementary_never_takes_budget_a_required_target_still_needs() -> None:
    required = covered_target(
        "Section 4.2 | need: definitions | priority: required",
        [semantic(chunk(5, 2, "r1", 300), 0.6), semantic(chunk(6, 2, "r2", 300), 0.6)],
        MISSING,
    )
    extra = covered_target(
        "page 9 | need: context | priority: supplementary",
        [semantic(chunk(30, 9, "e", 300), 0.95)],
        MISSING,
    )

    selection = select_evidence([], [required, extra], budget=600, floor=0.45)

    assert [c.ordinal for c in selection.chunks] == [5, 6]
    assert [(e["ordinal"], e["reason"]) for e in selection.log if not e["kept"]] == [
        (30, "over the evidence budget")
    ]


def test_a_supplementary_chunk_that_repeats_selected_text_is_not_added() -> None:
    text = "the dual level retrieval paradigm combines low level and high level retrieval"
    base = [chunk(10, 7, text, 100)]
    near_copy = chunk(11, 7, text + " for better results", 100)
    fresh = chunk(12, 7, "incremental updates integrate new entities without rebuilding", 100)
    extra = covered_target(
        "page 7 | need: context | priority: supplementary",
        [semantic(near_copy, 0.95), semantic(fresh, 0.8)],
        MISSING,
    )

    selection = select_evidence(base, [extra], budget=10_000, floor=0.45)

    assert [c.ordinal for c in selection.chunks] == [10, 12]
    assert [(e["ordinal"], e["reason"]) for e in selection.log if not e["kept"]] == [
        (11, "repeats evidence already selected")
    ]


def test_a_required_target_that_does_not_fit_the_budget_is_recorded_as_unmet() -> None:
    required = covered_target(
        "Table 6 | need: the comparisons | priority: required",
        [structural(chunk(74, 26, "Table 6: …", 900))],
        MISSING,
    )

    selection = select_evidence([chunk(1, 9, "top", 300)], [required], budget=1_000, floor=0.45)

    assert [c.ordinal for c in selection.chunks] == [1]
    assert selection.unmet_required == ["Table 6"]
    assert selection.targets[0]["excluded"] == [
        {"ordinal": 74, "reason": "over the evidence budget"}
    ]
