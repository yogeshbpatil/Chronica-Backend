"""
Database Models - SQLAlchemy ORM definitions.
These models represent tables in the PostgreSQL database.
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class User(Base):
    """
    User model for authentication.
    Stores user account information.
    """

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(80), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chess_games = relationship("ChessGame", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


class GameResult(str, enum.Enum):
    """Enum for chess game results"""

    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"


class ChessGame(Base):
    """
    Chess Game model for storing game records.
    Each game is associated with a user and contains game details.
    """

    __tablename__ = "chess_games"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(120), nullable=False, index=True)
    opponent = Column(String(100), nullable=False)
    result = Column(SQLEnum(GameResult), nullable=False, index=True)
    opening = Column(String(120), nullable=True, default="")
    notes = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chess_games")

    def __repr__(self) -> str:
        return f"<ChessGame(id={self.id}, title={self.title}, opponent={self.opponent}, result={self.result})>"
