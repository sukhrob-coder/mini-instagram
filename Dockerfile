FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --no-root




FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y gettext netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .

COPY ./scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
