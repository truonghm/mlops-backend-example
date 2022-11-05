from datetime import timedelta, tzinfo

import json, os, datetime, pytz, sys, pendulum
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator

sys.path.append(os.getenv("AIRFLOW_MAIN_PATH", "/opt/airflow/dags/repo"))
print(sys.path)

from utils import *
from orm import FeaturesTable

local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")



def insert_data(df:pd.DataFrame, ORM:str):
    with SessionLocal() as session:
        session.bulk_insert_mappings(ORM, df.to_dict(orient="records"))
        session.commit()

def preprocessing():
    try:
        print(connection_string)
        order_df, product_df, store_df = get_data_db(engine)

        store_product_df = transform_order_data(order_df)
        product_df = transform_product_data(product_df)
        store_df = transform_store_data(store_df)
        final_df = join_all_data(store_product_df, store_df, product_df)

        features = get_features(final_df)

        # train.to_csv(DATA_PATH + "train.csv", index=False)
        # test.to_csv(DATA_PATH + "test.csv", index=False)
        # features.to_csv(DATA_PATH + "features.csv", index=False)

        features.columns = [col.lower() for col in features.columns]
        features = features.fillna(0)

        # print(features.head(1).to_dict(orient="records"))
        insert_data(features, FeaturesTable)

    except Exception as e:
        print(repr(e))
        raise e

default_args = {
    "owner": "truonghm",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
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
    params={},
) as update_data_agg_dag:
    update_data_agg_dag.doc_md = __doc__
    test_dremio = PythonOperator(
        task_id="quantity_prediction_preprocessing",
        python_callable=preprocessing,
    )
