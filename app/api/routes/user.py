from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

from app.schemas.user import User
import app.database as db


router = APIRouter()

@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(db.get_active_user)],
):
    if not current_user:
        raise HTTPException(status_code=400, detail="User not authenticated")
    return current_user

@router.delete("/me")
async def delete_user(
    current_user: Annotated[User, Depends(db.get_active_user)],
    session: Session = Depends(db.get_session)
):
    if not current_user.user_id:
        raise HTTPException(status_code=400, detail="User not authenticated")
    db.delete_user(current_user.user_id, session)
    return current_user
