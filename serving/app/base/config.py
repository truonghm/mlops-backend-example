import os, json
from pathlib import Path

class Settings(object):

	ROOT_DIR = Path(__file__).parent.parent.parent.parent
	API_HOST_PORT = int(os.getenv('API_HOST_PORT',8000))
	API_HOST_DOMAIN = os.getenv('API_HOST_DOMAIN','0.0.0.0')
	RELOAD_CODE = False
	NUMBER_OF_WORKER = int(os.getenv('NUMBER_OF_WORKER',2))
	NUMBER_OF_API_INSTANCES = int(os.getenv('NUMBER_OF_API_INSTANCES',2))
	NUMBER_OF_DB_CONNECT = (NUMBER_OF_API_INSTANCES + NUMBER_OF_WORKER) * 4
	METRICS_NAMESPACE = os.getenv('API_HOST_DOMAIN',"fastapi")
	METRICS_SUBSYSTEM = os.getenv('API_HOST_DOMAIN',"model")
	CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL',"redis://localhost:6379/0")
	# MLFLOW_TRACKING_URI = f"http://{os.getenv('MLFLOW_HOST')}:{os.getenv('MLFLOW_PORT')}"
	MLFLOW_TRACKING_URI = "http://mlflow:5000"
	# MLFLOW_REGISTRY_URI = os.getenv('MLFLOW_ARTIFACT_ROOT')
	MLFLOW_REGISTRY_URI = f"mysql+pymysql://{os.getenv('MYSQL_MLFLOW_USER')}:{os.getenv('MYSQL_MLFLOW_PWD')}@mysql_mlflow:3306/{os.getenv('MYSQL_MLFLOW_DB')}"
	# MYSQL_HOST = os.getenv("MYSQL_HOST")
	MYSQL_HOST = "mysql"
	MYSQL_USER = os.getenv("MYSQL_USER")
	MYSQL_PWD = os.getenv("MYSQL_PWD") 
	MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
	MYSQL_DB = os.getenv("MYSQL_DB")
## Double check for review
settings = Settings()