from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel import Session

from app.db.session import get_session
import app.security as security
from app.db.user import get_user_from_id
from app.schemas.user import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_active_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session)
)-> UserDB | None:
    active_user_id = security.decode_token(token)
    active_user = get_user_from_id(active_user_id, session)
    return UserDB.model_validate(active_user)

async def get_admin_user(
    current_user: Annotated[UserDB, Depends(get_active_user)]
) -> UserDB:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user