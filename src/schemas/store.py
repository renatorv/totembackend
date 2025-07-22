from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.user import User


# Modelos / Classes para entrada e saída de dados do backend, usa o pydantic - SCHEMAS
# Model para entrada e saída de dados do banco de dados - MODEL
# SCHEMAS: entrada e saída de dados

class StoreBase(BaseModel):
    name: str = Field(min_length=4, max_length=20)

class Store(StoreBase):
    id: int
    owner: User

class CreateStore(StoreBase):
    owner_id: int

class PatchStore(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=20)
    owner_id: int | None = None