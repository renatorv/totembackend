
from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from src.core import models
from src.core.database import GetDBDep
from src.core.dependencies import get_current_user
from src.schemas.store import Store, CreateStore, PatchStore

router = APIRouter(prefix="/admin/stores", tags=["Stores"])


@router.post("", response_model=Store)
def create_store(store: CreateStore, db: GetDBDep):
    user = db.query(models.User).filter(models.User.id == store.owner_id).first()

    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User not found!")

    db_store = models.Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store


@router.get("", response_model=list[Store])
def list_stores(db: GetDBDep, current_user: models.User = Depends(get_current_user)):
    # aqui models.Store é usado para pegar o model e não o Schema
    store_list = db.query(models.Store).all()
    return store_list


@router.get("/{store_id}", response_model=Store)
def get_store(store_id: int, db: GetDBDep):
    db_store = db.get(models.Store, store_id)

    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    return db_store


# put = altera o objeto completo
@router.put("/{store_id}", response_model=Store)
def update_store(store_id: int, store: CreateStore, db: GetDBDep):
    db_store = db.get(models.Store, store_id)

    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    db_store.name = store.name
    db.store.owner_id = store.owner_id
    db.commit()

    return db_store


# patch = atualiza somente os dados que foram passados
@router.patch("/{store_id}", response_model=Store)
def patch_store(store_id: int, store: PatchStore, db: GetDBDep):
    db_store = db.get(models.Store, store_id)

    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    if store.name:
        db_store.name = store.name

    if store.owner_id:
        db_store.owner_id = store.owner_id

    db.commit()

    return db_store


@router.delete("/{store_id}")
def delete_store(store_id: int, db: GetDBDep):
    db_store = db.get(models.Store, store_id)

    if db_store is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Store not found.")

    db.delete(db_store)
    db.commit()