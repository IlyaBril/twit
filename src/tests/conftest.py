import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app
from app.models.models import get_session

TEST_DB_URL = "postgresql+psycopg2://postgres:postgres@my_db:5432/test_db"


@pytest.fixture(scope="session")
def test_engine():
    return create_engine(TEST_DB_URL, echo=True)


@pytest.fixture(name="session", scope="session")
def session_fixture(test_engine):
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client", scope="session")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
