# import os
# from pathlib import Path

# from dotenv import load_dotenv
# load_dotenv()

import uvicorn
# import time
# import aioredis
from uvicorn.config import LOGGING_CONFIG

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.main_routers import add_all_routers
from app.base.config import settings
from app.base.errors import CustomException
from prometheus_fastapi_instrumentator import Instrumentator


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.code, "message": exc.msg}
        )

app = FastAPI(
    title="Pod Foods ML APIs",
    description="APIs for ML products of Pod Foods",
    version="0.0.1",
    docs_url="/documentation",
    redoc_url="/redoc",
)
init_listeners(app)
add_all_routers(app)

@app.on_event("startup")
async def startup_event():
    Instrumentator().instrument(app=app).expose(app, include_in_schema=False, should_gzip=True)

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = '%Y-%m-%d %H:%M:%S'

    uvicorn.run("main:app"
                ,host= settings.API_HOST_DOMAIN
                ,port= settings.API_HOST_PORT
                ,reload = settings.RELOAD_CODE
                ,workers = settings.NUMBER_OF_WORKER
                )
