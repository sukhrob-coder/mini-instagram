#!/bin/bash

set -e

echo "--> Docker entrypoint started..."

if [ -n "$DATABASE_URL" ]; then
    echo "--> Waiting for database..."

    DB_HOST=$(python -c "from urllib.parse import urlparse; print(urlparse('$DATABASE_URL').hostname)")
    DB_PORT=$(python -c "from urllib.parse import urlparse; print(urlparse('$DATABASE_URL').port or 5432)")

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "--> Database is ready!"
fi

if [ "$AUTO_MIGRATE" = "true" ]; then
    echo "--> Running database migrations..."
    python manage.py migrate --noinput
fi
if [ "$AUTO_COLLECTSTATIC" = "true" ]; then
    echo "--> Collecting static files..."
    python manage.py collectstatic --noinput
fi

echo "--> Executing command: $@"
exec "$@"