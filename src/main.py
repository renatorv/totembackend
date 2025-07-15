from fastapi import FastAPI

from src.routes.stores import router as stores_router
from src.routes.products import router as products_router

app = FastAPI(title="TotemPro - API")

app.include_router(stores_router)
app.include_router(products_router)
