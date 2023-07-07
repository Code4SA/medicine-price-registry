#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

gunicorn mpr.wsgi:application --log-file - --bind 0.0.0.0:5000
