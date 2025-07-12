from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()


# Modelos / Classes para entrada e saída de dados do backend, usa o pydantic - SCHEMAS
# Model para entrada e saída de dados do banco de dados - MODEL
# SCHEMAS: entrada e saída de dados


db_stores = []


class Product(BaseModel):
    name: str
    description: str
    price: int


class StoreBase(BaseModel):
    name: str = Field(min_length=4, max_length=20)
    location: str | None = None

class Store(StoreBase):
    id: int

class DbStore(Store):
    create_at: datetime = datetime.now()

class CreateStore(StoreBase):
    pass

class PatchStore(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=20)
    location: str | None = None


@app.post("/stores", response_model=Store)
def create_store(store: CreateStore):
    db_store = DbStore(id=len(db_stores), **store.model_dump())
    db_stores.append(db_store)
    return db_store


@app.get("/stores", response_model=list[Store])
def list_stores():
    return db_stores


@app.get("/stores/{store_id}", response_model=Store)
def get_store(store_id: int):
    try:
        return db_stores[store_id]
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")


# put = altera o objeto completo
@app.put("/stores/{store_id}", response_model=Store)
def update_store(store_id: int, store: CreateStore):
    try:
        db_store = DbStore(id=store_id, **store.model_dump())
        db_stores[store_id] = db_store
        return db_store
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")


# patch = atualiza somente os dados que foram passados
@app.patch("/stores/{store_id}", response_model=Store)
def patch_store(store_id: int, store: PatchStore):
    try:
        db_store = db_stores[store_id]
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    if store.name:
        db_store.name = store.name
    if store.location:
        db_store.location = store.location

    return db_store


@app.delete("/stores/{store_id}")
def delete_store(store_id: int):
    try:
        db_stores.pop(store_id)
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    return {"message": "Store deleted successfully!"}


def get_store_dep(store_id: int) -> DbStore:
    try:
        return db_stores[store_id]
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")


@app.post("/stores/{store_id}/products")
def create_product(
        store: Annotated[DbStore, Depends(get_store_dep)],
        product: Product
):
    # criar o produto no BD
    return product
