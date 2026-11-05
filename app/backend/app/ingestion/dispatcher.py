"""Run whichever kind of job a job id refers to.

An index job that completes queues the summary job of its document; the
dispatcher runs that summary job right after, in the same background task, so
a document is processed from upload to summary without a queue service.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.ingestion.indexing import IndexJobRunner, JobOutcome
from app.ingestion.repository import IngestionRepository
from app.summarization.service import SummaryJobRunner


class JobDispatcher:
    def __init__(
        self,
        *,
        sessions: async_sessionmaker[AsyncSession],
        index_runner: IndexJobRunner,
        summary_runner: SummaryJobRunner,
    ) -> None:
        self._sessions = sessions
        self._index = index_runner
        self._summary = summary_runner

    async def run(self, job_id: uuid.UUID) -> None:
        async with self._sessions() as session:
            kind = await IngestionRepository(session).job_kind(job_id)
        if kind == "index":
            outcome = await self._index.run(job_id)
            summary_job = self._index.queued_summary_jobs.pop(job_id, None)
            if outcome is JobOutcome.COMPLETED and summary_job is not None:
                await self._summary.run(summary_job)
        elif kind == "summary":
            await self._summary.run(job_id)
