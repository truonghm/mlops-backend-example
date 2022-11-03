from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import databases
from app.base.config import settings


import pymysql
import cryptography

connection_string = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PWD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
print(connection_string)

engine = create_engine(connection_string, max_identifier_length=30, pool_size=2, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        # db.rollback()
        yield db
    finally:
        db.close()

