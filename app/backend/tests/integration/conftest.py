"""Fixtures for tests that run against a real PostgreSQL (marker: ``db``).

Repositories are tested against the real database on purpose: ownership filters
and constraints are part of what must be verified.
"""

from collections.abc import Callable, Iterator

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from app.core.env_loader import get_settings
from app.main import create_app
from tests.conftest import ALLOWED_ORIGIN

TABLES = "users, sessions, documents, ingestion_jobs, chunks, conversations, messages, llm_calls"


def _dsn(database: str) -> str:
    s = get_settings()
    return (
        f"host={s.db_host} port={s.db_port} dbname={database} "
        f"user={s.db_user} password={s.db_password}"
    )


@pytest.fixture(scope="session")
def database() -> str:
    """Create the test database if needed and migrate it to head."""
    name = get_settings().db_name
    assert name.endswith("_test"), "refusing to run integration tests on a non-test database"
    with psycopg.connect(_dsn("postgres"), autocommit=True) as conn:
        exists = conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (name,)).fetchone()
        if not exists:
            conn.execute(f'CREATE DATABASE "{name}"')
    command.upgrade(Config("alembic.ini"), "head")
    return name


@pytest.fixture()
def db(database: str) -> Iterator[psycopg.Connection]:
    """Direct connection for assertions on stored data. Tables start empty."""
    with psycopg.connect(_dsn(database), autocommit=True) as conn:
        conn.execute(f"TRUNCATE {TABLES} CASCADE")
        yield conn


@pytest.fixture()
def make_client(db: psycopg.Connection) -> Callable[..., TestClient]:
    """Factory for independent browsers (separate cookie jars)."""

    def _make(*, origin: str | None = ALLOWED_ORIGIN) -> TestClient:
        headers = {"Origin": origin} if origin else {}
        return TestClient(create_app(), headers=headers)

    return _make


@pytest.fixture()
def client(make_client: Callable[..., TestClient]) -> TestClient:
    return make_client()


def register_and_login(
    client: TestClient, username: str, password: str = "s3cret-password"
) -> dict:
    assert (
        client.post(
            "/api/v1/auth/register", json={"username": username, "password": password}
        ).status_code
        == 201
    )
    response = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()
