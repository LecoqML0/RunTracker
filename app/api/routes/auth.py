from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.schemas.user import User_create_request
from app.security import create_access_token, hash_password, verify_password
from app.database import get_user_from_email, get_session, create_user

router = APIRouter()

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    session: Session = Depends(get_session)
):
    active_user = get_user_from_email(form_data.username, session)

    if not active_user or not active_user.user_id:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, active_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(active_user.user_id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_request : User_create_request,
    session: Session = Depends(get_session)
):
    try:
        new_user = create_user(user_request, session)
        return new_user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))