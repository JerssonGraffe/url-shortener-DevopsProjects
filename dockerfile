FROM public.ecr.aws/lambda/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
WORKDIR /var/task
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY entrypoints/app.py .
CMD ["app.lambda_handler"]