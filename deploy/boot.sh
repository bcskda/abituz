#!/bin/sh
. venv/bin/activate
./update.sh
exec gunicorn -b :5000 --access-logfile - --error-logfile - abituz:app
