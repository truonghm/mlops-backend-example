import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os

def get_data(query,conn):
	df = pd.read_sql(query, conn)
	df.drop(["id", "created_at"], axis=1, inplace=True)
	df.columns = [col.upper() for col in df.columns]

	return df

def transform_order_data(conn):

	order_df = get_data("select * from fact_order_item", conn)
	store_product_df = order_df.groupby(['STORE_ID','PRODUCT_ID','CHECKOUT_DATE'],as_index=False)['QUANTITY'].sum()

	return store_product_df

def transform_product_data(conn):
	product_df = get_data("select * from dim_product", conn)

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


def transform_store_data(conn):
	store_df = get_data("select * from dim_store", conn)

	store_df['STORE_TYPE'].fillna('Unknown', inplace=True)
	store_df['REGION_ID'].fillna(-1, inplace=True)
	store_df['STORE_SIZE'] .fillna(0, inplace=True)

	store_df.rename(columns={'REGION_ID':'STORE_REGION_ID'}, inplace=True)

	return store_df

	