"""Text embeddings from the local Ollama server.

The embedder sits behind a Protocol so that unit and integration tests can use
a fake one and never need a running model.
"""

from typing import Protocol

import httpx

from app.core.env_loader import Settings
from app.llm.ollama_api import embed_request
from app.models import EMBEDDING_DIMENSIONS


def _spellings(text: str) -> list[str]:
    """Equivalent spellings of a text, for a model that cannot embed the original."""
    stripped = text.rstrip(" .!?。！？")
    normalised = " ".join(text.split()) + "\n"
    return [stripped, normalised, stripped.lower(), text.lower()]


class EmbeddingError(RuntimeError):
    """The embeddings could not be produced. The message says why."""


class EmbeddingInputError(EmbeddingError):
    """The model could not compute a vector for this particular text (it answered with
    NaN values), while the service itself is up. Seen with bge-m3 on the GPU for some
    phrases (D70); the same text embeds on the CPU. Rewording the text is the way out."""


class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class OllamaEmbedder:
    def __init__(
        self,
        settings: Settings,
        *,
        timeout_seconds: float = 120,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._settings = settings
        self._timeout = timeout_seconds
        self._transport = transport

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """One vector per text, in the same order.

        bge-m3 on the GPU answers NaN for a few texts (D88: "Compare condition C2 with vector
        RAG (SS) … datasets." — with the final full stop; without it, or in lower case, it
        embeds). Equivalent spellings are tried in turn before the error is raised: without
        trailing punctuation, with normalised whitespace and a newline, in lower case. In a
        batch, the texts are embedded one by one so that the retries apply to the one that
        fails."""
        if not texts:
            return []
        try:
            return await self._embed(texts)
        except EmbeddingInputError:
            if len(texts) > 1:
                vectors = []
                for text in texts:
                    vectors.extend(await self.embed([text]))
                return vectors
            tried = {texts[0]}
            for variant in _spellings(texts[0]):
                if variant in tried:
                    continue
                tried.add(variant)
                try:
                    return await self._embed([variant])
                except EmbeddingInputError:
                    continue
            raise

    async def _embed(self, texts: list[str]) -> list[list[float]]:
        request = embed_request(self._settings, texts)
        try:
            async with httpx.AsyncClient(
                base_url=self._settings.ollama_base_url,
                timeout=self._timeout,
                transport=self._transport,
            ) as client:
                response = await client.post(request.path, json=request.body)
        except httpx.HTTPError as error:
            raise EmbeddingError(f"The embedding service could not be reached: {error}") from error

        if response.status_code != 200:
            if "NaN" in response.text:
                raise EmbeddingInputError(
                    "The embedding model could not compute a vector for this text "
                    f"(it answered {response.status_code}: {response.text[:200]})"
                )
            raise EmbeddingError(
                f"The embedding service answered {response.status_code}: {response.text[:200]}"
            )
        try:
            vectors = response.json().get("embeddings") or []
        except ValueError as error:
            raise EmbeddingError("The embedding service reply is not valid JSON.") from error

        if len(vectors) != len(texts):
            raise EmbeddingError(
                f"The embedding service returned {len(vectors)} vectors for {len(texts)} texts."
            )
        if any(len(vector) != EMBEDDING_DIMENSIONS for vector in vectors):
            raise EmbeddingError(
                f"The embedding service returned vectors that do not have "
                f"{EMBEDDING_DIMENSIONS} dimensions."
            )
        return [list(vector) for vector in vectors]
