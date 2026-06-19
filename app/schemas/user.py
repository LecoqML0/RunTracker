from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserDB(UserBase, table=True):
    __tablename__ = "users" # type: ignore
    __table_args__ = (
        UniqueConstraint("email"),
    )
    user_id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=18)
    is_admin: bool = Field(default=False)

class UserCreateForm(UserBase):
    password: str = Field(..., min_length=6, max_length=18)

class UserRead(UserBase):
    user_id: int
    is_admin: bool = Field(default=False)

    model_config = {"from_attributes": True}

class UserLoginForm(SQLModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=18)