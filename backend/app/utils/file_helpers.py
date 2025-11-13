# backend/app/utils/file_helpers.py
"""
File handling utilities
"""
from PIL import Image
import io
import logging
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/tiff',
    'image/webp'
]

def validate_image(file_content: bytes) -> Image.Image:
    """
    Validate and load image from bytes
    
    Args:
        file_content: Raw file bytes
        
    Returns:
        PIL Image object
        
    Raises:
        ValueError: If file is not a valid image
    """
    try:
        image = Image.open(io.BytesIO(file_content))
        image.verify()  # Verify it's a valid image
        
        # Reopen after verify (verify closes the file)
        image = Image.open(io.BytesIO(file_content))
        
        logger.info(f"Validated image: {image.format} {image.size}")
        return image
        
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        raise ValueError(f"Invalid image file: {str(e)}")

def check_explicit_content(image: Image.Image) -> bool:
    """
    Simple heuristic check for potentially explicit content
    
    This is a basic implementation. In production, use ML-based content moderation.
    
    Args:
        image: PIL Image object
        
    Returns:
        True if content appears explicit, False otherwise
    """
    try:
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        img_small = image.resize((64, 64))
        img_array = np.array(img_small)
        
        # Check for excessive skin tone colors (simple heuristic)
        # Skin tone roughly: R: 180-255, G: 120-200, B: 100-180
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        
        skin_mask = (
            (r > 180) & (r < 255) &
            (g > 120) & (g < 200) &
            (b > 100) & (b < 180)
        )
        
        skin_percentage = np.sum(skin_mask) / (64 * 64)
        
        # If more than 70% skin tone, flag as potentially explicit
        # This is very basic and will have false positives
        if skin_percentage > 0.7:
            logger.warning(f"Image flagged as potentially explicit (skin: {skin_percentage:.2%})")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Explicit content check failed: {e}")
        return False  # Fail open for non-critical check

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import os
    import re
    
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Remove any non-alphanumeric characters except . _ -
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Limit length
    if len(filename) > 255: