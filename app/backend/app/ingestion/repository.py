"""Data access for processing jobs and the chunks they produce.

Jobs are run by the system, not by a user, so they are addressed by job id. A
user never reaches a job or a chunk through this module: the document service
checks ownership before a job is created, retried or shown.

Every write first locks the document and then the job, in that order. Deleting
a document takes the same locks in the same order (the document row, then its
jobs through ON DELETE CASCADE), so a write and a deletion can only happen one
after the other:

- the write commits first, and the deletion then removes what it wrote; or
- the deletion commits first, and the write finds nothing to lock and gives up.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Chunk, Document, IngestionJob

ACTIVE_STATUSES = ("queued", "running")


@dataclass(frozen=True)
class ClaimedJob:
    job_id: uuid.UUID
    document_id: uuid.UUID
    storage_path: str
    media_type: str


@dataclass(frozen=True)
class ChunkRecord:
    ordinal: int
    page: int
    text: str
    token_count: int
    embedding: list[float]


class IngestionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def _lock(self, job_id: uuid.UUID) -> tuple[Document, IngestionJob] | None:
        """Lock the job's document, then the job. None if either no longer exists."""
        document_id = await self._db.scalar(
            select(IngestionJob.document_id).where(IngestionJob.id == job_id)
        )
        if document_id is None:
            return None
        document = await self._db.scalar(
            select(Document).where(Document.id == document_id).with_for_update()
        )
        if document is None:
            return None
        job = await self._db.scalar(
            select(IngestionJob).where(IngestionJob.id == job_id).with_for_update()
        )
        if job is None:
            return None
        return document, job

    async def claim_index_job(self, job_id: uuid.UUID) -> ClaimedJob | None:
        """Move a queued index job to running. None if it cannot be started."""
        locked = await self._lock(job_id)
        if locked is None:
            return None
        document, job = locked
        if job.kind != "index" or job.status != "queued":
            return None
        job.status = "running"
        job.stage = "parsing"
        job.progress_current = None
        job.progress_total = None
        job.error = None
        job.started_at = func.now()
        document.status = "processing"
        document.error = None
        await self._db.flush()
        return ClaimedJob(job.id, document.id, document.storage_path, document.media_type)

    async def set_progress(
        self, job_id: uuid.UUID, stage: str, current: int | None, total: int | None
    ) -> bool:
        """Record progress. False if the job is gone or no longer running."""
        result = await self._db.execute(
            update(IngestionJob)
            .where(IngestionJob.id == job_id, IngestionJob.status == "running")
            .values(stage=stage, progress_current=current, progress_total=total)
        )
        assert isinstance(result, CursorResult)
        return result.rowcount == 1

    async def complete_index_job(
        self, job_id: uuid.UUID, *, page_count: int, chunks: list[ChunkRecord]
    ) -> bool:
        """Store all chunks and mark the document ready, in the caller's transaction.

        Returns False, having written nothing, if the document was deleted or
        the job is no longer running.
        """
        locked = await self._lock(job_id)
        if locked is None:
            return False
        document, job = locked
        if job.status != "running":
            return False

        # A retry replaces whatever an earlier attempt stored.
        await self._db.execute(delete(Chunk).where(Chunk.document_id == document.id))
        if chunks:
            await self._db.execute(
                insert(Chunk),
                [
                    {
                        "document_id": document.id,
                        "ordinal": chunk.ordinal,
                        "page": chunk.page,
                        "text": chunk.text,
                        "token_count": chunk.token_count,
                        "embedding": chunk.embedding,
                    }
                    for chunk in chunks
                ],
            )
        document.status = "ready"
        document.page_count = page_count
        document.error = None
        job.status = "completed"
        job.progress_current = len(chunks)
        job.progress_total = len(chunks)
        job.completed_at = func.now()
        await self._db.flush()
        return True

    async def fail_job(self, job_id: uuid.UUID, reason: str) -> bool:
        """Mark an unfinished job, and what it was producing, as failed."""
        locked = await self._lock(job_id)
        if locked is None:
            return False
        document, job = locked
        if job.status not in ACTIVE_STATUSES:
            return False
        job.status = "failed"
        job.error = reason
        job.completed_at = func.now()
        if job.kind == "index":
            document.status = "failed"
            document.error = reason
        else:
            document.summary_status = "failed"
        await self._db.flush()
        return True
