import pytest

from httpx import ASGITransport, AsyncClient

from app.main import app


# @pytest.mark.anyio
# async def test_root(test_app):
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         response = await ac.get("/test")
#     assert response.status_code == 200


@pytest.mark.anyio
async def test_root_2(test_app):
    response = await test_app.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


@pytest.mark.anyio
async def test_root_3(test_app):
    response = await test_app.get("/api/tweets")
    assert response.status_code == 200
