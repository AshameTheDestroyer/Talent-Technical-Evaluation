from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import jwt

from config import settings
from database.database import get_db
from models.user import User
from utils.password_utils import get_password_hash, verify_password

# JWT token creation and verification functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with expiration time
    """
    to_encode = data.copy()

    # Set expiration time - default to 30 days if not specified
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)  # 30 days as requested

    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.JWTError:
        # Invalid token
        return None


def is_authenticated(token: str) -> Optional[User]:
    """
    Decode the token and return the user object based on the user ID
    or return None if not authenticated
    """
    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    # Verify the token
    payload = verify_token(token)
    if payload is None:
        return None

    # Extract user ID from the token
    user_id: str = payload.get("sub")
    if user_id is None:
        return None

    # Get the user from the database
    from database.database import get_db
    db: Session = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        db.close()