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
                source_operation_id=f"mock-ozon-{date_to.isoformat()}-101",
                sku="OZ-101",
                operation_date=date_to,
                quantity=2,
                revenue=Decimal("4400.00"),
                fees=(
                    FeeLine("commission", Decimal("1760.00")),
                    FeeLine("logistics", Decimal("400.00")),
                ),
            ),
        ]
