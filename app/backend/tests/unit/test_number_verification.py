"""AC-26: the numbers in an answer are checked against the original text of the cited pages.

A number counts as verified when the same value (ignoring thousands separators
and a percent sign) appears on one of those pages; a verified number carries
the page and a snippet of the original text; an unverified one is reported.
"""

import uuid

from app.chat.verification import PageText, numbers_in, verify_numbers

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
