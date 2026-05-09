from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Run(SQLModel, table=True):
    run_id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.user_id")
    run_name: str
    distance: float

class Run_create_request(BaseModel):
    run_name: str
    distance: float