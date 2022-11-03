from typing import List, Optional
# from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Response
from fastapi_cache.decorator import cache
from joblib import load
import numpy as np
from pathlib import Path

import pymysql
import cryptography
import pandas as pd
from sqlalchemy import text

from app.base.config import settings
from app.base.db import SessionLocal, engine

router = APIRouter()

@router.get("/ping")
async def healthcheck():
    return {"ping": "pong"}

@router.get("/get_db_version")
async def get_db_status():

    db = SessionLocal()
    version = db.execute(text('SELECT VERSION()')).fetchone()

    return {"table_list": {version[0]}}