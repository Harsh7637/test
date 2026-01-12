"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
import logging

from app.api.v1.api import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Self-hosted AI platform with image generation, resume builder, and ATS analyzer",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("generated_images", exist_ok=True)
os.makedirs("generated_resumes", exist_ok=True)
logger.info("Created output directories")

# Mount static file directories
app.mount("/images", StaticFiles(directory="generated_images"), name="images")
app.mount("/resumes", StaticFiles(directory="generated_resumes"), name="resumes")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Platform API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-platform-api",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("🚀 AI Platform API starting up...")
    logger.info(f"📝 Documentation available at /api/docs")
    logger.info(f"🎨 Image output: generated_images/")
    logger.info(f"📄 Resume output: generated_resumes/")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("👋 AI Platform API shutting down...")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )