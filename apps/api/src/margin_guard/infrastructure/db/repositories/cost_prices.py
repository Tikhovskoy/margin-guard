"""Репозиторий себестоимости."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import CostPriceEntry, Marketplace
from margin_guard.domain.ports import CostPriceRepository
from margin_guard.infrastructure.db.models import SkuCostPriceRow


class SqlAlchemyCostPriceRepository(CostPriceRepository):
    """Upsert себестоимости в PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_entries(self, entries: list[CostPriceEntry]) -> int:
        if not entries:
            return 0

        affected = 0
        now = datetime.now(UTC)
        for entry in entries:
            existing = await self._find_existing(entry)
            if existing is None:
                self._session.add(
                    SkuCostPriceRow(
                        marketplace=entry.marketplace.value,
                        sku=entry.sku,
                        cost_price=entry.cost_price,
                        updated_at=now,
                    ),
                )
                affected += 1
                continue
            existing.cost_price = entry.cost_price
            existing.updated_at = now
            affected += 1
        await self._session.flush()
        return affected

    async def list_entries(self, marketplace: Marketplace) -> list[CostPriceEntry]:
        stmt = select(SkuCostPriceRow).where(
            SkuCostPriceRow.marketplace == marketplace.value,
        )
        result = await self._session.execute(stmt)
        return [
            CostPriceEntry(
                marketplace=marketplace,
                sku=row.sku,
                cost_price=row.cost_price,
            )
            for row in result.scalars()
        ]

    async def _find_existing(self, entry: CostPriceEntry) -> SkuCostPriceRow | None:
        stmt = select(SkuCostPriceRow).where(
            SkuCostPriceRow.marketplace == entry.marketplace.value,
            SkuCostPriceRow.sku == entry.sku,
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()
