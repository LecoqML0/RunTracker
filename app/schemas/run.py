from typing import Optional
from sqlmodel import Field, SQLModel

from app.schemas.user import UserRead

class RunBase(SQLModel):
    run_name: str = Field(..., min_length=3, max_length=100)
    distance: float = Field(..., gt=0) # constraint for distance to be greater than 0

class RunDB(RunBase, table=True):
    __tablename__ = "runs"  # type: ignore
    run_id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="users.user_id")

class RunCreate(RunBase):
    user_id : int

class RunCreateForm(RunBase):
    pass

class RunRead(RunBase):
    run_id: int
    user_id: int

    model_config = {"from_attributes": True}