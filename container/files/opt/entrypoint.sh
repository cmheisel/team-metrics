#!/bin/sh
set -x

cd /app/
python="/app-ve/bin/python"

$python manage.py migrate
$python manage.py collectstatic --noinput


exec "$@"
