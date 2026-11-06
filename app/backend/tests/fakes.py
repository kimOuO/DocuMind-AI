"""Stand-ins for external services, used by tests instead of the real ones."""

import asyncio
import hashlib
import json
import math
import re
from collections.abc import Awaitable, Callable

import httpx

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


class RecordingScheduler:
    """Records what would have been run in the background, without running it."""

    def __init__(self) -> None:
        self.scheduled: list[tuple[str, str]] = []
        self.cancelled: list[str] = []

    def schedule(self, job_id, document_id) -> None:  # type: ignore[no-untyped-def]
        self.scheduled.append((str(job_id), str(document_id)))

    def cancel_document(self, document_id) -> None:  # type: ignore[no-untyped-def]
        self.cancelled.append(str(document_id))


class StubSummariser:
    """Plays the model for summary calls: answers from what the prompt asked for."""

    def __init__(
        self,
        *,
        fail_on_call: int | None = None,
        cut_short: bool = False,
        cut_short_calls: frozenset[int] = frozenset(),
    ) -> None:
        self.prompts: list[str] = []
        self.fail_on_call = fail_on_call
        self.cut_short = cut_short  # every call is cut short
        self.cut_short_calls = cut_short_calls  # only these calls (by index) are cut short
        self.pause: asyncio.Event | None = None

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert (body["truncate"], body["shift"]) == (False, False)
        assert body["options"]["num_ctx"] == 10_000 and body["options"]["num_predict"] == 1_500
        prompt = body["prompt"]
        self.prompts.append(prompt)
        if self.fail_on_call == len(self.prompts) - 1:
            return httpx.Response(500, json={"error": "model failed to load"})
        section = re.search(r"^Section: (.*)$", prompt, flags=re.M)
        if section:
            pages = re.search(r"^Pages: (.*)$", prompt, flags=re.M)
            first_page = pages.group(1).split("-")[0]  # type: ignore[union-attr]
            text = f"Summary of {section.group(1)}: key figure 67.6% (p. {first_page})."
        elif prompt.rstrip().endswith("Condensed summary:"):
            text = "Condensed: " + " ".join(re.findall(r"Summary of ([^:]+):", prompt))
        else:
            text = "Overall: the document proposes LightRAG; results 67.6% (p. 8)."
        cut = self.cut_short or (len(self.prompts) - 1) in self.cut_short_calls
        return httpx.Response(
            200,
            json={
                "response": text,
                "done": True,
                "done_reason": "length" if cut else "stop",
                "prompt_eval_count": 1_200,
                "eval_count": 300 if cut else 40,
            },
        )
