FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY apps/api/pyproject.toml apps/api/
COPY apps/api/src apps/api/src
COPY alembic.ini ./
COPY apps/api/alembic apps/api/alembic
RUN uv sync --frozen --package margin-guard-api --no-dev

ENV PYTHONPATH=/app/apps/api/src
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "margin_guard.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
