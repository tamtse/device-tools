from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_register_device(client):
    response = client.post("/Device/register", json={"userKey": "1234567890", "deviceType": "iOS"})
    assert response.status_code == 200
    assert response.json() == {"statusCode": 200}