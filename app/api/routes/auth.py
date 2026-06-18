from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreateForm, UserCreate, UserRead
from app.security import create_access_token, verify_password
from app.db.session import get_session
import app.db.user as user_db

router = APIRouter()

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    session: Session = Depends(get_session)
):
    active_user = user_db.get_user_from_email(form_data.username, session)

    if not active_user or not active_user.user_id:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, active_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(active_user.user_id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_request_form : UserCreateForm,
    session: Session = Depends(get_session)
):
    try:
        user_request = UserCreate(
            username=user_request_form.username,
            email=user_request_form.email,
            password=user_request_form.password,
            is_admin=False
        )
        new_user = user_db.create_user(user_request, session)
        return UserRead.model_validate(new_user)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Email already registered")