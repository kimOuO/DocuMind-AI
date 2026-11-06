"""The single place where environment variables are read.

Rule (docs/02-specs/03-interfaces.md, section 5.3): no other module may call
``os.getenv`` or touch ``os.environ``. Import ``get_settings`` instead.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../../.env", ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    # Database
    db_host: str = "127.0.0.1"
    db_port: int = 5433
    db_name: str = "documind"
    db_user: str = "documind"
    db_password: str = "documind"
    # Tests open a new event loop per request, so pooled connections cannot be reused.
    db_null_pool: bool = False

    # Cross-module API: Ollama
    http_ollama_host: str = "127.0.0.1"
    http_ollama_port: int = 11434

    # LLM and retrieval
    llm_model: str = "qwen3:32b"
    embed_model: str = "bge-m3"
    llm_context_limit: int = 10_000
    llm_thinking: bool = False
    chunk_size: int = 400
    chunk_overlap: int = 80
    top_k: int = 5
    min_similarity: float = 0.45
    token_safety_buffer: int = 16
    question_token_budget: int = 200

    # Experimental two-call answering (D69): a draft faulted by the checks is revised
    # once. Off by default; the default path is the single streamed call.
    answer_revision: bool = False
    revision_soft_triggers: bool = True  # doubtful citations may trigger a revision
    revision_completeness: bool = True  # a missing comparison target may trigger one
    revision_always: bool = False  # research control: revise every draft

    # Uploads
    max_upload_mb: int = 50
    data_dir: Path = Path(".data")

    # Sessions and request origin
    session_ttl_hours: int = 168
    session_cookie_secure: bool = False
    allowed_origins: str = (
        "http://127.0.0.1:3000,http://localhost:3000,http://127.0.0.1:5173,http://localhost:5173"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def ollama_base_url(self) -> str:
        return f"http://{self.http_ollama_host}:{self.http_ollama_port}"

    @property
    def allowed_origin_set(self) -> frozenset[str]:
        return frozenset(
            o.strip().rstrip("/") for o in self.allowed_origins.split(",") if o.strip()
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
