# Локальная разработка

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker и Docker Compose

## Установка

```bash
cd D:\work\margin-guard
cp .env.example .env
uv sync --all-packages --group dev
```

## Demo-режим

```bash
uv run python scripts/run_demo.py
```

Скрипт создаёт `.env` из `.env.example`, если его ещё нет, запускает Docker
Compose, применяет миграции Alembic, загружает `demo/cost-prices.csv` и выводит
preview маржи. Для Unix-окружения доступен эквивалент: `make demo`.

Внешний порт API задаётся переменной `API_PORT` в `.env` и по умолчанию равен
`8000`.

## Mock Telegram-алерты

`GET /api/v1/margins/preview` возвращает предупреждения для SKU, у которых
процент маржи ниже `LOW_MARGIN_THRESHOLD_PERCENT` (по умолчанию `20`). В
mock-режиме сообщения не отправляются во внешний Telegram API, а выводятся в
структурированный лог и в поле `alerts` ответа preview.

Поле `data_mode` явно показывает источник ответа: `mock` или `live`. Для SKU
без себестоимости расчёт помечается как `missing_cost`; значения себестоимости,
маржи и процента маржи возвращаются как `null`, и alert для такой позиции не
создаётся.

Каждая операция содержит обязательные `source_operation_id` и `quantity`.
Для WB дополнительно поддерживаются `rrd_id`, `srid` и `report_id`. Повторная
загрузка операции с тем же `marketplace + source_operation_id` обновляет запись,
а разные операции одного SKU за одну дату сохраняются отдельно. В расчёте
используется полная себестоимость `cost_amount = cost_price × quantity`.
Числовые идентификаторы WB API возвращает строками, чтобы frontend не терял
точность значений `int64`.

Порог можно изменить в `.env` или разово передать query-параметром:

```text
GET /api/v1/margins/preview?threshold_percent=25
```

## Запуск (Docker)

```bash
docker compose up -d
```

- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Превью маржи (mock): http://localhost:8000/api/v1/margins/preview
- Загрузка себестоимости (CSV): `POST /api/v1/cost-prices/upload`
- Загрузка первичного файла: `POST /api/v1/raw-sources/upload`

## Первичные файлы

API принимает исходные CSV/XLSX и сохраняет их байты без изменений. Метаданные
и SHA-256 записываются в PostgreSQL, а содержимое — в каталог
`RAW_SOURCE_DIR` (по умолчанию `data/raw-sources`). Повторная загрузка одинакового
файла для того же маркетплейса и типа источника возвращает существующую запись.

```bash
curl -X POST "http://localhost:8000/api/v1/raw-sources/upload?marketplace=wildberries&source_type=realization_report" \
  -F "file=@report.csv"
```

Доступные типы: `realization_report`, `marketplace_api`, `bank_statement`.
Максимальный размер задаёт `RAW_SOURCE_MAX_UPLOAD_BYTES` (по умолчанию 25 МБ).
В Docker содержимое сохраняется в именованном volume `raw_source_data`.

## Запуск без Docker (только API)

```bash
# PostgreSQL и Redis должны быть доступны
uv run --package margin-guard-api uvicorn margin_guard.api.main:app --reload --app-dir apps/api/src
```

## Миграции БД

PostgreSQL должен быть запущен (`docker compose up -d postgres`).

```bash
set PYTHONPATH=apps/api/src
uv run alembic -c alembic.ini upgrade head
```

Новая ревизия (после изменения ORM-моделей):

```bash
uv run alembic -c alembic.ini revision --autogenerate -m "описание"
uv run alembic -c alembic.ini upgrade head
```

## Тесты

```bash
set PYTHONPATH=apps/api/src;apps/worker/src
uv run pytest
uv run ruff check apps/api apps/worker scripts
uv run mypy apps/api/src
```

## Celery worker

```bash
uv run --package margin-guard-worker celery -A margin_guard_worker.celery_app worker --loglevel=info
```

`PYTHONPATH` должен включать `apps/api/src` и `apps/worker/src`.

## Режимы маркетплейсов

| Переменная | Значение |
|------------|----------|
| `WB_MODE` | `mock` (по умолчанию) или `live` |
| `OZON_MODE` | `mock` или `live` |

Live-адаптеры подключаются после получения API-токенов.

## Структура

```
apps/api/src/margin_guard/
  domain/           # сущности, расчёт маржи, порты
  application/      # use cases
  infrastructure/   # адаптеры WB/Ozon, БД, репозитории
    storage/         # локальное хранилище первичных файлов
  api/              # FastAPI routes
apps/api/alembic/   # миграции Alembic
apps/worker/        # Celery
```
