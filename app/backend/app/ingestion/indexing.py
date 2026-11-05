"""The index job: turn a stored file into searchable chunks.

    claim -> parse -> chunk -> embed in batches -> store everything at once

Nothing is stored until the end, and then all of it in one transaction, so a
failure at any step leaves no partial chunks. Before each step the job checks
that it is still wanted: if its document was deleted, it stops without writing.
"""

import asyncio
import logging
import uuid
from enum import StrEnum

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.env_loader import Settings
from app.documents.storage import FileStorage
from app.ingestion.chunking import ChunkDraft, ChunkTokenizer, chunk_pages
from app.ingestion.parsing import DocumentParseError, parse_document
from app.ingestion.repository import ChunkRecord, IngestionRepository
from app.llm.embedding import Embedder, EmbeddingError

logger = logging.getLogger(__name__)

EMBED_BATCH_SIZE = 16
MAX_REASON_LENGTH = 500


class JobOutcome(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    # The job was not run, or stopped without writing: it was not queued, or its
    # document was deleted in the meantime.
    ABANDONED = "abandoned"


class IndexJobRunner:
    def __init__(
        self,
        *,
        sessions: async_sessionmaker[AsyncSession],
        storage: FileStorage,
        tokenizer: ChunkTokenizer,
        embedder: Embedder,
        settings: Settings,
    ) -> None:
        self._sessions = sessions
        self._storage = storage
        self._tokenizer = tokenizer
        self._embedder = embedder
        self._settings = settings
        # The summary job queued by each completed index job, for the dispatcher.
        self.queued_summary_jobs: dict[uuid.UUID, uuid.UUID] = {}

    async def run(self, job_id: uuid.UUID) -> JobOutcome:
        async with self._sessions() as session, session.begin():
            claimed = await IngestionRepository(session).claim_index_job(job_id)
        if claimed is None:
            return JobOutcome.ABANDONED

        try:
            path = self._storage.absolute(claimed.storage_path)
            pages = await asyncio.to_thread(parse_document, path, claimed.media_type)

            if not await self._progress(job_id, "chunking", None, None):
                return JobOutcome.ABANDONED
            drafts = await asyncio.to_thread(
                chunk_pages,
                pages,
                self._tokenizer,
                chunk_size=self._settings.chunk_size,
                overlap=self._settings.chunk_overlap,
            )

            vectors: list[list[float]] = []
            for start in range(0, len(drafts), EMBED_BATCH_SIZE):
                # Also the moment to notice that the document was deleted.
                if not await self._progress(job_id, "embedding", len(vectors), len(drafts)):
                    return JobOutcome.ABANDONED
                batch = drafts[start : start + EMBED_BATCH_SIZE]
                vectors.extend(await self._embedder.embed([draft.text for draft in batch]))

            async with self._sessions() as session, session.begin():
                summary_job = await IngestionRepository(session).complete_index_job(
                    job_id, page_count=len(pages), chunks=_records(drafts, vectors)
                )
            if summary_job is None:
                return JobOutcome.ABANDONED
            self.queued_summary_jobs[job_id] = summary_job
            return JobOutcome.COMPLETED
        except (DocumentParseError, EmbeddingError) as error:
            return await self._fail(job_id, str(error))
        except Exception:
            logger.exception("Index job %s failed unexpectedly", job_id)
            return await self._fail(job_id, "The document could not be processed.")

    async def _progress(
        self, job_id: uuid.UUID, stage: str, current: int | None, total: int | None
    ) -> bool:
        async with self._sessions() as session, session.begin():
            return await IngestionRepository(session).set_progress(job_id, stage, current, total)

    async def _fail(self, job_id: uuid.UUID, reason: str) -> JobOutcome:
        async with self._sessions() as session, session.begin():
            failed = await IngestionRepository(session).fail_job(job_id, reason[:MAX_REASON_LENGTH])
        return JobOutcome.FAILED if failed else JobOutcome.ABANDONED


def _records(drafts: list[ChunkDraft], vectors: list[list[float]]) -> list[ChunkRecord]:
    if len(drafts) != len(vectors):
        raise EmbeddingError(
            f"Expected {len(drafts)} embeddings for the chunks, received {len(vectors)}."
        )
    return [
        ChunkRecord(draft.ordinal, draft.page, draft.text, draft.token_count, vector)
        for draft, vector in zip(drafts, vectors, strict=True)
    ]
