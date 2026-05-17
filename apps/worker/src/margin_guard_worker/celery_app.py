"""Конфигурация Celery."""

from celery import Celery

from margin_guard.config import get_settings

settings = get_settings()

celery_app = Celery(
    "margin_guard",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["margin_guard_worker.tasks.sync"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    beat_schedule={
        "sync-marketplaces-daily": {
            "task": "margin_guard_worker.tasks.sync.run_daily_sync",
            "schedule": 86400.0,
        },
    },
)
