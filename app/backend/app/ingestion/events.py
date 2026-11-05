"""Progress of a document's processing, as a stream of events.

The state is read from the database at a short interval and an event is sent
whenever something changed. Because the source is the stored job record, a
client that connects late, reloads the page or reconnects after a restart
still gets the current progress.
"""

import asyncio
import json
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import Document, IngestionJob

ACTIVE_STATUSES = ("queued", "running")


@dataclass(frozen=True)
class JobSnapshot:
    id: uuid.UUID
    kind: str
    status: str
    stage: str | None
    current: int | None
    total: int | None
    error: str | None


@dataclass(frozen=True)
class DocumentSnapshot:
    status: str
    summary_status: str
    # The job in progress if there is one, otherwise the most recent job.
    job: JobSnapshot | None

    @property
    def is_being_processed(self) -> bool:
        return self.job is not None and self.job.status in ACTIVE_STATUSES


@dataclass(frozen=True)
class Event:
    name: str
    data: dict[str, Any]


async def read_snapshot(
    sessions: async_sessionmaker[AsyncSession], owner_id: uuid.UUID, document_id: uuid.UUID
) -> DocumentSnapshot | None:
    """The current state of the owner's document, or None if there is no such document."""
    async with sessions() as session:
        document = (
            await session.execute(
                select(Document.status, Document.summary_status).where(
                    Document.id == document_id, Document.owner_id == owner_id
                )
            )
        ).one_or_none()
        if document is None:
            return None
        job = (
            await session.execute(
                select(
                    IngestionJob.id,
                    IngestionJob.kind,
                    IngestionJob.status,
                    IngestionJob.stage,
                    IngestionJob.progress_current,
                    IngestionJob.progress_total,
                    IngestionJob.error,
                )
                .where(IngestionJob.document_id == document_id)
                .order_by(
                    case((IngestionJob.status.in_(ACTIVE_STATUSES), 0), else_=1),
                    IngestionJob.created_at.desc(),
                    IngestionJob.retry_count.desc(),
                )
                .limit(1)
            )
        ).one_or_none()
    return DocumentSnapshot(
        document.status, document.summary_status, JobSnapshot(*job) if job else None
    )


def _status(snapshot: DocumentSnapshot) -> dict[str, Any]:
    return {"status": snapshot.status, "summary_status": snapshot.summary_status}


def _progress(job: JobSnapshot) -> Event:
    return Event(
        "progress",
        {"kind": job.kind, "stage": job.stage, "current": job.current, "total": job.total},
    )


def _failure(job: JobSnapshot) -> Event:
    return Event("error", {"kind": job.kind, "detail": job.error})


def initial_events(snapshot: DocumentSnapshot) -> list[Event]:
    """What a client is told as soon as it connects."""
    events = [Event("status", _status(snapshot))]
    job = snapshot.job
    if job is not None and job.status == "running":
        events.append(_progress(job))
    if job is not None and job.status == "failed":
        events.append(_failure(job))
    return events


def events_between(previous: DocumentSnapshot, current: DocumentSnapshot) -> list[Event]:
    """What changed between two readings."""
    events = []
    if _status(previous) != _status(current):
        events.append(Event("status", _status(current)))
    job = current.job
    if job is not None and job != previous.job:
        if job.status == "running":
            events.append(_progress(job))
        elif job.status == "failed":
            events.append(_failure(job))
    return events


async def document_event_stream(
    read: Callable[[], Awaitable[DocumentSnapshot | None]],
    *,
    interval: float,
    is_disconnected: Callable[[], Awaitable[bool]],
) -> AsyncIterator[Event]:
    """Events until processing ends. Ends with `done` unless the document disappears."""
    snapshot = await read()
    if snapshot is None:
        return
    for event in initial_events(snapshot):
        yield event

    while snapshot.is_being_processed:
        if await is_disconnected():
            return
        await asyncio.sleep(interval)
        current = await read()
        if current is None:
            yield Event("error", {"kind": None, "detail": "The document no longer exists."})
            return
        for event in events_between(snapshot, current):
            yield event
        snapshot = current

    yield Event("done", _status(snapshot))


def format_sse(event: Event) -> str:
    return f"event: {event.name}\ndata: {json.dumps(event.data, ensure_ascii=False)}\n\n"
