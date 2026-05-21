from fastapi import Query
from sqlmodel import select, Session
from typing import Annotated

from app.schemas.run import RunDB, RunCreate

def create_run(run_request: RunCreate, user_id: int, session: Session) -> RunDB:
    new_run = RunDB(
        user_id= user_id,
        run_name= run_request.run_name,
        distance= run_request.distance
    )
    session.add(new_run)
    session.commit()
    session.refresh(new_run)
    return new_run

def admin_delete_run(run_id: int, session: Session) -> RunDB:
    run = session.exec(select(RunDB).where(RunDB.run_id == run_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found")
    session.delete(run)
    session.commit()
    return run

def delete_user_run(user_id: int, run_id: int, session: Session) -> RunDB:
    run = session.exec(select(RunDB).where(RunDB.run_id == run_id, RunDB.user_id == user_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found or not owned by user {user_id}")
    session.delete(run)
    session.commit()
    return run

def get_user_runs_list(user_id: int, session: Session) -> list[RunDB]:
    runs = session.exec(select(RunDB).where(RunDB.user_id == user_id))
    return list(runs)

def get_user_run(user_id: int, run_id: int, session: Session) -> RunDB:
    run = session.exec(select(RunDB).where(RunDB.user_id == user_id, RunDB.run_id == run_id)).first()
    if not run:
        raise ValueError(f"Run {run_id} not found or not owned by user {user_id}")
    return run

def admin_get_runs(
        session: Session,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
        ) -> list[RunDB]:
    runs = session.exec(select(RunDB).offset(offset).limit(limit)).all()
    return list(runs)