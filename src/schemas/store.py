from datetime import datetime

from pydantic import BaseModel, Field



# Modelos / Classes para entrada e saída de dados do backend, usa o pydantic - SCHEMAS
# Model para entrada e saída de dados do banco de dados - MODEL
# SCHEMAS: entrada e saída de dados

class Product(BaseModel):
    name: str
    description: str
    price: int

class StoreBase(BaseModel):
    name: str = Field(min_length=4, max_length=20)
    owner: str

class Store(StoreBase):
    id: int

class DbStore(Store):
    create_at: datetime = datetime.now()

class CreateStore(StoreBase):
    pass

class PatchStore(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=20)
    owner: str | None = None