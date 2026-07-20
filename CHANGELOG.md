# История релизов

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).  
Версии: [Semantic Versioning](https://semver.org/lang/ru/).

Накопление изменений: файлы в `changelogs/unreleased/` (по одному на ветку).  
Сборка релиза: `make release_changelog v=0.1.0`.

Категории: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

## [0.1.0] - 2026-07-20

### Added

- каталог `changelogs/unreleased/`, `collector.py`, цели `make changelog` и `make release_changelog`
- шаблон PR только с чеклистом (пункт про changelog)
- `scripts/create_changelog.py` для Windows без make
- Сборка Docker-образов API и worker в GitHub Actions на PR и push в `main`/`dev`.
- сущность `CostPriceEntry`, парсер CSV, репозиторий и use case импорта
- `POST /api/v1/cost-prices/upload` (UTF-8, до 1 МБ)
- расчёт маржи по ключу `(marketplace, sku)`
- Alembic и начальная миграция: `sku_operations`, `sku_operation_fees`, `sku_cost_prices`
- ORM-модели, async `session_scope`, репозиторий операций
- use case `PersistMarketplaceOperations`, сохранение в worker sync
- тесты маппера и репозитория (SQLite)
- Demo CSV с себестоимостью для Wildberries и Ozon.
- Команда `uv run python scripts/run_demo.py` для запуска Docker, миграций и demo-flow.
- Цель `make demo` для Unix-окружений.
- Получение себестоимости SKU по маркетплейсу из репозитория.
- Use case формирования карты себестоимости для расчёта маржи.
- Mock Telegram-уведомления для SKU с маржой ниже настраиваемого порога.
- Поле `alerts` в preview маржи с наглядным текстом уведомления.


### Changed

- удалены парсинг changelog из текста PR и workflow `changelog-on-merge`
- `release.yml` использует `changelogs/collector.py`
- `CalculateMarginsUseCase` принимает карту себестоимости по маркетплейсу и SKU
- worker sync пишет операции в PostgreSQL
- README и инструкция локальной разработки описывают однокомандный demo-запуск.
- Внешний порт API настраивается переменной `API_PORT` и по умолчанию равен `8000`.
- В образ API добавлены конфигурация и файлы Alembic для запуска миграций внутри Docker.
- Preview маржи использует сохранённую в БД себестоимость вместо query-параметров.
- В `.env` добавлен `LOW_MARGIN_THRESHOLD_PERCENT` со значением по умолчанию `20`.
- README перестроен в формат витрины: проблема, demo-flow, результат расчёта, архитектура и команды проверки.


### Removed

- `scripts/changelog_extract.py`, `scripts/changelog_release.py`


### Fixed

- Docker-образы API и Celery worker теперь устанавливают зависимости в виртуальное окружение и используют его исполняемые файлы.
- Контейнерные подключения к PostgreSQL и Redis используют имена сервисов Docker Compose.
