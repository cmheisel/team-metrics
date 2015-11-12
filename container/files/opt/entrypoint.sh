#!/bin/sh

cd /app/
python="/app-ve/bin/python"

$python manage.py migrate
$python manage.py collectstatic --noinput
$python ./manage.py runserver 0.0.0.0:8000
