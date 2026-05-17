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

## Запуск (Docker)

```bash
docker compose up -d
```

- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Превью маржи (mock): http://localhost:8000/api/v1/margins/preview

## Запуск без Docker (только API)

```bash
# PostgreSQL и Redis должны быть доступны
uv run --package margin-guard-api uvicorn margin_guard.api.main:app --reload --app-dir apps/api/src
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
  infrastructure/   # адаптеры WB/Ozon
  api/              # FastAPI routes
apps/worker/        # Celery
```
