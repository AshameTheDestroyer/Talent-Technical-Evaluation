import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


def test_user_registration(client: TestClient, sample_user_data: dict):
    """Test user registration endpoint"""
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"].startswith("fake_token_for_")


def test_user_registration_duplicate_email(client: TestClient, sample_user_data: dict):
    """Test user registration with duplicate email"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    
    # Try to register with the same email
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_user_login_success(client: TestClient, sample_user_data: dict):
    """Test successful user login"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    
    # Login with correct credentials
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    response = client.post("/users/registration/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"].startswith("fake_token_for_")


def test_user_login_invalid_credentials(client: TestClient, sample_user_data: dict):
    """Test user login with invalid credentials"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    
    # Login with incorrect password
    login_data = {
        "email": sample_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/users/registration/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_user_logout(client: TestClient, sample_user_data: dict):
    """Test user logout"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    
    # Logout (should always succeed)
    response = client.post("/users/registration/logout", json={})
    assert response.status_code == 200


def test_get_user_details(client: TestClient, sample_user_data: dict, db_session: Session):
    """Test getting user details by ID"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    token_response = response.json()
    # Extract user ID from token (format is "fake_token_for_{user_id}")
    user_id = token_response["token"].replace("fake_token_for_", "")
    
    # Get user details
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == sample_user_data["email"]
    assert user_data["first_name"] == sample_user_data["first_name"]
    assert user_data["last_name"] == sample_user_data["last_name"]
    assert user_data["role"] == sample_user_data["role"]


def test_get_current_user_data(client: TestClient, sample_user_data: dict):
    """Test getting current user's data based on token"""
    # Register the user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    token_response = response.json()
    token = token_response["token"]

    # Get current user data using the token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == sample_user_data["email"]
    assert user_data["first_name"] == sample_user_data["first_name"]
    assert user_data["last_name"] == sample_user_data["last_name"]
    assert user_data["role"] == sample_user_data["role"]


def test_get_nonexistent_user(client: TestClient):
    """Test getting details for a nonexistent user"""
    response = client.get("/users/nonexistent-id")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]