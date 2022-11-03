import sys
import os
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

import pandas as pd


# from . import SessionLocal, engine, Base, bulk_drop
from orm import *
from utils import *

def insert_data(df:pd.DataFrame, ORM:str):
    with SessionLocal() as session:
        session.bulk_insert_mappings(ORM, df.to_dict(orient="records"))
        session.commit()
		
if __name__ == "__main__":
	store_product_df = transform_order_data()
	product_df = transform_product_data()
	store_df = transform_store_data()
	final_df = join_all_data(store_product_df, store_df, product_df)

	features = get_features(final_df)

	train, test = split_train_test(features)
	# features.to_csv(DATA_PATH + "features.csv", index=False)
	train.to_csv(DATA_PATH + "train.csv", index=False)
	test.to_csv(DATA_PATH + "test.csv", index=False)
	features.to_csv(DATA_PATH + "features.csv", index=False)

	bulk_drop(['features'])

	Base.metadata.create_all(engine)

	features.columns = [col.lower() for col in features.columns]
	features = features.fillna(0)

	# print(features.head(1).to_dict(orient="records"))
	insert_data(features, FeaturesTable)