"""Schemas module"""

from .auth import (
    UserCreate,
    UserResponse,
    AuthSessionResponse,
    LoginRequest,
    TokenData,
)
from .chess_game import (
    ChessGameCreate,
    ChessGameUpdate,
    ChessGameResponse,
    ChessGameListResponse,
    ChessGameStatsResponse,
    GameResultEnum,
)

__all__ = [
    # Auth schemas
    "UserCreate",
    "UserResponse",
    "AuthSessionResponse",
    "LoginRequest",
    "TokenData",
    # Chess game schemas
    "ChessGameCreate",
    "ChessGameUpdate",
    "ChessGameResponse",
    "ChessGameListResponse",
    "ChessGameStatsResponse",
    "GameResultEnum",
]
