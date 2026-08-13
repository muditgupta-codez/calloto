import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "unhealthy")
    assert "database" in data
    assert "voxvaani" in data


@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "name": "Test Plumber",
            "phone": "+447700900000",
            "trade_vertical": "plumbing",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test Plumber"
    assert data["subscription_status"] == "inactive"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    await client.post(
        "/api/signup",
        json={
            "email": "dup@example.com",
            "name": "Test 1",
            "phone": "+447700900001",
            "trade_vertical": "plumbing",
        },
    )
    response = await client.post(
        "/api/signup",
        json={
            "email": "dup@example.com",
            "name": "Test 2",
            "phone": "+447700900002",
            "trade_vertical": "electrical",
        },
    )
    assert response.status_code == 400
