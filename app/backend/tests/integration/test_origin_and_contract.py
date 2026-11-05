"""Origin verification (AC-44), REST conventions (AC-27), authentication coverage (AC-30)."""

import uuid
from collections.abc import Callable

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.main import API_PREFIX, PUBLIC_PATHS, create_app
from tests.conftest import ALLOWED_ORIGIN

pytestmark = pytest.mark.db

BODY = {"username": "kim", "password": "s3cret-password"}
REGISTER = f"{API_PREFIX}/auth/register"


def _user_count(db: psycopg.Connection) -> int:
    return db.execute("SELECT count(*) FROM users").fetchone()[0]  # type: ignore[index]


# --- AC-44: the five cases ---------------------------------------------------


def test_allowed_origin_is_accepted(make_client: Callable[..., TestClient]) -> None:
    response = make_client(origin=None).post(
        REGISTER, json=BODY, headers={"Origin": ALLOWED_ORIGIN}
    )
    assert response.status_code == 201


def test_foreign_origin_is_refused(
    make_client: Callable[..., TestClient], db: psycopg.Connection
) -> None:
    response = make_client(origin=None).post(
        REGISTER, json=BODY, headers={"Origin": "https://evil.example"}
    )
    assert response.status_code == 403
    assert response.json()["code"] == "ORIGIN_NOT_ALLOWED"
    assert _user_count(db) == 0


def test_allowed_referer_is_accepted_when_origin_is_absent(
    make_client: Callable[..., TestClient],
) -> None:
    response = make_client(origin=None).post(
        REGISTER, json=BODY, headers={"Referer": f"{ALLOWED_ORIGIN}/login?next=/"}
    )
    assert response.status_code == 201


def test_foreign_referer_is_refused_when_origin_is_absent(
    make_client: Callable[..., TestClient], db: psycopg.Connection
) -> None:
    response = make_client(origin=None).post(
        REGISTER, json=BODY, headers={"Referer": "https://evil.example/page"}
    )
    assert response.status_code == 403
    assert _user_count(db) == 0


def test_request_without_origin_and_referer_is_refused(
    make_client: Callable[..., TestClient], db: psycopg.Connection
) -> None:
    response = make_client(origin=None).post(REGISTER, json=BODY)
    assert response.status_code == 403
    assert _user_count(db) == 0


def test_origin_wins_over_referer(
    make_client: Callable[..., TestClient], db: psycopg.Connection
) -> None:
    response = make_client(origin=None).post(
        REGISTER, json=BODY, headers={"Origin": "https://evil.example", "Referer": ALLOWED_ORIGIN}
    )
    assert response.status_code == 403
    assert _user_count(db) == 0


def test_read_requests_are_not_subject_to_the_origin_check(
    make_client: Callable[..., TestClient],
) -> None:
    assert make_client(origin=None).get(f"{API_PREFIX}/health").status_code == 200


# --- AC-27 -------------------------------------------------------------------


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _api_operations() -> list[tuple[str, str]]:
    """Every (METHOD, path) the application serves, taken from its OpenAPI document."""
    paths = create_app().openapi()["paths"]
    return [
        (method.upper(), path)
        for path, operations in paths.items()
        for method in operations
        if method in HTTP_METHODS
    ]


def test_every_api_route_is_under_the_versioned_prefix_and_uses_rest_methods() -> None:
    operations = _api_operations()
    assert operations
    for method, path in operations:
        assert path.startswith(f"{API_PREFIX}/"), path
        assert method in {"GET", "POST", "PATCH", "DELETE"}, (method, path)


def test_nothing_is_served_outside_the_versioned_prefix() -> None:
    outside = [r.path for r in create_app().routes if hasattr(r, "path") and r.path]
    assert all(path.startswith(f"{API_PREFIX}/") for path in outside), outside


def test_api_documentation_is_served(make_client: Callable[..., TestClient]) -> None:
    client = make_client(origin=None)
    assert client.get(f"{API_PREFIX}/docs").status_code == 200
    assert client.get(f"{API_PREFIX}/openapi.json").json()["info"]["title"] == "DocuMind-AI"


# --- AC-30 -------------------------------------------------------------------


def test_every_non_public_route_requires_login(client: TestClient) -> None:
    checked = []
    for method, route_path in _api_operations():
        if route_path in PUBLIC_PATHS:
            continue
        path = route_path.replace("{id}", str(uuid.uuid4()))
        response = client.request(method, path, json={})
        assert response.status_code == 401, (method, path, response.status_code)
        checked.append((method, route_path))
    assert checked, "there should be at least one protected route"
