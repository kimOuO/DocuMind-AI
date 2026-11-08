"""The single place where environment variables are read.

Rule (docs/02-specs/03-interfaces.md, section 5.3): no other module may call
``os.getenv`` or touch ``os.environ``. Import ``get_settings`` instead.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
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
    # Cross-module API (HTTP_<module>_<field>): the Ollama server that serves the text-to-text
    # model and the embedding model. The scheme is explicit so an https deployment needs no
    # code change.
    http_ollama_scheme: str = "http"
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
    # P4 (ADR 0010, user's decision 2026-11-07): 0.50 refuses all three no-answer questions
    # of the question set at every chunk size with no wrong refusal; 0.45 refused one or two.
    # The margin to the answerable questions is 0.03–0.04. Also the navigate mode's
    # relevance floor for a target's candidates.
    min_similarity: float = 0.50
    token_safety_buffer: int = 16
    question_token_budget: int = 200

    # Experimental two-call answering (D69): a draft faulted by the checks is revised
    # once. Off by default; the default path is the single streamed call.
    answer_revision: bool = False
    revision_soft_triggers: bool = True  # doubtful citations may trigger a revision
    revision_completeness: bool = True  # a missing comparison target may trigger one
    revision_always: bool = False  # research control: revise every draft
    # Experimental answer modes (D71): "single" (default, one streamed call); "roles"
    # (one call, Navigator then Analyst in the same prompt, same evidence); "navigate"
    # (a navigation call produces a reading plan, located places are fetched and added
    # behind the Top-K, then the answer call).
    answer_mode: str = "single"
    # D75/D76: whether the deterministic correction of comparison words is applied to the
    # navigate-mode answer. Off by default: in the B4/B4b runs the checks' reading of a
    # sentence was not reliable enough to act on (48 figures rewritten in one answer, 15
    # sentences removed in another); the checks still run and report what they would have
    # changed. Summaries are never rewritten; their verification status is stored instead.
    auto_correction: bool = False
    # N4 (2026-11-07): sampling temperature of the Navigator call only (the answer call keeps
    # the model's default). 0 makes the reading plan repeatable; with the tables rule in the
    # Navigator prompt, that plan named the needed table in 10/10 runs for the two questions
    # whose table is never among the Top-K. None keeps the model's default.
    navigation_temperature: float | None = 0.0
    # D86: sampling temperature of the answer call (single mode's one call; navigate mode's
    # Analyst; the revision draft). None keeps the model's default (qwen3:32b: 0.6). 0 makes
    # the same evidence give the same answer — not a better one, a repeatable one.
    answer_temperature: float | None = 0.5
    # D87 experiment A: what the program's comparison facts do at answer time.
    #   off     — computed for the checks only (the behaviour so far)
    #   inject  — the facts that bear on the question go into the prompt before the sources
    #   replace — as inject, and a table chunk whose figures the facts cover is shown as the
    #             rows of the compared columns only (its caption and page kept)
    answer_facts: str = "inject"
    # D87 experiment B: when a section or document summary's figures contradict the tables
    # of its pages, the model is asked once to rewrite the contradicted sentences with the
    # table's own figures as evidence; what still contradicts afterwards is removed. Off by
    # default: the status is stored, the text kept as written.
    summary_repair: bool = True
    # D98 (user): the checks always run and go into the `done` event, but their notes are
    # appended to the answer only in debug mode; the demo shows the answer alone.
    check_notes: bool = False
    # D99: the conversation so far can go into the answer prompt as context (not a source).
    # Off by default: with it, Q3 wrote the variants' definitions and reversed them in both
    # flows; without it the follow-up is still answered from the previous turn's sources.
    answer_context: bool = False
    # The tokenizer file the budget guard counts with, relative to app/backend, and its
    # SHA-256. Must be the tokenizer of LLM_MODEL: the Qwen3 file undercounts qwen3.6's
    # table text by up to 3% (D77/M5), so a qwen3.6 run points these at
    # third-party/qwen3.6-tokenizer (see its README).
    tokenizer_path: str = "third-party/qwen3-tokenizer/tokenizer.json"
    tokenizer_sha256: str = "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4"

    @field_validator("answer_facts")
    @classmethod
    def _known_facts_mode(cls, value: str) -> str:
        if value not in ("off", "inject", "replace"):
            raise ValueError("ANSWER_FACTS must be off, inject or replace")
        return value

    @field_validator("navigation_temperature", "answer_temperature", mode="before")
    @classmethod
    def _empty_means_default(cls, value: object) -> object:
        """NAVIGATION_TEMPERATURE= or ANSWER_TEMPERATURE= (empty) keeps the model's default."""
        return None if isinstance(value, str) and not value.strip() else value

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
        return f"{self.http_ollama_scheme}://{self.http_ollama_host}:{self.http_ollama_port}"

    @property
    def allowed_origin_set(self) -> frozenset[str]:
        return frozenset(
            o.strip().rstrip("/") for o in self.allowed_origins.split(",") if o.strip()
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
