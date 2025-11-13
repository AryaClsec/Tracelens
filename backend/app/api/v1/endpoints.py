# backend/app/api/v1/endpoints.py
"""
API endpoints for TraceLens
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
import io

from app.api.v1.models import AnalysisResponse, HealthResponse
from app.services.metadata import extract_metadata
from app.services.ocr_service import extract_text_ocr
from app.services.ai_detector import detect_ai_generated
from app.services.phash import compute_phash, find_duplicates
from app.services.rev_search import reverse_image_search
from app.utils.file_helpers import validate_image, check_explicit_content
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image for OSINT intelligence
    
    Returns:
        - Metadata (EXIF/IPTC)
        - OCR extracted text
        - AI detection analysis
        - Perceptual hash
        - Reverse image search results
    """
    try:
        # Read file content
        content = await file.read()
        
        # Validate file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        # Validate image format
        image_data = validate_image(content)
        
        # Check for explicit content
        if check_explicit_content(image_data):
            raise HTTPException(
                status_code=400,
                detail="Image flagged as potentially explicit content. Analysis refused for ethical reasons."
            )
        
        logger.info(f"Analyzing image: {file.filename}")
        
        # Extract metadata
        metadata = extract_metadata(content)
        
        # Perform OCR
        ocr_result = extract_text_ocr(image_data)
        
        # AI detection
        ai_detection = detect_ai_generated(image_data)
        
        # Compute perceptual hash
        phash = compute_phash(image_data)
        
        # Find duplicates
        duplicates = find_duplicates(phash)
        
        # Reverse image search
        reverse_search_results = await reverse_image_search(image_data, phash)
        
        response = AnalysisResponse(
            filename=file.filename,
            metadata=metadata,
            ocr=ocr_result,
            ai_detection=ai_detection,
            perceptual_hash=phash,
            duplicates=duplicates,
            reverse_search=reverse_search_results
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")