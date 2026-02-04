from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from models.user import User
from schemas.user import UserCreate
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

def get_user(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    logger.debug(f"Retrieving user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.debug(f"Found user: {user.id}")
    else:
        logger.debug(f"User not found for ID: {user_id}")
    return user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    logger.debug(f"Retrieving user with email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.debug(f"Found user: {user.id} for email: {email}")
    else:
        logger.debug(f"User not found for email: {email}")
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users"""
    logger.debug(f"Retrieving users with skip={skip}, limit={limit}")
    users = db.query(User).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(users)} users")
    return users

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    logger.info(f"Creating new user with email: {user.email}")
    db_user = User(
        id=str(uuid.uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role
    )
    db_user.set_password(user.password)  # Properly hash the password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Successfully created user with ID: {db_user.id}")
    return db_user

def update_user(db: Session, user_id: str, **kwargs) -> Optional[User]:
    """Update a user"""
    logger.info(f"Updating user with ID: {user_id}")
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in kwargs.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Successfully updated user: {db_user.id}")
        return db_user
    logger.warning(f"Failed to update user - user not found: {user_id}")
    return None

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    logger.info(f"Authenticating user with email: {email}")
    user = get_user_by_email(db, email)
    if user and user.check_password(password):  # Verify the password using the model method
        logger.info(f"Authentication successful for user: {user.id}")
        return user
    logger.warning(f"Authentication failed for email: {email}")
    return None