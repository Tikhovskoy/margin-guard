"""Тесты репозитория себестоимости."""

from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import CostPriceEntry, Marketplace
from margin_guard.infrastructure.db.repositories.cost_prices import (
    SqlAlchemyCostPriceRepository,
)


@pytest.mark.asyncio
async def test_upsert_inserts_and_updates(db_session: AsyncSession) -> None:
    repository = SqlAlchemyCostPriceRepository(db_session)
    entry = CostPriceEntry(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        cost_price=Decimal("300.00"),
    )
    first = await repository.upsert_entries([entry])
    assert first == 1

    updated = CostPriceEntry(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        cost_price=Decimal("350.00"),
    )
    second = await repository.upsert_entries([updated])
    assert second == 1

    entries = await repository.list_entries(Marketplace.WILDBERRIES)
    assert entries == [updated]

    await db_session.commit()
