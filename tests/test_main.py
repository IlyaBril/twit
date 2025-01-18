import pytest

from fastapi.testclient import TestClient
from app.models.models import User
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session
from app.main import app
from app.models.models import get_session
from sqlmodel import (Session,
                      create_engine,
                      SQLModel)


def test_root_2(client):
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}



def create_hero(session, client):
    TEST_DB_URL = "postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/test_db"

    engine = create_engine(TEST_DB_URL, echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session


    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    client.post("/api/users", json={'id': 1, "name": "name_1", "api_key": "test"})
    response = client.get("/api/users/1")

    data = response.json()
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert data == {
        "result": True,
        "user": {
            "id": 1,
            "name": "name_1",
            "followers": [],
            "following": []
        }
    }


def test_create_user(client: TestClient):
    client.post("/api/users", json={'id': 1, "name": "name_1", "api_key": "test"})
    response = client.get("/api/users/1")

    data = response.json()

    assert response.status_code == 200
    assert data == {
        "result": True,
        "user": {
            "id": 1,
            "name": "name_1",
            "followers": [],
            "following": []
        }
    }



