from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.core import models
from src.core.database import GetDBDep
from src.core.dependencies import get_current_user
from src.schemas.user import UserCreate
from src.services.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("")
def create_user(user: UserCreate, db: GetDBDep):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    user_internal_dict = user.model_dump() # model_dump() => transforma um schema do pydantic em um dicionário Python
    user_internal_dict["hashed_password"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = models.User(**user_internal_dict)
    db.add(user_internal)
    db.commit()
    return "Sucesso!"


@router.get("/me")
def get_current_user(
        current_user: models.User = Depends(get_current_user)
):
    pass