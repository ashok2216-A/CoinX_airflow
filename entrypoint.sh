#!/bin/bash
set -e

if [ "$1" = "webserver" ]; then
    airflow db init
    airflow users create \
        --username admin \
        --password admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com
    exec airflow webserver
elif [ "$1" = "scheduler" ]; then
    exec airflow scheduler
else
    exec "$@"
fi
