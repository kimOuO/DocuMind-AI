"""Database tables. See docs/02-specs/03-interfaces.md, section 3.

All tables needed in P2 are defined here; ``summaries`` is added in P3.
"""

import uuid
from datetime import datetime
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

EMBEDDING_DIMENSIONS = 1024

DOCUMENT_STATUSES = ("uploaded", "processing", "ready", "failed")
SUMMARY_STATUSES = ("none", "processing", "ready", "failed")
JOB_KINDS = ("index", "summary")
JOB_STATUSES = ("queued", "running", "completed", "failed")
MESSAGE_ROLES = ("user", "assistant")
MESSAGE_STATUSES = ("pending", "streaming", "completed", "failed", "interrupted")
LLM_CALL_STATUSES = ("pending", "completed", "failed", "interrupted")
SUMMARY_LEVELS = ("section", "document")
LLM_FINISH_REASONS = ("stop", "output_limit", "context_exhausted", "client_disconnect", "unknown")


def _in(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


class Base(DeclarativeBase):
    pass


def _pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def _created() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), server_default=func.now())


def _updated() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = _pk()
    username: Mapped[str] = mapped_column(Text, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    display_name: Mapped[str] = mapped_column(Text)
    answer_language: Mapped[str] = mapped_column(Text, server_default="auto")
    answer_detail: Mapped[str] = mapped_column(Text, server_default="normal")
    created_at: Mapped[datetime] = _created()
    updated_at: Mapped[datetime] = _updated()
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = _pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(Text, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = _created()


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        UniqueConstraint("owner_id", "content_hash", name="uq_documents_owner_content"),
        CheckConstraint(_in("status", DOCUMENT_STATUSES), name="ck_documents_status"),
        CheckConstraint(
            _in("summary_status", SUMMARY_STATUSES), name="ck_documents_summary_status"
        ),
    )

    id: Mapped[uuid.UUID] = _pk()
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    filename: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(Text)
    media_type: Mapped[str] = mapped_column(Text)
    file_size: Mapped[int] = mapped_column(BigInteger)
    storage_path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, server_default="uploaded")
    summary_status: Mapped[str] = mapped_column(Text, server_default="none")
    error: Mapped[str | None] = mapped_column(Text)
    page_count: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = _created()
    updated_at: Mapped[datetime] = _updated()


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"
    __table_args__ = (
        CheckConstraint(_in("kind", JOB_KINDS), name="ck_ingestion_jobs_kind"),
        CheckConstraint(_in("status", JOB_STATUSES), name="ck_ingestion_jobs_status"),
        # At most one queued or running job per document and kind.
        Index(
            "uq_ingestion_jobs_active",
            "document_id",
            "kind",
            unique=True,
            postgresql_where=text("status IN ('queued', 'running')"),
        ),
    )

    id: Mapped[uuid.UUID] = _pk()
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, server_default="queued")
    stage: Mapped[str | None] = mapped_column(Text)
    progress_current: Mapped[int | None] = mapped_column(Integer)
    progress_total: Mapped[int | None] = mapped_column(Integer)
    retry_count: Mapped[int] = mapped_column(Integer, server_default="0")
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = _created()
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Chunk(Base):
    __tablename__ = "chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "ordinal", name="uq_chunks_document_ordinal"),
        Index(
            "ix_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[uuid.UUID] = _pk()
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    ordinal: Mapped[int] = mapped_column(Integer)
    page: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIMENSIONS))
    created_at: Mapped[datetime] = _created()


class Summary(Base):
    __tablename__ = "summaries"
    __table_args__ = (
        CheckConstraint(_in("level", SUMMARY_LEVELS), name="ck_summaries_level"),
        UniqueConstraint(
            "document_id", "level", "ordinal", name="uq_summaries_document_level_ordinal"
        ),
    )

    id: Mapped[uuid.UUID] = _pk()
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    level: Mapped[str] = mapped_column(Text)
    ordinal: Mapped[int] = mapped_column(Integer)  # section order; 0 for the document summary
    title: Mapped[str | None] = mapped_column(Text)
    page_start: Mapped[int] = mapped_column(Integer)
    page_end: Mapped[int] = mapped_column(Integer)
    # Section summary: the chunks of the pages it was made from. Document summary: empty.
    source_chunk_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), server_default=text("'{}'::uuid[]")
    )
    # Document summary: the section summaries it was merged from. Section summary: empty.
    source_summary_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), server_default=text("'{}'::uuid[]")
    )
    text: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer)
    # D76: how the summary's figures stood against the chunks of its pages when it was
    # stored: {"status": VERIFIED|CONTRADICTED|UNCERTAIN|NOT_CHECKED, "contradicted": [...],
    # "unverified": [...], "unresolved": [...], "checked_figures": n}; null for older rows.
    verification: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = _created()


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = _pk()
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(Text, server_default="")
    created_at: Mapped[datetime] = _created()
    updated_at: Mapped[datetime] = _updated()


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint(_in("role", MESSAGE_ROLES), name="ck_messages_role"),
        CheckConstraint(_in("status", MESSAGE_STATUSES), name="ck_messages_status"),
    )

    id: Mapped[uuid.UUID] = _pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, server_default="")
    sources: Mapped[list[dict[str, object]]] = mapped_column(
        JSONB, server_default=text("'[]'::jsonb")
    )
    status: Mapped[str] = mapped_column(Text)
    answered: Mapped[bool | None] = mapped_column(Boolean)
    created_at: Mapped[datetime] = _created()
    updated_at: Mapped[datetime] = _updated()


class LLMCall(Base):
    __tablename__ = "llm_calls"
    __table_args__ = (
        CheckConstraint(_in("status", LLM_CALL_STATUSES), name="ck_llm_calls_status"),
        CheckConstraint(
            _in("finish_reason", LLM_FINISH_REASONS), name="ck_llm_calls_finish_reason"
        ),
    )

    id: Mapped[uuid.UUID] = _pk()
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    # Kept for audit when the related object is deleted: the reference is cleared.
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("conversations.id", ondelete="SET NULL")
    )
    message_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL")
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL")
    )
    purpose: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, server_default="pending")
    estimated_prompt_tokens: Mapped[int] = mapped_column(Integer)
    max_output_tokens: Mapped[int] = mapped_column(Integer)
    # Measured values reported by Ollama only. NULL means "not known".
    prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    completion_tokens: Mapped[int | None] = mapped_column(Integer)
    received_output_tokens_estimated: Mapped[int | None] = mapped_column(Integer)
    # How the call ended, when it did end normally or was interrupted. NULL for a failed call.
    finish_reason: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = _created()
    updated_at: Mapped[datetime] = _updated()
