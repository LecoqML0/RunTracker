from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from typing import Annotated

from app.schemas.run import RunRead, RunCreateForm, RunDB, RunCreate
from app.schemas.user import UserDB
from app.db.session import get_session
import app.db.run as run_db
from app.auth import get_active_user


router = APIRouter()

@router.post("/")
async def create_run(
    active_user:  Annotated[UserDB, Depends(get_active_user)],
    run_request_form: RunCreateForm,
    session: Session = Depends(get_session)
) -> RunRead:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    run_request = RunCreate(
        run_name= run_request_form.run_name,
        distance= run_request_form.distance,
        user_id= active_user.user_id
    )
    new_run = run_db.create_run(run_request, active_user.user_id, session)
    return RunRead.model_validate(new_run)

@router.get("/", response_model=list[RunRead])
async def get_runs(
    active_user:  Annotated[UserDB, Depends(get_active_user)],
    session: Session = Depends(get_session)
) -> list[RunDB]:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    user_runs = run_db.get_user_runs_list(active_user.user_id, session)
    return user_runs

@router.get("/{run_id}")
async def get_run(
    run_id: int,
    active_user:  Annotated[UserDB, Depends(get_active_user)],
    session: Session = Depends(get_session)
) -> RunRead:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    try:
        run = run_db.get_user_run(active_user.user_id, run_id, session)
        return RunRead.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{run_id}")
async def delete_run(
    run_id: int,
    active_user:  Annotated[UserDB, Depends(get_active_user)],
    session: Session = Depends(get_session)
) -> RunRead:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    try:
        deleted_run = run_db.delete_user_run(active_user.user_id, run_id, session)
        return RunRead.model_validate(deleted_run)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))