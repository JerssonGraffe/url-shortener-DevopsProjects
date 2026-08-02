FROM python:3.13 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-dev

COPY entrypoints ./entrypoints

FROM python:3.13-slim

WORKDIR /var/task

RUN pip install --no-cache-dir awslambdaric

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app/entrypoints ./entrypoints

ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["entrypoints.app.handler"]