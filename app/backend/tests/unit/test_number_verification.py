"""AC-26: the numbers in an answer are checked against the original text of the cited pages.

A number counts as verified when the same value (ignoring thousands separators
and a percent sign) appears on one of those pages; a verified number carries
the page and a snippet of the original text; an unverified one is reported.
"""

import uuid

from app.chat.verification import (
    PageText,
    claim_note,
    label_note,
    numbers_in,
    verify_numbers,
)

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
    "Diversity — Agriculture: NaiveRAG 27.2%, -High 72.8%; CS: NaiveRAG 36.8%, -High 63.2%; "
    "Legal: NaiveRAG 16.8%, -High 83.2%; Mix: NaiveRAG 36.0%, -High 64.0%\n"
    "Overall — Agriculture: NaiveRAG 35.2%, -High 64.8%; CS: NaiveRAG 44.0%, -High 56.0%; "
    "Legal: NaiveRAG 22.0%, -High 78.0%; Mix: NaiveRAG 42.4%, -High 57.6%\n"
    "NaiveRAG -Low NaiveRAG -Low NaiveRAG -Low NaiveRAG -Low\n"
    "Diversity — Agriculture: NaiveRAG 28.0%, -Low 72.0%; CS: NaiveRAG 39.6%, -Low 60.4%; "
    "Legal: NaiveRAG 13.6%, -Low 86.4%; Mix: NaiveRAG 33.2%, -Low 66.8%\n"
    "NaiveRAG -Origin NaiveRAG -Origin NaiveRAG -Origin NaiveRAG -Origin\n"
    "Comprehensiveness — Agriculture: NaiveRAG 24.8%, -Origin 75.2%; CS: NaiveRAG 39.2%, "
    "-Origin 60.8%; Legal: NaiveRAG 16.4%, -Origin 83.6%; Mix: NaiveRAG 44.4%, -Origin 55.6%\n"
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
    assert wrong.source_labels == [["Comprehensiveness", "Mix", "-High", "vs NaiveRAG"]]
    assert wrong.sentence.startswith("In the Mix dataset, the Overall score")


def test_figures_attributed_as_the_table_attributes_them_pass() -> None:
    answer = (
        "For example, in the Agriculture dataset, the Comprehensiveness score drops from "
        "67.6% (LightRAG) to 65.2% (LightRAG -High), and in the Mix dataset the Overall "
        "score goes from 60.0% to 57.6% [1]."
    )

    assert verify_numbers(answer, [TABLE_PAGE]).mislabelled == []


def test_the_label_attached_to_the_figure_counts_and_case_does_not_matter() -> None:
    # "LightRAG" is mentioned, but "-High" is written with the figure; "overall" is lower case.
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
    assert wrong.source_labels == [
        ["Comprehensiveness", "Legal", "LightRAG", "vs NaiveRAG"],
        ["Comprehensiveness", "Legal", "-Origin", "vs NaiveRAG"],
    ]


def test_a_possessive_and_a_comparison_bind_each_figure_to_its_own_side() -> None:
    # Real answers (D64): "compared to NaiveRAG's 34.8%" must not hand NaiveRAG to 65.2%.
    answer = (
        "For Agriculture, the -High variant achieves 65.2% in Comprehensiveness, compared "
        "to NaiveRAG's 34.8% [1]. In Mix, its Overall score is 57.6% versus 60.0% for LightRAG."
    )

    result = verify_numbers(answer, [TABLE_PAGE])

    assert result.mislabelled == []
    # "its Overall score is 57.6%" names no method: the figure fits -High's cell, but the
    # answer does not say so, and the check does not guess (D67).
    assert [(u.number, u.reason) for u in result.unresolved] == [("57.6%", "missing")]


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
        "59.6% (answer: Overall, Mix, -High; source: Comprehensiveness, Mix, -High, vs NaiveRAG)."
    )
    assert label_note([wrong], "zh") == (
        "以下數字的標籤與原文表格不符：59.6%（答案：Overall、Mix、-High；"
        "原文：Comprehensiveness、Mix、-High、vs NaiveRAG）。"
    )


# --- D67: claims with roles, and three outcomes ---------------------------------------
#
# Table 1 of the paper as the chunker rewrites it (two of its four blocks). Every row
# group pairs a baseline with LightRAG, so each cell has a comparator: the other cell.
# A figure in the answer is a claim about a method, against a comparator, on a dataset
# and a metric. The claim is SUPPORTED when every label it gives fits one cell holding
# the value, CONTRADICTED when no cell fits the labels it gives, and UNRESOLVED when the
# labels it gives fit cells but leave out a category, or are ambiguous. Nothing is
# guessed from distance.

TABLE1_PAGE = PageText(
    DOC,
    7,
    "Table 1: Win rates (%) of baselines v.s. LightRAG across four datasets and four "
    "evaluation dimensions.\n"
    "Agriculture CS Legal Mix\n"
    "NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG NaiveRAG LightRAG\n"
    "Comprehensiveness — Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; CS: NaiveRAG 38.4%, "
    "LightRAG 61.6%; Legal: NaiveRAG 16.4%, LightRAG 83.6%; Mix: NaiveRAG 38.8%, LightRAG 61.2%\n"
    "Diversity — Agriculture: NaiveRAG 23.6%, LightRAG 76.4%; CS: NaiveRAG 38.0%, "
    "LightRAG 62.0%; Legal: NaiveRAG 13.6%, LightRAG 86.4%; Mix: NaiveRAG 32.4%, LightRAG 67.6%\n"
    "Empowerment — Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; CS: NaiveRAG 38.8%, "
    "LightRAG 61.2%; Legal: NaiveRAG 16.4%, LightRAG 83.6%; Mix: NaiveRAG 42.8%, LightRAG 57.2%\n"
    "GraphRAG LightRAG GraphRAG LightRAG GraphRAG LightRAG GraphRAG LightRAG\n"
    "Comprehensiveness — Agriculture: GraphRAG 45.6%, LightRAG 54.4%; CS: GraphRAG 48.4%, "
    "LightRAG 51.6%; Legal: GraphRAG 48.4%, LightRAG 51.6%; Mix: GraphRAG 50.4%, LightRAG 49.6%\n"
    "Diversity — Agriculture: GraphRAG 22.8%, LightRAG 77.2%; CS: GraphRAG 40.8%, "
    "LightRAG 59.2%; Legal: GraphRAG 26.4%, LightRAG 73.6%; Mix: GraphRAG 36.0%, LightRAG 64.0%\n"
    "LightRAG consistently outperforms GraphRAG.",
)
PAGES = [TABLE1_PAGE, TABLE_PAGE]


def outcomes(answer: str) -> tuple[list[str], list[tuple[str, str]]]:
    result = verify_numbers(answer, PAGES)
    return [m.number for m in result.mislabelled], [(u.number, u.reason) for u in result.unresolved]


def test_the_method_after_a_comparison_word_is_the_comparator_not_the_owner() -> None:
    # The real false positive (D66 retest): NaiveRAG stands nearest to 86.4%, but
    # "win rate over NaiveRAG" makes it the comparator; the figures are LightRAG's.
    answer = (
        "For example, in the Legal dataset, LightRAG achieved 83.6% win rate over NaiveRAG "
        "in Comprehensiveness, 86.4% in Diversity, and 83.6% in Empowerment [6]."
    )

    assert outcomes(answer) == ([], [])


def test_a_figure_claimed_for_the_wrong_side_of_the_comparison_is_contradicted() -> None:
    [wrong] = verify_numbers(
        "NaiveRAG achieved 86.4% over LightRAG in Legal Diversity [1].", PAGES
    ).mislabelled

    assert wrong.answer_labels == ["Diversity", "Legal", "NaiveRAG", "vs LightRAG"]
    assert wrong.source_labels == [
        ["Diversity", "Legal", "LightRAG", "vs NaiveRAG"],
        ["Diversity", "Legal", "-Low", "vs NaiveRAG"],
    ]


def test_a_figure_from_another_dataset_is_contradicted_when_the_dataset_is_named() -> None:
    assert outcomes("LightRAG achieved 64.0% in Legal Diversity against GraphRAG [1].") == (
        ["64.0%"],
        [],
    )
    assert outcomes("LightRAG achieved 64.0% in Mix Diversity against GraphRAG [1].") == ([], [])


def test_the_same_dataset_is_inherited_from_the_previous_sentence() -> None:
    # The real false negative (D66 retest): "the same dataset" is Legal, where the
    # Diversity figure against GraphRAG is 73.6%; 64.0% is Mix's.
    answer = (
        "In the Legal dataset, LightRAG achieved 83.6% win rate over NaiveRAG in "
        "Comprehensiveness [6]. Against GraphRAG, LightRAG achieved 51.6% win rate in "
        "Comprehensiveness and 64.0% in Diversity in the same dataset [6]."
    )

    [wrong] = verify_numbers(answer, PAGES).mislabelled

    assert wrong.number == "64.0%"
    assert wrong.answer_labels == ["Diversity", "Legal", "LightRAG", "vs GraphRAG"]


def test_a_pronoun_does_not_carry_a_dataset_over_so_the_figure_stays_unresolved() -> None:
    answer = "In Legal, LightRAG outperformed GraphRAG [1]. Its Diversity win rate was 64.0% [1]."

    assert outcomes(answer) == ([], [("64.0%", "missing")])


def test_a_figure_with_too_few_labels_to_pin_a_cell_is_unresolved_not_supported() -> None:
    assert outcomes("The Diversity win rate was 64.0% [1].") == ([], [("64.0%", "missing")])
    # Dataset missing: 51.6% fits both CS and Legal against GraphRAG.
    assert outcomes("LightRAG achieved 51.6% in Comprehensiveness against GraphRAG [1].") == (
        [],
        [("51.6%", "missing")],
    )


def test_two_metrics_and_two_figures_against_one_comparator_are_both_supported() -> None:
    answer = (
        "LightRAG achieved 83.6% in Comprehensiveness and 86.4% in Diversity in Legal "
        "against NaiveRAG [1]."
    )

    assert outcomes(answer) == ([], [])


def test_every_comparison_wording_marks_the_comparator() -> None:
    for wording in ("over", "against", "than", "versus", "vs.", "compared to", "compared with"):
        answer = f"In Legal Diversity, LightRAG scores 86.4% {wording} NaiveRAG [1]."
        assert outcomes(answer) == ([], []), wording
    assert outcomes("在 Legal 的 Diversity，LightRAG 以 86.4% 優於 NaiveRAG [1]。") == ([], [])


def test_a_comparator_that_the_table_pairs_differently_is_contradicted() -> None:
    # 86.4% is LightRAG's Legal Diversity figure against NaiveRAG, not against GraphRAG.
    [wrong] = verify_numbers(
        "LightRAG achieved 86.4% over GraphRAG in Legal Diversity [1].", PAGES
    ).mislabelled

    assert wrong.answer_labels == ["Diversity", "Legal", "LightRAG", "vs GraphRAG"]


def test_a_compared_method_with_its_own_figure_owns_that_figure() -> None:
    # "compared to NaiveRAG's 13.6%" compares two figures and claims nothing about the pairing.
    answer = "In Legal Diversity, LightRAG reaches 86.4%, compared to NaiveRAG's 13.6% [1]."

    assert outcomes(answer) == ([], [])


def test_two_free_methods_in_one_clause_are_ambiguous_not_nearest() -> None:
    # Both are true of 67.6%? No: only LightRAG has 67.6% in Agriculture Comprehensiveness.
    # The check cannot tell which method the answer means, so it does not decide.
    answer = "LightRAG and NaiveRAG reach 67.6% in Agriculture Comprehensiveness [1]."

    assert outcomes(answer) == ([], [("67.6%", "ambiguous")])


def test_the_same_value_in_another_table_does_not_support_a_claim_about_this_one() -> None:
    # 64.0% is also -High's Mix Diversity figure in Table 2; neither is Legal's.
    assert outcomes("In Mix, the -High variant reaches 64.0% in Diversity [1].") == ([], [])
    assert outcomes("In Legal, the -High variant reaches 64.0% in Diversity [1].") == (
        ["64.0%"],
        [],
    )


def test_a_number_without_the_tables_unit_is_not_a_claim_about_the_table() -> None:
    # 64.0 without a percent sign is not the 64.0% cell; it is left to the page check.
    result = verify_numbers("LightRAG indexed the Legal corpus in 64.0 minutes [1].", PAGES)

    assert result.mislabelled == [] and result.unresolved == []
    assert result.verified[0].number == "64.0"  # the digits do occur on the page


def test_a_figure_whose_sentence_names_no_label_at_all_is_left_to_the_page_check() -> None:
    assert outcomes("Win rates range from 13.6% to 86.4% [1].") == ([], [])


def test_the_label_note_lists_only_contradicted_figures_with_their_comparators() -> None:
    [wrong] = verify_numbers(
        "LightRAG achieved 86.4% over GraphRAG in Legal Diversity [1].", PAGES
    ).mislabelled

    assert label_note([wrong], "other") == (
        "Figures whose labels differ from the source table: 86.4% (answer: Diversity, Legal, "
        "LightRAG, vs GraphRAG; source: Diversity, Legal, LightRAG, vs NaiveRAG / "
        "Diversity, Legal, -Low, vs NaiveRAG)."
    )


def test_markdown_emphasis_around_figures_and_names_does_not_hide_the_roles() -> None:
    # The real answer (D67): bold markers stand between "Against" and the comparator.
    answer = (
        "In the **Legal dataset**, LightRAG achieved **83.6% win rate over NaiveRAG in "
        "Comprehensiveness** [6]. Against **GraphRAG**, LightRAG achieved **51.6% win rate "
        "in Comprehensiveness** and **64.0% in Diversity** in the same dataset [6]."
    )

    result = verify_numbers(answer, PAGES)

    assert [(m.number, m.answer_labels) for m in result.mislabelled] == [
        ("64.0%", ["Diversity", "Legal", "LightRAG", "vs GraphRAG"])
    ]
    assert result.unresolved == []


def test_figures_joined_into_a_range_share_their_labels() -> None:
    # "NaiveRAG (32.4%–38.8%)": the second figure is NaiveRAG's too, not the subject's;
    # the range names no dataset, so neither figure is contradicted nor confirmed.
    answer = (
        "LightRAG achieves 67.6% (Agriculture) and 61.2% (Mix) in Comprehensiveness, "
        "outperforming NaiveRAG (32.4%–38.8%) [1]."
    )

    assert outcomes(answer) == ([], [("32.4%", "missing"), ("38.8%", "missing")])


def test_a_possessive_written_in_bold_still_binds_its_figure() -> None:
    # "LightRAG’s **67.6%**": the blanked markers leave spaces between the name and the figure.
    answer = (
        "In Agriculture Comprehensiveness, -High scores 65.2%, down from LightRAG’s **67.6%** [1]."
    )

    assert outcomes(answer) == ([], [])


def test_the_heading_of_a_list_labels_the_items_under_it() -> None:
    # A real Q3 answer (D67 regression): the metric is a heading, each dataset an item.
    answer = (
        "Representative figures:\n\n"
        "- **Comprehensiveness**:\n"
        "  - Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; -High 65.2% [1].\n"
        "  - Legal: NaiveRAG 16.4%, LightRAG 83.6%; -High 76.4% [1].\n\n"
        "- **Diversity**:\n"
        "  - Legal: NaiveRAG 13.6%, LightRAG 86.4%; -High 83.2% [1].\n\n"
        "Prose after the list names no metric: in Legal, -High reaches 83.2% [1]."
    )

    mislabelled, unresolved = outcomes(answer)

    assert mislabelled == []
    # The heading stops at the first sentence that is not a list item.
    assert unresolved == [("83.2%", "missing")]


def test_a_wrong_item_under_a_list_heading_is_contradicted() -> None:
    answer = "- **Diversity**:\n  - Legal: NaiveRAG 13.6%, LightRAG 83.6% [1]."

    [wrong] = verify_numbers(answer, PAGES).mislabelled

    assert wrong.answer_labels == ["Diversity", "Legal", "LightRAG"]


# --- D68: a claim that one method wins everywhere, checked against the table -----------
#
# "X consistently outperforms Y across all datasets and metrics" is checked cell by cell:
# where X and Y share a row and column group, X is either above or below Y. Both ways in
# the same table means the claim fails whichever direction counts as better; the check
# assumes no direction. All one way is not contradicted (the direction is not known).

CORRECT_FIGURES = (
    "- Comprehensiveness:\n"
    "  - Agriculture: NaiveRAG 32.4%, LightRAG 67.6%; -High 65.2%; -Origin 75.2% [1].\n"
    "  - Mix: NaiveRAG 38.8%, LightRAG 61.2%; -High 59.6%; -Origin 55.6% [1].\n\n"
)


def test_a_claim_of_winning_everywhere_is_contradicted_by_cells_that_go_the_other_way() -> None:
    # The real Q3 regression answer (D68): every figure right, the closing sentence wrong.
    answer = CORRECT_FIGURES + (
        "In summary, the hybrid mode of LightRAG consistently outperforms the ablated versions "
        "across all datasets and metrics [1]."
    )

    [claim] = verify_numbers(answer, [TABLE_PAGE]).overstated

    assert claim.status == "contradicted"
    assert claim.method == "LightRAG"
    assert claim.sentence.startswith("In summary, the hybrid mode")
    assert claim.higher > 0 and claim.lower > 0
    assert (
        "Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8)" in claim.examples
    )
    assert all("GraphRAG" not in example for example in claim.examples)  # not in this table


def test_a_claim_with_a_hedge_is_not_a_universal_claim() -> None:
    answer = CORRECT_FIGURES + "LightRAG outperforms the ablated versions in most cases [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).overstated == []


def test_a_universal_claim_about_a_named_dataset_is_checked_only_there() -> None:
    # In CS, LightRAG is above -High in both rows the table has: nothing to report.
    answer = "In the CS dataset, LightRAG outperforms -High in all metrics [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).overstated == []


def test_a_method_that_is_below_the_other_everywhere_is_not_contradicted() -> None:
    # Whether lower is worse depends on the metric; the check does not assume it.
    answer = "In the CS dataset, -High outperforms LightRAG in all metrics [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).overstated == []


def test_a_universal_claim_against_a_method_the_tables_do_not_pair_is_unresolved() -> None:
    # In this table -Low has only a Diversity row and LightRAG has none: no shared cell.
    answer = "LightRAG consistently outperforms -Low in all cases [1]."

    [claim] = verify_numbers(answer, [TABLE_PAGE]).overstated

    assert claim.status == "unresolved" and claim.compared == ["-Low"]


def test_a_sentence_without_a_method_as_subject_is_not_checked() -> None:
    answer = "The dual-level design is better in all cases than a single level [1]."

    assert verify_numbers(answer, [TABLE_PAGE]).overstated == []


def test_a_chinese_universal_claim_is_checked_too() -> None:
    answer = "LightRAG 在所有資料集與指標上都優於消融版本 [1]。"

    [claim] = verify_numbers(answer, [TABLE_PAGE]).overstated

    assert claim.status == "contradicted" and claim.method == "LightRAG"


def test_the_claim_note_names_the_sentence_the_counts_and_an_example() -> None:
    answer = CORRECT_FIGURES + (
        "In summary, LightRAG consistently outperforms the ablated versions across all datasets "
        "and metrics [1]."
    )
    [claim] = verify_numbers(answer, [TABLE_PAGE]).overstated

    note = claim_note([claim], "other")
    assert note.startswith('A claim the source table does not bear out: "In summary, LightRAG')
    assert (
        f"LightRAG is above the compared methods in {claim.higher} cells and below in {claim.lower}"
        in note
    )
    assert "Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8)" in note
    zh = claim_note([claim], "zh")
    assert zh.startswith("以下結論與原文表格不符：「In summary, LightRAG")
    assert f"LightRAG 在 {claim.higher} 格高於比較對象、{claim.lower} 格低於" in zh


def test_a_hedged_comparison_is_not_a_universal_claim() -> None:
    # The paper's own wording: "particularly in larger datasets" leaves the smaller one out.
    answer = (
        "LightRAG consistently outperforms GraphRAG, particularly in larger datasets with "
        "complex language contexts [2]."
    )

    assert verify_numbers(answer, PAGES).overstated == []


def test_a_bare_all_over_one_dimension_stands_when_some_slice_is_one_way() -> None:
    # "in all evaluation dimensions" may be about one setting the sentence does not name
    # (the case study); in Agriculture LightRAG is above GraphRAG in every row, so the
    # claim is not contradicted. With "consistently" it would be: Mix goes the other way.
    answer = "In case studies, LightRAG outperforms GraphRAG in all evaluation dimensions [4]."
    assert verify_numbers(answer, PAGES).overstated == []

    answer = "LightRAG consistently outperforms GraphRAG in all evaluation dimensions [4]."
    [claim] = verify_numbers(answer, PAGES).overstated
    assert claim.status == "contradicted"
    assert claim.examples[0].startswith("Comprehensiveness / Mix: LightRAG 49.6% vs GraphRAG 50.4%")


def test_examples_come_from_every_table_that_contradicts_the_claim() -> None:
    answer = "LightRAG consistently outperforms all other methods across all datasets [1][2]."

    [claim] = verify_numbers(answer, PAGES).overstated

    pages = [example.rsplit("(p. ", 1)[-1] for example in claim.examples[:2]]
    assert sorted(pages) == ["7)", "8)"]


def test_each_comparator_belongs_to_the_figure_before_it() -> None:
    # Real Q1 answer (D68): three figures, three comparators; the first one is written
    # "Naive RAG", which is read as NaiveRAG.
    answer = (
        "In the Legal dataset, LightRAG achieves 83.6% win rate in Comprehensiveness against "
        "Naive RAG, 88.4% against RQ-RAG, and 73.2% against HyDE [1]."
    )
    table1 = PageText(
        DOC,
        7,
        TABLE1_PAGE.text + "\nRQ-RAG LightRAG RQ-RAG LightRAG RQ-RAG LightRAG RQ-RAG LightRAG\n"
        "Comprehensiveness — Agriculture: RQ-RAG 31.6%, LightRAG 68.4%; CS: RQ-RAG 38.8%, "
        "LightRAG 61.2%; Legal: RQ-RAG 15.2%, LightRAG 84.8%; Mix: RQ-RAG 39.2%, LightRAG 60.8%\n"
        "Diversity — Agriculture: RQ-RAG 29.2%, LightRAG 70.8%; CS: RQ-RAG 39.2%, LightRAG 60.8%; "
        "Legal: RQ-RAG 11.6%, LightRAG 88.4%; Mix: RQ-RAG 30.8%, LightRAG 69.2%\n"
        "HyDE LightRAG HyDE LightRAG HyDE LightRAG HyDE LightRAG\n"
        "Comprehensiveness — Agriculture: HyDE 26.0%, LightRAG 74.0%; CS: HyDE 41.6%, "
        "LightRAG 58.4%; Legal: HyDE 26.8%, LightRAG 73.2%; Mix: HyDE 40.4%, LightRAG 59.6%",
    )

    result = verify_numbers(answer, [table1])

    # 88.4% is LightRAG's Diversity figure against RQ-RAG, not Comprehensiveness: wrong.
    assert [(m.number, m.answer_labels) for m in result.mislabelled] == [
        ("88.4%", ["Comprehensiveness", "Legal", "LightRAG", "vs RQ-RAG"])
    ]
    assert result.unresolved == []  # 83.6% vs NaiveRAG and 73.2% vs HyDE are right


def test_a_comparator_the_tables_do_not_know_blocks_the_clause_wide_fallback() -> None:
    # "against the baseline" names no method of the table: 83.6% gets no comparator, and
    # the one RQ-RAG mention belongs to 88.4% only.
    answer = (
        "In Legal Comprehensiveness, LightRAG scores 83.6% against the baseline and 84.8% "
        "against RQ-RAG [1]."
    )
    table1 = PageText(
        DOC,
        7,
        TABLE1_PAGE.text + "\nRQ-RAG LightRAG RQ-RAG LightRAG RQ-RAG LightRAG RQ-RAG LightRAG\n"
        "Comprehensiveness — Agriculture: RQ-RAG 31.6%, LightRAG 68.4%; CS: RQ-RAG 38.8%, "
        "LightRAG 61.2%; Legal: RQ-RAG 15.2%, LightRAG 84.8%; Mix: RQ-RAG 39.2%, LightRAG 60.8%",
    )

    result = verify_numbers(answer, [table1])

    assert result.mislabelled == [] and result.unresolved == []
