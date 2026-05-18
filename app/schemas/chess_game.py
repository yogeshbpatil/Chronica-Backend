"""
Chess Games Schemas - Pydantic models for game CRUD operations.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class GameResultEnum(str, Enum):
    """Enum for game results"""

    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"


class ChessGameBase(BaseModel):
    """Base chess game schema with common fields"""

    title: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Game title/name"
    )
    opponent: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Opponent name"
    )
    result: GameResultEnum = Field(..., description="Game result")
    opening: str = Field(
        default="",
        max_length=120,
        description="Chess opening name"
    )
    notes: str = Field(
        default="",
        max_length=8000,
        description="Game notes and analysis"
    )


class ChessGameCreate(ChessGameBase):
    """Schema for creating a chess game"""

    pass


class ChessGameUpdate(BaseModel):
    """Schema for updating a chess game (all fields optional)"""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=120,
        description="Game title/name"
    )
    opponent: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Opponent name"
    )
    result: Optional[GameResultEnum] = Field(None, description="Game result")
    opening: Optional[str] = Field(
        None,
        max_length=120,
        description="Chess opening name"
    )
    notes: Optional[str] = Field(
        None,
        max_length=8000,
        description="Game notes and analysis"
    )


class ChessGameResponse(ChessGameBase):
    """Schema for chess game response"""

    id: str = Field(..., description="Game ID (UUID)")
    user_id: str = Field(..., description="User ID (owner)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class ChessGameListResponse(BaseModel):
    """Schema for list of chess games"""

    data: list[ChessGameResponse] = Field(..., description="List of chess games")
    total: int = Field(..., description="Total number of games")

    class Config:
        from_attributes = True


class ChessGameStatsResponse(BaseModel):
    """Schema for chess game statistics"""

    total: int = Field(..., description="Total games played")
    wins: int = Field(..., description="Total wins")
    losses: int = Field(..., description="Total losses")
    draws: int = Field(..., description="Total draws")
    win_rate: float = Field(..., description="Win rate percentage (0-100)")
