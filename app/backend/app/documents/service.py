"""Rules for uploading, listing, reading and deleting documents.

Every method takes the acting user explicitly; ownership is enforced here and in
the repository, never in the router.
"""

import uuid
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.documents.repository import DocumentRepository
from app.documents.storage import FileStorage, UploadTooLarge
from app.ingestion.scheduler import JobScheduler
from app.models import Document, IngestionJob, User

SUPPORTED_EXTENSIONS = {".pdf": "pdf", ".txt": "txt", ".md": "md"}
MAX_FILENAME_LENGTH = 255


@dataclass(frozen=True)
class DocumentView:
    document: Document
    chunk_count: int = 0
    jobs: list[IngestionJob] = field(default_factory=list)


def clean_filename(raw: str | None) -> str:
    """Keep only the final path component of a client-supplied file name."""
    name = PurePosixPath((raw or "").replace("\\", "/")).name.strip()
    return name[:MAX_FILENAME_LENGTH]


class DocumentService:
    def __init__(
        self, db: AsyncSession, settings: Settings, storage: FileStorage, scheduler: JobScheduler
    ) -> None:
        self._db = db
        self._repo = DocumentRepository(db)
        self._settings = settings
        self._storage = storage
        self._scheduler = scheduler

    async def upload(self, actor: User, upload: UploadFile) -> tuple[DocumentView, bool]:
        """Store an uploaded file and queue it for indexing.

        Returns the document and whether it was newly created. Uploading the
        same content again, as the same user, returns the existing document.
        """
        filename = clean_filename(upload.filename)
        extension = PurePosixPath(filename).suffix.lower()
        if not filename or extension not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ApiError(
                415, "UNSUPPORTED_MEDIA_TYPE", f"Unsupported file type. Supported: {supported}."
            )

        limit_mb = self._settings.max_upload_mb
        try:
            received = await self._storage.receive(upload, limit_mb * 1024 * 1024)
        except UploadTooLarge as exc:
            raise ApiError(
                413, "FILE_TOO_LARGE", f"The file is larger than {limit_mb} MB."
            ) from exc
        if received.size == 0:
            self._storage.discard(received.temp_path)
            raise ApiError(422, "EMPTY_FILE", "The file is empty.")

        existing = await self._repo.get_by_hash(actor.id, received.sha256)
        if existing is not None:
            self._storage.discard(received.temp_path)
            return await self._view(existing), False

        document_id = uuid.uuid4()
        relative_path = self._storage.relative_path(actor.id, document_id, extension)
        self._storage.commit(received, relative_path)
        document = Document(
            id=document_id,
            owner_id=actor.id,
            filename=filename,
            content_hash=received.sha256,
            media_type=SUPPORTED_EXTENSIONS[extension],
            file_size=received.size,
            storage_path=relative_path,
        )
        try:
            # The document and its first indexing job are created together.
            job = await self._repo.add_with_index_job(document)
            await self._db.commit()
        except IntegrityError:
            # The same content was uploaded concurrently by the same user.
            await self._db.rollback()
            self._storage.delete(relative_path)
            existing = await self._repo.get_by_hash(actor.id, received.sha256)
            if existing is None:
                raise
            return await self._view(existing), False
        except BaseException:
            await self._db.rollback()
            self._storage.delete(relative_path)
            raise
        # Only after the commit: the background job reads what was just stored.
        self._scheduler.schedule(job.id, document.id)
        return await self._view(document), True

    async def list_documents(self, actor: User) -> list[DocumentView]:
        documents = await self._repo.list_for_owner(actor.id)
        counts = await self._repo.chunk_counts([d.id for d in documents])
        return [DocumentView(d, counts.get(d.id, 0)) for d in documents]

    async def get(self, actor: User, document_id: uuid.UUID) -> DocumentView:
        return await self._view(await self._owned(actor, document_id))

    async def delete(self, actor: User, document_id: uuid.UUID) -> None:
        document = await self._owned(actor, document_id)
        relative_path = document.storage_path
        await self._repo.delete(document)
        await self._db.commit()
        # The file is removed only after the database change is committed.
        self._storage.delete(relative_path)
        # A job still working on it would write nothing anyway; this just stops it sooner.
        self._scheduler.cancel_document(document_id)

    async def retry(self, actor: User, document_id: uuid.UUID) -> DocumentView:
        """Queue a new attempt at indexing a document whose processing failed."""
        document = await self._repo.get_for_update(actor.id, document_id)
        if document is None:
            await self._db.rollback()
            raise ApiError(404, "DOCUMENT_NOT_FOUND", "Document not found.")
        if document.status != "failed":
            await self._db.rollback()
            raise ApiError(
                409, "RETRY_NOT_ALLOWED", "Only a document whose processing failed can be retried."
            )
        try:
            job = await self._repo.add_retry_job(document, "index")
            document.status = "processing"
            document.error = None
            await self._db.commit()
            # updated_at is set by the database; read it back before it is returned.
            await self._db.refresh(document)
        except IntegrityError as exc:
            # Another job of the same kind is already queued or running.
            await self._db.rollback()
            raise ApiError(
                409, "RETRY_NOT_ALLOWED", "This document is already being processed."
            ) from exc
        self._scheduler.schedule(job.id, document.id)
        return await self._view(document)

    async def _owned(self, actor: User, document_id: uuid.UUID) -> Document:
        document = await self._repo.get(actor.id, document_id)
        if document is None:
            # Same answer whether it does not exist or belongs to someone else.
            raise ApiError(404, "DOCUMENT_NOT_FOUND", "Document not found.")
        return document

    async def _view(self, document: Document) -> DocumentView:
        counts = await self._repo.chunk_counts([document.id])
        jobs = await self._repo.latest_jobs(document.id)
        return DocumentView(document, counts.get(document.id, 0), jobs)
