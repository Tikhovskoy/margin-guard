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
                source_operation_id=f"mock-wb-{date_to.isoformat()}-001",
                sku="WB-001",
                operation_date=date_to,
                quantity=2,
                revenue=Decimal("3000.00"),
                fees=(
                    FeeLine("commission", Decimal("450.00")),
                    FeeLine("logistics", Decimal("240.00")),
                ),
                rrd_id=100001,
                srid="mock-wb-srid-001",
                report_id=int(date_to.strftime("%Y%m%d")),
            ),
            SkuOperation(
                marketplace=Marketplace.WILDBERRIES,
                source_operation_id=f"mock-wb-{date_to.isoformat()}-002",
                sku="WB-002",
                operation_date=date_to,
                quantity=1,
                revenue=Decimal("800.00"),
                fees=(
                    FeeLine("commission", Decimal("200.00")),
                    FeeLine("logistics", Decimal("90.00")),
                    FeeLine("ads", Decimal("150.00")),
                ),
                rrd_id=100002,
                srid="mock-wb-srid-002",
                report_id=int(date_to.strftime("%Y%m%d")),
            ),
        ]
