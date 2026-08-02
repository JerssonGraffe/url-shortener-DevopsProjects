FROM public.ecr.aws/lambda/python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
WORKDIR /var/task
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=/var/lang
RUN uv sync --frozen --no-dev

COPY entrypoints/app.py .
CMD ["app.handler"]