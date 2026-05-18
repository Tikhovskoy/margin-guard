## [MR](https://github.com/Tikhovskoy/margin-guard/pull/0)

### Added

- сущность `CostPriceEntry`, парсер CSV, репозиторий и use case импорта
- `POST /api/v1/cost-prices/upload` (UTF-8, до 1 МБ)
- расчёт маржи по ключу `(marketplace, sku)`

### Changed

- `CalculateMarginsUseCase` принимает карту себестоимости по маркетплейсу и SKU
