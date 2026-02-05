from datetime import timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from services.user_service import authenticate_user, create_user as create_user_service
from utils.jwt_utils import create_access_token
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

def login_user_service(db: Session, credentials: UserLogin) -> Optional[dict]:
    """
    Service function to handle user login and return JWT token
    """
    logger.info(f"Attempting login for user: {credentials.email}")
    
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with 30 day expiration
    access_token_expires = timedelta(days=30)
    access_token = create_access_token(
        data={"sub": user.id},  # Store user ID in the token
        expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {user.id}")
    return {"token": access_token}


def register_user_service(db: Session, user_data: UserCreate) -> dict:
    """
    Service function to handle user registration and return JWT token
    """
    logger.info(f"Registering new user with email: {user_data.email}")
    
    # Check if user already exists
    from services.user_service import get_user_by_email
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        logger.warning(f"Attempt to register with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = create_user_service(db, user_data)
    logger.info(f"Successfully registered user with ID: {db_user.id}")
    
    # Create access token with 30 day expiration
    access_token_expires = timedelta(days=30)
    access_token = create_access_token(
        data={"sub": db_user.id},  # Store user ID in the token
        expires_delta=access_token_expires
    )
    
    logger.info(f"Generated JWT token for user: {db_user.id}")
    return {"token": access_token}