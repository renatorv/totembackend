from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


# Modelos / Classes para entrada e saída de dados do backend, usa o pydantic - SCHEMAS
# Model para entrada e saída de dados do banco de dados - MODEL


db_stores = []

class Store(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    location: str | None = None


@app.post("/stores", response_model=Store)
def create_store(store: Store):
    db_stores.append(store)
    return store


@app.get("/stores", response_model=list[Store])
def list_stores():
    return db_stores