import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from utils.jwt_utils import create_access_token, verify_token, get_password_hash, verify_password, is_authenticated
from datetime import timedelta
import uuid
from models.user import User
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session

def test_jwt_functions():
    print("Testing JWT functions...")
    
    # Test creating and verifying a token
    data = {"sub": "test_user_id", "name": "Test User"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    print(f"Created token: {token[:50]}...")
    
    payload = verify_token(token)
    print(f"Verified payload: {payload}")
    
    assert payload is not None
    assert payload["sub"] == "test_user_id"
    print("[PASS] JWT token creation and verification works")
    
    # Test password hashing
    plain_password = "test_password"
    hashed = get_password_hash(plain_password)
    print(f"Hashed password: {hashed[:50]}...")
    
    is_valid = verify_password(plain_password, hashed)
    print(f"Password verification: {is_valid}")
    
    assert is_valid
    print("[PASS] Password hashing and verification works")
    
    print("\nAll JWT functions tests passed!")


def test_database_and_authentication():
    print("\nTesting database and authentication integration...")
    
    # Create a test user in the database
    db = SessionLocal()
    try:
        # Create a test user
        user_id = str(uuid.uuid4())
        test_user = User(
            id=user_id,
            first_name="Test",
            last_name="User",
            email=f"test{user_id}@example.com",
            role="applicant"
        )
        test_user.set_password("test_password")
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Created test user with ID: {test_user.id}")
        
        # Test token creation for the user
        token = create_access_token(data={"sub": test_user.id})
        print(f"Created token for user: {token[:50]}...")
        
        # Test is_authenticated function
        authenticated_user = is_authenticated(token)
        print(f"Authenticated user: {authenticated_user.email if authenticated_user else None}")
        
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        
        print("[PASS] Database and authentication integration works")
        
        # Clean up: delete the test user
        db.delete(test_user)
        db.commit()
        
    finally:
        db.close()
    
    print("\nDatabase integration test passed!")


if __name__ == "__main__":
    test_jwt_functions()
    test_database_and_authentication()
    print("\n[SUCCESS] All authentication system tests passed!")