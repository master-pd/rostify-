#!/usr/bin/env python3
"""
Font Manager for Roastify Bot
Manages random font selection and font loading
"""

import os
import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from PIL import ImageFont

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import FONTS, PATHS
except ImportError:
    logger.error("Config module not found")
    sys.exit(1)


class FontManager:
    """Manages fonts and their random selection"""
    
    def __init__(self):
        """Initialize font manager"""
        self.config = FONTS
        self.fonts_dir = PATHS["fonts"]
        
        # Load available fonts
        self.available_fonts = self._load_fonts()
        
        # Font cache
        self.font_cache = {}  # (font_path, size) -> ImageFont
        
        # Track recent usage
        self.recent_fonts = []
        
        logger.info(f"Font Manager initialized with {len(self.available_fonts)} fonts")
    
    def _load_fonts(self) -> List[str]:
        """Load font files from directory"""
        fonts = []
        
        # Check for font files in directory
        if os.path.exists(self.fonts_dir):
            # Get all font files
            font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']
            
            for filename in os.listdir(self.fonts_dir):
                if any(filename.lower().endswith(ext) for ext in font_extensions):
                    font_path = os.path.join(self.fonts_dir, filename)
                    fonts.append(font_path)
        
        # If no fonts found, use system fonts
        if not fonts:
            fonts = self._get_system_fonts()
        
        return fonts
    
    def _get_system_fonts(self) -> List[str]:
        """Get system font paths"""
        system_fonts = []
        
        # Common font paths for different OS
        font_paths = [
            # Windows
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/cour.ttf",
            
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            
            # macOS
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Times.ttc"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                system_fonts.append(font_path)
        
        # If still no fonts, return empty list
        return system_fonts
    
    def get_random_font_path(self) -> Optional[str]:
        """Get a random font file path"""
        if not self.available_fonts:
            logger.warning("No fonts available")
            return None
        
        # Apply repetition avoidance
        no_repeat_until = self.config.get("no_repeat_until", 3)
        
        # Filter out recently used fonts
        available = [f for f in self.available_fonts 
                    if f not in self.recent_fonts[-no_repeat_until:]]
        
        # If all fonts recently used, use any
        if not available:
            available = self.available_fonts
        
        # Select random font
        selected = random.choice(available)
        
        # Update recent fonts
        self.recent_fonts.append(selected)
        if len(self.recent_fonts) > 10:  # Keep last 10
            self.recent_fonts.pop(0)
        
        logger.debug(f"Selected font: {os.path.basename(selected)}")
        return selected
    
    def get_font(self, font_path: str, size: int) -> Optional[ImageFont.FreeTypeFont]:
        """Get ImageFont object from font path and size"""
        try:
            # Check cache first
            cache_key = (font_path, size)
            if cache_key in self.font_cache:
                return self.font_cache[cache_key]
            
            # Load font
            font = ImageFont.truetype(font_path, size)
            
            # Cache it
            self.font_cache[cache_key] = font
            
            return font
            
        except Exception as e:
            logger.error(f"Error loading font {font_path}: {e}")
            
            # Try to use default font
            try:
                return ImageFont.load_default()
            except:
                return None
    
    def get_random_font(self, size: int) -> Optional[ImageFont.FreeTypeFont]:
        """Get random font with specified size"""
        font_path = self.get_random_font_path()
        
        if not font_path:
            return None
        
        return self.get_font(font_path, size)
    
    def get_font_variants(self, base_size: int) -> Dict[str, ImageFont.FreeTypeFont]:
        """Get multiple font sizes from same random font"""
        font_path = self.get_random_font_path()
        
        if not font_path:
            return {}
        
        variants = {
            "large": self.get_font(font_path, int(base_size * 1.5)),
            "medium": self.get_font(font_path, base_size),
            "small": self.get_font(font_path, int(base_size * 0.7)),
            "tiny": self.get_font(font_path, int(base_size * 0.5))
        }
        
        # Remove None values
        return {k: v for k, v in variants.items() if v is not None}
    
    def add_font_file(self, filepath: str) -> bool:
        """Add a new font file"""
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"Font file not found: {filepath}")
                return False
            
            # Copy to fonts directory
            import shutil
            filename = os.path.basename(filepath)
            dest_path = os.path.join(self.fonts_dir, filename)
            
            shutil.copy2(filepath, dest_path)
            
            # Reload fonts
            self.available_fonts = self._load_fonts()
            
            # Clear font cache for this font
            self._clear_font_cache()
            
            logger.info(f"Added new font: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding font file: {e}")
            return False
    
    def remove_font_file(self, filename: str) -> bool:
        """Remove a font file"""
        try:
            font_path = os.path.join(self.fonts_dir, filename)
            
            if not os.path.exists(font_path):
                logger.error(f"Font file not found: {font_path}")
                return False
            
            # Remove file
            os.remove(font_path)
            
            # Remove from available fonts if present
            if font_path in self.available_fonts:
                self.available_fonts.remove(font_path)
            
            # Remove from recent fonts if present
            if font_path in self.recent_fonts:
                self.recent_fonts.remove(font_path)
            
            # Clear font cache for this font
            self._clear_font_cache()
            
            logger.info(f"Removed font: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing font file: {e}")
            return False
    
    def _clear_font_cache(self):
        """Clear font cache"""
        self.font_cache.clear()
        logger.debug("Cleared font cache")
    
    def scan_for_new_fonts(self) -> List[str]:
        """Scan for new font files in directory"""
        old_count = len(self.available_fonts)
        
        # Reload fonts
        self.available_fonts = self._load_fonts()
        
        new_count = len(self.available_fonts)
        
        if new_count > old_count:
            logger.info(f"Found {new_count - old_count} new fonts")
        
        return self.available_fonts
    
    def get_font_stats(self) -> Dict[str, Any]:
        """Get font usage statistics"""
        return {
            "total_fonts": len(self.available_fonts),
            "font_cache_size": len(self.font_cache),
            "recently_used": len(self.recent_fonts),
            "font_files": [os.path.basename(f) for f in self.available_fonts],
            "recent_font_files": [os.path.basename(f) for f in self.recent_fonts[-5:]]
        }
    
    def get_font_info(self, font_path: str) -> Optional[Dict[str, Any]]:
        """Get information about a font"""
        try:
            if not os.path.exists(font_path):
                return None
            
            font = ImageFont.truetype(font_path, 12)  # Load with small size
            
            # Get some metrics
            bbox = font.getbbox("Test")
            
            info = {
                "filename": os.path.basename(font_path),
                "path": font_path,
                "size": os.path.getsize(font_path),
                "metrics": {
                    "ascent": font.getmetrics()[0],
                    "descent": font.getmetrics()[1],
                    "test_width": bbox[2] - bbox[0] if bbox else 0,
                    "test_height": bbox[3] - bbox[1] if bbox else 0
                }
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting font info: {e}")
            return None
    
    def validate_font(self, font_path: str) -> bool:
        """Validate if a font file can be loaded"""
        try:
            # Try to load the font
            font = ImageFont.truetype(font_path, 12)
            
            # Test rendering
            bbox = font.getbbox("Test")
            
            return bbox is not None
            
        except Exception as e:
            logger.error(f"Font validation failed: {e}")
            return False
    
    def create_font_preview(self, font_path: str, output_path: str, 
                           text: str = "Roastify Bot") -> bool:
        """Create a preview image for a font"""
        try:
            from PIL import Image, ImageDraw
            
            # Create preview image
            width, height = 800, 200
            image = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Load font at different sizes
            font_large = self.get_font(font_path, 48)
            font_medium = self.get_font(font_path, 24)
            font_small = self.get_font(font_path, 16)
            
            if not font_large:
                return False
            
            # Draw font name
            font_name = os.path.basename(font_path)
            draw.text((20, 20), font_name, font=font_small, fill=(100, 100, 100))
            
            # Draw sample text at different sizes
            y_offset = 70
            
            # Large text
            draw.text((20, y_offset), text, font=font_large, fill=(0, 0, 0))
            y_offset += 70
            
            # Medium text
            draw.text((20, y_offset), text, font=font_medium, fill=(50, 50, 50))
            y_offset += 40
            
            # Small text with more characters
            sample_text = "রোস্টিফাই বট - বাংলা রোস্টিং!"
            draw.text((20, y_offset), sample_text, font=font_small, fill=(100, 100, 100))
            
            # Save preview
            image.save(output_path, 'PNG', quality=95)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating font preview: {e}")
            return False