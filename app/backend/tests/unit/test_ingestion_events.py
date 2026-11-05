"""Progress events: what is sent when the state of a document changes."""

import json
import uuid

from app.ingestion.events import (
    DocumentSnapshot,
    Event,
    JobSnapshot,
    document_event_stream,
    format_sse,
)

JOB = uuid.uuid4()


def job(status: str, stage: str | None = None, current: int | None = None, total: int | None = None,
        error: str | None = None, job_id: uuid.UUID = JOB) -> JobSnapshot:  # fmt: skip
    return JobSnapshot(job_id, "index", status, stage, current, total, error)


def document(
    status: str, latest: JobSnapshot | None, summary_status: str = "none"
) -> DocumentSnapshot:
    return DocumentSnapshot(status, summary_status, latest)


async def collect(
    snapshots: list[DocumentSnapshot | None], *, disconnect_after: int | None = None
) -> list[Event]:
    remaining = list(snapshots)
    reads = 0

    async def read() -> DocumentSnapshot | None:
        nonlocal reads
        reads += 1
        return remaining.pop(0)

    async def is_disconnected() -> bool:
        return disconnect_after is not None and reads >= disconnect_after

    stream = document_event_stream(read, interval=0, is_disconnected=is_disconnected)
    return [event async for event in stream]


async def test_a_ready_document_reports_its_status_and_is_done() -> None:
    events = await collect([document("ready", job("completed", "embedding", 48, 48))])

    assert events == [
        Event("status", {"status": "ready", "summary_status": "none"}),
        Event("done", {"status": "ready", "summary_status": "none"}),
    ]


async def test_a_failed_document_reports_the_reason_and_is_done() -> None:
    events = await collect([document("failed", job("failed", "embedding", 16, 48, "service down"))])

    assert events == [
        Event("status", {"status": "failed", "summary_status": "none"}),
        Event("error", {"kind": "index", "detail": "service down"}),
        Event("done", {"status": "failed", "summary_status": "none"}),
    ]


async def test_progress_is_reported_as_the_job_advances_until_the_document_is_ready() -> None:
    events = await collect(
        [
            document("uploaded", job("queued")),
            document("processing", job("running", "parsing")),
            document("processing", job("running", "parsing")),  # nothing changed: nothing sent
            document("processing", job("running", "embedding", 0, 48)),
            document("processing", job("running", "embedding", 16, 48)),
            document("ready", job("completed", "embedding", 48, 48)),
        ]
    )

    assert events == [
        Event("status", {"status": "uploaded", "summary_status": "none"}),
        Event("status", {"status": "processing", "summary_status": "none"}),
        Event("progress", {"kind": "index", "stage": "parsing", "current": None, "total": None}),
        Event("progress", {"kind": "index", "stage": "embedding", "current": 0, "total": 48}),
        Event("progress", {"kind": "index", "stage": "embedding", "current": 16, "total": 48}),
        Event("status", {"status": "ready", "summary_status": "none"}),
        Event("done", {"status": "ready", "summary_status": "none"}),
    ]


async def test_connecting_in_the_middle_of_a_job_sends_the_current_progress_first() -> None:
    events = await collect(
        [
            document("processing", job("running", "embedding", 32, 48)),
            document("ready", job("completed", "embedding", 48, 48)),
        ]
    )

    assert events[:2] == [
        Event("status", {"status": "processing", "summary_status": "none"}),
        Event("progress", {"kind": "index", "stage": "embedding", "current": 32, "total": 48}),
    ]


async def test_a_failure_during_the_stream_is_reported_once() -> None:
    events = await collect(
        [
            document("processing", job("running", "embedding", 0, 48)),
            document("failed", job("failed", "embedding", 0, 48, "service down")),
        ]
    )

    assert events[2:] == [
        Event("status", {"status": "failed", "summary_status": "none"}),
        Event("error", {"kind": "index", "detail": "service down"}),
        Event("done", {"status": "failed", "summary_status": "none"}),
    ]


async def test_a_document_deleted_during_the_stream_ends_it() -> None:
    events = await collect([document("processing", job("running", "parsing")), None])

    assert events[-1] == Event("error", {"kind": None, "detail": "The document no longer exists."})
    assert all(event.name != "done" for event in events)


async def test_the_stream_stops_when_the_client_goes_away() -> None:
    events = await collect(
        [document("processing", job("running", "parsing")), document("ready", job("completed"))],
        disconnect_after=1,
    )

    assert [event.name for event in events] == ["status", "progress"]


async def test_nothing_is_sent_for_a_document_that_does_not_exist() -> None:
    assert await collect([None]) == []


def test_events_use_the_server_sent_events_format() -> None:
    text = format_sse(
        Event("progress", {"kind": "index", "stage": "embedding", "current": 2, "total": 5})
    )

    assert text.startswith("event: progress\ndata: ")
    assert text.endswith("\n\n")
    assert json.loads(text.split("data: ", 1)[1]) == {
        "kind": "index",
        "stage": "embedding",
        "current": 2,
        "total": 5,
    }
