"""
Chess Games Endpoints
CRUD operations for chess game records.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import (
    ChessGameCreate,
    ChessGameUpdate,
    ChessGameResponse,
    ChessGameListResponse,
    ChessGameStatsResponse,
)
from app.services import ChessGameService
from app.utils import get_current_user

router = APIRouter(
    prefix="/chess-games",
    tags=["Chess Games"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "",
    response_model=list[ChessGameResponse],
    summary="List all games",
    description="Retrieve all chess games for the current user"
)
async def list_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[ChessGameResponse]:
    """
    Get all chess games for the authenticated user.
    
    Returns games ordered by most recent first.
    """
    service = ChessGameService(db)
    return service.get_all_games(current_user.id)


@router.post(
    "",
    response_model=ChessGameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new game",
    description="Record a new chess game"
)
async def create_game(
    game_data: ChessGameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ChessGameResponse:
    """
    Create a new chess game record.
    
    - **title**: Game name/description (1-120 characters)
    - **opponent**: Opponent name (1-100 characters)
    - **result**: "win", "loss", or "draw"
    - **opening**: Chess opening name (optional, max 120 characters)
    - **notes**: Game analysis and notes (optional, max 8000 characters)
    """
    service = ChessGameService(db)
    return service.create_game(current_user.id, game_data)


@router.get(
    "/stats",
    response_model=ChessGameStatsResponse,
    summary="Get game statistics",
    description="Retrieve statistics for all games"
)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ChessGameStatsResponse:
    """
    Get chess game statistics for the current user.
    
    Returns:
    - **total**: Total games played
    - **wins**: Number of wins
    - **losses**: Number of losses
    - **draws**: Number of draws
    - **win_rate**: Win rate percentage (0-100)
    """
    service = ChessGameService(db)
    return service.get_game_stats(current_user.id)


@router.get(
    "/recent",
    response_model=list[ChessGameResponse],
    summary="Get recent games",
    description="Retrieve recent chess games"
)
async def get_recent_games(
    limit: int = Query(5, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[ChessGameResponse]:
    """
    Get recent chess games for the current user.
    
    - **limit**: Number of recent games to return (default 5, max 50)
    """
    service = ChessGameService(db)
    return service.get_recent_games(current_user.id, limit)


@router.get(
    "/{game_id}",
    response_model=ChessGameResponse,
    summary="Get a game",
    description="Retrieve a specific chess game by ID"
)
async def get_game(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ChessGameResponse:
    """
    Get a specific chess game by ID.
    
    - **game_id**: UUID of the game to retrieve
    """
    service = ChessGameService(db)
    return service.get_game_by_id(current_user.id, game_id)


@router.patch(
    "/{game_id}",
    response_model=ChessGameResponse,
    summary="Update a game",
    description="Update a chess game record"
)
async def update_game(
    game_id: str,
    game_data: ChessGameUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ChessGameResponse:
    """
    Update a chess game record.
    
    All fields are optional. Only provided fields will be updated.
    
    - **game_id**: UUID of the game to update
    """
    service = ChessGameService(db)
    return service.update_game(current_user.id, game_id, game_data)


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a game",
    description="Delete a chess game record"
)
async def delete_game(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a chess game record.
    
    - **game_id**: UUID of the game to delete
    """
    service = ChessGameService(db)
    service.delete_game(current_user.id, game_id)
