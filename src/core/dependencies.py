from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends

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