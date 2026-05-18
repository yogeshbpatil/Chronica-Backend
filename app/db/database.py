"""
Database configuration and session management.
Handles SQLAlchemy engine and session creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

settings = get_settings()

# Create database engine
# Using check_same_thread=False only for SQLite; for PostgreSQL this is unnecessary
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log all SQL statements if DEBUG is True
    future=True,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db() -> Session:
    """
    Dependency function to get database session.
    Used in FastAPI dependencies.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
