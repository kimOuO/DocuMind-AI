"""Reading stored summaries for answering. Every query carries the owner."""

import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document, Summary


@dataclass(frozen=True)
class DocumentSummaryState:
    document_id: uuid.UUID
    filename: str
    summary_status: str  # none | processing | ready | failed


@dataclass(frozen=True)
class StoredSummary:
    document_id: uuid.UUID
    filename: str
    level: str  # "document" or "section"
    ordinal: int  # 0 for the document summary, then the sections in order
    title: str | None
    page_start: int
    page_end: int
    text: str
    token_count: int
    verification: dict[str, Any] | None = None  # D76


class SummaryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def states(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[DocumentSummaryState]:
        """The summary status of the owner's documents, in the order given."""
        rows = (
            await self._db.execute(
                select(Document.id, Document.filename, Document.summary_status).where(
                    Document.owner_id == owner_id, Document.id.in_(document_ids)
                )
            )
        ).all()
        by_id = {
            row.id: DocumentSummaryState(row.id, row.filename, row.summary_status) for row in rows
        }
        return [by_id[i] for i in document_ids if i in by_id]

    async def ready_summaries(
        self, owner_id: uuid.UUID, document_ids: list[uuid.UUID]
    ) -> list[StoredSummary]:
        """The summaries of the owner's documents whose summary is ready.

        Documents come in the order given; within a document the whole-document
        summary first, then the sections in document order.
        """
        rows = (
            await self._db.execute(
                select(
                    Summary.document_id,
                    Document.filename,
                    Summary.level,
                    Summary.ordinal,
                    Summary.title,
                    Summary.page_start,
                    Summary.page_end,
                    Summary.text,
                    Summary.token_count,
                    Summary.verification,
                )
                .join(Document, Document.id == Summary.document_id)
                .where(
                    Document.owner_id == owner_id,
                    Document.id.in_(document_ids),
                    Document.summary_status == "ready",
                )
            )
        ).all()
        position = {document_id: index for index, document_id in enumerate(document_ids)}
        summaries = [StoredSummary(*row) for row in rows]
        summaries.sort(key=lambda s: (position[s.document_id], s.level != "document", s.ordinal))
        return summaries
