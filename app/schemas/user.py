from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class User(SQLModel, table=True):
    user_id : Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True)
    hashed_password: str

class User_create_request(BaseModel):
    username: str
    email: str
    password: str