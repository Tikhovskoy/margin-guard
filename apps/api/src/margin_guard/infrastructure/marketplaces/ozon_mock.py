"""Mock-адаптер Ozon."""

from datetime import date
from decimal import Decimal

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.domain.ports import MarketplaceAdapter


class OzonMockAdapter(MarketplaceAdapter):
    """Тестовые данные Ozon."""

    @property
    def marketplace(self) -> Marketplace:
        return Marketplace.OZON

    async def fetch_operations(
        self,
        date_from: date,
        date_to: date,
    ) -> list[SkuOperation]:
        _ = date_from, date_to
        return [
            SkuOperation(
                marketplace=Marketplace.OZON,
                sku="OZ-101",
                operation_date=date_to,
                revenue=Decimal("2200.00"),
                fees=(
                    FeeLine("commission", Decimal("880.00")),
                    FeeLine("logistics", Decimal("200.00")),
                ),
            ),
        ]
