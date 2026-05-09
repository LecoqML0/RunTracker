from typing import Annotated
from fastapi import Depends, APIRouter, Query
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.schemas.user import User
from app.schemas.run import Run
from app.security import hash_password
from app.database import get_session


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/users")
async def create_user(
    user: User,
    session: Session = Depends(get_session)
):
    user.hashed_password = hash_password(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users")
def read_users(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return list(users)

@router.get("/runs")
def read_runs(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Run]:
    runs = session.exec(select(Run).offset(offset).limit(limit)).all()
    return list(runs)