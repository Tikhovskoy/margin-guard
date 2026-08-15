"""Загрузка неизменяемого первичного файла."""

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import PurePosixPath
from uuid import uuid4

from margin_guard.domain.entities import (
    Marketplace,
    RawSource,
    RawSourceStatus,
    RawSourceType,
)
from margin_guard.domain.ports import RawSourceRepository, RawSourceStorage

ALLOWED_EXTENSIONS = frozenset({".csv", ".xlsx"})


class RawSourceUploadError(ValueError):
    """Некорректный первичный файл."""


@dataclass(frozen=True, slots=True)
class RawSourceUploadResult:
    """Результат идемпотентной загрузки."""

    source: RawSource
    created: bool


class UploadRawSource:
    """Сохраняет оригинальные байты и их метаданные."""

    def __init__(
        self,
        repository: RawSourceRepository,
        storage: RawSourceStorage,
    ) -> None:
        self._repository = repository
        self._storage = storage

    async def execute(
        self,
        *,
        marketplace: Marketplace,
        source_type: RawSourceType,
        original_filename: str,
        content_type: str,
        content: bytes,
    ) -> RawSourceUploadResult:
        """Загрузить источник или вернуть существующий для тех же байтов."""
        filename = self._normalize_filename(original_filename)
        if not content:
            raise RawSourceUploadError("Файл пуст")

        checksum = sha256(content).hexdigest()
        existing = await self._repository.get_by_checksum(
            marketplace,
            source_type,
            checksum,
        )
        if existing is not None:
            return RawSourceUploadResult(source=existing, created=False)

        storage_key = (
            f"{marketplace.value}/{source_type.value}/{checksum[:2]}/{checksum}"
        )
        await self._storage.store(storage_key, content)
        source = RawSource(
            id=str(uuid4()),
            marketplace=marketplace,
            source_type=source_type,
            original_filename=filename,
            content_type=content_type or "application/octet-stream",
            size_bytes=len(content),
            checksum_sha256=checksum,
            storage_key=storage_key,
            status=RawSourceStatus.UPLOADED,
            created_at=datetime.now(UTC),
        )
        return RawSourceUploadResult(
            source=await self._repository.add(source),
            created=True,
        )

    @staticmethod
    def _normalize_filename(filename: str) -> str:
        normalized = PurePosixPath(filename.replace("\\", "/")).name.strip()
        if not normalized:
            raise RawSourceUploadError("Не указано имя файла")
        if len(normalized) > 255:
            raise RawSourceUploadError("Имя файла длиннее 255 символов")
        if PurePosixPath(normalized).suffix.lower() not in ALLOWED_EXTENSIONS:
            raise RawSourceUploadError("Поддерживаются только CSV и XLSX")
        return normalized
