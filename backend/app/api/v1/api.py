"""
API v1 Router - Aggregates all endpoint routers
"""
from fastapi import APIRouter

from app.api.v1.endpoints import image_generation, resume, ats

api_router = APIRouter()

# Include all feature routers
api_router.include_router(
    image_generation.router,
    prefix="/image",
    tags=["Image Generation"]
)

api_router.include_router(
    resume.router,
    prefix="/resume",
    tags=["Resume Generator"]
)

api_router.include_router(
    ats.router,
    prefix="/ats",
    tags=["ATS Analyzer"]
)