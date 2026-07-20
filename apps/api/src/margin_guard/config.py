"""Настройки приложения."""

from decimal import Decimal
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

MarketplaceMode = Literal["mock", "live"]


class Settings(BaseSettings):
    """Конфигурация из переменных окружения."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: str = "local"
    log_level: str = "INFO"
    secret_key: str = "change-me"

    database_url: str = (
        "postgresql+asyncpg://margin_guard:margin_guard@localhost:5432/margin_guard"
    )
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    wb_mode: MarketplaceMode = "mock"
    ozon_mode: MarketplaceMode = "mock"
    wb_api_token: str = ""
    ozon_client_id: str = ""
    ozon_api_key: str = ""

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    low_margin_threshold_percent: Decimal = Decimal("20")


@lru_cache
def get_settings() -> Settings:
    """Кэшированный экземпляр настроек."""
    return Settings()
