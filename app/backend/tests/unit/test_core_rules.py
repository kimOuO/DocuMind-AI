"""Unit tests for rules that need no database: origin, passwords, tokens, settings."""

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.env_loader import Settings
from app.core.origin import is_origin_allowed, request_origin
from app.core.security import hash_password, hash_session_token, new_session_token, verify_password
from app.main import create_app
from app.monitoring.router import DependencyStatus, get_health_probe

ALLOWED = frozenset({"http://127.0.0.1:3000", "http://localhost:5173"})


@pytest.mark.parametrize(
    ("origin", "referer", "expected"),
    [
        ("http://127.0.0.1:3000", None, True),
        ("http://127.0.0.1:3000/", None, True),
        ("https://evil.example", None, False),
        (None, "http://localhost:5173/login?x=1", True),
        (None, "https://evil.example/", False),
        (None, None, False),
        (None, "not a url", False),
        # Origin, when present, is the one that counts.
        ("https://evil.example", "http://127.0.0.1:3000/", False),
        # Same host on another port or scheme is a different origin.
        ("http://127.0.0.1:3001", None, False),
        ("https://127.0.0.1:3000", None, False),
    ],
)
def test_origin_rule(origin: str | None, referer: str | None, expected: bool) -> None:
    assert is_origin_allowed(origin, referer, ALLOWED) is expected


def test_referer_is_reduced_to_its_origin() -> None:
    assert request_origin(None, "http://localhost:5173/a/b?c=d#e") == "http://localhost:5173"


def test_password_hashing_is_salted_and_verifiable() -> None:
    first, second = hash_password("s3cret-password"), hash_password("s3cret-password")

    assert first != second
    assert first.startswith("$argon2id$")
    assert verify_password(first, "s3cret-password")
    assert not verify_password(first, "another-password")


def test_verifying_against_a_missing_user_is_false() -> None:
    assert not verify_password(None, "anything")
    assert not verify_password("not-a-hash", "anything")


def test_session_tokens_are_random_and_only_their_hash_is_kept() -> None:
    token_a, hash_a = new_session_token()
    token_b, _ = new_session_token()

    assert token_a != token_b
    assert len(token_a) >= 43  # 32 random bytes, URL-safe base64
    assert hash_a == hash_session_token(token_a) != token_a


def test_settings_build_connection_values_from_the_agreed_variable_names() -> None:
    settings = Settings(
        _env_file=None,
        db_host="db",
        db_port=5432,
        db_name="n",
        db_user="u",
        db_password="p",
        http_ollama_host="ollama",
        http_ollama_port=1234,
        allowed_origins="http://a:1/, http://b:2",
    )

    assert settings.database_url == "postgresql+psycopg://u:p@db:5432/n"
    assert settings.ollama_base_url == "http://ollama:1234"
    assert settings.allowed_origin_set == {"http://a:1", "http://b:2"}
    assert settings.llm_context_limit == 10_000
    assert settings.question_token_budget == 200


def test_only_the_env_loader_reads_the_environment() -> None:
    """Spec 03, section 5.3: no os.getenv / os.environ outside app/core/env_loader.py."""
    app_dir = Path(__file__).resolve().parents[2] / "app"
    offenders = [
        str(path.relative_to(app_dir))
        for path in app_dir.rglob("*.py")
        if path.name != "env_loader.py" and re.search(r"os\.(getenv|environ)", path.read_text())
    ]
    assert offenders == []


class _FakeProbe:
    def __init__(self, database_ok: bool, ollama_ok: bool) -> None:
        self._database_ok, self._ollama_ok = database_ok, ollama_ok

    async def database(self) -> DependencyStatus:
        return DependencyStatus(ok=self._database_ok, detail="fake")

    async def ollama(self) -> DependencyStatus:
        return DependencyStatus(ok=self._ollama_ok, detail="fake")


@pytest.mark.parametrize(
    ("database_ok", "ollama_ok", "status"),
    [(True, True, "ok"), (False, True, "degraded"), (True, False, "degraded")],
)
def test_health_reports_each_dependency(database_ok: bool, ollama_ok: bool, status: str) -> None:
    app = create_app()
    app.dependency_overrides[get_health_probe] = lambda: _FakeProbe(database_ok, ollama_ok)

    body = TestClient(app).get("/api/v1/health").json()

    assert body["status"] == status
    assert body["database"]["ok"] is database_ok
    assert body["ollama"]["ok"] is ollama_ok
    assert body["llm_context_limit"] == 10_000
