#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

# Collect static files so WhiteNoise can serve them
DJANGO_SETTINGS_MODULE=hotwheels_project.settings.production python manage.py collectstatic --no-input

# Run database migrations
DJANGO_SETTINGS_MODULE=hotwheels_project.settings.production python manage.py migrate

# Create superuser if needed
DJANGO_SETTINGS_MODULE=hotwheels_project.settings.production python deploy_setup.py
