import pytest
import uuid

from app.tests.helpers import register_user, login_user


def test_register_user(client):
    response = register_user(
        client,
        "testuser",
        "valid.email@domain.com",
        "securepassword"
    )
    assert response.status_code == 201


def test_register_user_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "securepassword"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity due to email validation


def test_register_user_invalid_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": f"valid.email_{uuid.uuid4().hex[:8]}@domain.com",
            "password": "short"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity due to password validation


def test_login_user(client):
    email = f"logintest_{uuid.uuid4().hex[:8]}@example.com"
    # 1 : register the user
    register_user(client, "testuser", email, "securepassword")
    # 2 : attempt to login
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "securepassword"
        }
    )
    assert response.status_code == 200