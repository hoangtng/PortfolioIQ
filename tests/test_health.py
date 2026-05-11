import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

def test_health_endpoint_exists(client):
    response = client.get("/health/")
    assert response.status_code in [200, 503]  # Depending on service status
    data = response.json()
    assert "status" in data
    assert "services" in data

def test_health_response_has_all_services(client):
    response = client.get("/health/")
    data = response.json()["services"]
    assert "postgres" in data
    assert "redis" in data
    assert "elasticsearch" in data
    assert "celery" in data