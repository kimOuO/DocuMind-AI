"""Split pages into fixed-size chunks measured in tokens.

Each page is chunked on its own, so a chunk never crosses a page and the page
number cited with it is always right. Consecutive chunks of a page overlap, so
that a sentence cut at a boundary is whole in one of the two.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.ingestion.parsing import Page


class ChunkTokenizer(Protocol):
    def count(self, text: str) -> int: ...

    def spans(self, text: str) -> list[tuple[int, int]]: ...


@dataclass(frozen=True)
class ChunkDraft:
    ordinal: int  # position in the document, starting at 0
    page: int
    text: str
    token_count: int


def chunk_pages(
    pages: Sequence[Page], tokenizer: ChunkTokenizer, *, chunk_size: int, overlap: int
) -> list[ChunkDraft]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be at least 0 and smaller than chunk_size.")

    chunks: list[ChunkDraft] = []
    for page in pages:
        spans = tokenizer.spans(page.text)
        start = 0
        while start < len(spans):
            end = min(start + chunk_size, len(spans))
            text, count = _window(page.text, spans, start, end, tokenizer)
            # A slice of text does not always tokenize exactly like the same
            # tokens did inside the page; shrink until the count really fits.
            while count > chunk_size and end - start > 1:
                end -= 1
                text, count = _window(page.text, spans, start, end, tokenizer)
            if text:
                chunks.append(ChunkDraft(len(chunks), page.number, text, count))
            if end >= len(spans):
                break
            start = max(end - overlap, start + 1)
    return chunks


def _window(
    page_text: str, spans: list[tuple[int, int]], start: int, end: int, tokenizer: ChunkTokenizer
) -> tuple[str, int]:
    text = page_text[spans[start][0] : spans[end - 1][1]].strip()
    return text, tokenizer.count(text)
