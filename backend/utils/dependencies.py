from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from models.user import User
from utils.jwt_utils import is_authenticated

# HTTP Bearer token scheme for authentication
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """
    Dependency to get the current authenticated user from the JWT token
    """
    token = credentials.credentials
    user = is_authenticated(token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, or return None
    """
    token = credentials.credentials
    user = is_authenticated(token)
    
    return user