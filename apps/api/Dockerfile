FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY apps/api/pyproject.toml apps/api/
RUN uv sync --package margin-guard-api --no-dev 2>/dev/null || \
    pip install -e apps/api

COPY apps/api/src apps/api/src

ENV PYTHONPATH=/app/apps/api/src

CMD ["uvicorn", "margin_guard.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
