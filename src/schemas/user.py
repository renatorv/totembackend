from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    email: str
    name: str


class UserCreate(BaseModel):
    email: str
    name: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=16)


class ChangePasswordData(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=16)