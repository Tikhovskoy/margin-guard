"""Тесты уведомлений о низкой марже."""

from datetime import date
from decimal import Decimal

import pytest

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.application.send_low_margin_alerts import SendLowMarginAlerts
from margin_guard.domain.entities import FeeLine, MarginAlert, Marketplace, SkuOperation


class FakeNotifier:
    """Notifier для проверки отправленных предупреждений."""

    def __init__(self) -> None:
        self.sent: list[MarginAlert] = []

    async def send(self, alerts: list[MarginAlert]) -> None:
        self.sent = alerts


@pytest.mark.asyncio
async def test_sends_alert_only_for_margin_below_threshold() -> None:
    operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        operation_date=date(2026, 7, 20),
        revenue=Decimal("1000"),
        fees=(FeeLine("commission", Decimal("300")),),
    )
    margins = CalculateMarginsUseCase().execute(
        [operation],
        {(Marketplace.WILDBERRIES.value, "WB-001"): Decimal("500")},
    )
    notifier = FakeNotifier()

    alerts = await SendLowMarginAlerts(notifier).execute(
        Marketplace.WILDBERRIES,
        margins,
        Decimal("25"),
    )

    assert alerts == notifier.sent
    assert alerts[0].margin_percent == Decimal("20.00")
    assert alerts[0].message == (
        "⚠️ Низкая маржа: wildberries / WB-001 — 20.00% при пороге 25%"
    )
