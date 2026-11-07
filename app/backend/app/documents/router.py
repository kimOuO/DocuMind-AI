"""HTTP endpoints for documents: upload, list, read, delete, retry, progress."""

import uuid
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, Path, Request, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import current_user
from app.core.database import get_session, get_sessionmaker
from app.core.env_loader import Settings, get_settings
from app.core.errors import ApiError
from app.core.sse import SSE_HEADERS
from app.documents.service import DocumentService, DocumentView
from app.documents.storage import FileStorage
from app.ingestion.events import document_event_stream, format_sse, read_snapshot
from app.ingestion.scheduler import JobScheduler, get_job_scheduler
from app.models import User

router = APIRouter(tags=["documents"])

# How often the progress stream looks for changes.
EVENT_POLL_SECONDS = 0.5

DocumentId = Annotated[uuid.UUID, Path(alias="id")]


class JobResponse(BaseModel):
    id: uuid.UUID
    kind: str
    status: str
    stage: str | None
    progress_current: int | None
    progress_total: int | None
    retry_count: int
    error: str | None
    started_at: datetime | None
    completed_at: datetime | None


class DocumentResponse(BaseModel):
    id: uuid.UUID
    filename: str
    media_type: str
    file_size: int
    status: str
    summary_status: str
    build_summary: bool
    error: str | None
    page_count: int | None
    chunk_count: int
    created_at: datetime
    updated_at: datetime


class DocumentDetailResponse(DocumentResponse):
    jobs: list[JobResponse]


def _summary(view: DocumentView) -> DocumentResponse:
    d = view.document
    return DocumentResponse(
        id=d.id,
        filename=d.filename,
        media_type=d.media_type,
        file_size=d.file_size,
        status=d.status,
        summary_status=d.summary_status,
        build_summary=d.build_summary,
        error=d.error,
        page_count=d.page_count,
        chunk_count=view.chunk_count,
        created_at=d.created_at,
        updated_at=d.updated_at,
    )


def _detail(view: DocumentView) -> DocumentDetailResponse:
    jobs = [
        JobResponse(
            id=j.id,
            kind=j.kind,
            status=j.status,
            stage=j.stage,
            progress_current=j.progress_current,
            progress_total=j.progress_total,
            retry_count=j.retry_count,
            error=j.error,
            started_at=j.started_at,
            completed_at=j.completed_at,
        )
        for j in view.jobs
    ]
    return DocumentDetailResponse(**_summary(view).model_dump(), jobs=jobs)


def get_document_service(
    db: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
    scheduler: JobScheduler = Depends(get_job_scheduler),
) -> DocumentService:
    return DocumentService(db, settings, FileStorage(settings.data_dir), scheduler)


@router.post("/documents", status_code=202, response_model=DocumentDetailResponse)
async def upload_document(
    response: Response,
    file: UploadFile = File(...),
    build_summary: bool = Form(True),
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentDetailResponse:
    view, created = await service.upload(user, file, build_summary=build_summary)
    if not created:
        # Same content uploaded again by the same user: nothing new was queued.
        response.status_code = 200
    return _detail(view)


@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents(
    user: User = Depends(current_user), service: DocumentService = Depends(get_document_service)
) -> list[DocumentResponse]:
    return [_summary(view) for view in await service.list_documents(user)]


@router.get("/documents/{id}", response_model=DocumentDetailResponse)
async def read_document(
    document_id: DocumentId,
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentDetailResponse:
    return _detail(await service.get(user, document_id))


@router.get("/documents/{id}/file")
async def document_file(
    document_id: DocumentId,
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> FileResponse:
    """The original file, shown inline so that a browser opens a PDF at `#page=N` (D89)."""
    path, media_type, filename = await service.file(user, document_id)
    ascii_name = filename.encode("ascii", "ignore").decode() or "document"
    disposition = f"inline; filename=\"{ascii_name}\"; filename*=UTF-8''{quote(filename)}"
    return FileResponse(
        path,
        media_type=media_type,
        headers={"Content-Disposition": disposition, "Cache-Control": "private, no-store"},
    )


@router.delete("/documents/{id}", status_code=204)
async def delete_document(
    document_id: DocumentId,
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> None:
    await service.delete(user, document_id)


@router.post("/documents/{id}/retry", status_code=202, response_model=DocumentDetailResponse)
async def retry_document(
    document_id: DocumentId,
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentDetailResponse:
    return _detail(await service.retry(user, document_id))


@router.get("/documents/{id}/events")
async def document_events(
    document_id: DocumentId,
    request: Request,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_session),
) -> StreamingResponse:
    """Processing progress as server-sent events; ends with `done`."""
    sessions = get_sessionmaker()
    owner_id = user.id
    if await read_snapshot(sessions, owner_id, document_id) is None:
        # Same answer whether it does not exist or belongs to someone else.
        raise ApiError(404, "DOCUMENT_NOT_FOUND", "Document not found.")
    # The stream can stay open for a long time and reads through short sessions
    # of its own, so the request's database connection is released now.
    await db.close()

    async def body() -> AsyncIterator[str]:
        events = document_event_stream(
            lambda: read_snapshot(sessions, owner_id, document_id),
            interval=EVENT_POLL_SECONDS,
            is_disconnected=request.is_disconnected,
        )
        async for event in events:
            yield format_sse(event)

    return StreamingResponse(
        body(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )
