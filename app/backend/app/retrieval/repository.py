"""Similarity search over chunks.

Chunks have no owner column of their own: every search joins `documents` and
filters on its owner, whatever document ids the caller passes. Only documents
that are ready are searched.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Chunk, Document


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    filename: str
    page: int
    ordinal: int
    text: str
    token_count: int
    score: float  # cosine similarity with the question, 1 is identical


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
        distance = Chunk.embedding.cosine_distance(embedding)
        rows = await self._db.execute(
            select(
                Chunk.id,
                Chunk.document_id,
                Document.filename,
                Chunk.page,
                Chunk.ordinal,
                Chunk.text,
                Chunk.token_count,
                (1 - distance).label("score"),
            )
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Document.owner_id == owner_id,
                Document.status == "ready",
                Document.id.in_(document_ids),
            )
            .order_by(distance, Chunk.id)
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
