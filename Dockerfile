FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ADD . /app

WORKDIR /app

RUN uv sync --frozen

FROM python:3.13-alpine

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

WORKDIR /app

ADD ./app ./app
ADD ./pyproject.toml ./

RUN ls -lah

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "./", "--root-path", "./"]
