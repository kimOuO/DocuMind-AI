"""The real embedding model, through the application's embedding client.

Verified against Ollama 0.24.0 with bge-m3. Run again after an upgrade:
    pytest -m llm tests/integration/test_embedding_service.py
"""

import math

import pytest

from app.core.env_loader import get_settings
from app.llm.embedding import EmbeddingError, OllamaEmbedder
from app.models import EMBEDDING_DIMENSIONS

pytestmark = pytest.mark.llm


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


async def test_vectors_have_the_stored_dimension_and_are_normalised() -> None:
    embedder = OllamaEmbedder(get_settings())

    question, related, unrelated = await embedder.embed(
        [
            "How does LightRAG retrieve information?",
            "LightRAG uses a dual-level retrieval paradigm over a knowledge graph.",
            "Sourdough bread needs a long, slow fermentation.",
        ]
    )

    for vector in (question, related, unrelated):
        assert len(vector) == EMBEDDING_DIMENSIONS
        assert math.isclose(math.sqrt(sum(x * x for x in vector)), 1.0, abs_tol=1e-3)
    assert _cosine(question, related) > _cosine(question, unrelated) + 0.1


async def test_chinese_and_english_about_the_same_thing_are_close() -> None:
    embedder = OllamaEmbedder(get_settings())

    chinese, english, unrelated = await embedder.embed(
        [
            "LightRAG 如何檢索資訊？",
            "LightRAG uses a dual-level retrieval paradigm over a knowledge graph.",
            "Sourdough bread needs a long, slow fermentation.",
        ]
    )

    assert _cosine(chinese, english) > _cosine(chinese, unrelated) + 0.1


async def test_a_text_too_long_for_the_model_is_refused_not_truncated() -> None:
    embedder = OllamaEmbedder(get_settings())
    too_long = "The quick brown fox jumps over the lazy dog. " * 2_000  # about 20,000 tokens

    with pytest.raises(EmbeddingError, match="context length"):
        await embedder.embed([too_long])
