"""Local token counting with the tokenizer of the model Ollama serves.

Ollama has no tokenize endpoint and silently truncates a prompt that exceeds
num_ctx, so the prompt must be counted before it is sent. The tokenizer file is
vendored in third-party/qwen3-tokenizer (see the README there for its source).
"""

import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Protocol

from tokenizers import Tokenizer

BACKEND_ROOT = Path(__file__).resolve().parents[2]
TOKENIZER_PATH = BACKEND_ROOT / "third-party" / "qwen3-tokenizer" / "tokenizer.json"
TOKENIZER_SHA256 = "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4"


class TokenizerFileError(RuntimeError):
    """The tokenizer file is missing or is not the file that was verified."""


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...


class Qwen3TokenCounter:
    """Counts tokens exactly as the Qwen3 model served by Ollama does.

    The file's checksum is verified on load: a different file would count
    differently, and an undercount lets a prompt exceed the context limit.
    """

    def __init__(
        self, path: Path = TOKENIZER_PATH, expected_sha256: str = TOKENIZER_SHA256
    ) -> None:
        try:
            content = path.read_bytes()
        except OSError as error:
            raise TokenizerFileError(f"Cannot read the tokenizer file: {path}") from error
        digest = hashlib.sha256(content).hexdigest()
        if digest != expected_sha256:
            raise TokenizerFileError(
                f"Tokenizer file {path} has SHA-256 {digest}, expected {expected_sha256}."
            )
        self._tokenizer = Tokenizer.from_str(content.decode("utf-8"))

    def count(self, text: str) -> int:
        # The model's add_bos_token is false, so no special tokens are added.
        return len(self._tokenizer.encode(text, add_special_tokens=False).ids)

    def spans(self, text: str) -> list[tuple[int, int]]:
        """The character range of each token in `text`, in order."""
        return list(self._tokenizer.encode(text, add_special_tokens=False).offsets)


@lru_cache
def _counter(path: str, sha256: str) -> Qwen3TokenCounter:
    return Qwen3TokenCounter(BACKEND_ROOT / path, sha256)


def get_token_counter() -> Qwen3TokenCounter:
    """The process-wide tokenizer, the file named by the settings (the model's own; see
    Settings.tokenizer_path). Loading the file takes about half a second."""
    from app.core.env_loader import get_settings

    settings = get_settings()
    return _counter(settings.tokenizer_path, settings.tokenizer_sha256)


def get_token_counter_for(tokenizer_path: str, tokenizer_sha256: str) -> Qwen3TokenCounter:
    """The tokenizer of a model chosen per question (D104); loaded once per file."""
    return _counter(tokenizer_path, tokenizer_sha256)
