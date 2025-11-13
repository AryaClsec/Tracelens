# backend/app/services/ai_detector.py
"""
AI-generated image detection service
Uses heuristics and statistical analysis to detect AI-generated images
"""
import numpy as np
from PIL import Image
import imagehash
import logging
from typing import Dict, Any

from app.api.v1.models import AIDetectionResult
from app.core.config import settings

logger = logging.getLogger(__name__)

def detect_ai_generated(image: Image.Image) -> AIDetectionResult:
    """
    Detect if image is AI-generated using multiple heuristics
    
    Args:
        image: PIL Image object
        
    Returns:
        AIDetectionResult with score and explanation
    """
    signals = {}
    scores = []
    
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Signal 1: Noise level analysis
        noise_score = analyze_noise_level(img_array)
        signals["noise_analysis"] = {
            "score": noise_score,
            "description": "Low noise suggests potential AI generation"
        }
        scores.append(noise_score)
        
        # Signal 2: Frequency domain analysis
        freq_score = analyze_frequency_domain(img_array)
        signals["frequency_analysis"] = {
            "score": freq_score,
            "description": "Unusual frequency patterns common in AI images"
        }
        scores.append(freq_score)
        
        # Signal 3: Color distribution uniformity
        color_score = analyze_color_distribution(img_array)
        signals["color_distribution"] = {
            "score": color_score,
            "description": "Overly uniform colors may indicate AI generation"
        }
        scores.append(color_score)
        
        # Signal 4: Perceptual hash entropy
        entropy_score = analyze_hash_entropy(image)
        signals["hash_entropy"] = {
            "score": entropy_score,
            "description": "Hash patterns can reveal synthetic artifacts"
        }
        scores.append(entropy_score)
        
        # Compute weighted average
        final_score = np.mean(scores)
        
        # Determine verdict
        if final_score >= settings.AI_DETECTION_THRESHOLD:
            verdict = "ai"
            explanation = f"High probability of AI generation (score: {final_score:.2f}). "
            explanation += "Multiple signals indicate synthetic origin: "
            explanation += ", ".join([k for k, v in signals.items() if v["score"] > 0.6])
        elif final_score <= settings.UNCERTAIN_THRESHOLD:
            verdict = "human"
            explanation = f"Likely human-created (score: {final_score:.2f}). "
            explanation += "Natural artifacts and patterns detected."
        else:
            verdict = "uncertain"
            explanation = f"Uncertain origin (score: {final_score:.2f}). "
            explanation += "Mixed signals prevent definitive classification."
        
        logger.info(f"AI detection: {verdict} (score: {final_score:.3f})")
        
        return AIDetectionResult(
            score=round(final_score, 3),
            verdict=verdict,
            explanation=explanation,
            signals=signals
        )
        
    except Exception as e:
        logger.error(f"AI detection failed: {e}", exc_info=True)
        return AIDetectionResult(
            score=0.5,
            verdict="uncertain",
            explanation=f"Detection failed: {str(e)}",
            signals={"error": str(e)}
        )

def analyze_noise_level(img_array: np.ndarray) -> float:
    """Analyze image noise level - AI images often have unnaturally low noise"""
    try:
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        # Compute local variance as noise proxy
        from scipy.ndimage import generic_filter
        local_var = generic_filter(gray, np.var, size=3)
        avg_variance = np.mean(local_var)
        
        # Lower variance suggests AI (inverted score)
        # Normalize: typical photos have variance 100-2000
        normalized_var = min(avg_variance / 2000.0, 1.0)
        score = 1.0 - normalized_var  # Invert: low variance = high AI score
        
        return float(score)
    except:
        return 0.5

def analyze_frequency_domain(img_array: np.ndarray) -> float:
    """Analyze frequency domain - AI images may have unusual spectral patterns"""
    try:
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        # FFT analysis
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        
        # Check for unusual frequency concentration
        center_power = np.sum(magnitude[magnitude.shape[0]//4:3*magnitude.shape[0]//4,
                                       magnitude.shape[1]//4:3*magnitude.shape[1]//4])
        total_power = np.sum(magnitude)
        
        concentration = center_power / (total_power + 1e-10)
        
        # High concentration in mid-frequencies may indicate AI
        if concentration > 0.8:
            score = 0.7
        elif concentration > 0.7:
            score = 0.5
        else:
            score = 0.3
        
        return float(score)
    except:
        return 0.5

def analyze_color_distribution(img_array: np.ndarray) -> float:
    """Analyze color distribution uniformity"""
    try:
        if len(img_array.shape) != 3:
            return 0.5
        
        # Compute color histogram entropy for each channel
        entropies = []
        for channel in range(3):
            hist, _ = np.histogram(img_array[:,:,channel], bins=256, range=(0, 256))
            hist = hist / (hist.sum() + 1e-10)
            entropy = -np.sum(hist * np.log(hist + 1e-10))
            entropies.append(entropy)
        
        avg_entropy = np.mean(entropies)
        
        # Lower entropy suggests less natural variation
        # Natural photos typically have entropy 6-8
        if avg_entropy < 5.5:
            score = 0.7
        elif avg_entropy < 6.5:
            score = 0.5
        else:
            score = 0.3
        
        return float(score)
    except:
        return 0.5

def analyze_hash_entropy(image: Image.Image) -> float:
    """Analyze perceptual hash for patterns"""
    try:
        # Compute multiple hash types
        ahash = imagehash.average_hash(image)
        phash = imagehash.phash(image)
        dhash = imagehash.dhash(image)
        
        # Convert to binary strings
        ahash_bin = bin(int(str(ahash), 16))[2:].zfill(64)
        phash_bin = bin(int(str(phash), 16))[2:].zfill(64)
        dhash_bin = bin(int(str(dhash), 16))[2:].zfill(64)
        
        # Compute entropy
        combined = ahash_bin + phash_bin + dhash_bin
        ones = combined.count('1')
        entropy = min(ones, len(combined) - ones) / (len(combined) / 2)
        
        # Very uniform hashes may indicate AI
        if entropy < 0.4:
            score = 0.7
        elif entropy < 0.6:
            score = 0.5
        else:
            score = 0.3
        
        return float(score)
    except:
        return 0.5