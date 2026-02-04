from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from database.database import get_db
from schemas import UserCreate, UserLogin, UserLogout, UserResponse, TokenResponse
from services import get_user, login_user_service, register_user_service
from utils.dependencies import get_current_user
from models.user import User
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# Registration endpoints
@router.post("/registration/signup", response_model=TokenResponse)
def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    logger.info(f"Registering new user with email: {user.email}")

    # Use the authentication service to register the user and generate a token
    token_response = register_user_service(db, user)
    return token_response

@router.post("/registration/login", response_model=TokenResponse)
def login_user_endpoint(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login a user"""
    logger.info(f"Login attempt for user: {credentials.email}")

    # Use the authentication service to login the user and generate a token
    token_response = login_user_service(db, credentials)
    return token_response

@router.post("/registration/logout")
def logout_user(credentials: UserLogout, db: Session = Depends(get_db)):
    """Logout a user"""
    logger.info("User logout request")
    # In a real app, you would invalidate the token here
    # For now, just returning success
    return {}

# User endpoints
@router.get("/me", response_model=UserResponse)
def get_current_user_data(current_user: User = Depends(get_current_user)):
    """Get current user's details based on their token"""
    logger.info(f"Retrieving current user details for ID: {current_user.id}")

    # Return the current user's data extracted from the token
    logger.info(f"Successfully retrieved current user details for ID: {current_user.id}")
    return current_user

@router.get("/{id}", response_model=UserResponse)
def get_user_details(id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user details by ID"""
    logger.info(f"Retrieving user details for ID: {id} by user: {current_user.id}")

    # Users can only retrieve their own details, unless they are HR
    if current_user.id != id and current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to access user details by user: {current_user.id} for user: {id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user details"
        )

    user = get_user(db, id)
    if not user:
        logger.warning(f"User not found for ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Successfully retrieved user details for ID: {user.id}")
    return user