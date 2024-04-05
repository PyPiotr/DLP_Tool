#!/bin/sh

echo "Migrating the databse..."
pipenv run python manage.py migrate

echo "superuser"
pipenv run python manage.py createsu

echo "Starting the server..."


pipenv run gunicorn app.asgi --bind 0.0.0.0:8000 --chdir=/app -k uvicorn.workers.UvicornWorker