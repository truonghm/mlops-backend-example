from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData
import os
import sys

sys.path.insert(0, os.path.dirname(sys.path[0]))

# DB_NAME = "podfood.db"
DB_PATH = "sqlite:///database/podfood.db"

engine = create_engine(DB_PATH, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base.metadata.create_all(engine)


def bulk_drop(table_list):
    with engine.connect() as conn:
        for tb_name in table_list:
            conn.execute(str(f"DROP TABLE IF EXISTS [{tb_name}]"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()