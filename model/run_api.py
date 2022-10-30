import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import uvicorn, time
import aioredis
from uvicorn.config import LOGGING_CONFIG

from fastapi import FastAPI, Request
from app.main_routers import add_all_routers
from app.base.config import settings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# from app.base.databases import SessionLocal, engine

app = FastAPI(
    title="Pod Foods ML APIs",
    description="APIs for ML products of Pod Foods",
    version="0.0.1",
    docs_url="/documentation",
    redoc_url="/redoc",
)

add_all_routers(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup():
    redis =  aioredis.from_url(settings.CELERY_BROKER_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



from multiprocessing import Process
import subprocess

# def run_celery():
#     # subprocess.run('celery -A app.worker.celery_app worker -l INFO -c {}'.format(settings.NUMBER_OF_WORKER), shell=True)
#     # subprocess.run('celery -A app.worker.celery_app worker -B -l INFO -c {} --without-gossip --without-mingle --without-heartbeat -Ofair'.format(settings.NUMBER_OF_WORKER), shell=True)

#     # run this on windows
#     subprocess.run('redis-server', shell=True) 
#     subprocess.run('celery -A app.worker.celery_app worker -E -l INFO -c {} --without-gossip --without-mingle --without-heartbeat -Ofair --pool=gevent'.format(settings.NUMBER_OF_WORKER), shell=True)
#     # celery -A app.worker.celery_app worker -B -l info 


if __name__ == "__main__":
    # subprocess.run('set PATH=%PATH%;C:\Users\hai.dao_onemount\instantclient_21_3', shell=True)
    # celery_process = Process(target=run_celery, args=())
    # celery_process.start()
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = '%Y-%m-%d %H:%M:%S'

    uvicorn.run("run_api:app"
                ,host= settings.API_HOST_DOMAIN
                ,port= settings.API_HOST_PORT
                ,reload = settings.RELOAD_CODE
                ,workers = settings.NUMBER_OF_WORKER
                )
