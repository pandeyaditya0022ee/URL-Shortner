import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.utils.settings import settings
from src.utils.db import Base, get_db


# Test database
test_engine = create_engine(settings.TEST_DB_CONNECTION)

TestLocalSession = sessionmaker(bind=test_engine)

# Create tables in test DB
Base.metadata.create_all(test_engine)


# Clean database before every test
@pytest.fixture(autouse=True)
def clean_database():
    with test_engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())


# FastAPI DB override
def override_get_db():
    session = TestLocalSession()

    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def headers(client):
    # Create test user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "user6",
            "email": "user6@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "username": "user6",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }