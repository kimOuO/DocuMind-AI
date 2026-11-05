"""Stand-ins for external services, used by tests instead of the real ones."""

import hashlib
import math
from collections.abc import Awaitable, Callable

from app.llm.embedding import EmbeddingError
from app.models import EMBEDDING_DIMENSIONS


def fake_vector(text: str) -> list[float]:
    """A deterministic unit vector derived from the text."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [digest[index % len(digest)] / 255 + 0.01 for index in range(EMBEDDING_DIMENSIONS)]
    norm = math.sqrt(sum(value * value for value in values))
    return [value / norm for value in values]


class FakeEmbedder:
    """Embeds without a model. Can fail on a chosen call or pause before one."""

    def __init__(
        self,
        *,
        fail_on_call: int | None = None,
        before_call: Callable[[int], Awaitable[None]] | None = None,
    ) -> None:
        self.calls: list[list[str]] = []
        self._fail_on_call = fail_on_call
        self._before_call = before_call

    async def embed(self, texts: list[str]) -> list[list[float]]:
        index = len(self.calls)
        self.calls.append(list(texts))
        if self._before_call is not None:
            await self._before_call(index)
        if self._fail_on_call == index:
            raise EmbeddingError("The embedding service answered 500: simulated failure")
        return [fake_vector(text) for text in texts]
