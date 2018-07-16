#!/bin/sh
. venv/bin/activate
./update.sh

case "$APP_ROLE" in
	"update" ) exec flask ds update
		;;
	"view" | * ) exec gunicorn -b :5000 --access-logfile - --error-logfile - abituz:app
		;;
esac
