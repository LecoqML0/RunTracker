from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session

from app.schemas.user import User
from app.schemas.run import Run
from app.security import hash_password
import app.database as db


router = APIRouter()

@router.post("/users")
async def create_user(
    current_admin_user: Annotated[User, Depends(db.get_admin_user)],
    user: User,
    session: Session = Depends(db.get_session)
):
    user.hashed_password = hash_password(user.hashed_password)
    db.admin_create_user(user, session)
    return user

@router.get("/users")
def read_users(
    current_admin_user: Annotated[User, Depends(db.get_admin_user)],
    session: Session = Depends(db.get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = db.admin_get_users(session, offset, limit)
    return users

@router.get("/runs")
def read_runs(
    current_admin_user: Annotated[User, Depends(db.get_admin_user)],
    session: Session = Depends(db.get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Run]:
    runs = db.admin_get_runs(session, offset, limit)
    return runs
