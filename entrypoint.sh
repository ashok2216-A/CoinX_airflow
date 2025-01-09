#!/bin/bash

# Initialize the Airflow database
airflow db init

# Start the Airflow webserver and scheduler
airflow webserver -p 8080 &
sleep 10
airflow scheduler
