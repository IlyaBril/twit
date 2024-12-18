import asyncio
import httpx
import pytest

from fastapi.testclient import TestClient

from app.main import fast_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


#async def init_db():
#    test_settings = Settings()
#    test_settings.DATABASE_URL =
#    "mongodb://localhost:27017/testdb"
#    await test_settings.initialize_database()


@pytest.fixture(scope="session")
async def default_client():
    #await init_db()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fast_app),
                                 base_url="http://") as client:
        yield client
    #Clean up resources
