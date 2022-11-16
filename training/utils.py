import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import MetaData
import os

# from dotenv import load_dotenv
# load_dotenv(dotenv_path="local.env")

DATA_PATH = "data/"
connection_string = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PWD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"

engine = create_engine(connection_string, max_identifier_length=30, pool_size=2, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base.metadata.create_all(engine)


def bulk_drop(table_list):
    with engine.connect() as conn:
        for tb_name in table_list:
            conn.execute(str(f"DROP TABLE IF EXISTS {tb_name}"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_data_csv():
	order_df = pd.read_csv(DATA_PATH + "data_order.csv", parse_dates=["CHECKOUT_DATE"])
	product_df = pd.read_csv(DATA_PATH + "data_metadata_product.csv")
	store_df = pd.read_csv(DATA_PATH + "data_metadata_store.csv")

	return order_df, product_df, store_df

def get_data_db(conn):
	order_df = pd.read_sql("select order_id, store_id, brand_id, product_id, product_variant_id, quantity, variant_case_price_cents, checkout_date from fact_order_items", conn)
	order_df['checkout_date'] = pd.to_datetime(order_df['checkout_date'], format="%Y-%m-%d")
	product_df = pd.read_sql("select product_id, product_metadata from dim_product", conn)
	store_df = pd.read_sql("select store_id, store_type, region_id, store_size from dim_store", conn)

	order_df.columns = [col.upper() for col in order_df.columns]
	product_df.columns = [col.upper() for col in product_df.columns]
	store_df.columns = [col.upper() for col in store_df.columns]
	
	return order_df, product_df, store_df

def transform_order_data(order_df):
	
	store_product_df = order_df.groupby(['STORE_ID','PRODUCT_ID','CHECKOUT_DATE'],as_index=False)['QUANTITY'].sum()

	return store_product_df

def transform_product_data(product_df):
	

	product_df['DUP_CNT'] = product_df.groupby('PRODUCT_ID')['PRODUCT_METADATA'].rank(method="first", ascending=True)

	cate_df = pd.merge(
		product_df[product_df['DUP_CNT']==1],
		product_df[product_df['DUP_CNT']==2],
		how='outer',
		on='PRODUCT_ID'
	)[['PRODUCT_METADATA_x', 'PRODUCT_METADATA_y']].drop_duplicates().reset_index(drop=True)

	def cross_count(count_value_in:pd.Series, count_range:pd.Series):
		result = []
		for x in list(count_value_in):
			result.append(list(count_range).count(x))

		return result


	cate_df['cross_count_x'] = cross_count(cate_df['PRODUCT_METADATA_x'], cate_df['PRODUCT_METADATA_y'])
	cate_df['cross_count_y'] = cross_count(cate_df['PRODUCT_METADATA_y'], cate_df['PRODUCT_METADATA_x'])

	cate_df['self_count_x'] = cate_df.groupby('PRODUCT_METADATA_x')['PRODUCT_METADATA_x'].transform('count')
	cate_df['self_count_y'] = cate_df.groupby('PRODUCT_METADATA_y')['PRODUCT_METADATA_y'].transform('count')

	cate_df['all_count_x'] = cate_df['cross_count_x'] + cate_df['self_count_x']
	cate_df['all_count_y'] = cate_df['cross_count_y'] + cate_df['self_count_y']

	cate_df['SUB_CATE'] = np.where(cate_df['all_count_x'] < cate_df['all_count_y'], cate_df['PRODUCT_METADATA_x'], cate_df['PRODUCT_METADATA_y'])

	cate_df['SUB_CATE'] = np.where(cate_df['PRODUCT_METADATA_x'].str.contains('+', regex=False), cate_df['PRODUCT_METADATA_x'], cate_df['SUB_CATE'])
	cate_df['SUB_CATE'] = np.where(cate_df['PRODUCT_METADATA_y'].str.contains('+', regex=False), cate_df['PRODUCT_METADATA_y'], cate_df['SUB_CATE'])

	cate_df['CATE'] = np.where(cate_df['SUB_CATE']==cate_df['PRODUCT_METADATA_x'],cate_df['PRODUCT_METADATA_y'], cate_df['PRODUCT_METADATA_x'])

	cate_df['SUB_CATE'] = np.where(cate_df['SUB_CATE'].isnull(), 'Other ' + cate_df['CATE'], cate_df['SUB_CATE'])

	product_df = product_df.merge(
		cate_df[['SUB_CATE','CATE']], 
		how='left',
		left_on='PRODUCT_METADATA',
		right_on='SUB_CATE')

	product_df.dropna(inplace=True)
	product_df.drop(columns=['PRODUCT_METADATA','DUP_CNT'], inplace=True)

	return product_df


def transform_store_data(store_df):


	store_df['STORE_TYPE'].fillna('Unknown', inplace=True)
	store_df['REGION_ID'].fillna(-1, inplace=True)
	store_df['STORE_SIZE'] .fillna(0, inplace=True)

	store_df.rename(columns={'REGION_ID':'STORE_REGION_ID'}, inplace=True)

	return store_df

def get_features(final_df):
	# lb = LabelEncoder()
	# final_df['STORE_TYPE'] = lb.fit_transform(final_df['STORE_TYPE'])
	# final_df['CATE'] = lb.fit_transform(final_df['CATE'])
	# final_df['SUB_CATE'] = lb.fit_transform(final_df['SUB_CATE'])
	final_df['checkout_dow'] = final_df['CHECKOUT_DATE'].dt.dayofweek
	final_df['checkout_day'] = final_df['CHECKOUT_DATE'].dt.day

	feature_list_1 = {
		'avg_qty_store_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'STORE_ID', 'window':30},
		'avg_qty_product_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'PRODUCT_ID', 'window':30},
		'avg_qty_storetype_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'STORE_TYPE', 'window':30},
		'avg_qty_storeregion_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'STORE_REGION_ID', 'window':30},
		'avg_qty_cate_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'CATE', 'window':30},
		'avg_qty_subcate_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':'SUB_CATE', 'window':30},
		'avg_qty_store_product_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':['STORE_ID', 'PRODUCT_ID'], 'window':30},
		'avg_qty_store_cate_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':['STORE_ID', 'CATE'], 'window':30},
		'avg_qty_storeregion_cate_l30d': {'agg':'mean', 'object':'QUANTITY', 'scope':['STORE_REGION_ID', 'CATE'], 'window':30},
	}

	for key, val in feature_list_1.items():
		final_df[key] = final_df.groupby(val['scope'])[val['object']].transform(lambda x: x.rolling(window=val['window']).agg(val['agg']))
		final_df[key].fillna(0, inplace=True)

	lags = [1,2,3,4,5,6,7,14,28]
	for lag in lags:
		final_df[f'qty_store_product_lag_{lag}'] = final_df.groupby(['STORE_ID','PRODUCT_ID'],as_index=False)['QUANTITY'].shift(lag)

	feature_list_2 = {
		'dcnt_product_store_daily': {'agg':'nunique', 'object':'PRODUCT_ID', 'scope':['STORE_ID','CHECKOUT_DATE']},
		'dcnt_cate_store_daily': {'agg':'nunique', 'object':'CATE', 'scope':['STORE_ID','CHECKOUT_DATE']},
		'dcnt_subcate_store_daily': {'agg':'nunique', 'object':'SUB_CATE', 'scope':['STORE_ID','CHECKOUT_DATE']},
		'sum_qty_store_daily': {'agg':'sum', 'object':'QUANTITY', 'scope':['STORE_ID','CHECKOUT_DATE']},
	}

	for key, val in feature_list_2.items():
		final_df[key] = final_df.groupby(val['scope'])[val['object']].transform(val['agg'])

	lags = [1,3,7]
	for lag in lags:
		for k in feature_list_2.keys():
			final_df[f'{k}_lag_{lag}'] = final_df.groupby(['STORE_ID','PRODUCT_ID'],as_index=False)[k].shift(lag)

	return final_df

def join_all_data(store_product_df, store_df, product_df):
	
	final_df = store_product_df.merge(store_df, how='left', on='STORE_ID') \
						.merge(product_df, how='left', on='PRODUCT_ID').sort_values(by='CHECKOUT_DATE', ascending=True)

	final_df.sort_values(by=['CHECKOUT_DATE','STORE_ID','PRODUCT_ID'], ascending=True, inplace=True)

	return final_df

def split_train_test(final_df):
	train = final_df[final_df['CHECKOUT_DATE'].dt.month!=5]
	test = final_df[final_df['CHECKOUT_DATE'].dt.month==5]

	return train,test

