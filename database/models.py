import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    UnicodeText,
    Float,
    Date,
	PrimaryKeyConstraint
)
from sqlalchemy import UniqueConstraint, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from . import Base, engine, SessionLocal

class OrderTable(Base):
	__tablename__ = "fact_order_items"
	order_id = Column(Integer, default=None, unique=False, primary_key=False)
	store_id = Column(Integer, ForeignKey("dim_store.store_id"), default=None, unique=False)
	region_id = Column(Integer, default=None, unique=False)
	brand_id = Column(Integer, default=None, unique=False)
	product_id = Column(Integer, ForeignKey("dim_product.product_id"), default=None, unique=False)
	product_variant_id = Column(Integer, default=None, unique=False)
	quantity = Column(Integer, default=None, unique=False)
	variant_case_price_cents = Column(Float, default=None, unique=False)
	checkout_date = Column(Date, default=None)
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())

class StoreTable(Base):
	__tablename__ = "dim_store"
	store_id = Column(Integer, default=None, unique=False, primary_key=False)
	store_type = Column(String(128), nullable=True, unique=False)
	region_id = Column(Integer, default=None, nullable=True, unique=False)
	store_size = Column(Integer, default=None, nullable=True, unique=False)
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProductTable(Base):
	__tablename__ = "dim_product"
	product_id = Column(Integer, default=None, unique=False, primary_key=False)
	product_metadata = Column(String(128), nullable=True, unique=False)
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
