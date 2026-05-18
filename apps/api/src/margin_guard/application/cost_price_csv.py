"""Разбор CSV с себестоимостью."""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from io import StringIO

from margin_guard.domain.entities import CostPriceEntry, Marketplace

REQUIRED_COLUMNS = frozenset({"marketplace", "sku", "cost_price"})


class CostPriceCsvError(ValueError):
    """Ошибка формата CSV."""


class CostPriceCsvParser:
    """Парсит CSV: marketplace, sku, cost_price."""

    def parse(self, content: str) -> list[CostPriceEntry]:
        """Вернуть список записей или выбросить CostPriceCsvError."""
        if not content.strip():
            raise CostPriceCsvError("Файл пуст")

        reader = csv.DictReader(StringIO(content.strip()))
        if reader.fieldnames is None:
            raise CostPriceCsvError("Отсутствует строка заголовка")

        headers = {name.strip().lower() for name in reader.fieldnames if name}
        missing = REQUIRED_COLUMNS - headers
        if missing:
            cols = ", ".join(sorted(missing))
            raise CostPriceCsvError(f"Нет обязательных колонок: {cols}")

        entries: list[CostPriceEntry] = []
        for line_no, row in enumerate(reader, start=2):
            if not any(cell and cell.strip() for cell in row.values()):
                continue
            entries.append(self._parse_row(row, line_no))
        if not entries:
            raise CostPriceCsvError("Нет строк с данными")
        return entries

    def _parse_row(self, row: dict[str, str | None], line_no: int) -> CostPriceEntry:
        marketplace_raw = self._cell(row, "marketplace", line_no)
        sku = self._cell(row, "sku", line_no)
        cost_raw = self._cell(row, "cost_price", line_no)
        marketplace = self._parse_marketplace(marketplace_raw, line_no)
        cost_price = self._parse_decimal(cost_raw, line_no)
        if cost_price < 0:
            raise CostPriceCsvError(f"Строка {line_no}: себестоимость не может быть < 0")
        return CostPriceEntry(
            marketplace=marketplace,
            sku=sku,
            cost_price=cost_price,
        )

    def _cell(self, row: dict[str, str | None], column: str, line_no: int) -> str:
        for key, value in row.items():
            if key and key.strip().lower() == column:
                if value is None or not value.strip():
                    raise CostPriceCsvError(f"Строка {line_no}: пустое поле {column}")
                return value.strip()
        raise CostPriceCsvError(f"Строка {line_no}: нет поля {column}")

    def _parse_marketplace(self, raw: str, line_no: int) -> Marketplace:
        try:
            return Marketplace(raw.lower())
        except ValueError as exc:
            raise CostPriceCsvError(
                f"Строка {line_no}: неизвестный marketplace '{raw}'",
            ) from exc

    def _parse_decimal(self, raw: str, line_no: int) -> Decimal:
        normalized = raw.replace(",", ".")
        try:
            return Decimal(normalized)
        except InvalidOperation as exc:
            raise CostPriceCsvError(
                f"Строка {line_no}: неверное число '{raw}'",
            ) from exc
