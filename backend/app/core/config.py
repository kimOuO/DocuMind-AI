"""Application settings, loaded from environment variables or a local .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = "postgresql+psycopg://documind:documind@127.0.0.1:5433/documind"

    ollama_base_url: str = "http://127.0.0.1:11434"
    llm_model: str = "qwen3:32b"
    embed_model: str = "bge-m3"
    # Assignment constraint: prompt + completion tokens of a single LLM call.
    llm_context_limit: int = 10_000

    data_dir: Path = Path("../data")


@lru_cache
def get_settings() -> Settings:
    return Settings()
