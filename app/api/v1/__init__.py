"""API v1 module"""

from fastapi import APIRouter

from app.api.v1.endpoints import api_router

router = APIRouter(prefix="/api/v1")
router.include_router(api_router)

__all__ = ["router"]
