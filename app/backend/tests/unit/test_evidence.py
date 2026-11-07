"""D74: structured evidence analysis — the parts without a model or a database.

The Evidence Matrix is read from the table chunks the chunker already rewrote cell by
cell (tables.py), so that every figure keeps its dataset, metric, column and the column
it is paired with; method definitions are sentences of the sources that say what a
method does; the Analyst's preamble shows both; and two deterministic checks use the
matrix: the direction of a comparison between two figures, and whether an answer to a
question about variants compares them all under one condition.
"""

import uuid

from app.chat.evidence import (
    Completeness,
    analysis_preamble,
    build_matrix,
    check_completeness,
    check_directions,
    matrix_text,
    method_definitions,
    overall_status,
)
from app.chat.verification import NumberCheck, PageText, verify_numbers
from app.retrieval.repository import RetrievedChunk

DOC = uuid.uuid4()

# A table as the chunker rewrote it: two datasets, each pairing a reference with a
# method; a second block pairs the reference with a variant.
TABLE = (
    "Table 2: Win rates (%) of the variants, using Naive as reference.\n"
    "Agri Mix\n"
    "Naive Full Naive Full\n"
    "Comprehensiveness — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 38.8%, Full 61.2%\n"
    "Overall — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 40.0%, Full 60.0%\n"
    "Naive -High Naive -High\n"
    "Comprehensiveness — Agri: Naive 34.8%, -High 65.2%; Mix: Naive 40.4%, -High 59.6%\n"
    "Overall — Agri: Naive 35.2%, -High 64.8%; Mix: Naive 42.4%, -High 57.6%\n"
    "Naive -Low Naive -Low\n"
    "Comprehensiveness — Agri: Naive 36.0%, -Low 64.0%; Mix: Naive 36.0%, -Low 64.0%\n"
    "Overall — Agri: Naive 34.8%, -Low 65.2%; Mix: Naive 35.2%, -Low 64.8%\n"
)
COUNTS = (
    "Table 2: Number of context units and tokens for each condition.\n"
    "Podcast News\n"
    "Units Tokens Units Tokens\n"
    "C0 — Podcast: Units 34, Tokens 26,657; News: Units 55, Tokens 39,770\n"
    "TS — Podcast: Units 1,669, Tokens 1,014,611; News: Units 3,197, Tokens 1,707,694\n"
)
DISCUSSION = (
    "Low-level-only retrieval: the -High variant removes high-level retrieval and keeps "
    "the low level. High-level-only retrieval: the -Low variant removes low-level "
    "retrieval. The -High variant is slower. We also tried a Mix of both."
)


def chunk(ordinal: int, page: int, text: str, origin: str = "retrieval") -> RetrievedChunk:
    return RetrievedChunk(uuid.uuid4(), DOC, "paper.pdf", page, ordinal, text, 100, 0.5, origin)


def pages(*texts: str) -> list[PageText]:
    return [PageText(DOC, 8, "\n".join(texts))]


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


# --- the matrix ------------------------------------------------------------------------


def test_the_matrix_keeps_every_figure_with_its_dataset_metric_column_and_pairing() -> None:
    cells = build_matrix([(1, chunk(23, 8, TABLE)), (2, chunk(24, 8, DISCUSSION))])

    full = [c for c in cells if c.column == "Full" and c.row == "Overall"]
    assert [(c.group, c.value, c.paired_with, c.block) for c in full] == [
        ("Agri", "67.6%", "Naive", 0),
        ("Mix", "60.0%", "Naive", 0),
    ]
    low = next(c for c in cells if c.column == "-Low" and c.row == "Overall" and c.group == "Mix")
    assert (low.value, low.paired_with, low.block, low.unit) == ("64.8%", "Naive", 2, "%")
    assert {c.table for c in cells} == {"Table 2"}
    assert {c.source_index for c in cells} == {1}  # the discussion holds no cells
    assert {c.page for c in cells} == {8}
    # "win rates": higher is better, read from the caption, not assumed.
    assert {c.direction for c in cells} == {"higher"}
    assert len(cells) == 24


def test_the_reference_is_paired_with_each_column_and_told_apart_by_block() -> None:
    cells = build_matrix([(1, chunk(23, 8, TABLE))])
    reference = [
        c for c in cells if c.column == "Naive" and c.row == "Overall" and c.group == "Agri"
    ]

    assert [(c.value, c.paired_with) for c in reference] == [
        ("32.4%", "Full"),
        ("35.2%", "-High"),
        ("34.8%", "-Low"),
    ]


def test_counts_without_a_known_direction_stay_unknown_and_keep_their_dataset() -> None:
    cells = build_matrix([(3, chunk(30, 10, COUNTS))])

    news_units = [c for c in cells if c.group == "News" and c.column == "Units"]
    assert [(c.row, c.value) for c in news_units] == [("C0", "55"), ("TS", "3,197")]
    assert {c.direction for c in cells} == {"unknown"}
    assert {c.paired_with for c in cells} == {"Tokens", "Units"}  # the two sub-columns pair up
    assert all(c.unit == "" for c in cells)


def test_a_source_that_is_not_a_table_chunk_gives_no_cells() -> None:
    assert build_matrix([(1, chunk(1, 2, DISCUSSION))]) == []
    caption_only = "Table 6: Pairwise comparisons of six conditions.\nResults of tests indicated."
    assert build_matrix([(1, chunk(1, 26, caption_only))]) == []


def test_the_matrix_text_groups_cells_by_table_dataset_and_metric_within_a_budget() -> None:
    cells = build_matrix([(1, chunk(23, 8, TABLE))])

    text, left_out = matrix_text(cells, WordCounter(), budget=400)

    assert "Table 2 [1] (p. 8), higher is better" in text
    assert (
        "Agri / Overall: Naive 32.4% | Full 67.6%; Naive 35.2% | -High 64.8%; "
        "Naive 34.8% | -Low 65.2%"
    ) in text
    assert "Mix / Comprehensiveness:" in text
    assert left_out == []

    short, left_out = matrix_text(cells, WordCounter(), budget=10)
    assert short == "" and left_out == ["Table 2 [1]"]


# --- method definitions ----------------------------------------------------------------


def test_definitions_are_sentences_that_name_a_method_and_an_operation_with_their_source() -> None:
    definitions = method_definitions(
        [(2, chunk(24, 8, DISCUSSION))], methods=["Full", "-High", "-Low", "Naive"]
    )

    assert [(d.method, d.source_index, d.page) for d in definitions] == [
        ("-High", 2, 8),
        ("-Low", 2, 8),
    ]
    assert definitions[0].sentence.startswith("Low-level-only retrieval: the -High variant removes")
    # "The -High variant is slower" names the method but says nothing it removes or keeps.
    assert all("slower" not in d.sentence for d in definitions)
    # A method is never defined from its name alone.
    assert not any(d.method == "Full" for d in definitions)


def test_the_preamble_shows_the_matrix_the_definitions_and_the_order_of_analysis() -> None:
    sources = [(1, chunk(23, 8, TABLE)), (2, chunk(24, 8, DISCUSSION))]
    cells = build_matrix(sources)
    definitions = method_definitions(sources, methods={c.column for c in cells})

    preamble = analysis_preamble(cells, definitions, WordCounter(), budget=600)

    assert "Evidence matrix" in preamble and "Agri / Overall:" in preamble
    # D79: the definitions the program extracted are not shown — they depend on one paper's
    # wording, and a miss used to be announced as "no definition found". The model is sent
    # to the sources' own defining passages instead.
    assert "Method definitions" not in preamble and "no definition found" not in preamble
    assert "-High variant removes" not in preamble
    assert "passages of the sources that define each" in preamble
    assert "same dataset, the same metric and the same pairing" in preamble
    assert preamble.index("matrix") < preamble.index("Answer in this order")
    # Without any table there is no matrix and the Analyst is told so.
    plain = analysis_preamble([], [], WordCounter(), budget=600)
    assert "No structured table data" in plain


def test_the_order_of_analysis_is_the_b3_wording_with_definitions_read_from_the_sources() -> None:
    """D84: the counted-conclusion wording of D79 was reverted after B8 — asked to count
    conditions across separate pairings, the model filled the "lower in" lists with the
    conditions it had won, three runs out of three. B3's steps stay; only step (2) sends the
    model to the sources' defining passages (the extracted definitions are no longer shown)."""
    sources = [(1, chunk(23, 8, TABLE))]
    cells = build_matrix(sources)

    preamble = analysis_preamble(cells, [], WordCounter(), budget=600)

    assert "name the improvements, the regressions and every exception" in preamble
    assert "passages of the sources that define each" in preamble
    assert "how many of the conditions" not in preamble and "in most conditions" not in preamble


def test_tables_too_large_for_the_matrix_are_named_not_called_unreadable() -> None:
    """The Q2 trace of 2026-11-07: both tables exceeded the budget and the Analyst was
    told that no table data could be read, although the sources held two tables. A
    table left out is named, so that the model reads it in the sources."""
    sources = [(1, chunk(23, 8, TABLE))]
    cells = build_matrix(sources)

    preamble = analysis_preamble(cells, [], WordCounter(), budget=10)

    assert "No structured table data" not in preamble
    assert "too large for the matrix" in preamble and "Table 2 [1]" in preamble
    assert "read them in the sources" in preamble


def _four_block_table() -> str:
    """A table of the shape of a paper's main results: four datasets, four metrics, four
    baseline blocks each paired with the same method — 128 cells, rewritten cell by cell
    as the ingestion does (figures are synthetic)."""
    datasets = ["Alpha", "Beta", "Gamma", "Delta"]
    metrics = ["Comprehensiveness", "Diversity", "Empowerment", "Overall"]
    baselines = ["BaseOne", "BaseTwo", "BaseThree", "BaseFour"]
    lines = [
        "Table 9: Win rates (%) of baselines v.s. Method across four datasets and four "
        "evaluation dimensions.",
        " ".join(datasets),
    ]
    value = 20.0
    for baseline in baselines:
        lines.append(" ".join(f"{baseline} Method" for _ in datasets))
        for metric in metrics:
            parts = []
            for dataset in datasets:
                value = 20.0 + ((value * 7.0) % 30.0)
                parts.append(f"{dataset}: {baseline} {value:.1f}%, Method {100 - value:.1f}%")
            lines.append(f"{metric} — " + "; ".join(parts))
    return "\n".join(lines)


def test_a_full_four_block_table_fits_the_matrix_budget_with_the_real_tokenizer() -> None:
    """Measured, not assumed: before 2026-11-07 the budget (900) was below the cost of one
    such table (about 1,350 tokens), so the matrix never reached the model for the
    questions that need it. One full table must fit; two need not."""
    from app.chat.evidence import MATRIX_TOKEN_BUDGET
    from app.llm.tokenizer import Qwen3TokenCounter

    cells = build_matrix([(1, chunk(23, 8, _four_block_table()))])
    assert len(cells) == 128

    text, left_out = matrix_text(cells, Qwen3TokenCounter(), budget=MATRIX_TOKEN_BUDGET)

    assert left_out == [] and text.count("\n") == 16  # the heading and 16 condition rows


# --- the direction check ---------------------------------------------------------------


def test_a_comparison_whose_direction_contradicts_the_figures_is_flagged() -> None:
    answer = "In Mix, Full 60.0% outperforms -Low 64.8% in Overall [1]."

    [issue] = check_directions(answer, pages(TABLE))

    assert issue.status == "inconsistent"
    assert (issue.left, issue.right) == ("60.0%", "64.8%")
    assert "higher is better" in issue.detail


def test_a_comparison_in_the_right_direction_and_a_from_to_drop_are_not_flagged() -> None:
    answer = (
        "In Mix, -Low 64.8% is higher than Full 60.0% in Overall [1]. "
        "In Agri, Comprehensiveness falls from 67.6% for Full to 65.2% for -High [1]."
    )

    assert check_directions(answer, pages(TABLE)) == []


def test_figures_of_different_conditions_are_not_compared_and_said_so() -> None:
    answer = "Full reaches 67.6% in Agri, better than 61.2% in Mix for Comprehensiveness [1]."

    [issue] = check_directions(answer, pages(TABLE))

    assert issue.status == "incomparable" and "Agri" in issue.detail and "Mix" in issue.detail


def test_an_unknown_metric_direction_gives_uncertain_not_an_error() -> None:
    answer = "C0 uses 34 Units on Podcast, better than TS with 1,669 Units [1]."

    [issue] = check_directions(answer, [PageText(DOC, 10, COUNTS)])

    assert issue.status == "uncertain"


def test_sentences_without_two_resolved_figures_or_a_cue_give_no_issue() -> None:
    assert check_directions("Full scores 67.6% in Agri [1].", pages(TABLE)) == []
    assert (
        check_directions("Full 67.6% and -High 65.2% in Agri Comprehensiveness [1].", pages(TABLE))
        == []
    )


# --- completeness ----------------------------------------------------------------------


def test_a_question_about_variants_is_complete_when_one_condition_shows_every_method() -> None:
    answer = (
        "In Agri, Overall: Full 67.6%, -High 64.8%, -Low 65.2% against Naive [1]. "
        "-High removes high-level retrieval [2]."
    )

    result = check_completeness("Performance of the ablated variants of Full", answer, pages(TABLE))

    assert result.status == "complete"
    assert result.required == ["-High", "-Low", "Full"]
    assert result.missing == [] and result.condition == "Agri / Overall"


def test_naming_every_variant_without_one_shared_condition_is_not_complete() -> None:
    """Three variants, two conditions: never one condition with every figure. The check
    cannot tie "-High 59.6%" to a dataset in the list sentence, so D76 leaves the verdict
    uncertain rather than calling the method missing."""
    answer = (
        "Full reaches 67.6% in Agri Overall; -High 59.6% and -Low 64.0% in Mix "
        "Comprehensiveness [1]."
    )

    result = check_completeness("Performance of the ablated variants of Full", answer, pages(TABLE))

    assert result.status == "uncertain"
    assert result.condition is None
    assert result.missing == ["-High"]  # Full and -Low are tied to figures; -High is not


def test_a_variant_left_out_is_named_as_missing() -> None:
    answer = "In Agri Overall, Full 67.6% and -High 64.8% [1]."

    result = check_completeness(
        "How do the ablated variants of Full perform?", answer, pages(TABLE)
    )

    assert result.status == "incomplete" and result.missing == ["-Low"]


def test_completeness_is_not_required_of_questions_that_do_not_ask_for_variants() -> None:
    result = check_completeness("Compare Full with Naive", "Full is better [1].", pages(TABLE))
    assert result.status == "not_applicable"
    # Nor when no table is parsed, even for a question about variants.
    result = check_completeness("the ablated variants", "text", [PageText(DOC, 26, "prose only")])
    assert result.status == "not_applicable"


# --- the overall status ----------------------------------------------------------------


def test_the_overall_status_separates_factual_errors_from_missing_content() -> None:
    page = pages(TABLE)
    complete = Completeness("complete", ["-High", "-Low", "Full"], [], "Agri / Overall")
    incomplete = Completeness("incomplete", ["-High", "-Low", "Full"], ["-Low"], None)
    clean = NumberCheck([], [], [], [], [])
    wrong = verify_numbers("In Mix, Full reaches 64.8% Overall [1].", page)  # -Low's figure

    assert overall_status(clean, [], complete) == "SUPPORTED_AND_COMPLETE"
    assert overall_status(clean, [], incomplete) == "FACTUALLY_CORRECT_BUT_INCOMPLETE"
    assert overall_status(wrong, [], complete) == "FACTUALLY_INCORRECT"
    inconsistent = check_directions(
        "In Mix, Full 60.0% outperforms -Low 64.8% in Overall [1].", page
    )
    assert overall_status(clean, inconsistent, complete) == "FACTUALLY_INCORRECT"
    assert overall_status(clean, [], Completeness("not_applicable", [], [], None)) == "UNCERTAIN"


# --- D76: comparison facts, exception lists and conclusions ---------------------------------

from app.chat.evidence import (  # noqa: E402
    ArithmeticIssue,
    check_arithmetic,
    check_conclusions,
    comparison_facts,
    facts_text,
)

PAIRED = (
    "Table 1: Win rates (%) of the baselines v.s. Full across two datasets.\n"
    "Agri Mix\n"
    "Naive Full Naive Full\n"
    "Comprehensiveness — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 38.8%, Full 61.2%\n"
    "Overall — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 40.0%, Full 60.0%\n"
    "Other Full Other Full\n"
    "Comprehensiveness — Agri: Other 45.6%, Full 54.4%; Mix: Other 50.4%, Full 49.6%\n"
    "Overall — Agri: Other 45.2%, Full 54.8%; Mix: Other 50.4%, Full 49.6%\n"
)


def test_facts_are_built_only_between_cells_of_one_condition_and_carry_their_setting() -> None:
    cells = build_matrix([(1, chunk(20, 7, PAIRED))])

    facts = comparison_facts(cells, "compare Full with Other")

    direct = [f for f in facts if {f.method_a, f.method_b} == {"Full", "Other"}]
    assert len(direct) == 4  # two datasets × two metrics, the direct pairs only
    mix_overall = next(f for f in direct if f.group == "Mix" and f.row == "Overall")
    assert (mix_overall.value_a, mix_overall.value_b, mix_overall.relation) == (
        "49.6%",
        "50.4%",
        "LESS",
    )
    assert mix_overall.setting == "direct pair" and mix_overall.direction == "higher"
    assert mix_overall.better == "Other"
    # Naive and Other were each measured against Full, never against each other: the fact
    # between them is indirect and carries no verdict on which is better.
    indirect = [f for f in facts if {f.method_a, f.method_b} == {"Naive", "Other"}]
    assert indirect and all(f.confidence == "indirect" for f in indirect)
    assert all(f.setting == "each against Full" and f.better is None for f in indirect)


def test_facts_across_blocks_against_one_reference_are_marked_indirect() -> None:
    cells = build_matrix([(1, chunk(23, 8, TABLE))])

    facts = comparison_facts(cells, "the ablated variants of Full")

    full_vs_high = next(
        f
        for f in facts
        if {f.method_a, f.method_b} == {"Full", "-High"}
        and f.group == "Agri"
        and f.row == "Overall"
    )
    assert full_vs_high.setting == "each against Naive"
    assert full_vs_high.confidence == "indirect"
    assert (
        full_vs_high.direction == "higher" and full_vs_high.better is None
    )  # indirect: no verdict
    assert full_vs_high.relation == "GREATER"  # 67.6 against 64.8: the numbers, not a verdict


def test_the_facts_text_summarises_each_pair_with_its_exceptions_and_limits() -> None:
    cells = build_matrix([(1, chunk(20, 7, PAIRED))])
    facts = comparison_facts(cells, "compare Full with Other")

    text = facts_text(facts, WordCounter(), budget=300)

    assert "Full vs Other" in text
    assert "higher in 2 of 4" in text and "lower in 2" in text
    assert "Mix / Comprehensiveness: 49.6% vs 50.4%" in text
    assert "Mix / Overall: 49.6% vs 50.4%" in text
    assert "direct pair" in text


def test_an_only_exception_claim_is_contradicted_when_the_facts_hold_more() -> None:
    cells = build_matrix([(1, chunk(20, 7, PAIRED))])
    facts = comparison_facts(cells, "compare Full with Other")
    answer = (
        "Full is ahead of Other in most cells. The only exception is Mix in Overall, where "
        "Other is slightly higher [1]."
    )

    [issue] = check_conclusions(answer, facts)

    assert issue.status == "contradicted"
    assert "2 conditions" in issue.detail and "Mix / Comprehensiveness" in issue.detail


def test_a_correct_exception_list_and_a_hedged_conclusion_raise_nothing() -> None:
    cells = build_matrix([(1, chunk(20, 7, PAIRED))])
    facts = comparison_facts(cells, "compare Full with Other")
    answer = (
        "Full is ahead of Other in Agri; in Mix, Other is higher in Comprehensiveness and "
        "Overall [1]. Full leads in most conditions [1]."
    )

    assert check_conclusions(answer, facts) == []


# --- D76: completeness by structured coverage -------------------------------------------


def test_a_figure_that_only_coincides_with_the_full_methods_value_does_not_make_it_complete() -> (
    None
):
    """B4-Q3-2: -Origin's 83.6% equals Full's 83.6% under Legal / Comprehensiveness; the
    answer never gives Full's own figure. Coverage is read from labelled figures, not from
    numbers that happen to appear."""
    table = (
        "Table 2: Performance of the variants, using Naive as reference.\n"
        "Legal\nNaive Full\n"
        "Comprehensiveness — Legal: Naive 16.4%, Full 83.6%\n"
        "Naive -High\n"
        "Comprehensiveness — Legal: Naive 23.6%, -High 76.4%\n"
        "Naive -Origin\n"
        "Comprehensiveness — Legal: Naive 16.4%, -Origin 83.6%\n"
    )
    answer = "In Legal Comprehensiveness, -High reaches 76.4% and -Origin 83.6% against Naive [1]."

    result = check_completeness("Performance of the ablated variants of Full", answer, pages(table))

    assert result.status == "incomplete" and result.missing == ["Full"]


def test_completeness_is_uncertain_when_the_figures_cannot_be_tied_to_their_methods() -> None:
    table = (
        "Table 2: Performance of the variants, using Naive as reference.\n"
        "Legal\nNaive Full\n"
        "Comprehensiveness — Legal: Naive 16.4%, Full 83.6%\n"
        "Naive -High\n"
        "Comprehensiveness — Legal: Naive 23.6%, -High 76.4%\n"
        "Naive -Origin\n"
        "Comprehensiveness — Legal: Naive 16.4%, -Origin 83.6%\n"
    )
    answer = (
        "The variants Full, -High and -Origin reach 83.6%, 76.4% and 83.6% in Legal "
        "Comprehensiveness [1]."
    )

    result = check_completeness("Performance of the ablated variants of Full", answer, pages(table))

    assert result.status == "uncertain"


# --- D76: derived arithmetic ---------------------------------------------------------------


def test_a_stated_ratio_is_checked_against_the_two_figures_it_is_derived_from() -> None:
    page = [PageText(DOC, 10, COUNTS)]
    wrong = "On Podcast, C0 uses 34 Units while TS uses 1,669: C0 uses 9x fewer units [1]."
    right = "On Podcast, TS uses 49.09 times more Units than C0 (1,669 against 34) [1]."

    [issue] = check_arithmetic(wrong, page)
    assert isinstance(issue, ArithmeticIssue)
    assert (
        issue.status == "inconsistent" and issue.stated == "9x" and abs(issue.computed - 49.1) < 0.1
    )
    assert check_arithmetic(right, page) == []


def test_a_ratio_without_two_base_figures_in_the_sentence_is_unchecked_not_wrong() -> None:
    page = [PageText(DOC, 10, COUNTS)]
    [issue] = check_arithmetic("C0 uses about 38x fewer tokens than TS on Podcast [1].", page)
    assert issue.status == "unchecked"
