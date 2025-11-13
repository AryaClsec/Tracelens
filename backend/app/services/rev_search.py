# backend/app/services/rev_search.py
"""
Reverse image search service
Falls back to local perceptual hash matching if no API key provided
"""
import os
import logging
from typing import List
from PIL import Image
import aiohttp

from app.api.v1.models import ReverseSearchMatch
from app.core.config import settings
from app.services.phash import find_duplicates

logger = logging.getLogger(__name__)

async def reverse_image_search(image: Image.Image, phash: str) -> List[ReverseSearchMatch]:
    """
    Perform reverse image search using external API or local fallback
    
    Args:
        image: PIL Image object
        phash: Perceptual hash of the image
        
    Returns:
        List of reverse search matches
    """
    # Try external API if key is available
    if settings.REVSEARCH_API_KEY:
        try:
            results = await search_external_api(image)
            if results:
                return results
        except Exception as e:
            logger.warning(f"External API search failed: {e}, falling back to local")
    
    # Fallback to local perceptual hash matching
    logger.info("Using local perceptual hash matching for reverse search")
    return search_local_fallback(phash)

async def search_external_api(image: Image.Image) -> List[ReverseSearchMatch]:
    """
    Search using external reverse image search API
    
    NOTE: This is a placeholder implementation. In production, integrate with
    services like Google Vision API, Bing Image Search, or TinEye API.
    
    Example API call structure:
    """
    api_key = settings.REVSEARCH_API_KEY
    
    # Placeholder API endpoint (replace with actual service)
    api_url = "https://api.example-reverse-search.com/v1/search"
    
    try:
        # Convert image to bytes for upload
        from io import BytesIO
        img_bytes = BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Example API call structure
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('image', img_bytes, filename='query.jpg')
            
            headers = {'Authorization': f'Bearer {api_key}'}
            
            async with session.post(api_url, data=form_data, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    # Parse response (adjust based on actual API)
                    matches = []
                    for result in data.get('matches', [])[:5]:
                        matches.append(ReverseSearchMatch(
                            source=result.get('source', 'Unknown'),
                            similarity=result.get('similarity', 0.0),
                            url=result.get('url'),
                            thumbnail=result.get('thumbnail')
                        ))
                    
                    return matches
                else:
                    logger.error(f"API returned status {resp.status}")
                    return []
                    
    except Exception as e:
        logger.error(f"External API search failed: {e}")
        raise

def search_local_fallback(phash: str) -> List[ReverseSearchMatch]:
    """
    Fallback reverse search using local perceptual hash database
    
    Args:
        phash: Perceptual hash to search for
        
    Returns:
        List of matches from local database
    """
    matches = []
    
    try:
        # Find duplicates using perceptual hash
        duplicates = find_duplicates(phash, threshold=15)
        
        # Convert to reverse search format
        for dup in duplicates[:5]:  # Limit to top 5
            matches.append(ReverseSearchMatch(
                source="Local Database",
                similarity=dup.similarity_percentage / 100.0,
                url=None,
                thumbnail=None
            ))
        
        if not matches:
            # Add a demo message if no matches found
            matches.append(ReverseSearchMatch(
                source="Local Database",
                similarity=0.0,
                url=None,
                thumbnail=None
            ))
        
    except Exception as e:
        logger.error(f"Local fallback search failed: {e}")
    
    return matches