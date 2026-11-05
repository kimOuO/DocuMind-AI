"""Runs processing jobs in the background of the server process.

There is no separate worker or queue service. Jobs wait their turn inside the
process and run a few at a time, which suits a handful of documents; a restart
interrupts them, and the startup recovery then marks them failed so the user
can retry.
"""

import asyncio
import logging
import uuid
from typing import Protocol

from fastapi import Request

logger = logging.getLogger(__name__)


class JobRunner(Protocol):
    async def run(self, job_id: uuid.UUID) -> object: ...


class JobScheduler(Protocol):
    def schedule(self, job_id: uuid.UUID, document_id: uuid.UUID) -> None: ...

    def cancel_document(self, document_id: uuid.UUID) -> None: ...


class NullScheduler:
    """Used when the application was not started: jobs stay queued."""

    def schedule(self, job_id: uuid.UUID, document_id: uuid.UUID) -> None:
        return None

    def cancel_document(self, document_id: uuid.UUID) -> None:
        return None


class InProcessScheduler:
    def __init__(self, runner: JobRunner, *, concurrency: int = 1) -> None:
        self._runner = runner
        self._slots = asyncio.Semaphore(concurrency)
        self._tasks: dict[uuid.UUID, asyncio.Task[None]] = {}

    def schedule(self, job_id: uuid.UUID, document_id: uuid.UUID) -> None:
        """Queue a job. It stays `queued` in the database until its turn comes."""
        task = asyncio.create_task(self._run(job_id), name=f"job-{job_id}")
        self._tasks[document_id] = task
        task.add_done_callback(lambda done: self._forget(document_id, done))

    def cancel_document(self, document_id: uuid.UUID) -> None:
        """Stop the job of a deleted document as soon as possible.

        This only saves work. Correctness does not depend on it: a job always
        checks that its document still exists before it writes.
        """
        task = self._tasks.get(document_id)
        if task is not None:
            task.cancel()

    async def wait_until_idle(self) -> None:
        while self._tasks:
            await asyncio.gather(*self._tasks.values(), return_exceptions=True)
            await asyncio.sleep(0)

    async def shutdown(self) -> None:
        for task in list(self._tasks.values()):
            task.cancel()
        await self.wait_until_idle()

    async def _run(self, job_id: uuid.UUID) -> None:
        async with self._slots:
            try:
                await self._runner.run(job_id)
            except Exception:
                logger.exception("Job %s raised outside its own error handling", job_id)

    def _forget(self, document_id: uuid.UUID, task: asyncio.Task[None]) -> None:
        if self._tasks.get(document_id) is task:
            del self._tasks[document_id]


_NOT_STARTED = NullScheduler()


def get_job_scheduler(request: Request) -> JobScheduler:
    scheduler: JobScheduler = getattr(request.app.state, "job_scheduler", _NOT_STARTED)
    return scheduler
