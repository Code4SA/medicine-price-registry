#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

npm install
python manage.py collectstatic --noinput
gunicorn mpr.wsgi:application --log-file - --bind 0.0.0.0:5000
