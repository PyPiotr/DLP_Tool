#!/bin/sh

echo "Migrating the databse..."
pipenv run python manage.py migrate

echo "superuser"
pipenv run python manage.py createsu

echo "Starting the server..."
pipenv run python manage.py runserver 0.0.0.0:8000