import os, json
from pathlib import Path

class Settings(object):

	ROOT_DIR = Path(__file__).parent.parent.parent.parent
	API_HOST_PORT = int(os.getenv('API_HOST_PORT',8000))
	API_HOST_DOMAIN = os.getenv('API_HOST_DOMAIN','0.0.0.0')
	RELOAD_CODE = False
	NUMBER_OF_WORKER = int(os.getenv('NUMBER_OF_WORKER',2))
	METRICS_NAMESPACE = os.getenv('API_HOST_DOMAIN',"fastapi")
	METRICS_SUBSYSTEM = os.getenv('API_HOST_DOMAIN',"model")
	CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL',"redis://localhost:6379/0")
	
    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL',"redis://localhost:6379/0")
    # CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND',"redis://localhost:6379/0")

## Double check for review
settings = Settings()