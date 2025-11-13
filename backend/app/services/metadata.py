# backend/app/services/metadata.py
"""
Image metadata extraction service
Extracts EXIF, IPTC, and other metadata from images
"""
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
from typing import Dict, Any
import io
import logging

logger = logging.getLogger(__name__)

def extract_metadata(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract comprehensive metadata from image
    
    Args:
        image_bytes: Raw image data
        
    Returns:
        Dictionary containing metadata fields
    """
    metadata = {
        "exif": {},
        "iptc": {},
        "basic": {},
        "gps": {}
    }
    
    try:
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Basic metadata
        metadata["basic"] = {
            "format": image.format,
            "mode": image.mode,
            "size": {"width": image.width, "height": image.height},
            "file_size_bytes": len(image_bytes)
        }
        
        # Extract EXIF data
        exif_data = image.getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # Handle GPS data separately
                if tag_name == "GPSInfo":
                    gps_info = {}
                    for gps_tag_id, gps_value in value.items():
                        gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag_name] = str(gps_value)
                    metadata["gps"] = gps_info
                else:
                    # Convert complex types to strings
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)
                    elif not isinstance(value, (str, int, float, bool, type(None))):
                        value = str(value)
                    
                    metadata["exif"][tag_name] = value
        
        # Extract IPTC data using piexif if available
        try:
            exif_dict = piexif.load(image_bytes)
            if "0th" in exif_dict:
                for tag, value in exif_dict["0th"].items():
                    tag_name = piexif.TAGS["0th"].get(tag, {}).get("name", str(tag))
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='ignore')
                    metadata["iptc"][tag_name] = value
        except Exception as e:
            logger.debug(f"Could not extract IPTC data: {e}")
        
        logger.info(f"Extracted metadata: {len(metadata['exif'])} EXIF tags, {len(metadata['gps'])} GPS tags")
        
    except Exception as e:
        logger.error(f"Error extracting metadata: {e}", exc_info=True)
        metadata["error"] = str(e)
    
    return metadata