"""The only way the application talks to the language model.

Text in, text out. Every call:

1. is counted locally and refused before sending if the prompt, the safety
   buffer and the room reserved for the answer do not fit the context limit;
2. is recorded in the ledger before it is sent;
3. is sent with the limits that make Ollama itself refuse an over-long input
   and stop when the context is full (see ollama_api);
4. has its outcome recorded: completed (with what Ollama measured and why it
   stopped), failed, or interrupted.

A request refused in step 1 was never sent: it is not an LLM call and is not
recorded in the ledger, only logged.
"""

import asyncio
import json
import logging
import time
import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Protocol

import httpx
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.env_loader import Settings
from app.llm.chat_template import render_prompt
from app.llm.ledger import INPUT_EXCEEDS_CONTEXT, CallContext, LedgerRepository
from app.llm.ollama_api import FinishReason, generate_request, is_input_too_long, read_finish_reason
from app.llm.tokenizer import TokenCounter

logger = logging.getLogger(__name__)

__all__ = [
    "CallContext",
    "ContextBudgetExceeded",
    "LLMCallFailed",
    "LLMChunk",
    "LLMGateway",
    "LLMResult",
    "OllamaGateway",
    "check_budget",
    "estimate_prompt_tokens",
]

LLM_UNAVAILABLE = "LLM_UNAVAILABLE"
MAX_ERROR_LENGTH = 500


class ContextBudgetExceeded(Exception):
    """The call would not fit the context limit. Nothing was sent."""

    def __init__(self, estimated_prompt_tokens: int, max_output_tokens: int, limit: int) -> None:
        self.estimated_prompt_tokens = estimated_prompt_tokens
        self.max_output_tokens = max_output_tokens
        self.limit = limit
        super().__init__(
            f"Prompt ({estimated_prompt_tokens} tokens, estimated) plus reserved output "
            f"({max_output_tokens}) is {estimated_prompt_tokens + max_output_tokens} tokens, "
            f"over the limit of {limit}."
        )


class LLMCallFailed(Exception):
    """The call was sent and did not produce a complete response."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class LLMResult:
    call_id: uuid.UUID
    text: str
    # Measured by Ollama; None when it did not report them.
    prompt_tokens: int | None
    completion_tokens: int | None
    finish_reason: FinishReason


@dataclass(frozen=True)
class LLMChunk:
    """A piece of streamed text. The last chunk carries the result instead."""

    text: str
    result: LLMResult | None = None


class LLMGateway(Protocol):
    async def generate(
        self,
        prompt: str,
        *,
        purpose: str,
        max_output_tokens: int,
        context: CallContext,
        temperature: float | None = None,
    ) -> LLMResult: ...

    def stream(
        self, prompt: str, *, purpose: str, max_output_tokens: int, context: CallContext
    ) -> AsyncIterator[LLMChunk]: ...


def estimate_prompt_tokens(counter: TokenCounter, settings: Settings, prompt: str) -> int:
    """Tokens the prompt will use once Ollama wraps it, plus the safety buffer."""
    rendered = render_prompt(prompt, thinking=settings.llm_thinking)
    return counter.count(rendered) + settings.token_safety_buffer


def check_budget(*, estimated_prompt_tokens: int, max_output_tokens: int, limit: int) -> None:
    if estimated_prompt_tokens + max_output_tokens > limit:
        raise ContextBudgetExceeded(estimated_prompt_tokens, max_output_tokens, limit)


class OllamaGateway:
    def __init__(
        self,
        *,
        settings: Settings,
        sessions: async_sessionmaker[AsyncSession],
        counter: TokenCounter,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout_seconds: float = 600,
    ) -> None:
        self._settings = settings
        self._sessions = sessions
        self._counter = counter
        self._transport = transport
        self._timeout = httpx.Timeout(timeout_seconds, connect=10)

    async def generate(
        self,
        prompt: str,
        *,
        purpose: str,
        max_output_tokens: int,
        context: CallContext,
        temperature: float | None = None,
    ) -> LLMResult:
        """One answer to the prompt. `temperature` overrides the model's default sampling
        for this call only (None keeps it); the budget guard and the ledger apply as ever."""
        call_id, started = await self._open(prompt, purpose, max_output_tokens, context)
        request = generate_request(
            self._settings,
            prompt=prompt,
            max_output_tokens=max_output_tokens,
            stream=False,
            temperature=temperature,
        )
        try:
            async with self._client() as client:
                response = await client.post(request.path, json=request.body)
            if response.status_code != 200:
                raise _rejection(response.status_code, response.text)
            final = response.json()
            if not isinstance(final, dict):
                raise ValueError("unexpected response")
        except LLMCallFailed as failure:
            await self._failed(call_id, started, failure, [])
            raise
        except (httpx.HTTPError, ValueError) as error:
            unavailable = LLMCallFailed(LLM_UNAVAILABLE, str(error) or type(error).__name__)
            await self._failed(call_id, started, unavailable, [])
            raise unavailable from error
        return await self._completed(
            call_id, started, str(final.get("response") or ""), final, max_output_tokens
        )

    async def stream(
        self, prompt: str, *, purpose: str, max_output_tokens: int, context: CallContext
    ) -> AsyncIterator[LLMChunk]:
        call_id, started = await self._open(prompt, purpose, max_output_tokens, context)
        request = generate_request(
            self._settings, prompt=prompt, max_output_tokens=max_output_tokens, stream=True
        )
        received: list[str] = []
        final: dict[str, Any] | None = None
        try:
            async with (
                self._client() as client,
                client.stream("POST", request.path, json=request.body) as response,
            ):
                if response.status_code != 200:
                    body = (await response.aread()).decode("utf-8", errors="replace")
                    raise _rejection(response.status_code, body)
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    if item.get("error"):
                        raise LLMCallFailed(LLM_UNAVAILABLE, str(item["error"]))
                    text = str(item.get("response") or "")
                    if text:
                        received.append(text)
                        yield LLMChunk(text)
                    if item.get("done"):
                        final = item
                        break
            if final is None:
                raise LLMCallFailed(LLM_UNAVAILABLE, "The response ended without a final report.")
        except LLMCallFailed as failure:
            await self._failed(call_id, started, failure, received)
            raise
        except (httpx.HTTPError, ValueError) as error:
            unavailable = LLMCallFailed(LLM_UNAVAILABLE, str(error) or type(error).__name__)
            await self._failed(call_id, started, unavailable, received)
            raise unavailable from error
        except (asyncio.CancelledError, GeneratorExit):
            # The reader went away (for example the browser closed the page).
            await asyncio.shield(self._interrupted(call_id, started, received))
            raise

        result = await self._completed(
            call_id, started, "".join(received), final, max_output_tokens
        )
        yield LLMChunk("", result)

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._settings.ollama_base_url,
            timeout=self._timeout,
            transport=self._transport,
        )

    async def _open(
        self, prompt: str, purpose: str, max_output_tokens: int, context: CallContext
    ) -> tuple[uuid.UUID, float]:
        estimated = estimate_prompt_tokens(self._counter, self._settings, prompt)
        try:
            check_budget(
                estimated_prompt_tokens=estimated,
                max_output_tokens=max_output_tokens,
                limit=self._settings.llm_context_limit,
            )
        except ContextBudgetExceeded as exceeded:
            logger.warning("LLM call not sent (%s): %s", purpose, exceeded)
            raise
        async with self._sessions() as session, session.begin():
            call_id = await LedgerRepository(session).open(
                context,
                purpose=purpose,
                model=self._settings.llm_model,
                estimated_prompt_tokens=estimated,
                max_output_tokens=max_output_tokens,
            )
        return call_id, time.monotonic()

    async def _completed(
        self,
        call_id: uuid.UUID,
        started: float,
        text: str,
        final: dict[str, Any],
        max_output_tokens: int,
    ) -> LLMResult:
        prompt_tokens = _measured(final.get("prompt_eval_count"))
        completion_tokens = _measured(final.get("eval_count"))
        finish_reason = read_finish_reason(final, max_output_tokens=max_output_tokens)
        async with self._sessions() as session, session.begin():
            await LedgerRepository(session).complete(
                call_id,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                finish_reason=finish_reason.value,
                duration_ms=_elapsed_ms(started),
            )
        return LLMResult(call_id, text, prompt_tokens, completion_tokens, finish_reason)

    async def _failed(
        self, call_id: uuid.UUID, started: float, failure: LLMCallFailed, received: list[str]
    ) -> None:
        async with self._sessions() as session, session.begin():
            await LedgerRepository(session).fail(
                call_id,
                error=str(failure)[:MAX_ERROR_LENGTH],
                duration_ms=_elapsed_ms(started),
                received_output_tokens_estimated=self._count(received) if received else None,
            )

    async def _interrupted(self, call_id: uuid.UUID, started: float, received: list[str]) -> None:
        async with self._sessions() as session, session.begin():
            await LedgerRepository(session).interrupt(
                call_id,
                finish_reason="client_disconnect",
                duration_ms=_elapsed_ms(started),
                received_output_tokens_estimated=self._count(received),
            )

    def _count(self, received: list[str]) -> int:
        return self._counter.count("".join(received))


def _rejection(status_code: int, body: str) -> LLMCallFailed:
    if is_input_too_long(status_code, body):
        return LLMCallFailed(
            INPUT_EXCEEDS_CONTEXT, "Ollama refused the input: it exceeds the context length."
        )
    return LLMCallFailed(LLM_UNAVAILABLE, f"Ollama answered {status_code}: {body[:200]}")


def _measured(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)
