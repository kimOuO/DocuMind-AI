"""Conversations: create, list, read, delete, and isolation between users.

Covers AC-40 (conversations survive a new login; deleting one removes its
messages and keeps the LLM call records) and the read/delete part of AC-33.
"""

import json
import uuid
from collections.abc import Callable

import psycopg
import pytest
from fastapi.testclient import TestClient

from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

CONVERSATIONS = "/api/v1/conversations"


@pytest.fixture()
def user(client: TestClient) -> TestClient:
    register_and_login(client, "kim")
    return client


@pytest.fixture()
def other(make_client: Callable[..., TestClient]) -> TestClient:
    client = make_client()
    register_and_login(client, "lee")
    return client


def add_messages(db: psycopg.Connection, conversation_id: str) -> tuple[str, str]:
    """Store a question and its answer directly, as the chat service will."""
    source = {
        "index": 1,
        "kind": "chunk",
        "document_id": str(uuid.uuid4()),
        "filename": "paper.pdf",
        "page_start": 8,
        "page_end": 8,
        "section_title": None,
        "snippet": "Table 2: Performance of ablated versions",
        "score": 0.61,
    }
    question = db.execute(
        "INSERT INTO messages (id, conversation_id, role, content, status, created_at) "
        "VALUES (gen_random_uuid(), %s, 'user', 'What is LightRAG?', 'completed', now()) "
        "RETURNING id",
        (conversation_id,),
    ).fetchone()
    answer = db.execute(
        "INSERT INTO messages "
        "(id, conversation_id, role, content, status, answered, sources, created_at) "
        "VALUES (gen_random_uuid(), %s, 'assistant', 'A RAG system [1].', 'completed', true, %s, "
        "now() + interval '1 millisecond') RETURNING id",
        (conversation_id, json.dumps([source])),
    ).fetchone()
    assert question and answer
    return str(question[0]), str(answer[0])


def test_a_conversation_is_created_with_or_without_a_title(user: TestClient) -> None:
    titled = user.post(CONVERSATIONS, json={"title": "  LightRAG questions  "})
    untitled = user.post(CONVERSATIONS, json={})

    assert titled.status_code == untitled.status_code == 201
    assert titled.json()["title"] == "LightRAG questions"
    assert untitled.json()["title"] == ""
    assert set(titled.json()) == {"id", "title", "created_at", "updated_at"}


def test_a_title_that_is_too_long_is_refused(user: TestClient) -> None:
    assert user.post(CONVERSATIONS, json={"title": "x" * 201}).status_code == 422


def test_conversations_are_listed_most_recently_updated_first(
    user: TestClient, db: psycopg.Connection
) -> None:
    first = user.post(CONVERSATIONS, json={"title": "first"}).json()["id"]
    second = user.post(CONVERSATIONS, json={"title": "second"}).json()["id"]
    db.execute(
        "UPDATE conversations SET updated_at = now() + interval '1 hour' WHERE id = %s", (first,)
    )

    listed = user.get(CONVERSATIONS).json()

    assert [c["id"] for c in listed] == [first, second]
    assert all("messages" not in c for c in listed)


def test_a_conversation_is_read_with_its_messages_in_order(
    user: TestClient, db: psycopg.Connection
) -> None:
    conversation = user.post(CONVERSATIONS, json={"title": "paper"}).json()["id"]
    question_id, answer_id = add_messages(db, conversation)

    body = user.get(f"{CONVERSATIONS}/{conversation}").json()

    assert body["title"] == "paper"
    question, answer = body["messages"]
    assert (question["id"], question["role"], question["content"]) == (
        question_id,
        "user",
        "What is LightRAG?",
    )
    assert (answer["id"], answer["role"], answer["status"], answer["answered"]) == (
        answer_id,
        "assistant",
        "completed",
        True,
    )
    assert answer["sources"][0]["filename"] == "paper.pdf"
    assert answer["sources"][0]["page_start"] == 8
    assert set(answer) == {
        "id",
        "role",
        "content",
        "status",
        "answered",
        "sources",
        "temperature",
        "created_at",
    }


def test_conversations_survive_logging_out_and_in_again(
    user: TestClient, db: psycopg.Connection
) -> None:
    """AC-40: conversations and messages are still there after a new login."""
    conversation = user.post(CONVERSATIONS, json={"title": "kept"}).json()["id"]
    add_messages(db, conversation)
    assert user.post("/api/v1/auth/logout").status_code == 204
    assert user.get(CONVERSATIONS).status_code == 401

    login = user.post("/api/v1/auth/login", json={"username": "kim", "password": "s3cret-password"})

    assert login.status_code == 200
    assert [c["title"] for c in user.get(CONVERSATIONS).json()] == ["kept"]
    assert len(user.get(f"{CONVERSATIONS}/{conversation}").json()["messages"]) == 2


def test_deleting_a_conversation_removes_its_messages_and_keeps_the_llm_calls(
    user: TestClient, db: psycopg.Connection
) -> None:
    """AC-40: the ledger entry stays, with its references cleared."""
    conversation = user.post(CONVERSATIONS, json={}).json()["id"]
    _, answer_id = add_messages(db, conversation)
    owner = db.execute("SELECT id FROM users WHERE username = 'kim'").fetchone()
    assert owner
    db.execute(
        "INSERT INTO llm_calls (id, owner_id, conversation_id, message_id, purpose, model, status, "
        "estimated_prompt_tokens, max_output_tokens) "
        "VALUES (gen_random_uuid(), %s, %s, %s, 'answer', 'qwen3:32b', 'completed', 100, 200)",
        (owner[0], conversation, answer_id),
    )

    assert user.delete(f"{CONVERSATIONS}/{conversation}").status_code == 204

    assert user.get(f"{CONVERSATIONS}/{conversation}").status_code == 404
    assert db.execute("SELECT count(*) FROM messages").fetchone() == (0,)
    assert db.execute("SELECT conversation_id, message_id, owner_id FROM llm_calls").fetchone() == (
        None,
        None,
        owner[0],
    )
    # Deleting it again is the same as deleting something that never existed.
    assert user.delete(f"{CONVERSATIONS}/{conversation}").status_code == 404


def test_another_users_conversation_cannot_be_read_or_deleted(
    user: TestClient, other: TestClient, db: psycopg.Connection
) -> None:
    """AC-33 (read, delete): the answer is the same as for one that does not exist."""
    conversation = user.post(CONVERSATIONS, json={"title": "private"}).json()["id"]
    add_messages(db, conversation)
    missing = f"{CONVERSATIONS}/{uuid.uuid4()}"

    read = other.get(f"{CONVERSATIONS}/{conversation}")
    deleted = other.delete(f"{CONVERSATIONS}/{conversation}")

    assert read.status_code == deleted.status_code == 404
    assert (
        read.json() == other.get(missing).json() == deleted.json() == other.delete(missing).json()
    )
    assert read.json()["code"] == "CONVERSATION_NOT_FOUND"
    assert other.get(CONVERSATIONS).json() == []
    # Nothing changed for the owner.
    assert len(user.get(f"{CONVERSATIONS}/{conversation}").json()["messages"]) == 2
