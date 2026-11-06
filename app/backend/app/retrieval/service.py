"""Deciding what to search, and searching it.

Every method takes the acting user: the search never leaves that user's own
documents.
"""

import uuid
from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.env_loader import Settings
from app.core.errors import ApiError
from app.llm.embedding import Embedder
from app.models import User
from app.retrieval.expansion import MAX_FOLLOWING, table_context, tables_in
from app.retrieval.repository import RetrievalRepository, RetrievedChunk

__all__ = ["RetrievalService", "RetrievedChunk", "SearchScope"]


@dataclass(frozen=True)
class SearchScope:
    """The documents a question is answered from."""

    # "all": every ready document of the user; "selected": the ones they named.
    mode: Literal["all", "selected"]
    document_ids: list[uuid.UUID]


class RetrievalService:
    def __init__(self, db: AsyncSession, embedder: Embedder, settings: Settings) -> None:
        self._repo = RetrievalRepository(db)
        self._embedder = embedder
        self._settings = settings

    async def resolve_scope(self, actor: User, document_ids: list[uuid.UUID] | None) -> SearchScope:
        """Check the requested documents, or fall back to all that are ready.

        Raises 404 if a named document does not exist or belongs to someone
        else, and 409 if a named document is not ready or there is nothing
        ready to search.
        """
        if document_ids:
            wanted = list(dict.fromkeys(document_ids))
            found = {d.id: d for d in await self._repo.documents_in(actor.id, wanted)}
            if len(found) != len(wanted):
                # Same answer whether it does not exist or belongs to someone else.
                raise ApiError(404, "DOCUMENT_NOT_FOUND", "Document not found.")
            not_ready = [found[i] for i in wanted if found[i].status != "ready"]
            if not_ready:
                names = ", ".join(f"{d.filename} ({d.id})" for d in not_ready)
                raise ApiError(
                    409,
                    "DOCUMENT_NOT_READY",
                    f"These documents are not ready to be searched: {names}",
                )
            return SearchScope("selected", wanted)

        ready = await self._repo.ready_document_ids(actor.id)
        if not ready:
            raise ApiError(
                409, "NO_READY_DOCUMENT", "There is no document ready to be searched yet."
            )
        return SearchScope("all", ready)

    async def embed(self, question: str) -> list[float]:
        [embedding] = await self._embedder.embed([question])
        return embedding

    async def search(
        self,
        actor: User,
        scope: SearchScope,
        question: str,
        embedding: list[float] | None = None,
    ) -> list[RetrievedChunk]:
        """The Top-K chunks for the question, shared across the documents in scope. The
        question's embedding may be passed in when the caller already has it."""
        if embedding is None:
            embedding = await self.embed(question)
        return await self._repo.search(
            actor.id, scope.document_ids, embedding, self._settings.top_k
        )

    async def with_table_context(
        self, actor: User, chunks: list[RetrievedChunk]
    ) -> list[RetrievedChunk]:
        """The search results, followed by the discussion of any table among them (D62).

        The added chunks come after the search's own results, so that a tight
        evidence budget drops them first, and carry origin="table_context".
        """
        already = {(c.document_id, c.ordinal) for c in chunks}
        added: list[RetrievedChunk] = []
        for table in tables_in(chunks):
            following = await self._repo.chunks_after(
                actor.id, table.document_id, table.ordinal, limit=MAX_FOLLOWING
            )
            ordinals = {o for d, o in already if d == table.document_id}
            for chunk in table_context(table, following, ordinals):
                if (chunk.document_id, chunk.ordinal) not in already:
                    added.append(chunk)
                    already.add((chunk.document_id, chunk.ordinal))
        return [*chunks, *added]
