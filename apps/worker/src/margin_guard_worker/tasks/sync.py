"""Синхронизация отчётов маркетплейсов."""

import asyncio
from datetime import date, timedelta

import structlog

from margin_guard.config import get_settings
from margin_guard.domain.entities import Marketplace
from margin_guard.infrastructure.marketplaces.factory import create_adapter
from margin_guard_worker.celery_app import celery_app

logger = structlog.get_logger()


async def _sync_marketplace(marketplace: Marketplace) -> int:
    settings = get_settings()
    adapter = create_adapter(marketplace, settings)
    date_to = date.today()
    date_from = date_to - timedelta(days=1)
    operations = await adapter.fetch_operations(date_from, date_to)
    logger.info(
        "sync_complete",
        marketplace=marketplace.value,
        operations=len(operations),
        mode=settings.wb_mode
        if marketplace == Marketplace.WILDBERRIES
        else settings.ozon_mode,
    )
    return len(operations)


@celery_app.task(name="margin_guard_worker.tasks.sync.run_daily_sync")
def run_daily_sync() -> dict[str, int]:
    """Ежедневная синхронизация WB и Ozon (mock/live)."""

    async def _run() -> dict[str, int]:
        wb = await _sync_marketplace(Marketplace.WILDBERRIES)
        ozon = await _sync_marketplace(Marketplace.OZON)
        return {"wildberries": wb, "ozon": ozon}

    return asyncio.run(_run())
