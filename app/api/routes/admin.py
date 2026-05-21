from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session

from app.schemas.user import UserRead, UserDB, UserCreate
from app.schemas.run import RunRead, RunDB
from app.security import hash_password
from app.db.session import get_session
import app.db.user as user_db
import app.db.run as run_db
from app.auth import get_admin_user


router = APIRouter()

@router.post("/users")
async def create_user(
    current_admin_user: Annotated[UserDB, Depends(get_admin_user)],
    user: UserCreate,
    session: Session = Depends(get_session)
) -> UserRead:
    user.hashed_password = hash_password(user.password)
    user_db.create_user(user, session)
    return UserRead.model_validate(user)

@router.get("/users", response_model=list[UserRead])
def read_users(
    current_admin_user: Annotated[UserDB, Depends(get_admin_user)],
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserDB]:
    users = user_db.admin_get_users(session, offset, limit)
    return users

@router.get("/runs", response_model=list[RunRead])
def read_runs(
    current_admin_user: Annotated[UserDB, Depends(get_admin_user)],
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[RunDB]:
    runs = run_db.admin_get_runs(session, offset, limit)
    return runs
