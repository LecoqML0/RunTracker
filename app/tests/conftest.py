import pytest
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
from app.schemas import run, user
from app.main import app
from app.db.session import get_session
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c