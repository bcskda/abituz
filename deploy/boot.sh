#!/bin/sh
source venv/bin/activate
while true
do
	sleep 20
	flask db upgrade
	if [ "$?" -eq 0 ]
	then
		break
	fi
	echo 'DB connect failed'
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - abituz:app