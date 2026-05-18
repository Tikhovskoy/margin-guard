"""Точка входа FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from margin_guard import __version__
from margin_guard.api.routes import cost_prices, health, margins
from margin_guard.config import get_settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Жизненный цикл приложения."""
    settings = get_settings()
    logger.info("startup", env=settings.app_env, version=__version__)
    yield
    logger.info("shutdown")


def create_app() -> FastAPI:
    """Фабрика приложения."""
    app = FastAPI(
        title="margin-guard",
        version=__version__,
        description="Контроль маржи для селлеров WB и Ozon",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(margins.router, prefix="/api/v1")
    app.include_router(cost_prices.router, prefix="/api/v1")
    return app


app = create_app()
