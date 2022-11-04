from app.modules.healthcheck.routers import router as hc_router
from app.modules.quantity.routers import router as quantity_router

def add_all_routers(app):

    app.include_router(hc_router, prefix="/healthcheck", tags=["test"])
    app.include_router(quantity_router, prefix="/quantity", tags=["quantity"])