import xgboost as xgb
import pandas as pd
import logging
import mlflow
import numpy as np
from sklearn.preprocessing import LabelEncoder


logger = logging.getLogger(__name__)
mlflow.set_tracking_uri("http://0.0.0.0:5000")

def downcast_dtypes(df):
    float_cols = [c for c in df if df[c].dtype == "float64"]
    int_cols = [c for c in df if df[c].dtype in ["int64", "int32"]]
    df[float_cols] = df[float_cols].astype(np.float32)
    df[int_cols] = df[int_cols].astype(np.float32)
    return df

def train():
	model = xgb.XGBRegressor()

	train = pd.read_csv('data/train.csv', parse_dates=['CHECKOUT_DATE'])
	test = pd.read_csv('data/test.csv', parse_dates=['CHECKOUT_DATE'])
	
	train.columns = [col.lower() for col in train]
	test.columns = [col.lower() for col in test]

	lb = LabelEncoder()
	train['store_type'] = lb.fit_transform(train['store_type'])
	train['cate'] = lb.fit_transform(train['cate'])
	train['sub_cate'] = lb.fit_transform(train['sub_cate'])

	test['store_type'] = lb.fit_transform(test['store_type'])
	test['cate'] = lb.fit_transform(test['cate'])
	test['sub_cate'] = lb.fit_transform(test['sub_cate'])

	train = downcast_dtypes(train)
	test = downcast_dtypes(test)

	X_train = train.drop(['quantity','checkout_date'], axis=1)
	y_train = train['quantity']
	X_test = test.drop(['quantity','checkout_date'], axis=1)
	y_test = test['quantity']

	mlflow.xgboost.autolog(log_models=True)
	with mlflow.start_run():
		try:
			model = xgb.XGBRegressor(n_estimators=1000)
			model.fit(X_train, y_train,
					eval_set=[(X_train, y_train), (X_test, y_test)],
					early_stopping_rounds=50,
					verbose=False)

			model_uri = mlflow.sklearn.log_model(model, registered_model_name='PF_Quantity_Prediction', artifact_path="").model_uri

			print("MODEL URI:", model_uri)

		except Exception as e:
			print(e)
			mlflow.end_run()

if __name__ == "__main__":
    train()