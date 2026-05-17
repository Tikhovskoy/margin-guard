"""Mock-адаптер Wildberries."""

from datetime import date
from decimal import Decimal

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.domain.ports import MarketplaceAdapter


class WildberriesMockAdapter(MarketplaceAdapter):
    """Тестовые данные WB (структура как в отчёте реализации)."""

    @property
    def marketplace(self) -> Marketplace:
        return Marketplace.WILDBERRIES

    async def fetch_operations(
        self,
        date_from: date,
        date_to: date,
    ) -> list[SkuOperation]:
        _ = date_from, date_to
        return [
            SkuOperation(
                marketplace=Marketplace.WILDBERRIES,
                sku="WB-001",
                operation_date=date_to,
                revenue=Decimal("1500.00"),
                fees=(
                    FeeLine("commission", Decimal("225.00")),
                    FeeLine("logistics", Decimal("120.00")),
                ),
            ),
            SkuOperation(
                marketplace=Marketplace.WILDBERRIES,
                sku="WB-002",
                operation_date=date_to,
                revenue=Decimal("800.00"),
                fees=(
                    FeeLine("commission", Decimal("200.00")),
                    FeeLine("logistics", Decimal("90.00")),
                    FeeLine("ads", Decimal("150.00")),
                ),
            ),
        ]
