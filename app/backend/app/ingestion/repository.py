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
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Chunk, ChunkVector, Document, IngestionJob, Summary

ACTIVE_STATUSES = ("queued", "running")
RESTART_REASON = "Processing was interrupted because the service restarted. Please retry."


@dataclass(frozen=True)
class ClaimedJob:
    job_id: uuid.UUID
    document_id: uuid.UUID
    storage_path: str
    media_type: str


@dataclass(frozen=True)
class ClaimedSummaryJob:
    job_id: uuid.UUID
    document_id: uuid.UUID
    owner_id: uuid.UUID
    filename: str
    storage_path: str
    media_type: str


@dataclass(frozen=True)
class SummaryRecord:
    level: str  # "section" or "document"
    ordinal: int
    title: str | None
    page_start: int
    page_end: int
    source_chunk_ids: list[uuid.UUID]
    text: str
    token_count: int
    verification: dict[str, Any] | None = None  # D76: see Summary.verification


@dataclass(frozen=True)
class ChunkRecord:
    ordinal: int
    page: int
    text: str
    token_count: int
    embedding: list[float]
    # D82: one vector per block of a multi-block table; empty for every other chunk.
    block_embeddings: list[list[float]] = field(default_factory=list)


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
    ) -> uuid.UUID | None:
        """Store all chunks, mark the document ready and queue its summary job.

        All in the caller's transaction. Returns the id of the queued summary
        job, or None, having written nothing, if the document was deleted or
        the job is no longer running.
        """
        locked = await self._lock(job_id)
        if locked is None:
            return None
        document, job = locked
        if job.status != "running":
            return None

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
            with_blocks = [chunk for chunk in chunks if chunk.block_embeddings]
            if with_blocks:
                ids = dict(
                    (
                        await self._db.execute(
                            select(Chunk.ordinal, Chunk.id).where(
                                Chunk.document_id == document.id,
                                Chunk.ordinal.in_([c.ordinal for c in with_blocks]),
                            )
                        )
                    ).all()
                )
                await self._db.execute(
                    insert(ChunkVector),
                    [
                        {"chunk_id": ids[chunk.ordinal], "ordinal": index, "embedding": vector}
                        for chunk in with_blocks
                        for index, vector in enumerate(chunk.block_embeddings)
                    ],
                )
        document.status = "ready"
        document.page_count = page_count
        document.error = None
        job.status = "completed"
        job.progress_current = len(chunks)
        job.progress_total = len(chunks)
        job.completed_at = func.now()
        # The summary is built next, as a job of its own (see the architecture, section 7).
        previous = await self._db.scalar(
            select(func.max(IngestionJob.retry_count)).where(
                IngestionJob.document_id == document.id, IngestionJob.kind == "summary"
            )
        )
        summary_job = IngestionJob(
            document_id=document.id,
            kind="summary",
            status="queued",
            retry_count=0 if previous is None else previous + 1,
        )
        self._db.add(summary_job)
        await self._db.flush()
        return summary_job.id

    async def claim_summary_job(self, job_id: uuid.UUID) -> ClaimedSummaryJob | None:
        """Move a queued summary job to running. None if it cannot be started."""
        locked = await self._lock(job_id)
        if locked is None:
            return None
        document, job = locked
        if job.kind != "summary" or job.status != "queued" or document.status != "ready":
            return None
        job.status = "running"
        job.stage = "summarizing"
        job.progress_current = None
        job.progress_total = None
        job.error = None
        job.started_at = func.now()
        document.summary_status = "processing"
        await self._db.flush()
        return ClaimedSummaryJob(
            job.id,
            document.id,
            document.owner_id,
            document.filename,
            document.storage_path,
            document.media_type,
        )

    async def chunk_ids_for_pages(
        self, document_id: uuid.UUID, page_start: int, page_end: int
    ) -> list[uuid.UUID]:
        result = await self._db.scalars(
            select(Chunk.id)
            .where(
                Chunk.document_id == document_id,
                Chunk.page >= page_start,
                Chunk.page <= page_end,
            )
            .order_by(Chunk.ordinal)
        )
        return list(result)

    async def chunk_texts_for_pages(
        self, document_id: uuid.UUID, page_start: int, page_end: int
    ) -> list[tuple[int, str]]:
        """(page, text) of the document's chunks on the pages, in document order (D75: the
        source the summary of those pages is checked against; tables come rewritten cell
        by cell as the chunker left them)."""
        rows = await self._db.execute(
            select(Chunk.page, Chunk.text)
            .where(
                Chunk.document_id == document_id,
                Chunk.page >= page_start,
                Chunk.page <= page_end,
            )
            .order_by(Chunk.ordinal)
        )
        return [(row.page, row.text) for row in rows]

    async def complete_summary_job(
        self, job_id: uuid.UUID, *, sections: list[SummaryRecord], document_summary: SummaryRecord
    ) -> bool:
        """Store every summary and mark the summary ready, in the caller's transaction.

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
        await self._db.execute(delete(Summary).where(Summary.document_id == document.id))
        stored: list[Summary] = []
        for record in sections:
            summary = Summary(
                document_id=document.id,
                level=record.level,
                ordinal=record.ordinal,
                title=record.title,
                page_start=record.page_start,
                page_end=record.page_end,
                source_chunk_ids=record.source_chunk_ids,
                text=record.text,
                token_count=record.token_count,
                verification=record.verification,
            )
            self._db.add(summary)
            stored.append(summary)
        await self._db.flush()
        self._db.add(
            Summary(
                document_id=document.id,
                level="document",
                ordinal=0,
                title=document_summary.title,
                page_start=document_summary.page_start,
                page_end=document_summary.page_end,
                source_summary_ids=[s.id for s in stored],
                text=document_summary.text,
                token_count=document_summary.token_count,
                verification=document_summary.verification,
            )
        )
        document.summary_status = "ready"
        job.status = "completed"
        job.progress_current = job.progress_total
        job.completed_at = func.now()
        await self._db.flush()
        return True

    async def job_kind(self, job_id: uuid.UUID) -> str | None:
        return await self._db.scalar(select(IngestionJob.kind).where(IngestionJob.id == job_id))

    async def fail_unfinished_jobs(self, reason: str) -> int:
        """Mark every queued or running job, and its document, as failed.

        Called once when the service starts: nothing is running yet, so any job
        still marked unfinished was interrupted by the previous shutdown.
        """
        active = IngestionJob.status.in_(ACTIVE_STATUSES)

        def documents_of(kind: str):  # type: ignore[no-untyped-def]
            return select(IngestionJob.document_id).where(active, IngestionJob.kind == kind)

        # Documents first, then jobs: the same order as every other write.
        await self._db.execute(
            update(Document)
            .where(Document.id.in_(documents_of("index")))
            .values(status="failed", error=reason)
        )
        await self._db.execute(
            update(Document)
            .where(Document.id.in_(documents_of("summary")))
            .values(summary_status="failed")
        )
        result = await self._db.execute(
            update(IngestionJob)
            .where(active)
            .values(status="failed", error=reason, completed_at=func.now())
        )
        assert isinstance(result, CursorResult)
        return result.rowcount

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
