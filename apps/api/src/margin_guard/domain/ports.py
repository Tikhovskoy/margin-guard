"""Порты (интерфейсы) домена."""

from abc import ABC, abstractmethod
from datetime import date

from margin_guard.domain.entities import (
    CostPriceEntry,
    MarginAlert,
    Marketplace,
    RawSource,
    RawSourceType,
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


class RawSourceRepository(ABC):
    """Метаданные неизменяемых первичных источников."""

    @abstractmethod
    async def get_by_checksum(
        self,
        marketplace: Marketplace,
        source_type: RawSourceType,
        checksum_sha256: str,
    ) -> RawSource | None:
        """Найти ранее загруженный источник по содержимому."""

    @abstractmethod
    async def add(self, source: RawSource) -> RawSource:
        """Сохранить метаданные нового источника."""


class RawSourceStorage(ABC):
    """Хранилище неизменяемых байтов первичного источника."""

    @abstractmethod
    async def store(self, storage_key: str, content: bytes) -> None:
        """Сохранить байты без возможности перезаписи."""

    @abstractmethod
    async def read(self, storage_key: str) -> bytes:
        """Прочитать исходные байты."""
