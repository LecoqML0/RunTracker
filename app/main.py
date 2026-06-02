from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import auth, user, run, admin

app = FastAPI(title="RunTracker")

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(run.router, prefix="/run")
app.include_router(admin.router, prefix="/admin")