"""Тесты HTTP API."""

from fastapi.testclient import TestClient

from margin_guard.api.main import create_app


def test_health() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["wb_mode"] == "mock"
