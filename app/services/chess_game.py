"""
Chess Games Service - Business logic for chess game CRUD operations.
Handles game creation, retrieval, updates, and deletion.
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status

from app.models import ChessGame, GameResult, User
from app.schemas import (
    ChessGameCreate,
    ChessGameUpdate,
    ChessGameResponse,
    ChessGameStatsResponse,
)


class ChessGameService:
    """Service class for chess game operations"""

    def __init__(self, db: Session):
        """
        Initialize chess game service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create_game(self, user_id: str, game_data: ChessGameCreate) -> ChessGameResponse:
        """
        Create a new chess game record.
        
        Args:
            user_id: User ID (owner of the game)
            game_data: Game details
            
        Returns:
            Created ChessGameResponse
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create game
        db_game = ChessGame(
            user_id=user_id,
            title=game_data.title,
            opponent=game_data.opponent,
            result=GameResult(game_data.result),
            opening=game_data.opening,
            notes=game_data.notes,
        )

        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)

        return ChessGameResponse.model_validate(db_game)

    def get_all_games(self, user_id: str) -> list[ChessGameResponse]:
        """
        Retrieve all chess games for a user, ordered by most recent first.
        
        Args:
            user_id: User ID
            
        Returns:
            List of ChessGameResponse objects
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        games = self.db.query(ChessGame).filter(
            ChessGame.user_id == user_id
        ).order_by(desc(ChessGame.created_at)).all()

        return [ChessGameResponse.model_validate(game) for game in games]

    def get_game_by_id(self, user_id: str, game_id: str) -> ChessGameResponse:
        """
        Retrieve a specific chess game by ID.
        
        Args:
            user_id: User ID (for authorization)
            game_id: Game ID
            
        Returns:
            ChessGameResponse
            
        Raises:
            HTTPException: If game not found or not authorized
        """
        game = self.db.query(ChessGame).filter(
            ChessGame.id == game_id,
            ChessGame.user_id == user_id
        ).first()

        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )

        return ChessGameResponse.model_validate(game)

    def update_game(
        self,
        user_id: str,
        game_id: str,
        game_data: ChessGameUpdate
    ) -> ChessGameResponse:
        """
        Update a chess game record.
        
        Args:
            user_id: User ID (for authorization)
            game_id: Game ID
            game_data: Updated game data (partial update)
            
        Returns:
            Updated ChessGameResponse
            
        Raises:
            HTTPException: If game not found or not authorized
        """
        game = self.db.query(ChessGame).filter(
            ChessGame.id == game_id,
            ChessGame.user_id == user_id
        ).first()

        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )

        # Update only provided fields
        if game_data.title is not None:
            game.title = game_data.title
        if game_data.opponent is not None:
            game.opponent = game_data.opponent
        if game_data.result is not None:
            game.result = GameResult(game_data.result)
        if game_data.opening is not None:
            game.opening = game_data.opening
        if game_data.notes is not None:
            game.notes = game_data.notes

        self.db.commit()
        self.db.refresh(game)

        return ChessGameResponse.model_validate(game)

    def delete_game(self, user_id: str, game_id: str) -> None:
        """
        Delete a chess game record.
        
        Args:
            user_id: User ID (for authorization)
            game_id: Game ID
            
        Raises:
            HTTPException: If game not found or not authorized
        """
        game = self.db.query(ChessGame).filter(
            ChessGame.id == game_id,
            ChessGame.user_id == user_id
        ).first()

        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )

        self.db.delete(game)
        self.db.commit()

    def get_game_stats(self, user_id: str) -> ChessGameStatsResponse:
        """
        Calculate game statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            ChessGameStatsResponse with calculated stats
        """
        games = self.db.query(ChessGame).filter(
            ChessGame.user_id == user_id
        ).all()

        total = len(games)
        wins = sum(1 for game in games if game.result == GameResult.WIN)
        losses = sum(1 for game in games if game.result == GameResult.LOSS)
        draws = sum(1 for game in games if game.result == GameResult.DRAW)

        win_rate = (wins / total * 100) if total > 0 else 0.0

        return ChessGameStatsResponse(
            total=total,
            wins=wins,
            losses=losses,
            draws=draws,
            win_rate=round(win_rate, 2)
        )

    def get_recent_games(self, user_id: str, limit: int = 5) -> list[ChessGameResponse]:
        """
        Retrieve recent chess games for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of recent games to return
            
        Returns:
            List of ChessGameResponse objects (most recent first)
        """
        games = self.db.query(ChessGame).filter(
            ChessGame.user_id == user_id
        ).order_by(desc(ChessGame.created_at)).limit(limit).all()

        return [ChessGameResponse.model_validate(game) for game in games]
