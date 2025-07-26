#!/bin/sh

echo "Waiting for the Database..."
while ! nc -z $DATABASE_HOST 5432; do
    sleep 1
done
echo "Database is Ready"

python manage.py migrate

python manage.py runserver 0.0.0.0:8000