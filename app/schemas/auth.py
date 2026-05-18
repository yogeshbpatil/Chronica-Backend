"""
Authentication Schemas - Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields"""

    name: str = Field(..., min_length=1, max_length=80, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for user registration/creation"""

    password: str = Field(..., min_length=8, max_length=100, description="User's password")


class UserResponse(UserBase):
    """Schema for user response (without password)"""

    id: str = Field(..., description="User ID (UUID)")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True


class AuthSessionResponse(BaseModel):
    """Schema for authentication response"""

    user: UserResponse = Field(..., description="User information")
    token: str = Field(..., description="JWT Bearer token")
    expires_at: datetime = Field(..., description="Token expiration timestamp")

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request"""

    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., description="User's password")


class TokenData(BaseModel):
    """Schema for decoded token data"""

    user_id: Optional[str] = Field(None, description="User ID from token")
