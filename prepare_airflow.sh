#!/usr/bin/env sh

mkdir -p ./etl/logs ./etl/plugins
echo "AIRFLOW_UID=$(id -u)" >> .env
