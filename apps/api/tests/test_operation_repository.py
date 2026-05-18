"""Тесты репозитория операций."""

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.infrastructure.db.repositories.operations import (
    SqlAlchemyOperationRepository,
)


@pytest.mark.asyncio
async def test_upsert_inserts_and_updates(db_session: AsyncSession) -> None:
    repository = SqlAlchemyOperationRepository(db_session)
    operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        operation_date=date(2026, 5, 1),
        revenue=Decimal("1000.00"),
        fees=(FeeLine("commission", Decimal("100.00")),),
    )
    inserted = await repository.upsert_operations([operation])
    assert inserted == 1

    updated_operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        operation_date=date(2026, 5, 1),
        revenue=Decimal("1200.00"),
        fees=(
            FeeLine("commission", Decimal("120.00")),
            FeeLine("logistics", Decimal("30.00")),
        ),
    )
    updated = await repository.upsert_operations([updated_operation])
    assert updated == 1

    again = await repository.upsert_operations([updated_operation])
    assert again == 1

    await db_session.commit()
