import numpy as np

import mlflow
from mlflow.tracking import MlflowClient
from utils import engine
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# mlflowclient = MlflowClient()
# mlflow.set_tracking_uri("0.0.0.0:5000")
# mlflow.set_registry_uri("0.0.0.0:5000")

def predict(store_product_pair:list):
    # model_name = "PF_Quantity_Prediction"
    # # Fetch the last model in production
    # model = mlflow.sklearn.load_model(
    #     model_uri=f"models:/{model_name}/latest"
    # )

	model = pickle.load(open('artifacts/0/5a2797a7f4d64d8db270031cab2cfb14/artifacts/model.pkl', 'rb'))
	pairs = [f"{pair['store_id']}_{pair['product_id']}" for pair in store_product_pair]

	query = f"""
	select * from features
	where concat(store_id, '_', product_id) in ('f"{"','".join(pairs)}"')
	"""

	# features = pd.read_sql(query, engine)
	features = pd.read_csv('data/features.csv')
	features.columns = [col.lower() for col in features]
	
	# features.drop(['id','created_at', 'quantity', 'checkout_date'], axis=1, inplace=True)
	features.drop(['quantity', 'checkout_date'], axis=1, inplace=True)
	lb = LabelEncoder()
	features['store_type'] = lb.fit_transform(features['store_type'])
	features['cate'] = lb.fit_transform(features['cate'])
	features['sub_cate'] = lb.fit_transform(features['sub_cate'])

	res = np.ceil(model.predict(features))

	return {'prediction': res.tolist()}

if __name__ == "__main__":
	request = [
		{'store_id': 55, 'product_id': 1866},
		{'store_id': 55, 'product_id': 1867},
		{'store_id': 55, 'product_id': 1939}
		]

	print(predict(request))