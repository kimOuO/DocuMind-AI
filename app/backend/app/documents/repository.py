"""Data access for documents and their processing jobs.

Every query takes the owner: a document that belongs to someone else is
indistinguishable from one that does not exist.
"""

import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Chunk, Document, IngestionJob


class DocumentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get(self, owner_id: uuid.UUID, document_id: uuid.UUID) -> Document | None:
        return await self._db.scalar(
            select(Document).where(Document.id == document_id, Document.owner_id == owner_id)
        )

    async def get_by_hash(self, owner_id: uuid.UUID, content_hash: str) -> Document | None:
        return await self._db.scalar(
            select(Document).where(
                Document.owner_id == owner_id, Document.content_hash == content_hash
            )
        )

    async def list_for_owner(self, owner_id: uuid.UUID) -> list[Document]:
        result = await self._db.scalars(
            select(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc(), Document.id)
        )
        return list(result)

    async def chunk_counts(self, document_ids: list[uuid.UUID]) -> dict[uuid.UUID, int]:
        if not document_ids:
            return {}
        rows = await self._db.execute(
            select(Chunk.document_id, func.count())
            .where(Chunk.document_id.in_(document_ids))
            .group_by(Chunk.document_id)
        )
        return {document_id: count for document_id, count in rows}

    async def latest_jobs(self, document_id: uuid.UUID) -> list[IngestionJob]:
        """The most recent job of each kind for one document."""
        result = await self._db.scalars(
            select(IngestionJob)
            .where(IngestionJob.document_id == document_id)
            .order_by(IngestionJob.created_at.desc(), IngestionJob.id)
        )
        latest: dict[str, IngestionJob] = {}
        for job in result:
            latest.setdefault(job.kind, job)
        return [latest[kind] for kind in sorted(latest)]

    async def add_with_index_job(self, document: Document) -> Document:
        self._db.add(document)
        await self._db.flush()
        self._db.add(IngestionJob(document_id=document.id, kind="index", status="queued"))
        await self._db.flush()
        await self._db.refresh(document)
        return document

    async def delete(self, document: Document) -> None:
        # Jobs, chunks and summaries go with it (ON DELETE CASCADE).
        await self._db.execute(delete(Document).where(Document.id == document.id))
