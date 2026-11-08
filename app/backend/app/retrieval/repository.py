"""Similarity search over chunks.

Chunks have no owner column of their own: every search joins `documents` and
filters on its owner, whatever document ids the caller passes. Only documents
that are ready are searched.
"""

import re
import uuid
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import and_, func, or_, select, text, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.headings import find_headings
from app.ingestion.parsing import Page
from app.models import Chunk, ChunkVector, Document

_CAPTION_LINE = re.compile(r"^\s*(?:Table|Figure|Fig\.)\s*\d+\s*[.:]", re.IGNORECASE)
# A line that may be a numbered heading ("4.3 ABLATION STUDIES"); the recogniser decides.
_NUMBERED_LINE_SQL = r"(^|\n)\s*\d{1,2}(\.\d{1,2})*\s+[A-Za-z]"


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    filename: str
    page: int
    ordinal: int
    text: str
    token_count: int
    score: float | None  # cosine similarity with the question, 1 is identical; None if not searched
    # "retrieval": found by similarity search; "table_context": the discussion that
    # follows a retrieved table, added for its structure, not its similarity.
    origin: str = "retrieval"


class RetrievalRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def documents_in(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[Document]:
        """The owner's documents among the given ids."""
        result = await self._db.scalars(
            select(Document).where(Document.owner_id == owner_id, Document.id.in_(document_ids))
        )
        return list(result)

    async def ready_document_ids(self, owner_id: uuid.UUID) -> list[uuid.UUID]:
        result = await self._db.scalars(
            select(Document.id)
            .where(Document.owner_id == owner_id, Document.status == "ready")
            .order_by(Document.created_at, Document.id)
        )
        return list(result)

    async def search(
        self,
        owner_id: uuid.UUID,
        document_ids: list[uuid.UUID],
        embedding: list[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """The `top_k` chunks closest to the embedding, most similar first."""
        # With the approximate index, a filter is applied after the nearest
        # neighbours are found; keep scanning until enough rows pass the filter.
        await self._db.execute(text("SET LOCAL hnsw.iterative_scan = strict_order"))
        # D82: a chunk's distance is the best of its own vector and its table blocks'
        # vectors, so that a table holding several comparisons is found by the one asked
        # about. Prose chunks have no block vectors and score by their own.
        in_scope = (
            select(Chunk.id)
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Document.owner_id == owner_id,
                Document.status == "ready",
                Document.id.in_(document_ids),
            )
        )
        own = select(
            Chunk.id.label("chunk_id"),
            Chunk.embedding.cosine_distance(embedding).label("distance"),
        ).where(Chunk.id.in_(in_scope))
        blocks = select(
            ChunkVector.chunk_id.label("chunk_id"),
            ChunkVector.embedding.cosine_distance(embedding).label("distance"),
        ).where(ChunkVector.chunk_id.in_(in_scope))
        candidates = union_all(own, blocks).subquery("candidates")
        best = (
            select(
                candidates.c.chunk_id,
                func.min(candidates.c.distance).label("distance"),
            )
            .group_by(candidates.c.chunk_id)
            .subquery("best")
        )
        rows = await self._db.execute(
            select(
                Chunk.id,
                Chunk.document_id,
                Document.filename,
                Chunk.page,
                Chunk.ordinal,
                Chunk.text,
                Chunk.token_count,
                (1 - best.c.distance).label("score"),
            )
            .join(best, best.c.chunk_id == Chunk.id)
            .join(Document, Document.id == Chunk.document_id)
            .order_by(best.c.distance, Chunk.id)
            .limit(top_k)
        )
        return [
            RetrievedChunk(
                chunk_id=row.id,
                document_id=row.document_id,
                filename=row.filename,
                page=row.page,
                ordinal=row.ordinal,
                text=row.text,
                token_count=row.token_count,
                score=float(row.score),
            )
            for row in rows
        ]

    async def by_ids(
        self, owner_id: uuid.UUID, chunk_ids: Sequence[uuid.UUID]
    ) -> list[RetrievedChunk]:
        """The owner's chunks with these ids, in document order, unscored (D99: the sources of
        the previous turn, brought back for a follow-up that retrieval cannot place)."""
        if not chunk_ids:
            return []
        rows = await self._db.execute(
            select(
                Chunk.id,
                Chunk.document_id,
                Document.filename,
                Chunk.page,
                Chunk.ordinal,
                Chunk.text,
                Chunk.token_count,
            )
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Chunk.id.in_(list(chunk_ids)),
                Document.owner_id == owner_id,
                Document.status == "ready",
            )
            .order_by(Chunk.document_id, Chunk.ordinal)
        )
        return [
            RetrievedChunk(
                chunk_id=row.id,
                document_id=row.document_id,
                filename=row.filename,
                page=row.page,
                ordinal=row.ordinal,
                text=row.text,
                token_count=row.token_count,
                score=None,
                origin="previous_turn",
            )
            for row in rows
        ]

    async def page_texts(
        self, owner_id: uuid.UUID, ranges: list[tuple[uuid.UUID, int, int]]
    ) -> list[tuple[uuid.UUID, int, str]]:
        """The stored text of the owner's pages, one entry per (document, page).

        `ranges` are (document id, first page, last page). Chunks of a page are
        joined in order; their overlap does no harm to a lookup.
        """
        if not ranges:
            return []
        rows = (
            await self._db.execute(
                select(Chunk.document_id, Chunk.page, Chunk.text)
                .join(Document, Document.id == Chunk.document_id)
                .where(
                    Document.owner_id == owner_id,
                    or_(
                        *(
                            and_(
                                Chunk.document_id == document_id,
                                Chunk.page >= first,
                                Chunk.page <= last,
                            )
                            for document_id, first, last in ranges
                        )
                    ),
                )
                .order_by(Chunk.document_id, Chunk.page, Chunk.ordinal)
            )
        ).all()
        pages: list[tuple[uuid.UUID, int, str]] = []
        for document_id, page, chunk_text in rows:
            if pages and pages[-1][:2] == (document_id, page):
                pages[-1] = (document_id, page, pages[-1][2] + "\n" + chunk_text)
            else:
                pages.append((document_id, page, chunk_text))
        return pages

    async def caption_lines(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[tuple[uuid.UUID, str, int, int, str]]:
        """Every line of the owner's chunks that starts a table or figure caption
        ("Table 2: …", "Figure 1: …"), with its document, page and chunk ordinal (D71:
        the document map)."""
        if not document_ids:
            return []
        rows = await self._db.execute(
            select(Chunk.document_id, Document.filename, Chunk.page, Chunk.ordinal, Chunk.text)
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Document.owner_id == owner_id,
                Chunk.document_id.in_(document_ids),
                Chunk.text.op("~*")(r"(^|\n)\s*(Table|Figure|Fig\.)\s*\d+\s*[.:]"),
            )
            .order_by(Chunk.document_id, Chunk.ordinal)
        )
        captions: list[tuple[uuid.UUID, str, int, int, str]] = []
        for document_id, filename, page, ordinal, chunk_text in rows:
            for line in chunk_text.splitlines():
                if _CAPTION_LINE.match(line):
                    captions.append((document_id, filename, page, ordinal, line.strip()))
        return captions

    async def heading_lines(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[tuple[uuid.UUID, str, int, int, int, str]]:
        """Every numbered heading the recogniser (AC-53) finds in the owner's chunks, with
        its document, page, chunk ordinal and line within the chunk (D73: sections and
        subsections of the document map, with their chunk ranges)."""
        if not document_ids:
            return []
        rows = await self._db.execute(
            select(Chunk.document_id, Document.filename, Chunk.page, Chunk.ordinal, Chunk.text)
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Document.owner_id == owner_id,
                Chunk.document_id.in_(document_ids),
                Chunk.text.op("~")(_NUMBERED_LINE_SQL),
            )
            .order_by(Chunk.document_id, Chunk.ordinal)
        )
        headings: list[tuple[uuid.UUID, str, int, int, int, str]] = []
        for document_id, filename, page, ordinal, chunk_text in rows:
            for h in find_headings([Page(page, chunk_text)]):
                if h.number is not None:
                    headings.append((document_id, filename, page, ordinal, h.line, h.raw))
        return headings

    async def chunk_pages(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[tuple[uuid.UUID, int, int]]:
        """(document, ordinal, page) of every chunk of the owner's documents."""
        if not document_ids:
            return []
        rows = await self._db.execute(
            select(Chunk.document_id, Chunk.ordinal, Chunk.page)
            .join(Document, Document.id == Chunk.document_id)
            .where(Document.owner_id == owner_id, Chunk.document_id.in_(document_ids))
            .order_by(Chunk.document_id, Chunk.ordinal)
        )
        return [(row.document_id, row.ordinal, row.page) for row in rows]

    async def rank_chunks(
        self,
        owner_id: uuid.UUID,
        document_id: uuid.UUID,
        embeddings: list[list[float]],
        *,
        ordinals: tuple[int, int] | None = None,
        pages: list[int] | None = None,
        limit: int,
    ) -> list[tuple[RetrievedChunk, list[float]]]:
        """The owner's chunks of a document within a chunk range or on given pages, with
        their cosine similarity to each embedding, ranked by the mean similarity (D73:
        the candidates of a Navigator target). Without embeddings: document order."""
        if ordinals is None and not pages:
            return []
        scores = [
            (1 - Chunk.embedding.cosine_distance(e)).label(f"score_{i}")
            for i, e in enumerate(embeddings)
        ]
        query = (
            select(
                Chunk.id,
                Chunk.document_id,
                Document.filename,
                Chunk.page,
                Chunk.ordinal,
                Chunk.text,
                Chunk.token_count,
                *scores,
            )
            .join(Document, Document.id == Chunk.document_id)
            .where(Document.owner_id == owner_id, Chunk.document_id == document_id)
        )
        if ordinals is not None:
            query = query.where(Chunk.ordinal >= ordinals[0], Chunk.ordinal <= ordinals[1])
        else:
            query = query.where(Chunk.page.in_(pages or []))
        if scores:
            mean = sum(scores[1:], scores[0]) / len(scores)
            query = query.order_by(mean.desc(), Chunk.ordinal)
        else:
            query = query.order_by(Chunk.ordinal)
        rows = await self._db.execute(query.limit(limit))
        return [
            (
                RetrievedChunk(
                    chunk_id=row.id,
                    document_id=row.document_id,
                    filename=row.filename,
                    page=row.page,
                    ordinal=row.ordinal,
                    text=row.text,
                    token_count=row.token_count,
                    score=None,
                    origin="navigation",
                ),
                [float(getattr(row, f"score_{i}")) for i in range(len(embeddings))],
            )
            for row in rows
        ]

    async def chunks_after(
        self, owner_id: uuid.UUID, document_id: uuid.UUID, ordinal: int, *, limit: int
    ) -> list[RetrievedChunk]:
        """The owner's chunks that follow the given one in document order."""
        rows = await self._db.execute(
            select(
                Chunk.id,
                Chunk.document_id,
                Document.filename,
                Chunk.page,
                Chunk.ordinal,
                Chunk.text,
                Chunk.token_count,
            )
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Document.owner_id == owner_id,
                Chunk.document_id == document_id,
                Chunk.ordinal > ordinal,
            )
            .order_by(Chunk.ordinal)
            .limit(limit)
        )
        return [
            RetrievedChunk(
                chunk_id=row.id,
                document_id=row.document_id,
                filename=row.filename,
                page=row.page,
                ordinal=row.ordinal,
                text=row.text,
                token_count=row.token_count,
                score=None,
                origin="table_context",
            )
            for row in rows
        ]
