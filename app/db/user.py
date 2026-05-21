from typing import Annotated
from fastapi import Query
from sqlmodel import select, Session

from app.schemas.user import UserDB, UserCreate
import app.security as security

def get_user_from_id(id: int, session: Session):
    user = session.exec(select(UserDB).where(UserDB.user_id == id)).first()
    return user

def get_user_from_email(email: str, session: Session):
    user = session.exec(select(UserDB).where(UserDB.email == email)).first()
    return user

def create_user(user_request : UserCreate, session: Session) -> UserDB:
    new_user = UserDB(
        username = user_request.username,
        email = user_request.email,
        hashed_password = security.hash_password(user_request.password),
        is_admin=user_request.is_admin
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def delete_user(user_id:int, session: Session):
    user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()
    if not user:
        raise ValueError(f"User {user_id} not found")
    session.delete(user)
    session.commit()
    return user

def admin_get_users(
        session: Session,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
        ) -> list[UserDB]:
    users = session.exec(select(UserDB).offset(offset).limit(limit)).all()
    return list(users)