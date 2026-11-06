"""AC-13 (D68): a statement's citation should point at the source that states it.

The check is lexical and conservative: it only doubts a citation when the cited
sources hardly share the statement's content words while another source the
model was given shares most of them. It never declares a citation correct.
"""

import uuid

from app.chat.citation_check import SourceText, check_citations

COST = (
    "In the retrieval phase GraphRAG consumes about 610,000 tokens and hundreds of API calls "
    "to read its community reports, while LightRAG needs fewer than 100 tokens and a single "
    "API call because it retrieves entities and relations directly from the graph."
)
UPDATE = (
    "When new documents arrive, GraphRAG must dismantle its existing community structure and "
    "regenerate every community report, whereas LightRAG merges the new entities and relations "
    "into the existing graph without rebuilding the index."
)
DOC = uuid.uuid4()
SOURCES = [SourceText(1, COST, DOC, 9, 9), SourceText(2, UPDATE, DOC, 10, 10)]


def test_a_statement_cited_to_a_source_about_another_matter_is_doubted() -> None:
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive, while LightRAG "
        "merges the new entities into the existing graph without rebuilding [1]."
    )

    [doubt] = check_citations(answer, SOURCES)

    assert doubt.cited == [1] and doubt.closer == [2]
    assert doubt.sentence.startswith("GraphRAG dismantles its community structure")
    assert doubt.coverage_closer > doubt.coverage_cited


def test_a_statement_cited_to_the_source_that_states_it_is_not_doubted() -> None:
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive, while LightRAG "
        "merges the new entities into the existing graph without rebuilding [2]."
    )

    assert check_citations(answer, SOURCES) == []


def test_a_statement_that_cites_both_sources_is_not_doubted() -> None:
    answer = "GraphRAG dismantles its community structure to add new documents [1][2]."

    assert check_citations(answer, SOURCES) == []


def test_statements_without_a_citation_or_with_few_content_words_are_not_checked() -> None:
    # A paragraph of its own without a citation is not checked; short statements and
    # statements in a language without space-separated words are not checked either.
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive.\n\n"
        "LightRAG is cheaper [1]. 它會重建社群結構 [1]."
    )

    assert check_citations(answer, SOURCES) == []


def test_a_statement_both_sources_cover_about_equally_is_not_doubted() -> None:
    # "GraphRAG", "LightRAG", "graph", "community" occur in both: nothing distinguishes them.
    answer = "GraphRAG and LightRAG both build a graph over the community reports [1]."

    assert check_citations(answer, SOURCES) == []


def test_a_cited_source_that_shares_a_fair_part_of_the_statement_is_left_alone() -> None:
    # Half cost, half mechanism: the cost source covers enough of it not to be doubted.
    answer = (
        "GraphRAG spends about 610,000 tokens and hundreds of API calls, and must dismantle "
        "its community structure when new documents arrive [1]."
    )

    assert check_citations(answer, SOURCES) == []


def test_a_source_on_the_same_page_as_the_cited_one_is_not_closer() -> None:
    # The citation already sends the reader to the right page; the chunk split is not an error.
    same_page = [SourceText(1, COST, DOC, 9, 9), SourceText(2, UPDATE, DOC, 9, 9)]
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive, while LightRAG "
        "merges the new entities into the existing graph without rebuilding [1]."
    )

    assert check_citations(answer, same_page) == []


def test_figures_count_as_content_so_a_numeric_statement_keeps_its_citation() -> None:
    # The figure stands in the cost source; the words around it happen to be the update's.
    answer = (
        "GraphRAG needs 610,000 tokens to regenerate its community reports after new documents [1]."
    )

    assert check_citations(answer, SOURCES) == []


def test_a_statement_whose_figure_stands_in_the_cited_source_is_trusted_for_it() -> None:
    # Mostly update-mechanism words, but the figure is the cost source's: cited for the figure.
    answer = (
        "GraphRAG would need hundreds of API calls to regenerate every community report after "
        "new documents arrive and rebuild the index [1]."
    )

    assert check_citations(answer, SOURCES) == []


def test_an_uncited_statement_takes_the_next_citation_of_its_paragraph() -> None:
    # The model often cites once at the end of a paragraph; the first statement is judged
    # by that citation too. Here it is the cost source, which does not state it.
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive, while LightRAG "
        "merges the new entities into the existing graph without rebuilding. GraphRAG reads "
        "community reports worth 610,000 tokens and hundreds of API calls [1].\n\n"
        "A new paragraph without any citation says nothing about the first."
    )

    [doubt] = check_citations(answer, SOURCES)

    assert doubt.sentence.startswith("GraphRAG dismantles") and doubt.cited == [1]


def test_a_source_on_the_cited_page_covers_the_statement_for_the_citation() -> None:
    # [1] and [2] are on the same page; [3] is the abstract on page 1. The statement is
    # [2]'s but cites [1]: the citation points at the right page, so nothing is doubted,
    # even though the abstract shares more words with the statement than [1] does.
    abstract = (
        "LightRAG merges new entities into the existing graph without rebuilding, and GraphRAG "
        "dismantles its community structure when new documents arrive."
    )
    sources = [
        SourceText(1, COST, DOC, 9, 9),
        SourceText(2, UPDATE, DOC, 9, 9),
        SourceText(3, abstract, DOC, 1, 1),
    ]
    answer = (
        "GraphRAG dismantles its community structure when new documents arrive, while LightRAG "
        "merges the new entities into the existing graph without rebuilding [1]."
    )

    assert check_citations(answer, sources) == []
