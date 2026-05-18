"""
Authentication Service - Business logic for auth operations.
Handles user registration, login, and session management.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import User
from app.schemas import UserCreate, LoginRequest, AuthSessionResponse, UserResponse
from app.core.security import SecurityUtils


class AuthService:
    """Service class for authentication operations"""

    def __init__(self, db: Session):
        """
        Initialize auth service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.security = SecurityUtils()

    def register(self, user_data: UserCreate) -> AuthSessionResponse:
        """
        Register a new user.
        
        Args:
            user_data: User registration data (name, email, password)
            
        Returns:
            AuthSessionResponse with user info and token
            
        Raises:
            HTTPException: If email already exists
        """
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(
                User.email == user_data.email
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="An account with this email already exists."
                )

            # Create new user
            hashed_password = self.security.hash_password(user_data.password)
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=hashed_password,
            )

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)

            # Generate token
            token, expires_at = self._create_token(db_user.id)

            return AuthSessionResponse(
                user=UserResponse.model_validate(db_user),
                token=token,
                expires_at=expires_at
            )

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists."
            )
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed. Please try again."
            )

    def login(self, login_data: LoginRequest) -> AuthSessionResponse:
        """
        Authenticate user and create session.
        
        Args:
            login_data: Login credentials (email, password)
            
        Returns:
            AuthSessionResponse with user info and token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        user = self.db.query(User).filter(
            User.email == login_data.email
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please try again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not self.security.verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please try again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate token
        token, expires_at = self._create_token(user.id)

        return AuthSessionResponse(
            user=UserResponse.model_validate(user),
            token=token,
            expires_at=expires_at
        )

    def get_user_by_id(self, user_id: str) -> User:
        """
        Retrieve user by ID.
        
        Args:
            user_id: User UUID
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    @staticmethod
    def _create_token(user_id: str) -> tuple[str, datetime]:
        """
        Create JWT token for user.
        
        Args:
            user_id: User UUID
            
        Returns:
            Tuple of (token, expiration_datetime)
        """
        expires_delta = timedelta(days=7)
        to_encode = {"sub": user_id}
        token = SecurityUtils.create_access_token(to_encode, expires_delta)
        expires_at = datetime.utcnow() + expires_delta
        return token, expires_at
