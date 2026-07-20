"""Порты (интерфейсы) домена."""

from abc import ABC, abstractmethod
from datetime import date

from margin_guard.domain.entities import (
    CostPriceEntry,
    MarginAlert,
    Marketplace,
    SkuOperation,
)


class MarketplaceAdapter(ABC):
    """Адаптер финансовых отчётов маркетплейса."""

    @property
    @abstractmethod
    def marketplace(self) -> Marketplace:
        """Идентификатор площадки."""

    @abstractmethod
    async def fetch_operations(
        self,
        date_from: date,
        date_to: date,
    ) -> list[SkuOperation]:
        """Загрузить операции за период."""


class OperationRepository(ABC):
    """Сохранение операций маркетплейсов в БД."""

    @abstractmethod
    async def upsert_operations(self, operations: list[SkuOperation]) -> int:
        """Сохранить операции; вернуть число затронутых строк."""


class CostPriceRepository(ABC):
    """Сохранение себестоимости в БД."""

    @abstractmethod
    async def upsert_entries(self, entries: list[CostPriceEntry]) -> int:
        """Сохранить записи; вернуть число затронутых строк."""

    @abstractmethod
    async def list_entries(self, marketplace: Marketplace) -> list[CostPriceEntry]:
        """Вернуть себестоимость всех SKU маркетплейса."""


class AlertNotifier(ABC):
    """Отправка уведомлений о низкой марже."""

    @abstractmethod
    async def send(self, alerts: list[MarginAlert]) -> None:
        """Отправить список предупреждений."""
