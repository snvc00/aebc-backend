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
    # Run development environment
    python3 manage.py runserver 0.0.0.0:8000
else
    # Change ownership of media dir
    chown -R aecb /var/www/media

    # Enable uWSGI application
    uwsgi --uid aecb --gid 1000 --socket :8000 --master --enable-threads --wsgi-file /api/aecb/wsgi.py
fi