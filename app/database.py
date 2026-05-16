from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated
from fastapi import Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import User, User_create_request
from app.schemas.run import Run, Run_create_request
import app.security as security
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

engine = create_engine(settings.database_url)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def get_user_from_id(id: int, session: Session):
    user = session.exec(select(User).where(User.user_id == id)).first()
    return user

def get_user_from_email(email: str, session: Session):
    user = session.exec(select(User).where(User.email == email)).first()
    return user

def create_user(user_request : User_create_request, session: Session) -> User:
    new_user = User(
        username = user_request.username,
        email = user_request.email,
        hashed_password = security.hash_password(user_request.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def admin_create_user(user: User, session: Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(user_id:int, session: Session):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise ValueError(f"User {user_id} not found")
    session.delete(user)
    session.commit()
    return user

def admin_get_users(
        session: Session,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
        ) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return list(users)

def create_run(run_request: Run_create_request, user_id: int, session: Session):
    new_run = Run(
        user_id= user_id,
        run_name= run_request.run_name,
        distance= run_request.distance
    )
    session.add(new_run)
    session.commit()
    session.refresh(new_run)
    return new_run

def admin_delete_run(run_id: int, session: Session) -> Run:
    run = session.exec(select(Run).where(Run.run_id == run_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found")
    session.delete(run)
    session.commit()
    return run

def delete_user_run(user_id: int, run_id: int, session: Session) -> Run:
    run = session.exec(select(Run).where(Run.run_id == run_id, Run.user_id == user_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found or not owned by user {user_id}")
    session.delete(run)
    session.commit()
    return run

def get_user_runs_list(user_id: int, session: Session) -> list[Run]:
    runs = session.exec(select(Run).where(User.user_id == user_id))
    return list(runs)

def get_user_run(user_id: int, run_id: int, session: Session) -> Run:
    run = session.exec(select(Run).where(User.user_id == user_id, Run.run_id == run_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found or not owned by user {user_id}")
    return run

def admin_get_runs(
        session: Session,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
        ) -> list[Run]:
    runs = session.exec(select(Run).offset(offset).limit(limit)).all()
    return list(runs)

async def get_active_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session)
)-> User | None:
    active_user_id = security.decode_token(token)
    active_user = get_user_from_id(active_user_id, session)
    return active_user

async def get_admin_user(
    current_user: Annotated[User, Depends(get_active_user)]
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user