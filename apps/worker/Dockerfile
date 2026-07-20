FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY apps/api/pyproject.toml apps/api/
COPY apps/worker/pyproject.toml apps/worker/
COPY apps/api/src apps/api/src
COPY apps/worker/src apps/worker/src
RUN uv sync --frozen --package margin-guard-worker --no-dev

ENV PYTHONPATH=/app/apps/api/src:/app/apps/worker/src
ENV PATH="/app/.venv/bin:$PATH"

CMD ["celery", "-A", "margin_guard_worker.celery_app", "worker", "--loglevel=info"]
