"""Use case: получение себестоимости для расчёта маржи."""

from decimal import Decimal

from margin_guard.domain.entities import Marketplace
from margin_guard.domain.ports import CostPriceRepository


class GetCostPricesForMarketplace:
    """Возвращает себестоимость SKU заданного маркетплейса."""

    def __init__(self, repository: CostPriceRepository) -> None:
        self._repository = repository

    async def execute(self, marketplace: Marketplace) -> dict[tuple[str, str], Decimal]:
        """Собрать карту себестоимости по ключу маркетплейс/SKU."""
        entries = await self._repository.list_entries(marketplace)
        return {
            (entry.marketplace.value, entry.sku): entry.cost_price for entry in entries
        }
