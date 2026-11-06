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
    assert "-High [2]: Low-level-only retrieval: the -High variant removes" in preamble
    assert "Full: no definition found in the sources" in preamble
    assert "same dataset, the same metric and the same pairing" in preamble
    assert (
        preamble.index("matrix")
        < preamble.index("Method definitions")
        < preamble.index("Answer in this order")
    )
    # Without any table there is no matrix and the Analyst is told so.
    plain = analysis_preamble([], [], WordCounter(), budget=600)
    assert "No structured table data" in plain


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


def test_naming_every_variant_without_one_shared_condition_is_incomplete() -> None:
    answer = (
        "Full reaches 67.6% in Agri Overall; -High 59.6% and -Low 64.0% in Mix "
        "Comprehensiveness [1]."
    )

    result = check_completeness("Performance of the ablated variants of Full", answer, pages(TABLE))

    assert result.status == "incomplete"
    assert result.condition is None
    assert "Full" not in result.missing  # named with a figure, but never in one condition


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
