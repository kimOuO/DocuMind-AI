"""D75: fact verification of comparisons and deterministic correction — the parts without
a model or a database.

Three things are told apart: the numeric ordering of two figures (arithmetic, needs no
definition), the orientation of a metric (which way is better: stated in the sources, or
unknown) and a performance conclusion (needs the orientation). Method aliases come from
the definition sentences of the sources. A fault with one clear reading in the table is
corrected in place; one without is removed; a correct sentence is never touched.
"""

import uuid

from app.chat.correction import correct, strip_step_numbering
from app.chat.evidence import (
    build_matrix,
    check_directions,
    matrix_cells_of_pages,
    method_aliases,
    method_definitions,
)
from app.chat.verification import PageText, verify_numbers
from app.retrieval.repository import RetrievedChunk

DOC = uuid.uuid4()

# Win rates stated in the caption: orientation known (higher is better).
WIN_RATES = (
    "Table 1: Win rates (%) of the baselines v.s. Full across two datasets.\n"
    "Agri Mix\n"
    "Naive Full Naive Full\n"
    "Overall — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 40.0%, Full 60.0%\n"
    "Other Full Other Full\n"
    "Overall — Agri: Other 45.2%, Full 54.8%; Mix: Other 50.4%, Full 49.6%\n"
)
# The same shape without the word: complementary pairs, orientation not stated.
ABLATION = (
    "Table 2: Performance of the variants, using Naive as reference.\n"
    "Agri Mix\n"
    "Naive Full Naive Full\n"
    "Comprehensiveness — Agri: Naive 32.4%, Full 67.6%; Mix: Naive 38.8%, Full 61.2%\n"
    "Diversity — Agri: Naive 23.6%, Full 76.4%; Mix: Naive 32.4%, Full 67.6%\n"
    "Naive -High Naive -High\n"
    "Comprehensiveness — Agri: Naive 34.8%, -High 65.2%; Mix: Naive 40.4%, -High 59.6%\n"
    "Diversity — Agri: Naive 27.2%, -High 72.8%; Mix: Naive 36.0%, -High 64.0%\n"
    "Naive -Low Naive -Low\n"
    "Comprehensiveness — Agri: Naive 36.0%, -Low 64.0%; Mix: Naive 36.0%, -Low 64.0%\n"
    "Diversity — Agri: Naive 28.0%, -Low 72.0%; Mix: Naive 33.2%, -Low 66.8%\n"
)
# Not percentages that pair up: counts.
COUNTS = (
    "Table 3: Number of context units and tokens for each condition.\n"
    "Podcast News\n"
    "Units Tokens Units Tokens\n"
    "C0 — Podcast: Units 34, Tokens 26,657; News: Units 55, Tokens 39,770\n"
    "TS — Podcast: Units 1,669, Tokens 1,014,611; News: Units 3,197, Tokens 1,707,694\n"
)
DISCUSSION = (
    "Low-level-only retrieval: the -High variant removes high-level retrieval and keeps "
    "the low level. High-level-only retrieval: the -Low variant removes low-level retrieval."
)
STATED = "We report win rates: the share of questions on which a method's answer was preferred."


def chunk(ordinal: int, page: int, text: str) -> RetrievedChunk:
    return RetrievedChunk(
        uuid.uuid4(), DOC, "paper.pdf", page, ordinal, text, 100, 0.5, "retrieval"
    )


def pages(*texts: str, page: int = 8) -> list[PageText]:
    return [PageText(DOC, page, "\n".join(texts))]


ALIASES = method_aliases(
    method_definitions([(2, chunk(24, 8, DISCUSSION))], methods=["Full", "-High", "-Low", "Naive"])
)


# --- orientation -----------------------------------------------------------------------


def test_orientation_comes_from_the_caption_or_stays_unknown_even_for_complementary_pairs() -> None:
    stated = build_matrix([(1, chunk(20, 7, WIN_RATES))])
    assert {c.direction for c in stated} == {"higher"} and {c.direction_basis for c in stated} == {
        "caption"
    }

    pairs_only = build_matrix([(1, chunk(23, 8, ABLATION))])
    assert {c.direction for c in pairs_only} == {"unknown"}
    assert all(
        c.complementary for c in pairs_only
    )  # the auxiliary signal is recorded, not acted on

    counts = build_matrix([(1, chunk(30, 10, COUNTS))])
    assert {c.direction for c in counts} == {"unknown"} and not any(c.complementary for c in counts)


def test_complementary_pairs_plus_a_metric_stated_in_the_sources_give_an_inferred_orientation() -> (
    None
):
    cells = build_matrix([(1, chunk(23, 8, ABLATION)), (2, chunk(24, 8, STATED))])

    assert {c.direction for c in cells} == {"higher"}
    assert {c.direction_basis for c in cells} == {
        "complementary shares; metric stated in the sources"
    }


# --- ordering versus performance -------------------------------------------------------


def test_a_wrong_ordering_word_is_inconsistent_whatever_the_orientation() -> None:
    answer = "In Mix, Comprehensiveness drops from 61.2% for Full to 64.0% for -Low [1]."

    [issue] = check_directions(answer, pages(ABLATION))

    assert (issue.kind, issue.status) == ("ordering", "inconsistent")
    assert issue.cue == "drops"


def test_a_performance_word_needs_the_orientation_and_is_uncertain_without_it() -> None:
    uncertain = check_directions(
        "In Agri, -Low 64.0% is worse than Full 67.6% [1].", pages(ABLATION)
    )
    assert [(i.kind, i.status) for i in uncertain] == [("performance", "uncertain")]

    known = check_directions(
        "In Mix, Full 49.6% outperforms Other 50.4% in Overall [1].", pages(WIN_RATES, page=7)
    )
    assert [(i.kind, i.status) for i in known] == [("performance", "inconsistent")]


def test_a_cue_before_a_parenthesised_pair_reads_as_a_change_from_the_first_to_the_second() -> None:
    page = pages(ABLATION)
    assert check_directions("Diversity drops in Agri (76.4% vs 72.8%) for -High [1].", page) == []
    [issue] = check_directions("Diversity drops in Mix (32.4% vs 67.6%) for Full [1].", page)
    assert issue.status == "inconsistent" and issue.kind == "ordering"


def test_two_comparisons_in_one_sentence_are_each_checked() -> None:
    answer = (
        "In Agri, Full 67.6% is higher than -High 65.2% in Comprehensiveness, "
        "and -Low 72.0% is higher than -High 72.8% in Diversity [1]."
    )

    issues = check_directions(answer, pages(ABLATION))

    assert [(i.left, i.right, i.status) for i in issues] == [("72.0%", "72.8%", "inconsistent")]


# --- aliases -----------------------------------------------------------------------------


def test_a_method_is_recognised_by_the_operation_its_definition_states() -> None:
    assert sorted(ALIASES) == ["-High", "-Low"]
    assert ALIASES["-High"][0].search("a variant removing high-level retrieval") is not None
    assert ALIASES["-High"][0].search("removes the high level") is None

    answer = (
        "The variant removing high-level retrieval reaches 34.8% in Agri Comprehensiveness [1]."
    )
    check = verify_numbers(answer, pages(ABLATION), aliases=ALIASES)
    assert [m.number for m in check.mislabelled] == ["34.8%"]  # that is Naive's figure, not -High's


# --- correction --------------------------------------------------------------------------


def test_a_correct_number_under_the_wrong_subject_gets_the_subjects_own_figure() -> None:
    """Case 6 of the brief: a summary gives another method's figure as this method's.
    With the method, metric and dataset all stated, the cell is unique, so the figure is
    replaced — never invented."""
    text = (
        "Ablation studies confirm the design, with the variant removing high-level retrieval "
        "showing a significant drop in comprehensiveness (34.8% vs. 67.6%) in Agri."
    )

    result = correct(text, pages(ABLATION), aliases=ALIASES)

    assert "(65.2% vs. 67.6%)" in result.text
    assert [(e["kind"], e["before"], e["after"]) for e in result.edits] == [
        ("figure", "34.8%", "65.2%")
    ]
    assert result.remaining == [] and result.removed == []


def test_a_correct_number_credited_to_the_wrong_method_gets_the_methods_name_fixed() -> None:
    """Case 1: the figure is right, the subject is wrong; the table has it under exactly one
    other method of the same row and group."""
    text = "In Agri, Full has 67.6% in Comprehensiveness versus 32.4% for Other [1]."

    result = correct(text, pages(ABLATION), aliases=ALIASES)

    assert result.text == "In Agri, Full has 67.6% in Comprehensiveness versus 32.4% for Naive [1]."
    assert [(e["kind"], e["before"], e["after"]) for e in result.edits] == [
        ("label", "Other", "Naive")
    ]


def test_a_wrong_comparator_is_fixed_the_same_way() -> None:
    text = "Full reaches 67.6% in Agri Comprehensiveness against -High [1]."

    result = correct(text, pages(ABLATION), aliases=ALIASES)

    assert result.text == "Full reaches 67.6% in Agri Comprehensiveness against Naive [1]."


def test_a_wrong_ordering_word_is_replaced_by_its_antonym() -> None:
    text = "In Mix, Comprehensiveness drops from 61.2% for Full to 64.0% for -Low [1]."

    result = correct(text, pages(ABLATION), aliases=ALIASES)

    assert (
        result.text == "In Mix, Comprehensiveness rises from 61.2% for Full to 64.0% for -Low [1]."
    )
    assert [(e["kind"], e["before"], e["after"]) for e in result.edits] == [
        ("ordering", "drops", "rises")
    ]


def test_a_wrong_performance_word_is_replaced_only_when_the_orientation_is_known() -> None:
    known = correct(
        "In Mix, Full 49.6% outperforms Other 50.4% in Overall [1].", pages(WIN_RATES, page=7)
    )
    assert known.text == "In Mix, Full 49.6% underperforms Other 50.4% in Overall [1]."

    unknown = correct(
        "In Agri, -Low 64.0% is worse than Full 67.6% [1].", pages(ABLATION), aliases=ALIASES
    )
    assert unknown.text == "In Agri, -Low 64.0% is worse than Full 67.6% [1]."
    assert unknown.edits == [] and [i.status for i in unknown.uncertain] == ["uncertain"]


def test_a_figure_with_no_single_reading_is_removed_with_its_parenthesis_not_invented() -> None:
    # 99.9% is in no cell; the subject is given, but the table has no such figure to swap in
    # and no cell to take the value from under another method. Inside parentheses: the
    # parenthesis goes; the sentence stays.
    text = "Full leads in Agri Comprehensiveness (99.9% vs. 32.4%) and in Mix [1]."

    result = correct(text, pages(ABLATION), aliases=ALIASES, unverified=["99.9%"])

    assert result.text == "Full leads in Agri Comprehensiveness and in Mix [1]."
    assert result.removed == ["(99.9% vs. 32.4%)"]


def test_correct_sentences_are_left_exactly_as_they_are() -> None:
    text = (
        "In Agri, Full 67.6% is higher than -High 65.2% in Comprehensiveness [1]. "
        "Diversity falls from 76.4% for Full to 72.8% for -High in Agri [1]. "
        "C0 uses 34 Units on Podcast [2]."
    )

    result = correct(text, pages(ABLATION, COUNTS), aliases=ALIASES)

    assert result.text == text and result.edits == [] and result.removed == []


def test_without_table_cells_nothing_is_corrected() -> None:
    text = "C2 reached 77.76 against SS at 22.24 on Podcast [1]."
    result = correct(text, [PageText(DOC, 26, "prose: C2 SS 77.76 22.24 -8.17 <0.001")])
    assert (
        result.text == text
        and result.edits == []
        and matrix_cells_of_pages(result_pages := [PageText(DOC, 26, "prose")]) == []
    )
    assert result_pages


def test_the_analysts_step_numbering_is_stripped_from_the_answer() -> None:
    text = (
        "(1) The question asks for a comparison.\n\n(2) Method definitions: none.\n\n"
        "(3) Full 67.6% against Naive 32.4% [1].\n\nIn conclusion, Full leads [1]."
    )

    assert strip_step_numbering(text) == (
        "The question asks for a comparison.\n\nMethod definitions: none.\n\n"
        "Full 67.6% against Naive 32.4% [1].\n\nIn conclusion, Full leads [1]."
    )
    # A single parenthesised number is not a step list.
    assert strip_step_numbering("(1) is the first equation.") == "(1) is the first equation."
