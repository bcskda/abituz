#!/bin/sh
echo 'Trying to update'
while true
do
	APP_UPDATE_AUTO=0 flask db upgrade
	if [ "$?" -eq 0 ]
	then
		break
	fi
	echo 'DB connect failed'
	sleep 10
done
