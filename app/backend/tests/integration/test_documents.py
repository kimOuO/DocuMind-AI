"""Document management: upload, list, read, delete, de-duplication, isolation.

Covers AC-02 and AC-35, and the read/delete part of AC-32. Documents are stored
and queued here; they are not processed until P2-C.
"""

import hashlib
import uuid
from collections.abc import Callable
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.core.env_loader import get_settings
from app.main import create_app
from tests.conftest import ALLOWED_ORIGIN
from tests.integration.conftest import register_and_login

pytestmark = pytest.mark.db

DOCUMENTS = "/api/v1/documents"
SAMPLE_PDF = Path(__file__).resolve().parents[4] / "sample-documents" / "2410.05779v3.pdf"
TEXT = b"LightRAG combines graph structures with dual-level retrieval.\n"


def upload(client: TestClient, name: str, content: bytes):  # type: ignore[no-untyped-def]
    return client.post(DOCUMENTS, files={"file": (name, content)})


def stored_files() -> list[Path]:
    base = get_settings().data_dir
    return sorted(p for p in base.rglob("*") if p.is_file()) if base.exists() else []


def count(db: psycopg.Connection, table: str) -> int:
    return db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]  # type: ignore[index]


@pytest.fixture()
def user(client: TestClient) -> TestClient:
    for path in stored_files():
        path.unlink()
    register_and_login(client, "kim")
    return client


@pytest.fixture()
def other(make_client: Callable[..., TestClient]) -> TestClient:
    client = make_client()
    register_and_login(client, "lee")
    return client


# --- upload (AC-01, storage part) ---------------------------------------------


@pytest.mark.parametrize(
    ("name", "content", "media_type"),
    [("notes.txt", TEXT, "txt"), ("README.md", b"# Title\n\nBody.\n", "md")],
)
def test_upload_stores_the_file_and_queues_an_index_job(
    user: TestClient, db: psycopg.Connection, name: str, content: bytes, media_type: str
) -> None:
    response = upload(user, name, content)

    assert response.status_code == 202
    body = response.json()
    assert body["filename"] == name
    assert body["media_type"] == media_type
    assert body["file_size"] == len(content)
    assert body["status"] == "uploaded"
    assert body["summary_status"] == "none"
    assert body["chunk_count"] == 0
    assert [(j["kind"], j["status"], j["retry_count"]) for j in body["jobs"]] == [
        ("index", "queued", 0)
    ]
    assert "storage_path" not in body and "content_hash" not in body
    files = stored_files()
    assert len(files) == 1 and files[0].read_bytes() == content
    assert count(db, "ingestion_jobs") == 1


def test_upload_accepts_the_sample_pdf(user: TestClient) -> None:
    content = SAMPLE_PDF.read_bytes()

    response = upload(user, SAMPLE_PDF.name, content)

    assert response.status_code == 202
    assert response.json()["media_type"] == "pdf"
    assert (
        hashlib.sha256(stored_files()[0].read_bytes()).hexdigest()
        == hashlib.sha256(content).hexdigest()
    )


def test_client_supplied_paths_never_reach_the_filesystem(user: TestClient) -> None:
    response = upload(user, "../../outside/evil.txt", TEXT)

    assert response.status_code == 202
    assert response.json()["filename"] == "evil.txt"
    base = get_settings().data_dir.resolve()
    assert all(base in path.resolve().parents for path in stored_files())


# --- AC-02 ---------------------------------------------------------------------


@pytest.mark.parametrize("name", ["report.docx", "archive.zip", "no-extension", "image.PNG"])
def test_unsupported_format_is_refused_and_leaves_nothing_behind(
    user: TestClient, db: psycopg.Connection, name: str
) -> None:
    response = upload(user, name, b"some bytes")

    assert response.status_code == 415
    assert response.json()["code"] == "UNSUPPORTED_MEDIA_TYPE"
    assert ".pdf" in response.json()["detail"]
    assert count(db, "documents") == 0
    assert stored_files() == []


def test_extension_check_ignores_case(user: TestClient) -> None:
    assert upload(user, "NOTES.TXT", TEXT).status_code == 202


def test_empty_file_is_refused(user: TestClient, db: psycopg.Connection) -> None:
    response = upload(user, "empty.txt", b"")

    assert response.status_code == 422
    assert response.json()["code"] == "EMPTY_FILE"
    assert count(db, "documents") == 0
    assert stored_files() == []


def test_file_over_the_size_limit_is_refused(
    make_client: Callable[..., TestClient], db: psycopg.Connection
) -> None:
    from app.core.env_loader import get_settings as real_settings

    app = create_app()
    app.dependency_overrides[real_settings] = lambda: real_settings().model_copy(
        update={"max_upload_mb": 1}
    )
    client = TestClient(app, headers={"Origin": ALLOWED_ORIGIN})
    register_and_login(client, "kim")

    response = upload(client, "big.txt", b"x" * (1024 * 1024 + 1))

    assert response.status_code == 413
    assert response.json()["code"] == "FILE_TOO_LARGE"
    assert count(db, "documents") == 0
    assert stored_files() == []


# --- AC-35 ---------------------------------------------------------------------


def test_same_user_uploading_the_same_content_gets_the_existing_document(
    user: TestClient, db: psycopg.Connection
) -> None:
    first = upload(user, "notes.txt", TEXT)
    again = upload(user, "renamed-copy.txt", TEXT)

    assert first.status_code == 202
    assert again.status_code == 200
    assert again.json()["id"] == first.json()["id"]
    assert again.json()["filename"] == "notes.txt"
    assert count(db, "documents") == 1
    assert count(db, "ingestion_jobs") == 1
    assert len(stored_files()) == 1


def test_different_users_uploading_the_same_content_each_get_their_own_document(
    user: TestClient, other: TestClient, db: psycopg.Connection
) -> None:
    mine = upload(user, "notes.txt", TEXT)
    theirs = upload(other, "notes.txt", TEXT)

    assert mine.status_code == theirs.status_code == 202
    assert mine.json()["id"] != theirs.json()["id"]
    assert count(db, "documents") == 2
    assert len(stored_files()) == 2
    assert [d["id"] for d in user.get(DOCUMENTS).json()] == [mine.json()["id"]]
    assert [d["id"] for d in other.get(DOCUMENTS).json()] == [theirs.json()["id"]]


# --- list and read ---------------------------------------------------------------


def test_list_shows_only_my_documents_newest_first(user: TestClient, other: TestClient) -> None:
    first = upload(user, "a.txt", b"first").json()["id"]
    second = upload(user, "b.txt", b"second").json()["id"]
    upload(other, "c.txt", b"third")

    listing = user.get(DOCUMENTS).json()

    assert {d["id"] for d in listing} == {first, second}
    assert "jobs" not in listing[0]


def test_read_returns_the_document_with_its_latest_job(user: TestClient) -> None:
    document_id = upload(user, "notes.txt", TEXT).json()["id"]

    response = user.get(f"{DOCUMENTS}/{document_id}")

    assert response.status_code == 200
    assert response.json()["id"] == document_id
    assert response.json()["jobs"][0]["kind"] == "index"


def test_unknown_document_is_not_found(user: TestClient) -> None:
    response = user.get(f"{DOCUMENTS}/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["code"] == "DOCUMENT_NOT_FOUND"


# --- isolation (read and delete part of AC-32) ------------------------------------


def test_another_user_cannot_read_or_delete_my_document(
    user: TestClient, other: TestClient, db: psycopg.Connection
) -> None:
    document_id = upload(user, "notes.txt", TEXT).json()["id"]

    read = other.get(f"{DOCUMENTS}/{document_id}")
    deleted = other.delete(f"{DOCUMENTS}/{document_id}")

    # Indistinguishable from a document that does not exist.
    assert read.status_code == deleted.status_code == 404
    assert read.json() == user.get(f"{DOCUMENTS}/{uuid.uuid4()}").json()
    assert user.get(f"{DOCUMENTS}/{document_id}").status_code == 200
    assert count(db, "documents") == 1
    assert len(stored_files()) == 1


# --- delete ------------------------------------------------------------------------


def test_delete_removes_the_document_its_job_and_its_file(
    user: TestClient, db: psycopg.Connection
) -> None:
    document_id = upload(user, "notes.txt", TEXT).json()["id"]

    response = user.delete(f"{DOCUMENTS}/{document_id}")

    assert response.status_code == 204
    assert user.get(f"{DOCUMENTS}/{document_id}").status_code == 404
    assert user.get(DOCUMENTS).json() == []
    assert count(db, "documents") == 0
    assert count(db, "ingestion_jobs") == 0
    assert stored_files() == []


def test_deleted_content_can_be_uploaded_again(user: TestClient) -> None:
    first = upload(user, "notes.txt", TEXT).json()["id"]
    user.delete(f"{DOCUMENTS}/{first}")

    again = upload(user, "notes.txt", TEXT)

    assert again.status_code == 202
    assert again.json()["id"] != first


def test_deleting_twice_is_not_found(user: TestClient) -> None:
    document_id = upload(user, "notes.txt", TEXT).json()["id"]
    user.delete(f"{DOCUMENTS}/{document_id}")

    assert user.delete(f"{DOCUMENTS}/{document_id}").status_code == 404


def test_the_owner_can_open_the_original_file_and_nobody_else_can(
    user: TestClient, other: TestClient
) -> None:
    """D89: a source card links to the paper at the cited page; the file is served inline to
    its owner only, and a stranger gets the same 404 as for a missing document."""
    body = upload(user, "notes.md", b"# Notes\n\nLightRAG builds a graph.\n").json()

    response = user.get(f"{DOCUMENTS}/{body['id']}/file")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert response.headers["content-disposition"].startswith('inline; filename="notes.md"')
    assert response.content == b"# Notes\n\nLightRAG builds a graph.\n"
    assert other.get(f"{DOCUMENTS}/{body['id']}/file").status_code == 404
    assert user.get(f"{DOCUMENTS}/{uuid.uuid4()}/file").status_code == 404


def test_a_ready_document_without_a_summary_can_have_one_queued(
    user: TestClient, db: psycopg.Connection
) -> None:
    """D89: a document indexed before summaries existed has summary_status "none"; the
    retry queues a summary job for it instead of refusing."""
    body = upload(user, "notes.md", b"# Notes\n\nLightRAG builds a graph.\n").json()
    db.execute(
        "UPDATE documents SET status = 'ready', summary_status = 'none' WHERE id = %s",
        (body["id"],),
    )
    db.commit()

    response = user.post(f"{DOCUMENTS}/{body['id']}/retry")

    assert response.status_code == 202
    kinds = [(j["kind"], j["status"]) for j in response.json()["jobs"]]
    assert ("summary", "queued") in kinds
