"""Split pages into chunks measured in tokens: fixed-size prose, tables kept whole.

Each page is chunked on its own, so a chunk never crosses a page and the page
number cited with it is always right. Prose is cut into fixed-size chunks;
consecutive ones overlap, so that a sentence cut at a boundary is whole in one
of the two. A table region (caption, headers and number rows) is one chunk of
its own, up to TABLE_CHUNK_FACTOR times the chunk size, so that its numbers
stay next to the headers that give them meaning (AC-14).
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

from app.ingestion.parsing import Page
from app.ingestion.tables import find_table_regions, linearize_table, split_table, table_blocks

# A table may be this many times the chunk size before it is split by rows.
TABLE_CHUNK_FACTOR = 4


class ChunkTokenizer(Protocol):
    def count(self, text: str) -> int: ...

    def spans(self, text: str) -> list[tuple[int, int]]: ...


@dataclass(frozen=True)
class ChunkDraft:
    ordinal: int  # position in the document, starting at 0
    page: int
    text: str
    token_count: int
    # D82: the blocks of a multi-block table, each embedded on its own; empty otherwise.
    blocks: list[str] = field(default_factory=list)


def chunk_pages(
    pages: Sequence[Page], tokenizer: ChunkTokenizer, *, chunk_size: int, overlap: int
) -> list[ChunkDraft]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be at least 0 and smaller than chunk_size.")

    chunks: list[ChunkDraft] = []
    for page in pages:
        for text, is_table in _segments(page.text):
            if is_table:
                pieces = split_table(
                    linearize_table(text), tokenizer, max_tokens=TABLE_CHUNK_FACTOR * chunk_size
                )
                for piece in pieces:
                    chunks.append(
                        ChunkDraft(
                            len(chunks),
                            page.number,
                            piece,
                            tokenizer.count(piece),
                            table_blocks(piece),
                        )
                    )
            else:
                _chunk_prose(text, page.number, tokenizer, chunk_size, overlap, chunks)
    return chunks


def _segments(page_text: str) -> list[tuple[str, bool]]:
    """The page as alternating prose and table pieces, in order, empty ones dropped."""
    segments: list[tuple[str, bool]] = []
    position = 0
    for start, end in find_table_regions(page_text):
        segments.append((page_text[position:start], False))
        segments.append((page_text[start:end], True))
        position = end
    segments.append((page_text[position:], False))
    return [(text, is_table) for text, is_table in segments if text.strip()]


def _chunk_prose(
    text: str,
    page_number: int,
    tokenizer: ChunkTokenizer,
    chunk_size: int,
    overlap: int,
    chunks: list[ChunkDraft],
) -> None:
    spans = tokenizer.spans(text)
    start = 0
    while start < len(spans):
        end = min(start + chunk_size, len(spans))
        # A slice of text does not always tokenize exactly like the same
        # tokens did inside the page; shrink until the count really fits. A boundary
        # inside a word or a number ("8,|564") is moved back to the token before it (D87:
        # a chunk that began ",564 nodes" lost the 8).
        while end - start > 1 and (
            _splits_a_word(text, spans[end - 1][1])
            or _window(text, spans, start, end, tokenizer)[1] > chunk_size
        ):
            end -= 1
        piece, count = _window(text, spans, start, end, tokenizer)
        if piece:
            chunks.append(ChunkDraft(len(chunks), page_number, piece, count))
        if end >= len(spans):
            break
        previous = start
        start = max(end - overlap, start + 1)
        while start > previous + 1 and _splits_a_word(text, spans[start][0]):
            start -= 1


_WORD_CHARACTER = re.compile(r"[A-Za-z0-9,.%\-]")


def _splits_a_word(text: str, position: int) -> bool:
    """Whether a boundary at `position` falls between two characters of one word or
    number ("8,|564", "Light|RAG"). Scripts without spaces (Chinese) are not words in
    this sense and may be cut anywhere."""
    return (
        0 < position < len(text)
        and _WORD_CHARACTER.match(text[position - 1]) is not None
        and _WORD_CHARACTER.match(text[position]) is not None
    )


def _window(
    page_text: str, spans: list[tuple[int, int]], start: int, end: int, tokenizer: ChunkTokenizer
) -> tuple[str, int]:
    text = page_text[spans[start][0] : spans[end - 1][1]].strip()
    return text, tokenizer.count(text)
