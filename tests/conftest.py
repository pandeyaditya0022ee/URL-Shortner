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


# FastAPI DB override
def override_get_db():
    session = TestLocalSession()

    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


# Shared TestClient fixture
@pytest.fixture
def client():
    return TestClient(app)