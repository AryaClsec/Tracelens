# backend/app/services/phash.py
"""
Perceptual hashing and duplicate detection service
"""
import imagehash
from PIL import Image
import logging
from typing import List, Dict
from app.api.v1.models import DuplicateMatch

logger = logging.getLogger(__name__)

# In-memory storage for perceptual hashes
hash_store: Dict[str, str] = {}

def compute_phash(image: Image.Image) -> str:
    """
    Compute perceptual hash of image
    
    Args:
        image: PIL Image object
        
    Returns:
        Hexadecimal perceptual hash string
    """
    try:
        phash = imagehash.phash(image)
        hash_str = str(phash)
        
        # Store in memory (in production, use a proper database)
        hash_store[hash_str] = hash_str
        
        logger.info(f"Computed pHash: {hash_str}")
        return hash_str
        
    except Exception as e:
        logger.error(f"Failed to compute pHash: {e}")
        return ""

def find_duplicates(target_hash: str, threshold: int = 10) -> List[DuplicateMatch]:
    """
    Find duplicate or similar images using Hamming distance
    
    Args:
        target_hash: Perceptual hash to compare against
        threshold: Maximum Hamming distance for matches
        
    Returns:
        List of duplicate matches
    """
    matches = []
    
    try:
        if not target_hash:
            return matches
        
        target = imagehash.hex_to_hash(target_hash)
        
        for stored_hash in hash_store.keys():
            if stored_hash == target_hash:
                continue  # Skip self
            
            try:
                stored = imagehash.hex_to_hash(stored_hash)
                distance = target - stored  # Hamming distance
                
                if distance <= threshold:
                    similarity = (1 - distance / 64.0) * 100  # Convert to percentage
                    matches.append(DuplicateMatch(
                        hash=stored_hash,
                        distance=distance,
                        similarity_percentage=round(similarity, 2)
                    ))
            except Exception as e:
                logger.warning(f"Error comparing hash {stored_hash}: {e}")
                continue
        
        # Sort by similarity
        matches.sort(key=lambda x: x.distance)
        
        logger.info(f"Found {len(matches)} duplicate/similar images")
        
    except Exception as e:
        logger.error(f"Duplicate detection failed: {e}")
    
    return matches

def seed_hash_store(demo_hashes: List[str]):
    """
    Seed the hash store with demo images
    
    Args:
        demo_hashes: List of perceptual hashes to add
    """
    for h in demo_hashes:
        hash_store[h] = h
    logger.info(f"Seeded hash store with {len(demo_hashes)} hashes")