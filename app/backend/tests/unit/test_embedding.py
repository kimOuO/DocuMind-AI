"""The embedding client: request shape, validation of the reply, and failures.

No test here calls Ollama; the HTTP layer is replaced by a stub transport.
"""

import json

import httpx
import pytest

from app.core.env_loader import Settings
from app.llm.embedding import EmbeddingError, OllamaEmbedder
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
