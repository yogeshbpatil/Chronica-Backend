"""API v1 endpoints module"""

from fastapi import APIRouter

from . import auth, chess_games

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(chess_games.router)

__all__ = ["api_router"]
