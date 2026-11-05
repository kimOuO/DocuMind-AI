"""Running jobs in the background of the server process."""

import asyncio
import uuid

from app.ingestion.scheduler import InProcessScheduler, NullScheduler


class StubRunner:
    """Stands in for the index job runner: records calls, can block or fail."""

    def __init__(self) -> None:
        self.started: list[uuid.UUID] = []
        self.finished: list[uuid.UUID] = []
        self.release = asyncio.Event()
        self.fail: set[uuid.UUID] = set()

    async def run(self, job_id: uuid.UUID) -> None:
        self.started.append(job_id)
        if job_id in self.fail:
            raise RuntimeError("boom")
        await self.release.wait()
        self.finished.append(job_id)


async def _settle() -> None:
    for _ in range(5):
        await asyncio.sleep(0)


async def test_a_scheduled_job_runs_in_the_background() -> None:
    runner = StubRunner()
    scheduler = InProcessScheduler(runner)
    job = uuid.uuid4()

    scheduler.schedule(job, uuid.uuid4())
    await _settle()
    assert runner.started == [job] and runner.finished == []

    runner.release.set()
    await scheduler.wait_until_idle()
    assert runner.finished == [job]


async def test_jobs_run_one_at_a_time_in_the_order_they_were_scheduled() -> None:
    runner = StubRunner()
    scheduler = InProcessScheduler(runner)
    first, second = uuid.uuid4(), uuid.uuid4()

    scheduler.schedule(first, uuid.uuid4())
    scheduler.schedule(second, uuid.uuid4())
    await _settle()
    # The second job waits: only a few documents are processed at a time.
    assert runner.started == [first]

    runner.release.set()
    await scheduler.wait_until_idle()
    assert runner.finished == [first, second]


async def test_cancelling_a_document_stops_its_job_and_lets_the_next_one_run() -> None:
    runner = StubRunner()
    scheduler = InProcessScheduler(runner)
    first, second = uuid.uuid4(), uuid.uuid4()
    first_document = uuid.uuid4()
    scheduler.schedule(first, first_document)
    scheduler.schedule(second, uuid.uuid4())
    await _settle()

    scheduler.cancel_document(first_document)
    await _settle()
    assert runner.started == [first, second]

    runner.release.set()
    await scheduler.wait_until_idle()
    assert runner.finished == [second]


async def test_cancelling_an_unknown_document_does_nothing() -> None:
    scheduler = InProcessScheduler(StubRunner())

    scheduler.cancel_document(uuid.uuid4())

    await scheduler.wait_until_idle()


async def test_a_job_that_raises_does_not_stop_the_following_ones() -> None:
    runner = StubRunner()
    runner.release.set()
    scheduler = InProcessScheduler(runner)
    bad, good = uuid.uuid4(), uuid.uuid4()
    runner.fail.add(bad)

    scheduler.schedule(bad, uuid.uuid4())
    scheduler.schedule(good, uuid.uuid4())
    await scheduler.wait_until_idle()

    assert runner.finished == [good]


async def test_shutdown_cancels_what_is_still_running() -> None:
    runner = StubRunner()
    scheduler = InProcessScheduler(runner)
    scheduler.schedule(uuid.uuid4(), uuid.uuid4())
    scheduler.schedule(uuid.uuid4(), uuid.uuid4())
    await _settle()

    await scheduler.shutdown()

    assert runner.finished == []
    await scheduler.wait_until_idle()


def test_the_null_scheduler_accepts_everything_and_runs_nothing() -> None:
    scheduler = NullScheduler()

    scheduler.schedule(uuid.uuid4(), uuid.uuid4())
    scheduler.cancel_document(uuid.uuid4())
