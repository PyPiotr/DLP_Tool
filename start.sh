#!/bin/sh

echo "Migrating the databse..."
pipenv run python manage.py migrate

echo "Starting the server..."
pipenv run python manage.py runserver 0.0.0.0:5050