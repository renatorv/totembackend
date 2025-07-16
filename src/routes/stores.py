
from fastapi import HTTPException, APIRouter
from starlette.status import HTTP_404_NOT_FOUND

from src.core.database import GetDBDep
from src.schemas.store import Store, CreateStore, DbStore, PatchStore


db_stores = []

router = APIRouter(prefix="/admin/stores", tags=["Stores"])


@router.post("", response_model=Store)
def create_store(store: CreateStore, db: GetDBDep):
    db_store = DbStore(id=len(db_stores), **store.model_dump())
    db_stores.append(db_store)
    return db_store


@router.get("", response_model=list[Store])
def list_stores(db: GetDBDep):
    return db_stores


@router.get("/{store_id}", response_model=Store)
def get_store(store_id: int, db: GetDBDep):
    try:
        return db_stores[store_id]
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")


# put = altera o objeto completo
@router.put("/{store_id}", response_model=Store)
def update_store(store_id: int, store: CreateStore, db: GetDBDep):
    try:
        db_store = DbStore(id=store_id, **store.model_dump())
        db_stores[store_id] = db_store
        return db_store
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")


# patch = atualiza somente os dados que foram passados
@router.patch("/{store_id}", response_model=Store)
def patch_store(store_id: int, store: PatchStore, db: GetDBDep):
    try:
        db_store = db_stores[store_id]
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    if store.name:
        db_store.name = store.name
    if store.location:
        db_store.location = store.location

    return db_store


@router.delete("/{store_id}")
def delete_store(store_id: int, db: GetDBDep):
    try:
        db_stores.pop(store_id)
    except IndexError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    return {"message": "Store deleted successfully!"}