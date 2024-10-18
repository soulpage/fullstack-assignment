#!/bin/sh

# Main entry point script for the Docker container

# Wait for SQLite
/wait-for-sqlite.sh python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Django application with Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
