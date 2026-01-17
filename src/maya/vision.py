"""
Vision and OCR capabilities for Maya AI.
Screen analysis, OCR text extraction, and image understanding.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import datetime

try:
    from PIL import Image, ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def capture_screen(save_path: Optional[str] = None) -> Optional[str]:
    """
    Capture screenshot and optionally save it.
    
    Args:
        save_path: Path to save screenshot. If None, saves to default location.
        
    Returns:
        Path to saved screenshot or None on failure
    """
    if not PIL_AVAILABLE:
        print("[Vision] PIL not installed. Run: pip install Pillow")
        return None
    
    try:
        # Capture screenshot
        screenshot = ImageGrab.grab()
        
        # Generate save path if not provided
        if save_path is None:
            screenshots_dir = Path.home() / "Pictures" / "Maya Screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = screenshots_dir / f"screenshot_{timestamp}.png"
        
        # Save screenshot
        screenshot.save(save_path)
        print(f"[Vision] Screenshot saved: {save_path}")
        return str(save_path)
        
    except Exception as e:
        print(f"[Vision] Failed to capture screenshot: {e}")
        return None


def extract_text_from_screen() -> Optional[str]:
    """
    Capture screenshot and extract text using OCR.
    
    Returns:
        Extracted text or None on failure
    """
    if not PIL_AVAILABLE:
        print("[Vision] PIL not installed. Run: pip install Pillow")
        return None
    
    if not TESSERACT_AVAILABLE:
        print("[Vision] pytesseract not installed. Run: pip install pytesseract")
        print("[Vision] Also install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        return None
    
    try:
        # Capture screenshot
        screenshot = ImageGrab.grab()
        
        # Extract text
        text = pytesseract.image_to_string(screenshot)
        
        print(f"[Vision] Extracted {len(text)} characters from screen")
        return text
        
    except Exception as e:
        print(f"[Vision] Failed to extract text: {e}")
        return None


def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Extract text from image file using OCR.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Extracted text or None on failure
    """
    if not PIL_AVAILABLE:
        print("[Vision] PIL not installed. Run: pip install Pillow")
        return None
    
    if not TESSERACT_AVAILABLE:
        print("[Vision] pytesseract not installed. Run: pip install pytesseract")
        return None
    
    try:
        # Open image
        image = Image.open(image_path)
        
        # Extract text
        text = pytesseract.image_to_string(image)
        
        print(f"[Vision] Extracted {len(text)} characters from {image_path}")
        return text
        
    except Exception as e:
        print(f"[Vision] Failed to extract text from image: {e}")
        return None


def describe_screenshot_ai(ai_module) -> Optional[str]:
    """
    Capture screenshot and get AI description.
    
    Args:
        ai_module: AI module with ask_ai function
        
    Returns:
        AI description of screenshot or None on failure
    """
    # Capture screenshot
    screenshot_path = capture_screen()
    if not screenshot_path:
        return None
    
    # Extract text from screenshot
    text = extract_text_from_image(screenshot_path)
    
    if text:
        # Ask AI to describe what's on screen based on OCR text
        prompt = f"""Based on this text extracted from a screenshot, describe what's on the screen:

{text}

Provide a brief, clear description of what application or content is visible."""
        
        description = ai_module.ask_ai(prompt)
        return description
    else:
        return "Screenshot captured but no text could be extracted"


def analyze_screen_content(ai_module) -> str:
    """
    Analyze current screen content and provide insights.
    
    Args:
        ai_module: AI module with ask_ai function
        
    Returns:
        Analysis result
    """
    try:
        # Extract text from screen
        text = extract_text_from_screen()
        
        if not text or len(text.strip()) < 10:
            return "Unable to extract meaningful text from screen"
        
        # Ask AI to analyze
        prompt = f"""Analyze this text from the user's screen and provide helpful insights:

{text[:1000]}  # Limit to first 1000 chars

What is the user looking at? Any important information or actions they should be aware of?"""
        
        analysis = ai_module.ask_ai(prompt)
        return analysis
        
    except Exception as e:
        return f"Failed to analyze screen: {e}"


def capture_region(x: int, y: int, width: int, height: int, save_path: Optional[str] = None) -> Optional[str]:
    """
    Capture specific region of screen.
    
    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of region
        height: Height of region
        save_path: Path to save screenshot
        
    Returns:
        Path to saved screenshot or None on failure
    """
    if not PIL_AVAILABLE:
        print("[Vision] PIL not installed. Run: pip install Pillow")
        return None
    
    try:
        # Capture region
        bbox = (x, y, x + width, y + height)
        screenshot = ImageGrab.grab(bbox=bbox)
        
        # Generate save path if not provided
        if save_path is None:
            screenshots_dir = Path.home() / "Pictures" / "Maya Screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = screenshots_dir / f"region_{timestamp}.png"
        
        # Save screenshot
        screenshot.save(save_path)
        print(f"[Vision] Region captured: {save_path}")
        return str(save_path)
        
    except Exception as e:
        print(f"[Vision] Failed to capture region: {e}")
        return None


def get_screen_info() -> Dict[str, Any]:
    """
    Get information about the screen.
    
    Returns:
        Dictionary with screen information
    """
    if not PIL_AVAILABLE:
        return {"error": "PIL not installed"}
    
    try:
        # Capture screenshot to get dimensions
        screenshot = ImageGrab.grab()
        width, height = screenshot.size
        
        return {
            "width": width,
            "height": height,
            "mode": screenshot.mode,
            "format": "Screenshot"
        }
        
    except Exception as e:
        return {"error": str(e)}
