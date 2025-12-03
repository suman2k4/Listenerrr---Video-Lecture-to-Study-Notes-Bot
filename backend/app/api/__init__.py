from fastapi import APIRouter

from app.api import status, upload

api_router = APIRouter()
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(status.router, prefix="/jobs", tags=["jobs"])

__all__ = ["api_router"]
