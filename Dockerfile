FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src ./src


FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

EXPOSE 8005

CMD ["sh", "-c", "python -m granian --interface asgi ${APP_MODULE:-src.main:app} --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8005} --workers ${APP_WORKERS:-2} --loop uvloop"]
