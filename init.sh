#!/bin/bash

set -e

# Check for schema changes and apply them
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
python3 manage.py defaultsuperuser

# Check the existance of all the required media directories
python3 manage.py check_media_dirs

if [ "$DJANGO_ENV" == "development" ]
then
    # Create test accounts
    python3 manage.py test_accounts

    # Run development environment
    python3 manage.py runserver 0.0.0.0:8000
else
    # Enable uWSGI application
    uwsgi --socket :8000 --master --enable-threads --wsgi-file /api/aecb/wsgi.py
fi