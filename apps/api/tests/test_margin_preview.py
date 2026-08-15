"""Тесты preview маржи с себестоимостью из БД."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from margin_guard.api.main import create_app
from margin_guard.api.routes import margins
from margin_guard.domain.entities import CostPriceEntry, Marketplace


class FakeCostPriceRepository:
    """Репозиторий себестоимости для HTTP-теста."""

    def __init__(self, _session: object) -> None:
        pass

    async def list_entries(self, marketplace: Marketplace) -> list[CostPriceEntry]:
        if marketplace is not Marketplace.WILDBERRIES:
            return []
        return [
            CostPriceEntry(
                marketplace=Marketplace.WILDBERRIES,
                sku="WB-001",
                cost_price=Decimal("600.00"),
            ),
        ]


def test_preview_uses_cost_prices_from_repository(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Preview берёт себестоимость из репозитория, а не из query-параметров."""

    @asynccontextmanager
    async def fake_session_scope() -> AsyncIterator[object]:
        yield object()

    monkeypatch.setattr(margins, "session_scope", fake_session_scope)
    monkeypatch.setattr(
        margins,
        "SqlAlchemyCostPriceRepository",
        FakeCostPriceRepository,
    )

    response = TestClient(create_app()).get(
        "/api/v1/margins/preview?threshold_percent=40",
    )

    assert response.status_code == 200
    assert response.json()["data_mode"] == "mock"
    items = response.json()["items"]
    assert items[0]["sku"] == "WB-001"
    assert items[0]["quantity"] == 2
    assert items[0]["source_operation_id"].startswith("mock-wb-")
    assert items[0]["cost_price"] == "600.00"
    assert items[0]["cost_amount"] == "1200.00"
    assert items[0]["margin"] == "1110.00"
    assert items[0]["rrd_id"] == "100001"
    assert items[0]["srid"] == "mock-wb-srid-001"
    assert items[0]["report_id"] == "20260815"
    assert items[0]["calculation_status"] == "complete"
    assert items[1]["sku"] == "WB-002"
    assert items[1]["cost_price"] is None
    assert items[1]["margin"] is None
    assert items[1]["margin_percent"] is None
    assert items[1]["calculation_status"] == "missing_cost"
    alerts = response.json()["alerts"]
    assert alerts == [
        {
            "sku": "WB-001",
            "margin_percent": "37.00",
            "threshold_percent": "40",
            "message": "⚠️ Низкая маржа: wildberries / WB-001 — 37.00% при пороге 40%",
        },
    ]
