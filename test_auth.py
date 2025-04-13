import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register
        response = await client.post("/register", json={
            "email": "test@example.com",
            "password": "test123",
            "full_name": "Test User",
            "role": "patient"
        })
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

        # Login
        response = await client.post("/token", data={
            "username": "test@example.com",
            "password": "test123"
        })
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
