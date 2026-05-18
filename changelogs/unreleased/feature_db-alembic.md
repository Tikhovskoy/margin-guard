## [MR](https://github.com/Tikhovskoy/margin-guard/pull/0)

### Added

- Alembic и начальная миграция: `sku_operations`, `sku_operation_fees`, `sku_cost_prices`
- ORM-модели, async `session_scope`, репозиторий операций
- use case `PersistMarketplaceOperations`, сохранение в worker sync
- тесты маппера и репозитория (SQLite)

### Changed

- worker sync пишет операции в PostgreSQL
