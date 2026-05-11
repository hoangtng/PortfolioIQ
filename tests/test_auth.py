import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="thang",
        email="thanghn@example.com",
        password="testpassword123",
    )

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post("/api/v1/auth/register/", 
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123"
        },
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert "password" not in response.json()

@pytest.mark.django_db
def test_obtain_token(client, test_user):
    response = client.post("/api/v1/auth/token/", {
        "username": "thang",
        "password": "testpassword123"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()

@pytest.mark.django_db
def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_me_returns_user_info(client, test_user):
    token_response = client.post("/api/v1/auth/token/", {
        "username": "thang",
        "password": "testpassword123"
    })
    assert token_response.status_code == 200
    access_token = token_response.json()["access"]

    response = client.get("/api/v1/auth/me/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == 200
    assert response.json()["username"] == "thang"
    assert response.json()["email"] == "thanghn@example.com"
    assert "password" not in response.json()
