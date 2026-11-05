"""Health endpoint behaviour, with dependency probes replaced by fakes."""

from fastapi.testclient import TestClient

from app.api.health import DependencyStatus, get_health_probe
from app.main import create_app


class FakeProbe:
    def __init__(self, database_ok: bool, ollama_ok: bool) -> None:
        self._database_ok = database_ok
        self._ollama_ok = ollama_ok

    async def database(self) -> DependencyStatus:
        return DependencyStatus(ok=self._database_ok, detail="fake")

    async def ollama(self) -> DependencyStatus:
        return DependencyStatus(ok=self._ollama_ok, detail="fake")


def _client(database_ok: bool, ollama_ok: bool) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_health_probe] = lambda: FakeProbe(database_ok, ollama_ok)
    return TestClient(app)


def test_health_is_ok_when_all_dependencies_are_reachable() -> None:
    body = _client(database_ok=True, ollama_ok=True).get("/api/health").json()

    assert body["status"] == "ok"
    assert body["database"]["ok"] is True
    assert body["ollama"]["ok"] is True


def test_health_is_degraded_when_database_is_down() -> None:
    response = _client(database_ok=False, ollama_ok=True).get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "degraded"


def test_health_is_degraded_when_ollama_is_down() -> None:
    body = _client(database_ok=True, ollama_ok=False).get("/api/health").json()

    assert body["status"] == "degraded"
    assert body["ollama"]["ok"] is False


def test_health_reports_the_assignment_context_limit() -> None:
    body = _client(database_ok=True, ollama_ok=True).get("/api/health").json()

    assert body["llm_context_limit"] == 10_000
