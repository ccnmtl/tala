#!/bin/bash

cd /var/www/tala/tala/
python manage.py migrate --noinput --settings=tala.settings_docker
python manage.py collectstatic --noinput --settings=tala.settings_docker
python manage.py compress --settings=tala.settings_docker
exec gunicorn --env \
  DJANGO_SETTINGS_MODULE=tala.settings_docker \
  tala.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
