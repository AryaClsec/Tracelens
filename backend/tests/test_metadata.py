# backend/tests/test_metadata.py
"""
Unit tests for metadata extraction
"""
import pytest
from PIL import Image
import io
from app.services.metadata import extract_metadata
from app.services.phash import compute_phash, find_duplicates

def create_test_image(size=(100, 100), color=(255, 0, 0)):
    """Helper to create test image"""
    img = Image.new('RGB', size, color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()

def test_extract_metadata_basic():
    """Test basic metadata extraction"""
    img_bytes = create_test_image()
    metadata = extract_metadata(img_bytes)
    
    assert "basic" in metadata
    assert "exif" in metadata
    assert metadata["basic"]["format"] == "JPEG"
    assert metadata["basic"]["size"]["width"] == 100
    assert metadata["basic"]["size"]["height"] == 100

def test_extract_metadata_with_exif():
    """Test metadata extraction with EXIF data"""
    # Create image with EXIF
    img = Image.new('RGB', (200, 200), (0, 255, 0))
    
    # Add some basic EXIF data
    from PIL.PngImagePlugin import PngInfo
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    
    metadata = extract_metadata(img_bytes)
    
    assert metadata["basic"]["format"] == "JPEG"
    assert metadata["basic"]["size"]["width"] == 200

def test_compute_phash():
    """Test perceptual hash computation"""
    img = Image.new('RGB', (100, 100), (128, 128, 128))
    phash = compute_phash(img)
    
    assert phash is not None
    assert len(phash) > 0
    assert isinstance(phash, str)

def test_find_duplicates():
    """Test duplicate detection"""
    # Create similar images
    img1 = Image.new('RGB', (100, 100), (100, 100, 100))
    img2 = Image.new('RGB', (100, 100), (105, 105, 105))  # Very similar
    
    hash1 = compute_phash(img1)
    hash2 = compute_phash(img2)
    
    # Find duplicates for hash1
    duplicates = find_duplicates(hash1, threshold=10)
    
    # Should find img2 as similar
    assert isinstance(duplicates, list)

def test_metadata_error_handling():
    """Test metadata extraction with invalid data"""
    invalid_bytes = b"not an image"
    metadata = extract_metadata(invalid_bytes)
    
    assert "error" in metadata

if __name__ == "__main__":
    pytest.main([__file__, "-v"])