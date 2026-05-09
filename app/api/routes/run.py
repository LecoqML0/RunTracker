from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from typing import Annotated

from app.schemas.run import Run, Run_create_request
from app.schemas.user import User
import app.database as db


router = APIRouter()

@router.post("/")
async def create_run(
    active_user:  Annotated[User, Depends(db.get_active_user)],
    run_request: Run_create_request,
    session: Session = Depends(db.get_session)
) -> Run:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    new_run = db.create_run(run_request, active_user.user_id, session)
    return new_run

@router.get("/")
async def get_runs(
    active_user:  Annotated[User, Depends(db.get_active_user)],
    session: Session = Depends(db.get_session)
) -> list[Run]:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    user_runs = db.get_user_runs_list(active_user.user_id, session)
    return user_runs

@router.get("/{run_id}")
async def get_run(
    run_id: int,
    active_user:  Annotated[User, Depends(db.get_active_user)],
    session: Session = Depends(db.get_session)
) -> Run:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    try:
        run = db.get_user_run(active_user.user_id, run_id, session)
        return run
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{run_id}")
async def delete_run(
    run_id: int,
    active_user:  Annotated[User, Depends(db.get_active_user)],
    session: Session = Depends(db.get_session)
) -> Run:
    if active_user.user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found")
    try:
        deleted_run = db.delete_user_run(active_user.user_id, run_id, session)
        return deleted_run
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))