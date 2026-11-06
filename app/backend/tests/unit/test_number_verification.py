"""AC-26: the numbers in an answer are checked against the original text of the cited pages.

A number counts as verified when the same value (ignoring thousands separators
and a percent sign) appears on one of those pages; a verified number carries
the page and a snippet of the original text; an unverified one is reported.
"""

import uuid

from app.chat.verification import PageText, label_note, numbers_in, verify_numbers

DOC = uuid.uuid4()


def test_numbers_are_read_from_the_answer_without_citations_and_page_references() -> None:
    answer = (
        "LightRAG wins 83.6% in Comprehensiveness and 86.4% in Diversity [1][6]. "
        "GraphRAG needs 610,000 tokens (p. 9) and 1,399 communities [2, 3]; "
        "see arXiv 2410.05779v3 and the 4 datasets, version v3, in 2024."
    )

    assert numbers_in(answer) == [
        "83.6%",
        "86.4%",
        "610,000",
        "1,399",
        "2410.05779",
        "2024",
    ]


def test_repeated_numbers_are_reported_once_in_order_of_appearance() -> None:
    assert numbers_in("67.6% here, 67.6% again, then 32.4%") == ["67.6%", "32.4%"]


def test_small_integers_without_a_decimal_or_percent_are_not_checked() -> None:
    # "4 datasets" is usually written as "four" in the text; "Table 2" is a label.
    assert numbers_in("Table 2 lists the 4 datasets; 5% is a share; 0.45 a threshold") == [
        "5%",
        "0.45",
    ]


def test_a_number_found_on_a_cited_page_is_verified_with_a_snippet() -> None:
    pages = [
        PageText(DOC, 7, "Comprehensiveness 32.4% 67.6% 38.4% 61.6% 16.4% 83.6%"),
        PageText(DOC, 9, "a total token consumption of 610,000 tokens (610 communities)"),
    ]

    result = verify_numbers("LightRAG wins 83.6% [1] and GraphRAG uses 610,000 tokens [2].", pages)

    assert result.unverified == []
    assert [(v.number, v.document_id, v.page) for v in result.verified] == [
        ("83.6%", DOC, 7),
        ("610,000", DOC, 9),
    ]
    assert "83.6%" in result.verified[0].snippet
    assert "610,000 tokens" in result.verified[1].snippet


def test_thousands_separators_and_percent_signs_do_not_matter() -> None:
    pages = [PageText(DOC, 1, "610000 tokens and a 83.6 win rate; 2017886 tokens")]

    result = verify_numbers("610,000 tokens, 83.6%, and 2,017,886 tokens", pages)

    assert result.unverified == []
    assert [v.number for v in result.verified] == ["610,000", "83.6%", "2,017,886"]


def test_a_number_missing_from_the_cited_pages_is_reported() -> None:
    pages = [PageText(DOC, 7, "Agriculture 2,017,886 tokens; CS 2,306,535; Legal 5,081,069")]

    result = verify_numbers(
        "The datasets range from 600,000 to 5,000,000 tokens; Legal has 5,081,069 [1].", pages
    )

    assert result.unverified == ["600,000", "5,000,000"]
    assert [v.number for v in result.verified] == ["5,081,069"]


def test_a_different_value_that_shares_digits_is_not_a_match() -> None:
    pages = [PageText(DOC, 1, "win rate 83.6% and 1,836 cases")]

    result = verify_numbers("83.60% and 83% and 836", pages)

    assert result.unverified == ["83.60%", "83%", "836"]


def test_an_answer_without_numbers_verifies_nothing() -> None:
    result = verify_numbers("LightRAG builds a graph [1].", [PageText(DOC, 1, "graph 2024")])
    assert (result.verified, result.unverified) == ([], [])


# --- Labels: a figure from a table must be attributed as the table attributes it ------
#
# The pages hold the table as the chunker rewrote it, one row per line with every
# figure next to its labels. The model may copy a figure correctly and still put it
# under the wrong metric or variant (D64); the check compares the labels nearest to
# the figure in its sentence with the labels of the cells holding that value.

TABLE_PAGE = PageText(
    DOC,
    8,
    "Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference.\n"
    "Agriculture CS Legal Mix\n"
    "NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG\n"
    "Comprehensiveness — Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; CS: NaiveRAG 38.4%, "
    "LightRAG 61.6%; Legal: NaiveRAG 16.4%, LightRAG 83.6%; Mix: NaiveRAG 38.8%, LightRAG 61.2%\n"
    "Overall — Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; CS: NaiveRAG 38.8%, LightRAG 61.2%; "
    "Legal: NaiveRAG 15.2%, LightRAG 84.8%; Mix: NaiveRAG 40.0%, LightRAG 60.0%\n"
    "NaiveRAG -High NaiveRAG -High NaiveRAG -High NaiveRAG -High\n"
    "Comprehensiveness — Agriculture: NaiveRAG 34.8%, -High 65.2%; CS: NaiveRAG 42.8%, "
    "-High 57.2%; Legal: NaiveRAG 23.6%, -High 76.4%; Mix: NaiveRAG 40.4%, -High 59.6%\n"
    "Overall — Agriculture: NaiveRAG 35.2%, -High 64.8%; CS: NaiveRAG 44.0%, -High 56.0%; "
    "Legal: NaiveRAG 22.0%, -High 78.0%; Mix: NaiveRAG 42.4%, -High 57.6%\n"
    "The -High variant removes high-order retrieval.",
)


def test_a_figure_put_under_the_wrong_metric_is_reported_with_both_sets_of_labels() -> None:
    answer = (
        "Removing high-level retrieval hurts. In the Mix dataset, the Overall score "
        "decreases from 60.0% (LightRAG) to 59.6% (-High) [1]."
    )

    result = verify_numbers(answer, [TABLE_PAGE])

    assert result.unverified == []  # both figures are on the page...
    [wrong] = result.mislabelled  # ...but 59.6% is the -High Comprehensiveness figure
    assert wrong.number == "59.6%"
    assert wrong.answer_labels == ["Overall", "Mix", "-High"]
    assert wrong.source_labels == [["Comprehensiveness", "Mix", "-High"]]
    assert wrong.sentence.startswith("In the Mix dataset, the Overall score")


def test_figures_attributed_as_the_table_attributes_them_pass() -> None:
    answer = (
        "For example, in the Agriculture dataset, the Comprehensiveness score drops from "
        "67.6% (LightRAG) to 65.2% (LightRAG -High), and in the Mix dataset the Overall "
        "score goes from 60.0% to 57.6% [1]."
    )

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_the_label_nearest_to_the_figure_counts_and_case_does_not_matter() -> None:
    # "LightRAG" is mentioned, but "-High" stands next to the figure; "overall" is lower case.
    answer = "LightRAG keeps its lead: the overall win rate in Mix is 57.6% for -High [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_a_value_that_several_cells_share_passes_when_any_of_them_fits() -> None:
    # 67.6% is LightRAG's figure for Comprehensiveness and for Overall in Agriculture.
    answer = "In Agriculture, LightRAG reaches 67.6% in Comprehensiveness and 67.6% Overall [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_a_sentence_that_names_no_labels_is_not_checked_for_them() -> None:
    assert verify_numbers("Scores range from 32.4% to 84.8% [1].", [TABLE_PAGE]).mislabelled == []


def test_a_wrong_variant_is_reported_even_when_metric_and_dataset_are_right() -> None:
    answer = "In Legal, Comprehensiveness is 83.6% for the -High variant [1]."

    [wrong] = verify_numbers(answer, [TABLE_PAGE]).mislabelled

    assert wrong.answer_labels == ["Comprehensiveness", "Legal", "-High"]
    assert wrong.source_labels == [["Comprehensiveness", "Legal", "LightRAG"]]


def test_a_possessive_and_a_comparison_bind_each_figure_to_its_own_side() -> None:
    # Real answers (D64): "compared to NaiveRAG's 34.8%" must not hand NaiveRAG to 65.2%.
    answer = (
        "For Agriculture, the -High variant achieves 65.2% in Comprehensiveness, compared "
        "to NaiveRAG's 34.8% [1]. In Mix, its Overall score is 57.6% versus 60.0% for LightRAG."
    )

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_in_a_list_of_figures_a_label_after_a_comma_belongs_to_the_next_figure() -> None:
    answer = (
        "In Agriculture, LightRAG achieves 67.6% comprehensiveness, 67.6% overall; "
        "NaiveRAG 32.4%, LightRAG 67.6% in Comprehensiveness [1]."
    )

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_numbers_that_are_not_table_cells_are_left_to_the_page_check() -> None:
    pages = [TABLE_PAGE, PageText(DOC, 9, "a total of 610,000 tokens for 610 communities")]

    result = verify_numbers("GraphRAG spends 610,000 tokens Overall in Legal [2].", pages)

    assert result.mislabelled == [] and result.unverified == []


def test_the_label_note_names_each_figure_with_the_labels_from_both_sides() -> None:
    [wrong] = verify_numbers(
        "In the Mix dataset, the Overall score is 59.6% (-High) [1].", [TABLE_PAGE]
    ).mislabelled

    assert label_note([wrong], "other") == (
        "Figures whose labels differ from the source table: "
        "59.6% (answer: Overall, Mix, -High; source: Comprehensiveness, Mix, -High)."
    )
    assert label_note([wrong], "zh") == (
        "以下數字的標籤與原文表格不符：59.6%（答案：Overall、Mix、-High；原文：Comprehensiveness、Mix、-High）。"
    )
