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

from utils import Base

class OrderTable(Base):
	__tablename__ = "fact_order_items"
	order_id = Column(Integer, default=None, unique=False, primary_key=False)
	store_id = Column(Integer, default=None, unique=False)
	region_id = Column(Integer, default=None, unique=False)
	brand_id = Column(Integer, default=None, unique=False)
	product_id = Column(Integer, default=None, unique=False)
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

class FeaturesTable(Base):
	__tablename__ = "features"
	store_id = Column(Integer, default=None, unique=False, primary_key=False)
	product_id = Column(Integer, default=None, unique=False, primary_key=False)
	checkout_date = Column(DateTime(timezone=True), server_default=func.now())
	quantity = Column(Integer, default=None, unique=False)
	store_type = Column(String(128), nullable=True, unique=False)
	store_region_id = Column(Integer, default=None, nullable=True, unique=False)
	store_size = Column(Integer, default=None, unique=False)
	sub_cate = Column(String(128), nullable=True, unique=False)
	cate = Column(String(128), nullable=True, unique=False)
	checkout_dow = Column(Integer, default=None, unique=False)
	checkout_day = Column(Integer, default=None, unique=False)
	avg_qty_store_l30d = Column(Float, default=None, unique=False)
	avg_qty_product_l30d = Column(Float, default=None, unique=False)
	avg_qty_storetype_l30d = Column(Float, default=None, unique=False)
	avg_qty_storeregion_l30d = Column(Float, default=None, unique=False)
	avg_qty_cate_l30d = Column(Float, default=None, unique=False)
	avg_qty_subcate_l30d = Column(Float, default=None, unique=False)
	avg_qty_store_product_l30d = Column(Float, default=None, unique=False)
	avg_qty_store_cate_l30d = Column(Float, default=None, unique=False)
	avg_qty_storeregion_cate_l30d = Column(Float, default=None, unique=False)
	qty_store_product_lag_1 = Column(Float, default=None, unique=False)
	qty_store_product_lag_2 = Column(Float, default=None, unique=False)
	qty_store_product_lag_3 = Column(Float, default=None, unique=False)
	qty_store_product_lag_4 = Column(Float, default=None, unique=False)
	qty_store_product_lag_5 = Column(Float, default=None, unique=False)
	qty_store_product_lag_6 = Column(Float, default=None, unique=False)
	qty_store_product_lag_7 = Column(Float, default=None, unique=False)
	qty_store_product_lag_14 = Column(Float, default=None, unique=False)
	qty_store_product_lag_28 = Column(Float, default=None, unique=False)
	dcnt_product_store_daily = Column(Float, default=None, unique=False)
	dcnt_cate_store_daily = Column(Float, default=None, unique=False)
	dcnt_subcate_store_daily = Column(Float, default=None, unique=False)
	sum_qty_store_daily = Column(Float, default=None, unique=False)
	dcnt_product_store_daily_lag_1 = Column(Float, default=None, unique=False)
	dcnt_cate_store_daily_lag_1 = Column(Float, default=None, unique=False)
	dcnt_subcate_store_daily_lag_1 = Column(Float, default=None, unique=False)
	sum_qty_store_daily_lag_1 = Column(Float, default=None, unique=False)
	dcnt_product_store_daily_lag_3 = Column(Float, default=None, unique=False)
	dcnt_cate_store_daily_lag_3 = Column(Float, default=None, unique=False)
	dcnt_subcate_store_daily_lag_3 = Column(Float, default=None, unique=False)
	sum_qty_store_daily_lag_3 = Column(Float, default=None, unique=False)
	dcnt_product_store_daily_lag_7 = Column(Float, default=None, unique=False)
	dcnt_cate_store_daily_lag_7 = Column(Float, default=None, unique=False)
	dcnt_subcate_store_daily_lag_7 = Column(Float, default=None, unique=False)
	sum_qty_store_daily_lag_7 = Column(Float, default=None, unique=False)
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())