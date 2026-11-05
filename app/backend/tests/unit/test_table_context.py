"""Table-aware context expansion (D62): which chunks after a retrieved table are added."""

import uuid

from app.retrieval.expansion import MAX_FOLLOWING, table_context, tables_in
from app.retrieval.repository import RetrievedChunk

DOC = uuid.uuid4()
TABLE = "Table 2: Scores.\nA B\nx — A: 1%; B: 2%"


def chunk(ordinal: int, text: str, *, score: float | None = None) -> RetrievedChunk:
    return RetrievedChunk(uuid.uuid4(), DOC, "paper.pdf", 8, ordinal, text, 10, score)


def test_the_discussion_after_a_table_is_added_up_to_the_chunk_where_the_section_ends() -> None:
    table = chunk(22, TABLE, score=0.7)
    following = [
        chunk(23, "The -High variant removes high-level retrieval.\n4.4 CASE STUDY (RQ3)\nTo"),
        chunk(24, "cases of the next section"),
    ]

    added = table_context(table, following, already=set())

    # The first chunk starts in the table's section and holds the next heading: added, then stop.
    assert [c.ordinal for c in added] == [23]


def test_a_chunk_that_starts_with_a_heading_is_the_next_section_and_is_not_added() -> None:
    following = [chunk(23, "4.4 CASE STUDY (RQ3)\nTo provide a comparison"), chunk(24, "more")]
    assert table_context(chunk(22, TABLE), following, already=set()) == []

    markdown = [chunk(5, "## Methods\n\nWe did things."), chunk(6, "more")]
    assert table_context(chunk(4, TABLE), markdown, already=set()) == []


def test_another_table_or_an_already_retrieved_chunk_stops_the_expansion() -> None:
    following = [chunk(23, "Table 3: Other.\nA B\ny — A: 3%; B: 4%"), chunk(24, "text")]
    assert table_context(chunk(22, TABLE), following, already=set()) == []

    following = [chunk(23, "discussion"), chunk(24, "more discussion")]
    assert table_context(chunk(22, TABLE), following, already={23}) == []


def test_at_most_two_chunks_of_plain_discussion_are_added() -> None:
    following = [chunk(23, "first"), chunk(24, "second"), chunk(25, "third")]

    added = table_context(chunk(22, TABLE), following, already=set())

    assert [c.ordinal for c in added] == [23, 24] and MAX_FOLLOWING == 2


def test_only_table_chunks_trigger_an_expansion() -> None:
    chunks = [chunk(1, "prose about tables", score=0.8), chunk(22, TABLE, score=0.7)]
    assert [c.ordinal for c in tables_in(chunks)] == [22]
    assert tables_in([chunk(1, "Table 3 is discussed here, see below.", score=0.6)]) == []
