#!/usr/bin/env bash

cd /app || echo "Unable to navigate to /app"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
/usr/sbin/crond -f -l 8 &
python manage.py fcmdaemon &
gunicorn --worker-class=gevent --worker-connections=$WORKER_CONNECTIONS --timeout $WORKER_TIMEOUT --access-logfile - --workers $WORKERS --bind 0.0.0.0:80 wplusnotifier.wsgi:application