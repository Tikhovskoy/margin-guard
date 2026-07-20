"""Mock-уведомления Telegram без внешнего API."""

import structlog

from margin_guard.domain.entities import MarginAlert
from margin_guard.domain.ports import AlertNotifier

logger = structlog.get_logger()


class TelegramMockNotifier(AlertNotifier):
    """Пишет Telegram-подобные уведомления в структурированный лог."""

    async def send(self, alerts: list[MarginAlert]) -> None:
        for alert in alerts:
            logger.warning(
                "telegram_mock_alert",
                marketplace=alert.marketplace.value,
                sku=alert.sku,
                margin_percent=str(alert.margin_percent),
                threshold_percent=str(alert.threshold_percent),
                message=alert.message,
            )
