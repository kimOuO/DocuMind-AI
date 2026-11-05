"""Table-aware context expansion: the discussion that follows a retrieved table.

A table says what the numbers are; the text right after it says what they
mean. That text ranks low for a question about the table's subject, so when
the similarity search returns a table chunk, the chunks that follow it in the
document are added as long as they belong to the same section (D62):

- stop at a chunk that starts with a heading (the next section), at another
  table, at a chunk the search already returned, and after MAX_FOLLOWING chunks;
- a chunk with a heading further inside it still belongs to the table's section
  at its start, so it is added, and the expansion ends there.

Added chunks are marked origin="table_context", separately from the search's
own results, and go through the same evidence budget as everything else. No
LLM call, no rule about any particular document.
"""

from app.ingestion.headings import find_headings
from app.ingestion.parsing import Page
from app.ingestion.tables import is_table_chunk
from app.retrieval.repository import RetrievedChunk

MAX_FOLLOWING = 2


def _heading_lines(text: str) -> list[int]:
    return [h.line for h in find_headings([Page(1, text)])]


def table_context(
    table: RetrievedChunk, following: list[RetrievedChunk], already: set[int]
) -> list[RetrievedChunk]:
    """Which of the chunks after `table` (in document order) to add."""
    added: list[RetrievedChunk] = []
    for chunk in following[:MAX_FOLLOWING]:
        if chunk.ordinal in already or is_table_chunk(chunk.text):
            break
        headings = _heading_lines(chunk.text)
        if headings and headings[0] == 0:
            break  # the next section begins here
        added.append(chunk)
        if headings:
            break  # the section ends inside this chunk
    return added


def tables_in(chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    return [c for c in chunks if is_table_chunk(c.text)]
