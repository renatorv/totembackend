from typing import Annotated

from fastapi import HTTPException, Header
from fastapi.params import Depends
from starlette.requests import Request

from src.core import models
from src.core.database import GetDBDep
from src.services.auth import oauth2_scheme, verify_access_token


def get_current_user(
        db: GetDBDep,
        token: Annotated[str, Depends(oauth2_scheme)]
):

    email = verify_access_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

# Request: possui todos os dados da requisição
def get_optional_user(db: GetDBDep, authorizatio: Annotated[str | None, Header()] = None):
    token = authorizatio

    # Não tem usuário logado
    if not token:
        return None

    try:
        token_type, _, token_value = token.partition(" ")

        if token_type.lower() != "bearer" or not token_value:
            return None

        return get_current_user(db, token_value)
    except Exception:
        return None


GetCurrentUserDep = Annotated[models.User, Depends(get_current_user)]

GetOptionalUserDep = Annotated[models.User | None, Depends(get_optional_user)]