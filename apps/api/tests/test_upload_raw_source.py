"""Тесты загрузки первичного источника."""

from margin_guard.application.upload_raw_source import (
    RawSourceUploadError,
    UploadRawSource,
)
from margin_guard.domain.entities import Marketplace, RawSource, RawSourceType
from margin_guard.domain.ports import RawSourceRepository, RawSourceStorage


class MemoryRepository(RawSourceRepository):
    def __init__(self) -> None:
        self.sources: list[RawSource] = []

    async def get_by_checksum(
        self,
        marketplace: Marketplace,
        source_type: RawSourceType,
        checksum_sha256: str,
    ) -> RawSource | None:
        return next(
            (
                source
                for source in self.sources
                if source.marketplace == marketplace
                and source.source_type == source_type
                and source.checksum_sha256 == checksum_sha256
            ),
            None,
        )

    async def add(self, source: RawSource) -> RawSource:
        self.sources.append(source)
        return source


class MemoryStorage(RawSourceStorage):
    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}

    async def store(self, storage_key: str, content: bytes) -> None:
        self.files[storage_key] = content

    async def read(self, storage_key: str) -> bytes:
        return self.files[storage_key]


async def test_uploads_original_bytes_and_normalizes_filename() -> None:
    repository = MemoryRepository()
    storage = MemoryStorage()
    use_case = UploadRawSource(repository, storage)

    result = await use_case.execute(
        marketplace=Marketplace.WILDBERRIES,
        source_type=RawSourceType.REALIZATION_REPORT,
        original_filename=r"C:\reports\report.csv",
        content_type="text/csv",
        content=b"sku,amount\n1,100\n",
    )

    assert result.created is True
    assert result.source.original_filename == "report.csv"
    assert result.source.size_bytes == 17
    assert len(result.source.checksum_sha256) == 64
    assert storage.files[result.source.storage_key] == b"sku,amount\n1,100\n"


async def test_returns_existing_source_for_same_content() -> None:
    repository = MemoryRepository()
    storage = MemoryStorage()
    use_case = UploadRawSource(repository, storage)
    arguments = {
        "marketplace": Marketplace.OZON,
        "source_type": RawSourceType.MARKETPLACE_API,
        "original_filename": "report.xlsx",
        "content_type": "application/octet-stream",
        "content": b"same-content",
    }

    first = await use_case.execute(**arguments)
    second = await use_case.execute(**arguments)

    assert first.created is True
    assert second.created is False
    assert second.source.id == first.source.id
    assert len(storage.files) == 1


async def test_rejects_empty_or_unsupported_file() -> None:
    use_case = UploadRawSource(MemoryRepository(), MemoryStorage())

    try:
        await use_case.execute(
            marketplace=Marketplace.WILDBERRIES,
            source_type=RawSourceType.BANK_STATEMENT,
            original_filename="report.pdf",
            content_type="application/pdf",
            content=b"content",
        )
    except RawSourceUploadError as exc:
        assert str(exc) == "Поддерживаются только CSV и XLSX"
    else:
        raise AssertionError("Ожидалась ошибка расширения")

    try:
        await use_case.execute(
            marketplace=Marketplace.WILDBERRIES,
            source_type=RawSourceType.BANK_STATEMENT,
            original_filename="report.csv",
            content_type="text/csv",
            content=b"",
        )
    except RawSourceUploadError as exc:
        assert str(exc) == "Файл пуст"
    else:
        raise AssertionError("Ожидалась ошибка пустого файла")
