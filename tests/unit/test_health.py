from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_when_dependencies_are_healthy(monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.health.check_database",
        lambda db: True,
    )
    monkeypatch.setattr(
        "app.api.routes.health.check_redis",
        lambda: True,
    )

    response = client.get("/readiness")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "dependencies": {
            "database": "ok",
            "redis": "ok",
        },
    }


def test_readiness_when_dependency_is_unavailable(monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.health.check_database",
        lambda db: False,
    )
    monkeypatch.setattr(
        "app.api.routes.health.check_redis",
        lambda: True,
    )

    response = client.get("/readiness")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "dependencies": {
            "database": "unavailable",
            "redis": "ok",
        },
    }