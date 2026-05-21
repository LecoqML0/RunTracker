from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

from app.schemas.user import UserRead, UserDB
from app.db.session import get_session
from app.auth import get_active_user
import app.db.user as user_db


router = APIRouter()

@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserDB, Depends(get_active_user)],
) -> UserRead:
    if not current_user:
        raise HTTPException(status_code=400, detail="User not authenticated")
    return UserRead.model_validate(current_user)

@router.delete("/me")
async def delete_user(
    current_user: Annotated[UserDB, Depends(get_active_user)],
    session: Session = Depends(get_session)
) -> UserRead:
    if not current_user.user_id:
        raise HTTPException(status_code=400, detail="User not authenticated")
    user_db.delete_user(current_user.user_id, session)
    return UserRead.model_validate(current_user)
