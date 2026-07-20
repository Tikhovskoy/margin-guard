"""Use case: уведомление о SKU с низкой маржой."""

from decimal import Decimal

from margin_guard.domain.entities import MarginAlert, Marketplace, SkuMargin
from margin_guard.domain.ports import AlertNotifier


class SendLowMarginAlerts:
    """Находит низкую маржу и передаёт предупреждения notifier-у."""

    def __init__(self, notifier: AlertNotifier) -> None:
        self._notifier = notifier

    async def execute(
        self,
        marketplace: Marketplace,
        margins: list[SkuMargin],
        threshold_percent: Decimal,
    ) -> list[MarginAlert]:
        """Отправить уведомления для SKU с маржой ниже порога."""
        alerts = [
            MarginAlert(
                marketplace=marketplace,
                sku=margin.sku,
                margin_percent=margin.margin_percent,
                threshold_percent=threshold_percent,
            )
            for margin in margins
            if margin.margin_percent < threshold_percent
        ]
        await self._notifier.send(alerts)
        return alerts
