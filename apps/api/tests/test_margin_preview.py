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

    response = TestClient(create_app()).get("/api/v1/margins/preview")

    assert response.status_code == 200
    items = response.json()["items"]
    assert items[0]["sku"] == "WB-001"
    assert items[0]["cost_price"] == "600.00"
    assert items[0]["margin"] == "555.00"
    assert items[1]["sku"] == "WB-002"
    assert items[1]["cost_price"] == "0"
