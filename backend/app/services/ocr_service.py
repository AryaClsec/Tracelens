# backend/app/services/ocr_service.py
"""
OCR service using Tesseract
"""
import pytesseract
from PIL import Image
import io
import logging
from typing import Dict, Any

from app.core.config import settings
from app.api.v1.models import OCRResult

logger = logging.getLogger(__name__)

def extract_text_ocr(image: Image.Image) -> OCRResult:
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image: PIL Image object
        
    Returns:
        OCRResult with extracted text and confidence
    """
    try:
        # Perform OCR with data output
        ocr_data = pytesseract.image_to_data(
            image,
            lang=settings.TESSERACT_LANG,
            output_type=pytesseract.Output.DICT
        )
        
        # Extract text
        text = pytesseract.image_to_string(image, lang=settings.TESSERACT_LANG)
        
        # Calculate average confidence
        confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        logger.info(f"OCR extracted {len(text)} characters with confidence {avg_confidence:.2f}")
        
        return OCRResult(
            text=text.strip(),
            confidence=avg_confidence / 100.0,  # Normalize to 0-1
            language=settings.TESSERACT_LANG
        )
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}", exc_info=True)
        return OCRResult(
            text="",
            confidence=0.0,
            language=settings.TESSERACT_LANG
        )