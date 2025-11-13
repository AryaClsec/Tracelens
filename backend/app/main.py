# backend/app/main.py
"""
TraceLens - OSINT Image Analysis Platform
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.endpoints import router as api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TraceLens",
    description="OSINT Image Analysis Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Log ethics reminder on startup"""
    logger.warning(
        "⚖️  TraceLens is starting. Operators must comply with local laws and use this tool "
        "only for lawful, ethical OSINT research. Unauthorized surveillance or malicious use is prohibited."
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TraceLens OSINT Image Analysis Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }