"""
Authentication Endpoints
Handles user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import UserCreate, LoginRequest, AuthSessionResponse
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> AuthSessionResponse:
    """
    Register a new user.
    
    - **name**: User's full name (1-80 characters)
    - **email**: Unique email address
    - **password**: At least 8 characters
    """
    auth_service = AuthService(db)
    return auth_service.register(user_data)


@router.post(
    "/login",
    response_model=AuthSessionResponse,
    summary="Login user",
    description="Authenticate user and receive access token"
)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
) -> AuthSessionResponse:
    """
    Login with email and password.
    
    Returns a JWT token valid for 7 days (10080 minutes).
    """
    auth_service = AuthService(db)
    return auth_service.login(credentials)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Clear session (primarily for frontend cleanup)"
)
async def logout():
    """
    Logout endpoint.
    
    Note: JWT tokens are stateless. This endpoint is mainly for frontend
    to perform cleanup operations. The token remains valid until expiration.
    """
    return {"message": "Logged out successfully"}
