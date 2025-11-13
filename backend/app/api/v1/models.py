# backend/app/api/v1/models.py
"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str

class OCRResult(BaseModel):
    """OCR extraction result"""
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None

class AIDetectionResult(BaseModel):
    """AI-generated image detection result"""
    score: float = Field(..., ge=0.0, le=1.0, description="Probability of AI generation (0=human, 1=AI)")
    verdict: str = Field(..., description="human|ai|uncertain")
    explanation: str = Field(..., description="Explanation of the verdict")
    signals: Dict[str, Any] = Field(default_factory=dict, description="Detection signals")

class ReverseSearchMatch(BaseModel):
    """Reverse image search match"""
    source: str
    similarity: float
    url: Optional[str] = None
    thumbnail: Optional[str] = None

class DuplicateMatch(BaseModel):
    """Duplicate image match"""
    hash: str
    distance: int
    similarity_percentage: float

class AnalysisResponse(BaseModel):
    """Complete image analysis response"""
    filename: str
    metadata: Dict[str, Any]
    ocr: OCRResult
    ai_detection: AIDetectionResult
    perceptual_hash: str
    duplicates: List[DuplicateMatch]
    reverse_search: List[ReverseSearchMatch]