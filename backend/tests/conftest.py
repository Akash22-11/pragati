import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.config import settings
from main import fastapi_app


# Use a separate test database (SQLite in-memory for speed)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def student_payload():
    return {
        "full_name": "Test Student",
        "email": "teststudent@pragati.com",
        "password": "test1234",
        "role": "student",
        "institution": "Test College",
        "department": "Computer Science",
    }


@pytest.fixture
def faculty_payload():
    return {
        "full_name": "Test Faculty",
        "email": "testfaculty@pragati.com",
        "password": "test1234",
        "role": "faculty",
        "institution": "Test College",
        "department": "Computer Science",
    }