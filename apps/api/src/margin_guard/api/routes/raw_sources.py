"""Загрузка первичных финансовых файлов."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, Response, UploadFile, status
from pydantic import BaseModel

from margin_guard.application.upload_raw_source import (
    RawSourceUploadError,
    UploadRawSource,
)
from margin_guard.config import get_settings
from margin_guard.domain.entities import (
    Marketplace,
    RawSourceStatus,
    RawSourceType,
)
from margin_guard.infrastructure.db.repositories.raw_sources import (
    SqlAlchemyRawSourceRepository,
)
from margin_guard.infrastructure.db.session import session_scope
from margin_guard.infrastructure.storage.local_raw_sources import (
    LocalRawSourceStorage,
)

router = APIRouter(prefix="/raw-sources", tags=["raw-sources"])


class RawSourceUploadResponse(BaseModel):
    """Метаданные загруженного первичного файла."""

    id: str
    marketplace: Marketplace
    source_type: RawSourceType
    original_filename: str
    content_type: str
    size_bytes: int
    checksum_sha256: str
    status: RawSourceStatus
    created_at: datetime
    created: bool


@router.post(
    "/upload",
    response_model=RawSourceUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_raw_source(
    response: Response,
    file: Annotated[UploadFile, File(description="Исходный CSV или XLSX")],
    marketplace: Annotated[Marketplace, Query(description="Маркетплейс")],
    source_type: Annotated[RawSourceType, Query(description="Тип источника")],
) -> RawSourceUploadResponse:
    """Сохранить оригинальный файл и зарегистрировать его метаданные."""
    settings = get_settings()
    content = await file.read(settings.raw_source_max_upload_bytes + 1)
    if len(content) > settings.raw_source_max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Файл больше допустимого размера",
        )

    try:
        async with session_scope() as session:
            repository = SqlAlchemyRawSourceRepository(session)
            storage = LocalRawSourceStorage(settings.raw_source_dir)
            result = await UploadRawSource(repository, storage).execute(
                marketplace=marketplace,
                source_type=source_type,
                original_filename=file.filename or "",
                content_type=file.content_type or "application/octet-stream",
                content=content,
            )
    except RawSourceUploadError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    source = result.source
    if not result.created:
        response.status_code = status.HTTP_200_OK
    return RawSourceUploadResponse(
        id=source.id,
        marketplace=source.marketplace,
        source_type=source.source_type,
        original_filename=source.original_filename,
        content_type=source.content_type,
        size_bytes=source.size_bytes,
        checksum_sha256=source.checksum_sha256,
        status=source.status,
        created_at=source.created_at,
        created=result.created,
    )
