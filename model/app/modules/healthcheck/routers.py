from typing import List, Optional
# from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Response
from fastapi_cache.decorator import cache
from joblib import load
import numpy as np
from pathlib import Path

# from . import actions, models, schemas

# from app.modules.users import schemas as user_schemas
# from app.modules.users import actions as user_actions
# from app.base.databases import get_db, get_read_db
# from app.base.config import settings

# from .schemas import Wine, Rating, feature_names

router = APIRouter()

@router.get("/ping")
async def healthcheck():
    return "pong"