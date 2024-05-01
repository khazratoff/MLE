#!/bin/bash

airflow db migrate

airflow users create \
          --username admin \
          --firstname FIRST_NAME \
          --lastname LAST_NAME \
          --role Admin \
          --email admin@example.org \
          --password admin

airflow scheduler &

airflow webserver --port 8080
