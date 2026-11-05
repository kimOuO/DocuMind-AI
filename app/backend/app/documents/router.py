"""HTTP endpoints for documents: upload, list, read, delete."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Path, Response, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import current_user
from app.core.database import get_session
from app.core.env_loader import Settings, get_settings
from app.documents.service import DocumentService, DocumentView
from app.documents.storage import FileStorage
from app.models import User

router = APIRouter(tags=["documents"])

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
    db: AsyncSession = Depends(get_session), settings: Settings = Depends(get_settings)
) -> DocumentService:
    return DocumentService(db, settings, FileStorage(settings.data_dir))


@router.post("/documents", status_code=202, response_model=DocumentDetailResponse)
async def upload_document(
    response: Response,
    file: UploadFile = File(...),
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentDetailResponse:
    view, created = await service.upload(user, file)
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


@router.delete("/documents/{id}", status_code=204)
async def delete_document(
    document_id: DocumentId,
    user: User = Depends(current_user),
    service: DocumentService = Depends(get_document_service),
) -> None:
    await service.delete(user, document_id)
