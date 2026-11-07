"""The embedding client: request shape, validation of the reply, and failures.

No test here calls Ollama; the HTTP layer is replaced by a stub transport.
"""

import json

import httpx
import pytest

from app.core.env_loader import Settings
from app.llm.embedding import EmbeddingError, EmbeddingInputError, OllamaEmbedder
from app.llm.ollama_api import embed_request
from app.models import EMBEDDING_DIMENSIONS

SETTINGS = Settings(embed_model="bge-m3")


def _vector(seed: float) -> list[float]:
    return [seed] * EMBEDDING_DIMENSIONS


def _embedder(handler) -> OllamaEmbedder:  # type: ignore[no-untyped-def]
    return OllamaEmbedder(SETTINGS, transport=httpx.MockTransport(handler))


def test_the_request_asks_ollama_not_to_truncate() -> None:
    request = embed_request(SETTINGS, ["one", "two"])

    assert request.path == "/api/embed"
    assert request.body == {"model": "bge-m3", "input": ["one", "two"], "truncate": False}


async def test_texts_are_embedded_in_order() -> None:
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append({"path": request.url.path, "body": json.loads(request.content)})
        return httpx.Response(200, json={"embeddings": [_vector(0.1), _vector(0.2)]})

    vectors = await _embedder(handler).embed(["one", "two"])

    assert [vector[0] for vector in vectors] == [0.1, 0.2]
    assert seen == [
        {
            "path": "/api/embed",
            "body": {"model": "bge-m3", "input": ["one", "two"], "truncate": False},
        }
    ]


async def test_nothing_is_sent_for_an_empty_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("no request expected")

    assert await _embedder(handler).embed([]) == []


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (httpx.Response(500, json={"error": "model failed to load"}), "500"),
        (httpx.Response(400, json={"error": "the input length exceeds the context length"}), "400"),
        (httpx.Response(200, json={"embeddings": [_vector(0.1)]}), "1 vectors for 2 texts"),
        (httpx.Response(200, json={"embeddings": [[0.1, 0.2], [0.3, 0.4]]}), "dimensions"),
        (httpx.Response(200, json={"unexpected": True}), "0 vectors for 2 texts"),
        (httpx.Response(200, content=b"not json"), "not valid JSON"),
    ],
)
async def test_a_bad_reply_is_an_embedding_error(response: httpx.Response, expected: str) -> None:
    with pytest.raises(EmbeddingError, match=expected):
        await _embedder(lambda request: response).embed(["one", "two"])


async def test_an_unreachable_server_is_an_embedding_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    with pytest.raises(EmbeddingError, match="connection refused"):
        await _embedder(handler).embed(["one"])


async def test_a_nan_reply_is_an_input_error_not_a_service_error() -> None:
    """D70: bge-m3 on the GPU answers 500 with NaN for some phrases; the service is fine."""
    nan = httpx.Response(
        500, json={"error": "failed to encode response: json: unsupported value: NaN"}
    )

    with pytest.raises(EmbeddingInputError, match="could not compute a vector for this text"):
        await _embedder(lambda request: nan).embed(["the sections, tables and figures"])


async def test_a_nan_reply_is_retried_once_with_the_text_normalised() -> None:
    """D88: the question "Compare condition C2 with vector RAG (SS) …" embedded as NaN in the
    demo deployment; the same words with a newline appended embed fine. One retry, then
    the error."""
    seen: list[list[str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        texts = json.loads(request.content)["input"]
        seen.append(texts)
        if texts[0].endswith("."):  # the real case: the final full stop makes NaN
            return httpx.Response(
                500, json={"error": "failed to encode response: json: unsupported value: NaN"}
            )
        return httpx.Response(200, json={"embeddings": [_vector(0.1) for _ in texts]})

    vectors = await _embedder(handler).embed(["Compare condition C2 with vector RAG (SS)."])

    assert len(vectors) == 1 and len(vectors[0]) == EMBEDDING_DIMENSIONS
    assert seen == [
        ["Compare condition C2 with vector RAG (SS)."],
        ["Compare condition C2 with vector RAG (SS)"],
    ]


async def test_when_no_spelling_embeds_the_input_error_is_raised() -> None:
    nan = httpx.Response(500, json={"error": "unsupported value: NaN"})

    with pytest.raises(EmbeddingInputError):
        await _embedder(lambda request: nan).embed(["Still NaN."])


async def test_in_a_batch_the_failing_text_is_found_and_retried_alone() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        texts = json.loads(request.content)["input"]
        if any(t == "bad" for t in texts):
            return httpx.Response(500, json={"error": "unsupported value: NaN"})
        return httpx.Response(200, json={"embeddings": [_vector(0.2) for _ in texts]})

    vectors = await _embedder(handler).embed(["good", "bad", "also good"])

    assert len(vectors) == 3
