from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

import pandas as pd

import sys
import os

sys.path.insert(0, os.path.dirname(sys.path[0]))

from database import SessionLocal, engine, Base, bulk_drop
from database.models import *

def insert_data(df:pd.DataFrame, ORM:str):
    with SessionLocal() as session:
        session.bulk_insert_mappings(ORM, df.to_dict(orient="records"))
        session.commit()

if __name__ == "__main__":
    bulk_drop(['dim_product','dim_store','fact_order_item'])

    Base.metadata.create_all(engine)

    order_df = pd.read_csv('database/raw_data/data_order.csv', parse_dates=["CHECKOUT_DATE"])
    order_df.columns = [col.lower() for col in order_df.columns]
    store_df = pd.read_csv('database/raw_data/data_metadata_store.csv')
    store_df.columns = [col.lower() for col in store_df.columns]
    product_df = pd.read_csv('database/raw_data/data_metadata_product.csv')
    product_df.columns = [col.lower() for col in product_df.columns]

    print(order_df.head(1).to_dict(orient="records"))
    data_mapping = {
        OrderTable: order_df,
        ProductTable: product_df,
        StoreTable: store_df
    }


    for obj, df in data_mapping.items():
        print(len(df))
        insert_data(df, obj)