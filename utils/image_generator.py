# utils/image_generator.py - FIXED VERSION
import os
import logging
import random
import math
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

logger = logging.getLogger(__name__)

class ProfessionalImageGenerator:
    """High Quality 3D Image Generator - FIXED VERSION"""
    
    def __init__(self):
        self.fonts = self._load_fonts()
        self.default_font_size = 36
        self.effect_presets = self._create_effect_presets()
        
        logger.info(f"ProfessionalImageGenerator initialized with {len(self.fonts)} fonts")
    
    def _load_fonts(self) -> List[ImageFont.FreeTypeFont]:
        """Load fonts with size information"""
        fonts = []
        font_dir = "assets/fonts"
        
        if not os.path.exists(font_dir):
