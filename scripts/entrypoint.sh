#!/bin/sh
#
# Performs setup operations for the project in the production mode.

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py check --deploy --settings config.settings.production

mv ./media/* /media && rm -rf ./media

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --access-logfile -
