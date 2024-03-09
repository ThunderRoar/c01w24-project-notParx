#!/bin/ash

echo "Apply Database Migrations"
python manage.py migrate

exec "$@"