from datetime import timedelta, tzinfo

import json, os, datetime, pytz, sys, pendulum
import pandas as pd
import numpy as np
import sqlite3
import mysql.connector

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.sensors.external_task import ExternalTaskMarker, ExternalTaskSensor
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup

from utils import transform_order_data, transform_product_data, transform_store_data

mysql_user = os.getenv('MYSQL_USER')
mysql_pwd = os.getenv('MYSQL_PWD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_db = os.getenv('MYSQL_DB') 

local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")

def preprocessing():
	db_string = os.getenv("SQLITE_DB")
	try:
		conn = mysql.connector.connect(user=mysql_user, password=mysql_pwd, host=mysql_host,port=mysql_port, database=mysql_db)
		cursor = conn.cursor()

		store_product_df = transform_order_data(conn)
		product_df = transform_product_data(conn)
		store_df = transform_store_data(conn)

	except Exception as e:
		print(repr(e))
		raise e

default_args = {
    "owner": "truonghm",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "catchup": False,
}

with DAG(
    "quantity_prediction_preprocessing",
    default_args=default_args,
    description="Preprocess data for quantity prediction model",
    schedule_interval='0 6 * * *',
    start_date=datetime.datetime(2022, 11, 2, tzinfo=local_tz),
    tags=["ml"],
    catchup=False,
    params={
        'channel': '36k-gt-active',
        'date_lag': 1
    },
) as update_data_agg_dag:
    update_data_agg_dag.doc_md = __doc__
    test_dremio = PythonOperator(
        task_id="gt_active_alert",
        python_callable=preprocessing,
    )
