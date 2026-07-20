# margin-guard

Сервис контроля маржи для селлеров Wildberries и Ozon.

## Возможности (roadmap)

- Синхронизация финансовых отчётов (WB, Ozon)
- Расчёт маржи по SKU с учётом себестоимости
- Веб-дашборд и Telegram-алерты
- Режимы `mock` и `live` для интеграций с маркетплейсами

## Стек

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Celery, PostgreSQL, Redis
- **Frontend:** Next.js, TypeScript
- **Infra:** Docker Compose, GitHub Actions

## Быстрый старт

```bash
uv sync --all-packages --group dev
uv run python scripts/run_demo.py
```

Команда создаёт `.env` из шаблона при первом запуске, поднимает Docker Compose,
применяет миграции и загружает demo CSV.

- API: `http://localhost:8000/docs` (или порт из `API_PORT`)
- Health: `http://localhost:8000/health`
- Preview: `http://localhost:8000/api/v1/margins/preview`

Для Unix-окружения доступен эквивалент: `make demo`.

Подробнее: [docs/development.md](docs/development.md).

## Ветки

| Ветка | Назначение |
|-------|------------|
| `main` | Стабильная версия |
| `dev` | Обкатка изменений |
| `feature/*` | Новые задачи (от `main`, PR в `main`) |

Документация: [WORKFLOW.md](docs/WORKFLOW.md), [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Лицензия

MIT
