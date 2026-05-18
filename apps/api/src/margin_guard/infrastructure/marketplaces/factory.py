"""Фабрика адаптеров по режиму mock/live."""

from margin_guard.config import Settings
from margin_guard.domain.entities import Marketplace
from margin_guard.domain.ports import MarketplaceAdapter
from margin_guard.infrastructure.marketplaces.ozon_mock import OzonMockAdapter
from margin_guard.infrastructure.marketplaces.wildberries_mock import (
    WildberriesMockAdapter,
)


class LiveAdapterNotConfiguredError(RuntimeError):
    """Live-режим без реализации адаптера."""


def create_wb_adapter(settings: Settings) -> MarketplaceAdapter:
    """Создать адаптер Wildberries."""
    if settings.wb_mode == "mock":
        return WildberriesMockAdapter()
    if not settings.wb_api_token:
        msg = "WB_API_TOKEN обязателен для WB_MODE=live"
        raise LiveAdapterNotConfiguredError(msg)
    msg = "Live-адаптер WB ещё не реализован"
    raise LiveAdapterNotConfiguredError(msg)


def create_ozon_adapter(settings: Settings) -> MarketplaceAdapter:
    """Создать адаптер Ozon."""
    if settings.ozon_mode == "mock":
        return OzonMockAdapter()
    if not settings.ozon_client_id or not settings.ozon_api_key:
        msg = "OZON_CLIENT_ID и OZON_API_KEY обязательны для OZON_MODE=live"
        raise LiveAdapterNotConfiguredError(msg)
    msg = "Live-адаптер Ozon ещё не реализован"
    raise LiveAdapterNotConfiguredError(msg)


def create_adapter(
    marketplace: Marketplace,
    settings: Settings,
) -> MarketplaceAdapter:
    """Создать адаптер по площадке."""
    if marketplace == Marketplace.WILDBERRIES:
        return create_wb_adapter(settings)
    return create_ozon_adapter(settings)
