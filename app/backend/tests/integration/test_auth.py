"""Accounts and sessions: AC-28, AC-29, AC-31, AC-45."""

from collections.abc import Callable

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.security import SESSION_COOKIE_NAME
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

PASSWORD = "s3cret-password"


# --- AC-28 -----------------------------------------------------------------


def test_register_then_login_with_the_same_credentials(client: TestClient) -> None:
    created = client.post("/api/v1/auth/register", json={"username": "kim", "password": PASSWORD})
    assert created.status_code == 201
    assert created.json()["username"] == "kim"
    assert "password" not in created.text

    logged_in = client.post("/api/v1/auth/login", json={"username": "kim", "password": PASSWORD})
    assert logged_in.status_code == 200
    me = client.get("/api/v1/users/me")
    assert me.status_code == 200
    assert me.json()["username"] == "kim"
    assert me.json()["last_login_at"] is not None


def test_duplicate_username_is_rejected(client: TestClient) -> None:
    body = {"username": "kim", "password": PASSWORD}
    assert client.post("/api/v1/auth/register", json=body).status_code == 201

    again = client.post("/api/v1/auth/register", json={"username": "KIM", "password": PASSWORD})

    assert again.status_code == 409
    assert again.json()["code"] == "USERNAME_TAKEN"


def test_registering_does_not_log_the_user_in(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "kim", "password": PASSWORD})

    assert client.get("/api/v1/users/me").status_code == 401


def test_unknown_user_and_wrong_password_give_the_same_answer(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "kim", "password": PASSWORD})

    wrong = client.post(
        "/api/v1/auth/login", json={"username": "kim", "password": "not-the-password"}
    )
    unknown = client.post("/api/v1/auth/login", json={"username": "nobody", "password": PASSWORD})

    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_invalid_input_uses_the_uniform_error_format(client: TestClient) -> None:
    response = client.post("/api/v1/auth/register", json={"username": "kim", "password": "short"})

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
    assert isinstance(response.json()["detail"], str)


# --- AC-29 -----------------------------------------------------------------


def test_passwords_are_stored_as_salted_argon2id_hashes(
    client: TestClient, db: psycopg.Connection
) -> None:
    for name in ("kim", "lee"):
        client.post("/api/v1/auth/register", json={"username": name, "password": PASSWORD})

    hashes = [row[0] for row in db.execute("SELECT password_hash FROM users ORDER BY username")]

    assert len(hashes) == 2
    assert all(h.startswith("$argon2id$") for h in hashes)
    assert all(PASSWORD not in h for h in hashes)
    assert hashes[0] != hashes[1], "same password must not produce the same hash"


def test_session_token_is_not_stored_in_clear(client: TestClient, db: psycopg.Connection) -> None:
    register_and_login(client, "kim")
    token = client.cookies[SESSION_COOKIE_NAME]

    stored = [row[0] for row in db.execute("SELECT token_hash FROM sessions")]

    assert stored and token not in stored


# --- AC-31 -----------------------------------------------------------------


def test_logout_invalidates_the_session(
    client: TestClient, make_client: Callable[..., TestClient]
) -> None:
    register_and_login(client, "kim")
    old_token = client.cookies[SESSION_COOKIE_NAME]

    assert client.post("/api/v1/auth/logout").status_code == 204
    assert client.get("/api/v1/users/me").status_code == 401

    # Replaying the old cookie from another browser does not work either.
    replay = make_client()
    replay.cookies.set(SESSION_COOKIE_NAME, old_token)
    assert replay.get("/api/v1/users/me").status_code == 401


def test_expired_session_is_rejected(client: TestClient, db: psycopg.Connection) -> None:
    register_and_login(client, "kim")
    db.execute("UPDATE sessions SET expires_at = now() - interval '1 minute'")

    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
    assert response.json()["code"] == "SESSION_EXPIRED"
    assert db.execute("SELECT count(*) FROM sessions").fetchone() == (0,)


# --- AC-45 -----------------------------------------------------------------


def test_login_never_adopts_a_session_value_chosen_by_the_client(
    make_client: Callable[..., TestClient],
) -> None:
    make_client().post("/api/v1/auth/register", json={"username": "kim", "password": PASSWORD})
    planted = "value-planted-before-login"

    victim = make_client()
    response = victim.post(
        "/api/v1/auth/login",
        json={"username": "kim", "password": PASSWORD},
        cookies={SESSION_COOKIE_NAME: planted},
    )
    issued = response.cookies[SESSION_COOKIE_NAME]

    assert response.status_code == 200
    assert issued != planted
    attacker = make_client()
    attacker.cookies.set(SESSION_COOKIE_NAME, planted)
    assert attacker.get("/api/v1/users/me").status_code == 401
    owner = make_client()
    owner.cookies.set(SESSION_COOKIE_NAME, issued)
    assert owner.get("/api/v1/users/me").status_code == 200


def test_logging_in_again_replaces_the_previous_session(
    client: TestClient, make_client: Callable[..., TestClient]
) -> None:
    register_and_login(client, "kim")
    first = client.cookies[SESSION_COOKIE_NAME]

    client.post("/api/v1/auth/login", json={"username": "kim", "password": PASSWORD})
    second = client.cookies[SESSION_COOKIE_NAME]

    assert second != first
    stale = make_client()
    stale.cookies.set(SESSION_COOKIE_NAME, first)
    assert stale.get("/api/v1/users/me").status_code == 401


def test_session_cookie_attributes(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "kim", "password": PASSWORD})

    response = client.post("/api/v1/auth/login", json={"username": "kim", "password": PASSWORD})
    cookie = response.headers["set-cookie"].lower()

    assert "httponly" in cookie
    assert "samesite=lax" in cookie
    assert "path=/" in cookie
