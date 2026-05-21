from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    username: str
    email: str

class UserDB(UserBase, table=True):
    __tablename__ = "users" # type: ignore
    user_id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

class UserCreate(UserBase):
    password: str
    is_admin: bool = Field(default=False)

class UserCreateForm(UserBase):
    password: str

class UserRead(UserBase):
    user_id: int
    is_admin: bool = Field(default=False)

    model_config = {"from_attributes": True}