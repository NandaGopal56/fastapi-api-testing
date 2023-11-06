from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.base import get_db, Base
from fastapi.testclient import TestClient
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sqllite.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Dependency to get the SQLAlchemy session
def override_test_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close() 

@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_test_get_db

testClient = TestClient(app)


def test_main_home():
    response = testClient.get("/")
    assert response.status_code == 200
    assert response.json() == 'Welcome to the Notes App'
