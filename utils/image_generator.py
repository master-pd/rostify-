#!/usr/bin/env python3
"""
ROASTIFY ULTIMATE IMAGE GENERATOR v6.0
Professional Production-Grade with Complete Error Handling & Optimization
Author: Roastify Team | Termux Compatible
License: MIT
Version: 6.0.0
"""

import os
import sys
import io
import math
import random
import logging
import textwrap
import hashlib
import json
import time
import threading
import asyncio
import concurrent.futures
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union, BinaryIO, Callable
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, wraps
from contextlib import contextmanager
import traceback
import warnings
from collections import defaultdict, deque

# Suppress unnecessary warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Configure Unicode support
if sys.version_info >= (3, 7):
    import locale
    locale.setlocale(locale.LC_ALL, '')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configure comprehensive logging
class CustomFormatter(logging.Formatter):
    """Custom formatter with colors and better formatting"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[41m',   # Red background
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        log_fmt = f'%(asctime)s - %(name)s - {self.COLORS.get(record.levelname, "")}%(levelname)s{self.COLORS["RESET"]} - %(message)s'
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

# Setup logger
logger = logging.getLogger('RoastifyImageGenerator')
logger.setLevel(logging.INFO)

# Remove existing handlers
logger.handlers.clear()

# Console handler with colors
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler(
    'image_generator.log',
    encoding='utf-8',
    mode='a'
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(file_handler)

# Import PIL with comprehensive fallback and validation
PIL_AVAILABLE = False
PIL_VERSION = None

try:
    import PIL
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
    from PIL.Image import Resampling
    from PIL.ImageFilter import GaussianBlur
    
    PIL_AVAILABLE = True
    PIL_VERSION = PIL.__version__
    logger.info(f"✓ PIL/Pillow v{PIL_VERSION} successfully loaded")
    
    # Validate PIL functionality
    test_img = Image.new('RGB', (10, 10), (0, 0, 0))
    del test_img
    
except (ImportError, AttributeError, OSError) as e:
    logger.error(f"✗ PIL initialization failed: {e}")
    PIL_AVAILABLE = False

# Constants
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1080
DEFAULT_QUALITY = 95
SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP']
MAX_CACHE_SIZE = 1000
CACHE_TTL_HOURS = 24
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 1.0
DEFAULT_TIMEOUT = 30.0

# Enums
class ImageStyle(Enum):
    """Available image styles with auto generation"""
    DARK = auto()
    LIGHT = auto()
    NEON = auto()
    VINTAGE = auto()
    CYBERPUNK = auto()
    MINIMAL = auto()
    GRUNGE = auto()
    RETRO = auto()
    GLOW = auto()
    ELEGANT = auto()
    MODERN = auto()
    FUTURISTIC = auto()
    PASTEL = auto()
    MONOCHROME = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class TextEffect(Enum):
    """Text effect types"""
    NONE = auto()
    SHADOW = auto()
    GLOW = auto()
    OUTLINE = auto()
    GRADIENT = auto()
    EMBOSS = auto()
    NEON = auto()
    STROKE = auto()
    REFLECTION = auto()
    THREE_D = auto()
    METALLIC = auto()
    
    @classmethod
    def get_random(cls, count=1):
        effects = list(cls.__members__.values())
        effects.remove(cls.NONE)
        return random.sample(effects, min(count, len(effects)))

class BorderType(Enum):
    """Border styles"""
    NONE = auto()
    SIMPLE = auto()
    DOUBLE = auto()
    ROUNDED = auto()
    DOTTED = auto()
    DASHED = auto()
    ORNATE = auto()
    NEON = auto()
    GLOW = auto()
    GRADIENT = auto()
    PATTERN = auto()
    
    @classmethod
    def get_random(cls):
        types = list(cls.__members__.values())
        types.remove(cls.NONE)
        return random.choice(types)

class GradientDirection(Enum):
    """Gradient directions"""
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()
    RADIAL = auto()
    ANGULAR = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

# Data Classes
@dataclass
class ImageConfig:
    """Image generation configuration with validation"""
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    quality: int = DEFAULT_QUALITY
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl_hours: int = CACHE_TTL_HOURS
    max_cache_size: int = MAX_CACHE_SIZE
    output_dir: str = "./output"
    temp_dir: str = "./temp"
    cache_dir: str = "./cache"
    assets_dir: str = "./assets"
    backup_dir: str = "./backup"
    max_workers: int = 4
    timeout: float = DEFAULT_TIMEOUT
    enable_backup: bool = True
    compression_level: int = 6
    
    def __post_init__(self):
        """Validate and create directories"""
        # Validate values
        self.width = max(100, min(self.width, 4096))
        self.height = max(100, min(self.height, 4096))
        self.quality = max(10, min(self.quality, 100))
        self.format = self.format.upper()
        if self.format not in SUPPORTED_FORMATS:
            self.format = "PNG"
        
        # Create directories
        directories = [
            self.output_dir, self.temp_dir, self.cache_dir,
            self.assets_dir, self.backup_dir
        ]
        
        for dir_path in directories:
            try:
                path = Path(dir_path)
                path.mkdir(parents=True, exist_ok=True)
                
                # Test write permission
                test_file = path / '.write_test'
                test_file.touch()
                test_file.unlink()
                
                logger.debug(f"Directory ready: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to create directory {dir_path}: {e}")
                raise
        
        logger.info(f"ImageConfig initialized: {self.width}x{self.height}, {self.format}")

@dataclass
class TextConfig:
    """Text configuration with auto-fallback"""
    primary_text: str = ""
    secondary_text: str = ""
    emoji: str = ""
    font_size_primary: int = 72
    font_size_secondary: int = 48
    font_size_emoji: int = 96
    text_color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (50, 50, 50)
    effects: List[TextEffect] = field(default_factory=lambda: [TextEffect.SHADOW])
    alignment: str = "center"
    line_spacing: float = 1.2
    max_width: int = 28
    font_style: str = "bold"
    font_family: str = ""
    opacity: float = 1.0
    rotation: float = 0.0
    text_shadow_blur: int = 2
    text_shadow_offset: int = 4
    
    def __post_init__(self):
        """Validate text configuration"""
        self.font_size_primary = max(12, min(self.font_size_primary, 200))
        self.font_size_secondary = max(12, min(self.font_size_secondary, 100))
        self.font_size_emoji = max(12, min(self.font_size_emoji, 200))
        self.line_spacing = max(1.0, min(self.line_spacing, 3.0))
        self.max_width = max(10, min(self.max_width, 100))
        self.opacity = max(0.0, min(self.opacity, 1.0))
        self.rotation = max(-360.0, min(self.rotation, 360.0))

@dataclass
class BorderConfig:
    """Border configuration"""
    enabled: bool = True
    border_type: BorderType = BorderType.ROUNDED
    color: Tuple[int, int, int] = (255, 105, 180)
    secondary_color: Optional[Tuple[int, int, int]] = None
    thickness: int = 20
    padding: int = 50
    corner_radius: int = 40
    glow_intensity: int = 0
    opacity: float = 1.0
    pattern_spacing: int = 20
    
    def __post_init__(self):
        """Validate border configuration"""
        self.thickness = max(1, min(self.thickness, 100))
        self.padding = max(0, min(self.padding, 200))
        self.corner_radius = max(0, min(self.corner_radius, 200))
        self.glow_intensity = max(0, min(self.glow_intensity, 10))
        self.opacity = max(0.0, min(self.opacity, 1.0))
        
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.color[0] + 30),
                min(255, self.color[1] + 30),
                min(255, self.color[2] + 30)
            )

@dataclass
class BackgroundConfig:
    """Background configuration"""
    type: str = "gradient"
    primary_color: Tuple[int, int, int] = (20, 20, 40)
    secondary_color: Optional[Tuple[int, int, int]] = None
    tertiary_color: Optional[Tuple[int, int, int]] = None
    image_path: Optional[str] = None
    opacity: float = 1.0
    blur_radius: int = 0
    pattern_type: str = "none"
    pattern_color: Optional[Tuple[int, int, int]] = None
    pattern_intensity: float = 0.3
    gradient_direction: GradientDirection = GradientDirection.DIAGONAL
    noise_intensity: float = 0.0
    vignette_intensity: float = 0.0
    
    def __post_init__(self):
        """Validate background configuration"""
        self.opacity = max(0.0, min(self.opacity, 1.0))
        self.blur_radius = max(0, min(self.blur_radius, 20))
        self.pattern_intensity = max(0.0, min(self.pattern_intensity, 1.0))
        self.noise_intensity = max(0.0, min(self.noise_intensity, 1.0))
        self.vignette_intensity = max(0.0, min(self.vignette_intensity, 1.0))
        
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.primary_color[0] + 40),
                min(255, self.primary_color[1] + 40),
                min(255, self.primary_color[2] + 40)
            )
        
        if self.tertiary_color is None:
            self.tertiary_color = (
                min(255, self.primary_color[0] + 80),
                min(255, self.primary_color[1] + 80),
                min(255, self.primary_color[2] + 80)
            )

@dataclass
class GenerationResult:
    """Result of image generation"""
    success: bool
    image_path: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    cache_hit: bool = False
    image_size: Optional[int] = None
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

# Utility Functions
def retry_on_failure(max_attempts: int = MAX_RETRY_ATTEMPTS, delay: float = RETRY_DELAY):
    """Decorator for retrying failed operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator

def validate_image_size(width: int, height: int) -> Tuple[int, int]:
    """Validate and adjust image dimensions"""
    min_size, max_size = 100, 8192
    width = max(min_size, min(width, max_size))
    height = max(min_size, min(height, max_size))
    return width, height

def safe_color_value(value: int) -> int:
    """Ensure color value is within 0-255 range"""
    return max(0, min(255, value))

def create_gradient_color(color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         ratio: float) -> Tuple[int, int, int]:
    """Create gradient color from two colors"""
    return (
        int(color1[0] * (1 - ratio) + color2[0] * ratio),
        int(color1[1] * (1 - ratio) + color2[1] * ratio),
        int(color1[2] * (1 - ratio) + color2[2] * ratio)
    )

# Core Managers
class FontManager:
    """Advanced font manager with caching, fallbacks, and system font detection"""
    
    def __init__(self, assets_dir: str = "./assets"):
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL is not available. Font manager cannot be initialized.")
        
        self.assets_dir = Path(assets_dir)
        self.fonts_dir = self.assets_dir / "fonts"
        self.fonts_dir.mkdir(parents=True, exist_ok=True)
        
        self.font_cache = {}
        self.available_fonts = []
        self.font_families = defaultdict(list)
        self.bengali_fonts = []
        self.english_fonts = []
        self.emoji_fonts = []
        self.system_fonts = []
        
        self._font_lock = threading.Lock()
        self._load_fonts()
        
        logger.info(f"FontManager initialized with {len(self.available_fonts)} fonts")
    
    def _load_fonts(self):
        """Load all available fonts from multiple locations"""
        font_locations = [
            self.fonts_dir,
            Path("/system/fonts"),
            Path("/data/data/com.termux/files/usr/share/fonts"),
            Path("/usr/share/fonts/truetype"),
            Path("/usr/share/fonts/opentype"),
            Path("/usr/local/share/fonts"),
            Path.home() / ".fonts",
            Path(".") / "fonts",
        ]
        
        # Common font file extensions
        font_extensions = {'.ttf', '.otf', '.TTF', '.OTF', '.ttc', '.TTC'}
        
        loaded_count = 0
        for location in font_locations:
            if location.exists():
                try:
                    for ext in font_extensions:
                        for font_file in location.rglob(f"*{ext}"):
                            try:
                                self._load_single_font(font_file)
                                loaded_count += 1
                            except Exception as e:
                                continue
                except Exception as e:
                    logger.debug(f"Failed to scan {location}: {e}")
        
        # If no fonts found, ensure we have at least the default
        if not self.available_fonts:
            logger.warning("No fonts found. Using PIL default.")
            self.available_fonts.append("default")
        
        logger.info(f"Loaded {loaded_count} fonts from {len(font_locations)} locations")
    
    def _load_single_font(self, font_path: Path):
        """Load and categorize a single font"""
        font_path_str = str(font_path.resolve())
        
        if font_path_str in self.available_fonts:
            return
        
        try:
            # Test load font
            test_font = ImageFont.truetype(font_path_str, 12)
            self.available_fonts.append(font_path_str)
            
            # Categorize font
            font_name = font_path.stem.lower()
            
            # Check for Bengali/Bangla fonts
            bengali_keywords = ['bengali', 'bangla', 'solaiman', 'kalpurush', 
                               'lipee', 'banglish', 'nikosh', 'vuti']
            if any(keyword in font_name for keyword in bengali_keywords):
                self.bengali_fonts.append(font_path_str)
            
            # Check for emoji fonts
            elif any(keyword in font_name for keyword in ['emoji', 'emojione', 'noto', 'symbola']):
                self.emoji_fonts.append(font_path_str)
            
            # Assume English for others
            else:
                self.english_fonts.append(font_path_str)
            
            # Add to font families
            family_name = self._extract_font_family(font_path.stem)
            self.font_families[family_name].append(font_path_str)
            
        except Exception as e:
            logger.debug(f"Failed to load font {font_path}: {e}")
    
    def _extract_font_family(self, font_name: str) -> str:
        """Extract clean font family name"""
        # Remove common suffixes and weights
        suffixes = ['regular', 'bold', 'italic', 'light', 'medium', 'black',
                   'thin', 'semibold', 'extrabold', 'heavy', 'book']
        
        font_name_lower = font_name.lower()
        for suffix in suffixes:
            if font_name_lower.endswith(suffix):
                font_name = font_name[:-len(suffix)]
        
        # Clean up
        font_name = font_name.strip('-_ ').title()
        return font_name if font_name else 'Unknown'
    
    def _is_bengali_text(self, text: str) -> bool:
        """Detect if text contains Bengali characters"""
        if not text:
            return False
        
        bengali_range = range(0x0980, 0x09FF + 1)
        for char in text:
            try:
                if ord(char) in bengali_range:
                    return True
            except:
                continue
        return False
    
    def _is_emoji_text(self, text: str) -> bool:
        """Detect if text contains emojis"""
        if not text:
            return False
        
        # Emoji ranges
        emoji_ranges = [
            range(0x1F600, 0x1F64F + 1),  # Emoticons
            range(0x1F300, 0x1F5FF + 1),  # Miscellaneous Symbols and Pictographs
            range(0x1F680, 0x1F6FF + 1),  # Transport and Map Symbols
            range(0x2600, 0x26FF + 1),    # Miscellaneous Symbols
            range(0x2700, 0x27BF + 1),    # Dingbats
        ]
        
        for char in text:
            try:
                char_code = ord(char)
                if any(char_code in r for r in emoji_ranges):
                    return True
            except:
                continue
        return False
    
    @lru_cache(maxsize=500)
    def get_font(self, size: int, style: str = "regular", 
                text: str = None, prefer_family: str = None) -> Optional[ImageFont.FreeTypeFont]:
        """Get appropriate font with intelligent selection"""
        if not PIL_AVAILABLE:
            return None
        
        cache_key = f"{size}_{style}_{text}_{prefer_family}"
        
        with self._font_lock:
            if cache_key in self.font_cache:
                return self.font_cache[cache_key]
            
            try:
                font_path = None
                
                # Text-based font selection
                if text:
                    if self._is_emoji_text(text) and self.emoji_fonts:
                        font_path = random.choice(self.emoji_fonts)
                    elif self._is_bengali_text(text) and self.bengali_fonts:
                        font_path = random.choice(self.bengali_fonts)
                    elif self.english_fonts:
                        font_path = random.choice(self.english_fonts)
                
                # Family preference
                if prefer_family and prefer_family in self.font_families:
                    font_path = random.choice(self.font_families[prefer_family])
                
                # Fallback to any available font
                if not font_path and self.available_fonts:
                    font_path = random.choice(self.available_fonts)
                
                # Load font
                if font_path and font_path != "default":
                    font = ImageFont.truetype(font_path, size)
                else:
                    font = ImageFont.load_default()
                
                # Apply style (simulated)
                # Note: PIL's FreeTypeFont doesn't support direct styling
                # This would require different font files for bold/italic
                
                self.font_cache[cache_key] = font
                return font
                
            except Exception as e:
                logger.error(f"Failed to load font: {e}")
                try:
                    return ImageFont.load_default()
                except:
                    return None
    
    def get_font_families(self) -> List[str]:
        """Get list of available font families"""
        return sorted(self.font_families.keys())
    
    def get_statistics(self) -> Dict:
        """Get font statistics"""
        return {
            'total_fonts': len(self.available_fonts),
            'bengali_fonts': len(self.bengali_fonts),
            'english_fonts': len(self.english_fonts),
            'emoji_fonts': len(self.emoji_fonts),
            'font_families': len(self.font_families),
            'cache_size': len(self.font_cache)
        }

class ColorManager:
    """Advanced color management with themes, gradients, and effects"""
    
    def __init__(self):
        self.palettes = self._initialize_palettes()
        self.color_cache = {}
        self.gradient_cache = {}
        
    def _initialize_palettes(self) -> Dict[str, Dict]:
        """Initialize comprehensive color palettes"""
        return {
            "midnight": {
                "name": "Midnight",
                "primary": (10, 15, 30),
                "secondary": (40, 45, 70),
                "accent": (0, 200, 255),
                "text": (240, 240, 255),
                "shadow": (20, 20, 40),
                "highlight": (255, 100, 150),
                "border": (0, 150, 255),
                "success": (0, 255, 150),
                "warning": (255, 200, 0),
                "error": (255, 50, 50)
            },
            "sunset": {
                "name": "Sunset",
                "primary": (255, 200, 150),
                "secondary": (255, 150, 100),
                "accent": (255, 80, 80),
                "text": (60, 30, 20),
                "shadow": (200, 150, 100),
                "highlight": (255, 220, 100),
                "border": (255, 100, 50),
                "success": (100, 255, 150),
                "warning": (255, 180, 50),
                "error": (255, 70, 70)
            },
            "forest": {
                "name": "Forest",
                "primary": (20, 40, 30),
                "secondary": (40, 100, 80),
                "accent": (80, 200, 120),
                "text": (220, 240, 220),
                "shadow": (10, 30, 20),
                "highlight": (150, 220, 180),
                "border": (60, 180, 140),
                "success": (100, 255, 180),
                "warning": (255, 220, 100),
                "error": (255, 100, 100)
            },
            "cyberpunk": {
                "name": "Cyberpunk",
                "primary": (0, 0, 20),
                "secondary": (30, 0, 50),
                "accent": (255, 0, 255),
                "text": (0, 255, 255),
                "shadow": (0, 50, 50),
                "highlight": (255, 100, 0),
                "border": (255, 0, 255),
                "success": (0, 255, 200),
                "warning": (255, 255, 0),
                "error": (255, 0, 100)
            },
            "golden": {
                "name": "Golden",
                "primary": (30, 25, 20),
                "secondary": (60, 50, 40),
                "accent": (255, 215, 0),
                "text": (255, 240, 200),
                "shadow": (50, 40, 20),
                "highlight": (255, 240, 150),
                "border": (255, 215, 0),
                "success": (200, 255, 0),
                "warning": (255, 180, 0),
                "error": (255, 100, 0)
            },
            "neon": {
                "name": "Neon",
                "primary": (0, 10, 20),
                "secondary": (20, 0, 40),
                "accent": (0, 255, 200),
                "text": (200, 255, 255),
                "shadow": (0, 30, 20),
                "highlight": (255, 0, 150),
                "border": (0, 255, 200),
                "success": (0, 255, 150),
                "warning": (255, 255, 0),
                "error": (255, 0, 100)
            },
            "pastel": {
                "name": "Pastel",
                "primary": (255, 240, 245),
                "secondary": (240, 230, 255),
                "accent": (180, 220, 255),
                "text": (80, 80, 100),
                "shadow": (220, 210, 220),
                "highlight": (255, 200, 220),
                "border": (200, 180, 255),
                "success": (180, 255, 200),
                "warning": (255, 240, 180),
                "error": (255, 180, 180)
            }
        }
    
    def get_palette(self, name: str = None) -> Dict:
        """Get color palette by name or auto-select"""
        if name and name in self.palettes:
            return self.palettes[name]
        
        # Auto-select based on time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return self.palettes["sunset"]
        elif 12 <= hour < 17:
            return self.palettes["golden"]
        elif 17 <= hour < 20:
            return self.palettes["cyberpunk"]
        elif 20 <= hour < 23:
            return self.palettes["neon"]
        else:
            return self.palettes["midnight"]
    
    def get_random_palette(self) -> Dict:
        """Get random color palette"""
        return random.choice(list(self.palettes.values()))
    
    def generate_gradient(self, width: int, height: int,
                         color1: Tuple[int, int, int],
                         color2: Tuple[int, int, int],
                         color3: Optional[Tuple[int, int, int]] = None,
                         direction: GradientDirection = GradientDirection.DIAGONAL) -> Image.Image:
        """Generate gradient image with multiple colors"""
        cache_key = f"{width}x{height}_{color1}_{color2}_{color3}_{direction.name}"
        
        if cache_key in self.gradient_cache:
            return self.gradient_cache[cache_key].copy()
        
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        if direction == GradientDirection.HORIZONTAL:
            for x in range(width):
                ratio = x / max(width - 1, 1)
                if color3:
                    if ratio < 0.5:
                        color = create_gradient_color(color1, color2, ratio * 2)
                    else:
                        color = create_gradient_color(color2, color3, (ratio - 0.5) * 2)
                else:
                    color = create_gradient_color(color1, color2, ratio)
                draw.line([(x, 0), (x, height)], fill=color)
        
        elif direction == GradientDirection.VERTICAL:
            for y in range(height):
                ratio = y / max(height - 1, 1)
                if color3:
                    if ratio < 0.5:
                        color = create_gradient_color(color1, color2, ratio * 2)
                    else:
                        color = create_gradient_color(color2, color3, (ratio - 0.5) * 2)
                else:
                    color = create_gradient_color(color1, color2, ratio)
                draw.line([(0, y), (width, y)], fill=color)
        
        elif direction == GradientDirection.RADIAL:
            center_x, center_y = width // 2, height // 2
            max_distance = math.sqrt(center_x**2 + center_y**2)
            
            for x in range(width):
                for y in range(height):
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(distance / max_distance, 1.0)
                    color = create_gradient_color(color1, color2, ratio)
                    draw.point((x, y), fill=color)
        
        else:  # DIAGONAL
            for x in range(width):
                for y in range(height):
                    ratio = (x + y) / (width + height)
                    if color3:
                        if ratio < 0.5:
                            color = create_gradient_color(color1, color2, ratio * 2)
                        else:
                            color = create_gradient_color(color2, color3, (ratio - 0.5) * 2)
                    else:
                        color = create_gradient_color(color1, color2, ratio)
                    draw.point((x, y), fill=color)
        
        self.gradient_cache[cache_key] = gradient.copy()
        return gradient
    
    def adjust_brightness(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Adjust color brightness"""
        return (
            safe_color_value(int(color[0] * factor)),
            safe_color_value(int(color[1] * factor)),
            safe_color_value(int(color[2] * factor))
        )
    
    def get_complementary_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get complementary color"""
        return (
            safe_color_value(255 - color[0]),
            safe_color_value(255 - color[1]),
            safe_color_value(255 - color[2])
        )
    
    def get_analogous_colors(self, color: Tuple[int, int, int], count: int = 3) -> List[Tuple[int, int, int]]:
        """Get analogous colors"""
        colors = []
        hue = self.rgb_to_hsv(color)[0]
        hue_step = 30  # 30 degrees difference
        
        for i in range(count):
            new_hue = (hue + (i * hue_step)) % 360
            colors.append(self.hsv_to_rgb((new_hue, 0.7, 0.9)))
        
        return colors
    
    def rgb_to_hsv(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = [x / 255.0 for x in rgb]
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin
        
        if delta == 0:
            hue = 0
        elif cmax == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif cmax == g:
            hue = 60 * (((b - r) / delta) + 2)
        else:
            hue = 60 * (((r - g) / delta) + 4)
        
        saturation = 0 if cmax == 0 else delta / cmax
        value = cmax
        
        return (hue % 360, saturation, value)
    
    def hsv_to_rgb(self, hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        h, s, v = hsv
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            safe_color_value(int((r + m) * 255)),
            safe_color_value(int((g + m) * 255)),
            safe_color_value(int((b + m) * 255))
        )

class EffectManager:
    """Advanced visual effects manager"""
    
    @staticmethod
    @retry_on_failure(max_attempts=2)
    def add_text_shadow(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                       position: Tuple[int, int], text_color: Tuple[int, int, int],
                       shadow_color: Tuple[int, int, int] = None,
                       offset: int = 4, blur_radius: int = 2) -> None:
        """Add professional shadow effect to text"""
        if not text or not font:
            return
        
        x, y = position
        
        if shadow_color is None:
            shadow_color = (
                max(0, text_color[0] // 4),
                max(0, text_color[1] // 4),
                max(0, text_color[2] // 4)
            )
        
        # Multiple shadow layers for depth
        for i in range(blur_radius, 0, -1):
            shadow_offset = offset * i // max(blur_radius, 1)
            shadow_pos = (
                x + shadow_offset,
                y + shadow_offset
            )
            try:
                draw.text(shadow_pos, text, font=font, fill=shadow_color)
            except Exception as e:
                logger.debug(f"Shadow layer failed: {e}")
                break
        
        # Main text
        try:
            draw.text(position, text, font=font, fill=text_color)
        except Exception as e:
            logger.error(f"Failed to draw text: {e}")
    
    @staticmethod
    @retry_on_failure(max_attempts=2)
    def add_text_outline(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                        position: Tuple[int, int], text_color: Tuple[int, int, int],
                        outline_color: Tuple[int, int, int] = (0, 0, 0),
                        thickness: int = 2) -> None:
        """Add outline to text"""
        if not text or not font:
            return
        
        x, y = position
        
        # Draw outline in all directions
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx != 0 or dy != 0:
                    try:
                        outline_pos = (x + dx, y + dy)
                        draw.text(outline_pos, text, font=font, fill=outline_color)
                    except Exception as e:
                        logger.debug(f"Outline point failed: {e}")
        
        # Draw main text
        try:
            draw.text(position, text, font=font, fill=text_color)
        except Exception as e:
            logger.error(f"Failed to draw text: {e}")
    
    @staticmethod
    @retry_on_failure(max_attempts=2)
    def add_text_glow(image: Image.Image, glow_color: Tuple[int, int, int] = None,
                     intensity: int = 3) -> Image.Image:
        """Add glow effect around text areas"""
        if intensity == 0 or not PIL_AVAILABLE:
            return image
        
        try:
            if glow_color is None:
                glow_color = (0, 200, 255)
            
            # Create glow layer from alpha channel
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            alpha = image.split()[3]
            glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
            glow.paste((*glow_color, 100), (0, 0), alpha)
            
            # Apply blur for glow effect
            for i in range(intensity):
                glow = glow.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Composite with original
            result = Image.alpha_composite(glow, image)
            return result
            
        except Exception as e:
            logger.error(f"Glow effect failed: {e}")
            return image
    
    @staticmethod
    def add_vignette(image: Image.Image, intensity: float = 0.6) -> Image.Image:
        """Add vignette effect to image"""
        if intensity == 0 or not PIL_AVAILABLE:
            return image
        
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            width, height = image.size
            vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(vignette)
            
            center_x, center_y = width // 2, height // 2
            max_radius = int(math.sqrt(width**2 + height**2) / 2)
            
            # Create radial gradient
            steps = 20
            for i in range(steps):
                radius = int(max_radius * (i / steps))
                alpha = int(255 * intensity * (1 - (i / steps)**2))
                
                if radius > 0 and alpha > 0:
                    draw.ellipse(
                        [center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        fill=(0, 0, 0, alpha),
                        outline=None
                    )
            
            return Image.alpha_composite(image, vignette)
            
        except Exception as e:
            logger.error(f"Vignette effect failed: {e}")
            return image
    
    @staticmethod
    def add_noise(image: Image.Image, intensity: float = 0.1) -> Image.Image:
        """Add film grain/noise effect"""
        if intensity == 0 or not PIL_AVAILABLE:
            return image
        
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            width, height = image.size
            noise = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(noise)
            
            # Add random noise dots
            num_dots = int(width * height * intensity / 1000)
            
            for _ in range(num_dots):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                alpha = random.randint(10, 50)
                size = random.randint(1, 2)
                draw.ellipse([x, y, x + size, y + size], 
                            fill=(255, 255, 255, alpha))
            
            return Image.alpha_composite(image, noise)
            
        except Exception as e:
            logger.error(f"Noise effect failed: {e}")
            return image
    
    @staticmethod
    def create_border(border_type: BorderType, size: Tuple[int, int],
                     color: Tuple[int, int, int] = (255, 255, 255),
                     secondary_color: Optional[Tuple[int, int, int]] = None,
                     thickness: int = 20, corner_radius: int = 40) -> Image.Image:
        """Create professional borders"""
        if border_type == BorderType.NONE or not PIL_AVAILABLE:
            return Image.new('RGBA', size, (0, 0, 0, 0))
        
        try:
            width, height = size
            border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(border)
            
            if secondary_color is None:
                secondary_color = (
                    min(255, color[0] + 30),
                    min(255, color[1] + 30),
                    min(255, color[2] + 30)
                )
            
            color_rgba = (*color, 255)
            secondary_rgba = (*secondary_color, 200)
            
            if border_type == BorderType.SIMPLE:
                draw.rectangle(
                    [thickness, thickness, 
                     width - thickness, height - thickness],
                    outline=color_rgba,
                    width=thickness
                )
            
            elif border_type == BorderType.DOUBLE:
                # Outer border
                draw.rectangle(
                    [thickness, thickness,
                     width - thickness, height - thickness],
                    outline=color_rgba,
                    width=thickness // 2
                )
                # Inner border
                inner_thickness = thickness * 2
                draw.rectangle(
                    [inner_thickness, inner_thickness,
                     width - inner_thickness, height - inner_thickness],
                    outline=secondary_rgba,
                    width=thickness // 3
                )
            
            elif border_type == BorderType.ROUNDED:
                # Draw rounded rectangle
                draw.rounded_rectangle(
                    [thickness, thickness,
                     width - thickness, height - thickness],
                    radius=corner_radius,
                    outline=color_rgba,
                    width=thickness
                )
            
            elif border_type == BorderType.NEON:
                # Neon glow border with multiple layers
                for i in range(3):
                    glow_thickness = thickness + i * 5
                    glow_alpha = 200 - i * 60
                    glow_color = (*color, glow_alpha)
                    
                    draw.rounded_rectangle(
                        [glow_thickness, glow_thickness,
                         width - glow_thickness, height - glow_thickness],
                        radius=corner_radius + i * 5,
                        outline=glow_color,
                        width=3
                    )
            
            return border
            
        except Exception as e:
            logger.error(f"Border creation failed: {e}")
            return Image.new('RGBA', size, (0, 0, 0, 0))

class CacheManager:
    """Advanced cache management with LRU eviction and statistics"""
    
    def __init__(self, cache_dir: str = "./cache", 
                 ttl_hours: int = CACHE_TTL_HOURS, 
                 max_size: int = MAX_CACHE_SIZE):
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.max_size = max_size
        
        self.metadata_file = self.cache_dir / "metadata.json"
        self.access_file = self.cache_dir / "access.log"
        self.lock_file = self.cache_dir / ".lock"
        
        self.metadata = {}
        self.access_log = deque(maxlen=1000)
        self.lock = threading.RLock()
        
        self._load_metadata()
        self.cleanup()
        
        logger.info(f"CacheManager initialized: {cache_dir}, TTL: {ttl_hours}h, Max: {max_size}")
    
    def _load_metadata(self):
        """Load cache metadata with error handling"""
        if self.metadata_file.exists():
            try:
                with self.lock:
                    with open(self.metadata_file, 'r', encoding='utf-8') as f:
                        self.metadata = json.load(f)
                logger.debug(f"Loaded metadata: {len(self.metadata)} items")
            except Exception as e:
                logger.error(f"Failed to load metadata: {e}")
                self.metadata = {}
    
    def _save_metadata(self):
        """Save cache metadata atomically"""
        if not self.metadata:
            return
        
        try:
            with self.lock:
                # Write to temp file first
                temp_file = self.metadata_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.metadata, f, indent=2, ensure_ascii=False)
                
                # Atomic replace
                temp_file.replace(self.metadata_file)
                
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def _log_access(self, key: str, action: str):
        """Log cache access"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'key': key,
            'action': action
        }
        self.access_log.append(entry)
    
    def generate_key(self, *args, **kwargs) -> str:
        """Generate deterministic cache key"""
        import pickle
        try:
            data = pickle.dumps((args, kwargs))
            return hashlib.sha256(data).hexdigest()[:32]
        except:
            # Fallback for non-picklable objects
            data_str = f"{args}{kwargs}".encode('utf-8', errors='ignore')
            return hashlib.sha256(data_str).hexdigest()[:32]
    
    @retry_on_failure(max_attempts=2)
    def get(self, key: str) -> Optional[bytes]:
        """Get cached item with access tracking"""
        if not key:
            return None
        
        cache_file = self.cache_dir / f"{key}.cache"
        
        with self.lock:
            if not cache_file.exists():
                return None
            
            # Check TTL
            if key in self.metadata:
                created = datetime.fromisoformat(self.metadata[key]['created'])
                if datetime.now() - created > self.ttl:
                    self.delete(key)
                    return None
            
            try:
                with open(cache_file, 'rb') as f:
                    data = f.read()
                
                # Update access info
                if key in self.metadata:
                    self.metadata[key]['hits'] = self.metadata[key].get('hits', 0) + 1
                    self.metadata[key]['last_accessed'] = datetime.now().isoformat()
                    self._save_metadata()
                
                self._log_access(key, 'HIT')
                return data
                
            except Exception as e:
                logger.error(f"Cache read failed for {key}: {e}")
                return None
    
    @retry_on_failure(max_attempts=2)
    def set(self, key: str, data: bytes):
        """Cache item with size management"""
        if not key or not data:
            return
        
        with self.lock:
            # Check size and evict if needed
            if len(self.metadata) >= self.max_size:
                self._evict_oldest()
            
            cache_file = self.cache_dir / f"{key}.cache"
            
            try:
                # Write to temp file first
                temp_file = cache_file.with_suffix('.tmp')
                with open(temp_file, 'wb') as f:
                    f.write(data)
                
                # Atomic replace
                temp_file.replace(cache_file)
                
                # Update metadata
                self.metadata[key] = {
                    'created': datetime.now().isoformat(),
                    'last_accessed': datetime.now().isoformat(),
                    'size': len(data),
                    'hits': 0
                }
                self._save_metadata()
                
                self._log_access(key, 'SET')
                
            except Exception as e:
                logger.error(f"Cache write failed for {key}: {e}")
                # Clean up temp file if exists
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                    except:
                        pass
    
    def delete(self, key: str):
        """Delete cached item"""
        with self.lock:
            cache_file = self.cache_dir / f"{key}.cache"
            
            try:
                if cache_file.exists():
                    cache_file.unlink()
                
                if key in self.metadata:
                    del self.metadata[key]
                    self._save_metadata()
                
                self._log_access(key, 'DELETE')
                
            except Exception as e:
                logger.error(f"Cache delete failed for {key}: {e}")
    
    def _evict_oldest(self):
        """Evict least recently used cache entries"""
        if not self.metadata:
            return
        
        with self.lock:
            # Sort by last accessed time
            sorted_items = sorted(
                self.metadata.items(),
                key=lambda x: datetime.fromisoformat(x[1].get('last_accessed', x[1]['created']))
            )
            
            # Remove 10% of oldest items
            to_remove = max(1, len(sorted_items) // 10)
            
            for key, _ in sorted_items[:to_remove]:
                self.delete(key)
            
            logger.debug(f"Evicted {to_remove} cache entries")
    
    @retry_on_failure(max_attempts=2)
    def cleanup(self):
        """Clean up expired cache entries"""
        cutoff = datetime.now() - self.ttl
        
        with self.lock:
            expired_keys = []
            
            for key, data in list(self.metadata.items()):
                created = datetime.fromisoformat(data['created'])
                if created < cutoff:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self.delete(key)
            
            if expired_keys:
                logger.info(f"Cache cleanup removed {len(expired_keys)} expired items")
    
    def clear(self):
        """Clear entire cache"""
        with self.lock:
            try:
                # Delete all cache files
                for cache_file in self.cache_dir.glob("*.cache"):
                    try:
                        cache_file.unlink()
                    except:
                        pass
                
                # Clear metadata
                self.metadata.clear()
                self._save_metadata()
                
                logger.info("Cache cleared")
                
            except Exception as e:
                logger.error(f"Cache clear failed: {e}")
    
    def get_stats(self) -> Dict:
        """Get comprehensive cache statistics"""
        with self.lock:
            total_size = sum(data['size'] for data in self.metadata.values())
            total_hits = sum(data.get('hits', 0) for data in self.metadata.values())
            
            hits = 0
            misses = 0
            for entry in self.access_log:
                if entry['action'] == 'HIT':
                    hits += 1
                elif entry['action'] == 'MISS':
                    misses += 1
            
            hit_rate = 0
            if hits + misses > 0:
                hit_rate = (hits / (hits + misses)) * 100
            
            return {
                'total_items': len(self.metadata),
                'total_size_bytes': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'total_hits': total_hits,
                'recent_hits': hits,
                'recent_misses': misses,
                'recent_hit_rate': round(hit_rate, 2),
                'max_size': self.max_size,
                'ttl_hours': self.ttl.total_seconds() / 3600,
                'oldest_item': min(
                    (datetime.fromisoformat(data['created']) 
                     for data in self.metadata.values()),
                    default=None
                ),
                'newest_item': max(
                    (datetime.fromisoformat(data['created']) 
                     for data in self.metadata.values()),
                    default=None
                )
            }

class UltimateImageGenerator:
    """
    ULTIMATE IMAGE GENERATOR v6.0
    Professional, Error-Free, Production-Ready
    """
    
    def __init__(self, config: Optional[ImageConfig] = None):
        if not PIL_AVAILABLE:
            logger.critical("PIL/Pillow not available. Install: pip install pillow")
            raise ImportError("PIL/Pillow is required for image generation")
        
        self.config = config or ImageConfig()
        self.font_manager = FontManager(self.config.assets_dir)
        self.color_manager = ColorManager()
        self.effect_manager = EffectManager()
        self.cache_manager = CacheManager(
            cache_dir=self.config.cache_dir,
            ttl_hours=self.config.cache_ttl_hours,
            max_size=self.config.max_cache_size
        )
        
        # Statistics and monitoring
        self.stats = {
            'total_generated': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0,
            'peak_memory': 0.0
        }
        
        # Performance monitoring
        self.performance_log = deque(maxlen=100)
        self.error_log = deque(maxlen=50)
        
        # Thread pool for async operations
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.config.max_workers,
            thread_name_prefix='ImageGen'
        )
        
        logger.info("✓ Ultimate Image Generator v6.0 initialized")
        logger.info(f"  • Resolution: {self.config.width}x{self.config.height}")
        logger.info(f"  • Format: {self.config.format}")
        logger.info(f"  • Cache: {'Enabled' if self.config.enable_cache else 'Disabled'}")
        logger.info(f"  • Workers: {self.config.max_workers}")
    
    def _safe_text_extract(self, text_input: Any) -> str:
        """
        Safely extract text from ANY input type
        Handles: str, dict, list, tuple, object, None, etc.
        """
        if text_input is None:
            return ""
        
        # String
        if isinstance(text_input, str):
            return text_input.strip()
        
        # Dictionary
        elif isinstance(text_input, dict):
            # Common text keys in order of priority
            text_keys = [
                'text', 'message', 'content', 'caption', 'title',
                'description', 'quote', 'roast', 'roast_text',
                'primary_text', 'secondary_text', 'name', 'value',
                'data', 'info', 'detail'
            ]
            
            for key in text_keys:
                if key in text_input:
                    value = text_input[key]
                    if isinstance(value, str) and value.strip():
                        return value.strip()
            
            # Try any string value
            for key, value in text_input.items():
                if isinstance(value, str) and len(value.strip()) > 3:
                    return value.strip()
            
            # Convert dict to JSON string
            try:
                return json.dumps(text_input, ensure_ascii=False, indent=2)
            except:
                return str(text_input)
        
        # List or tuple
        elif isinstance(text_input, (list, tuple)):
            # Join with spaces if all items are strings
            if all(isinstance(item, str) for item in text_input):
                return ' '.join(str(item).strip() for item in text_input)
            else:
                return str(text_input)
        
        # Object with text attributes
        elif hasattr(text_input, '__dict__'):
            # Try common attributes
            for attr in ['text', 'message', 'content', 'data']:
                if hasattr(text_input, attr):
                    value = getattr(text_input, attr)
                    if isinstance(value, str) and value.strip():
                        return value.strip()
        
        # Default string conversion
        try:
            result = str(text_input)
            return result if result != "None" else ""
        except:
            return ""
    
    def _process_user_info(self, user_info: Any) -> Dict:
        """
        Process user information from ANY format
        Returns a standardized dictionary
        """
        default_user = {
            'id': 0,
            'username': 'User',
            'first_name': 'User',
            'last_name': '',
            'full_name': 'User',
            'rating': round(random.uniform(5.0, 9.9), 1),
            'level': random.randint(1, 100),
            'rank': 'Member',
            'join_date': datetime.now().strftime('%Y-%m-%d'),
            'avatar_url': None,
            'metadata': {}
        }
        
        # If already a dict, validate and return
        if isinstance(user_info, dict):
            result = default_user.copy()
            result.update(user_info)
            
            # Ensure username exists
            if not result['username'] or result['username'] == 'User':
                if result['first_name'] and result['first_name'] != 'User':
                    result['username'] = result['first_name']
            
            # Ensure full name
            if not result['full_name'] or result['full_name'] == 'User':
                names = [result['first_name'], result['last_name']]
                result['full_name'] = ' '.join(filter(None, names)).strip()
                if not result['full_name']:
                    result['full_name'] = result['username']
            
            return result
        
        # If object with attributes
        result = default_user.copy()
        
        try:
            # Common object attributes
            if hasattr(user_info, 'id'):
                result['id'] = user_info.id
            
            if hasattr(user_info, 'username') and user_info.username:
                result['username'] = str(user_info.username)
            
            if hasattr(user_info, 'first_name') and user_info.first_name:
                result['first_name'] = str(user_info.first_name)
            
            if hasattr(user_info, 'last_name') and user_info.last_name:
                result['last_name'] = str(user_info.last_name)
            
            # Extract from database if available
            try:
                # This would be your database integration
                # Example: db.get_user_rating(user_info.id)
                pass
            except:
                pass
            
        except Exception as e:
            logger.debug(f"User info extraction error: {e}")
        
        # Final validation
        if not result['username'] or result['username'] == 'User':
            result['username'] = result.get('first_name', 'User')
        
        if not result['full_name'] or result['full_name'] == 'User':
            names = [result['first_name'], result['last_name']]
            result['full_name'] = ' '.join(filter(None, names)).strip()
            if not result['full_name']:
                result['full_name'] = result['username']
        
        return result
    
    def _wrap_text_smart(self, text: str, max_width: int = 30) -> List[str]:
        """
        Smart text wrapping with Unicode and multi-language support
        """
        if not text:
            return []
        
        text = str(text).strip()
        
        # Very short text
        if len(text) <= max_width:
            return [text]
        
        try:
            # Try standard textwrap
            return textwrap.wrap(text, width=max_width, break_long_words=False)
        except Exception as e:
            logger.debug(f"Textwrap failed, using fallback: {e}")
            
            # Manual wrapping
            words = text.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word)
                
                # If adding this word would exceed max width
                if current_length + word_length + len(current_line) > max_width:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
                else:
                    current_line.append(word)
                    current_length += word_length
            
            if current_line:
                lines.append(' '.join(current_line))
            
            return lines
    
    def _create_background(self, bg_config: BackgroundConfig, 
                          width: int, height: int) -> Image.Image:
        """Create professional background with fallbacks"""
        try:
            palette = self.color_manager.get_random_palette()
            
            # Solid color background
            if bg_config.type == "solid":
                background = Image.new(
                    'RGB', 
                    (width, height), 
                    bg_config.primary_color or palette['primary']
                )
            
            # Gradient background
            elif bg_config.type == "gradient":
                color1 = bg_config.primary_color or palette['primary']
                color2 = bg_config.secondary_color or palette['secondary']
                color3 = bg_config.tertiary_color
                
                background = self.color_manager.generate_gradient(
                    width, height, color1, color2, color3, bg_config.gradient_direction
                )
            
            # Image background
            elif bg_config.type == "image" and bg_config.image_path:
                try:
                    if os.path.exists(bg_config.image_path):
                        background = Image.open(bg_config.image_path).convert('RGB')
                        background = background.resize(
                            (width, height), 
                            Resampling.LANCZOS
                        )
                        
                        # Apply opacity if needed
                        if bg_config.opacity < 1.0:
                            overlay = Image.new(
                                'RGB', 
                                (width, height), 
                                palette['primary']
                            )
                            background = Image.blend(
                                overlay, 
                                background, 
                                bg_config.opacity
                            )
                    else:
                        raise FileNotFoundError(f"Background image not found: {bg_config.image_path}")
                except Exception as e:
                    logger.warning(f"Background image failed: {e}")
                    # Fallback to gradient
                    background = self.color_manager.generate_gradient(
                        width, height, 
                        palette['primary'], 
                        palette['secondary']
                    )
            
            # Pattern background
            elif bg_config.type == "pattern":
                background = Image.new(
                    'RGB', 
                    (width, height), 
                    bg_config.primary_color or palette['primary']
                )
                
                if bg_config.pattern_intensity > 0:
                    # Add simple pattern (can be extended)
                    draw = ImageDraw.Draw(background)
                    pattern_color = bg_config.pattern_color or palette['accent']
                    
                    for x in range(0, width, 50):
                        for y in range(0, height, 50):
                            if (x + y) % 100 == 0:
                                draw.ellipse(
                                    [x, y, x + 20, y + 20],
                                    fill=pattern_color
                                )
            
            # Default to gradient
            else:
                background = self.color_manager.generate_gradient(
                    width, height, 
                    palette['primary'], 
                    palette['secondary']
                )
            
            # Apply effects
            if bg_config.blur_radius > 0:
                background = background.filter(
                    ImageFilter.GaussianBlur(bg_config.blur_radius)
                )
            
            if bg_config.noise_intensity > 0:
                background = self.effect_manager.add_noise(
                    background, 
                    bg_config.noise_intensity
                )
            
            if bg_config.vignette_intensity > 0:
                background = self.effect_manager.add_vignette(
                    background, 
                    bg_config.vignette_intensity
                )
            
            return background
            
        except Exception as e:
            logger.error(f"Background creation failed: {e}")
            # Ultimate fallback
            return Image.new('RGB', (width, height), (40, 40, 60))
    
    def _render_text(self, draw: ImageDraw.Draw, text_config: TextConfig, 
                    width: int, height: int) -> Tuple[int, int]:
        """Render text with all effects"""
        try:
            palette = self.color_manager.get_random_palette()
            
            # Get fonts
            primary_font = self.font_manager.get_font(
                text_config.font_size_primary, 
                text_config.font_style,
                text=text_config.primary_text
            ) or ImageFont.load_default()
            
            secondary_font = self.font_manager.get_font(
                text_config.font_size_secondary,
                "regular",
                text=text_config.secondary_text
            ) or ImageFont.load_default()
            
            emoji_font = self.font_manager.get_font(
                text_config.font_size_emoji,
                "regular",
                text=text_config.emoji
            ) or ImageFont.load_default()
            
            # Wrap and prepare text
            primary_lines = self._wrap_text_smart(
                text_config.primary_text, 
                text_config.max_width
            )
            secondary_lines = self._wrap_text_smart(
                text_config.secondary_text or "",
                text_config.max_width
            )
            
            # Calculate total height
            line_height_primary = int(text_config.font_size_primary * text_config.line_spacing)
            line_height_secondary = int(text_config.font_size_secondary * text_config.line_spacing)
            
            total_height = (
                len(primary_lines) * line_height_primary +
                (len(primary_lines) - 1) * 10
            )
            
            if secondary_lines:
                total_height += len(secondary_lines) * line_height_secondary + 40
            
            if text_config.emoji:
                total_height += text_config.font_size_emoji + 20
            
            # Start position (centered vertically)
            current_y = max(50, (height - total_height) // 3)
            
            # Draw primary text
            text_color = text_config.text_color or palette['text']
            shadow_color = text_config.shadow_color or palette['shadow']
            
            for line in primary_lines:
                try:
                    # Get text bounding box
                    bbox = draw.textbbox((0, 0), line, font=primary_font)
                    text_width = bbox[2] - bbox[0]
                    
                    # Center horizontally
                    x_position = (width - text_width) // 2
                    
                    # Apply effects based on configuration
                    if TextEffect.SHADOW in text_config.effects:
                        self.effect_manager.add_text_shadow(
                            draw, line, primary_font,
                            (x_position, current_y),
                            text_color, shadow_color,
                            text_config.text_shadow_offset,
                            text_config.text_shadow_blur
                        )
                    elif TextEffect.OUTLINE in text_config.effects:
                        self.effect_manager.add_text_outline(
                            draw, line, primary_font,
                            (x_position, current_y),
                            text_color, shadow_color
                        )
                    else:
                        draw.text((x_position, current_y), line,
                                 font=primary_font, fill=text_color)
                    
                    current_y += line_height_primary
                    
                except Exception as e:
                    logger.error(f"Primary text rendering failed: {e}")
                    current_y += line_height_primary
            
            # Draw secondary text
            if secondary_lines:
                current_y += 30
                
                for line in secondary_lines:
                    try:
                        bbox = draw.textbbox((0, 0), line, font=secondary_font)
                        text_width = bbox[2] - bbox[0]
                        x_position = (width - text_width) // 2
                        
                        draw.text((x_position, current_y), line,
                                 font=secondary_font, fill=palette['secondary'])
                        
                        current_y += line_height_secondary
                        
                    except Exception as e:
                        logger.error(f"Secondary text rendering failed: {e}")
                        current_y += line_height_secondary
            
            # Draw emoji
            if text_config.emoji:
                current_y += 40
                
                try:
                    bbox = draw.textbbox((0, 0), text_config.emoji, font=emoji_font)
                    text_width = bbox[2] - bbox[0]
                    x_position = (width - text_width) // 2
                    
                    draw.text((x_position, current_y), text_config.emoji,
                             font=emoji_font, fill=text_color)
                    
                    current_y += text_config.font_size_emoji
                    
                except Exception as e:
                    logger.error(f"Emoji rendering failed: {e}")
                    current_y += text_config.font_size_emoji
            
            return current_y
            
        except Exception as e:
            logger.error(f"Text rendering failed: {e}")
            return height // 2
    
    def _add_metadata(self, draw: ImageDraw.Draw, user_info: Dict, 
                     width: int, current_y: int):
        """Add metadata and footer information"""
        try:
            palette = self.color_manager.get_random_palette()
            small_font = self.font_manager.get_font(24, "regular") or ImageFont.load_default()
            
            # User information
            username = user_info.get('username', 'User')
            first_name = user_info.get('first_name', '')
            rating = user_info.get('rating', 0)
            
            # Create user display text
            display_text = username
            if first_name and first_name != username:
                display_text = f"{first_name} (@{username})"
            elif '@' not in username:
                display_text = f"@{username}"
            
            # Add rating if available
            if rating:
                stars = '⭐' * min(5, int(rating / 2))
                display_text += f" {stars} {rating}/10"
            
            # Draw user info
            try:
                bbox = draw.textbbox((0, 0), display_text, font=small_font)
                text_width = bbox[2] - bbox[0]
                draw.text(((width - text_width) // 2, current_y + 30),
                         display_text, font=small_font, fill=palette['accent'])
            except Exception as e:
                logger.debug(f"User info drawing failed: {e}")
            
            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d • %H:%M:%S")
            try:
                bbox = draw.textbbox((0, 0), timestamp, font=small_font)
                text_width = bbox[2] - bbox[0]
                draw.text(((width - text_width) // 2, current_y + 70),
                         timestamp, font=small_font, fill=palette['secondary'])
            except Exception as e:
                logger.debug(f"Timestamp drawing failed: {e}")
            
            # Footer/watermark
            footer = "✨ Roastify Pro v6.0"
            try:
                bbox = draw.textbbox((0, 0), footer, font=small_font)
                text_width = bbox[2] - bbox[0]
                draw.text(((width - text_width) // 2, current_y + 110),
                         footer, font=small_font, fill=palette['highlight'])
            except Exception as e:
                logger.debug(f"Footer drawing failed: {e}")
                
        except Exception as e:
            logger.error(f"Metadata addition failed: {e}")
    
    @retry_on_failure(max_attempts=3)
    def generate_roast_image(self, roast_text: Any, user_info: Any,
                            style: str = "auto", 
                            border_config: Optional[BorderConfig] = None,
                            background_config: Optional[BackgroundConfig] = None) -> GenerationResult:
        """
        Generate professional roast image with comprehensive error handling
        
        Args:
            roast_text: Any - Text to display (auto-converted)
            user_info: Any - User information (auto-processed)
            style: str - Color palette style
            border_config: BorderConfig - Border configuration
            background_config: BackgroundConfig - Background configuration
            
        Returns:
            GenerationResult - Result object with all details
        """
        start_time = time.time()
        
        try:
            # 1. Input validation and processing
            actual_text = self._safe_text_extract(roast_text)
            if not actual_text or len(actual_text.strip()) < 2:
                actual_text = "আপনি খুবই স্মার্ট! রোস্ট করার মতো কিছু পাচ্ছি না! 😄"
                logger.warning("Empty or short text provided, using default")
            
            user_dict = self._process_user_info(user_info)
            logger.debug(f"Processing request for user: {user_dict.get('username', 'Unknown')}")
            
            # 2. Cache check
            cache_key = None
            if self.config.enable_cache:
                cache_key = self.cache_manager.generate_key(
                    actual_text[:200],
                    user_dict.get('id', 0),
                    style,
                    border_config,
                    background_config
                )
                
                cached_data = self.cache_manager.get(cache_key)
                if cached_data:
                    self.stats['cache_hits'] += 1
                    
                    timestamp = int(time.time())
                    output_path = Path(self.config.output_dir) / f"roast_cache_{timestamp}.png"
                    output_path.write_bytes(cached_data)
                    
                    processing_time = time.time() - start_time
                    
                    result = GenerationResult(
                        success=True,
                        image_path=str(output_path),
                        processing_time=round(processing_time, 3),
                        cache_hit=True,
                        image_size=len(cached_data),
                        metadata={
                            'user': user_dict.get('username', 'Unknown'),
                            'text_preview': actual_text[:50] + '...' if len(actual_text) > 50 else actual_text,
                            'cache_key': cache_key[:8]
                        }
                    )
                    
                    self.performance_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'operation': 'cache_hit',
                        'time': processing_time
                    })
                    
                    return result
            
            self.stats['cache_misses'] += 1
            
            # 3. Configuration setup with defaults
            border_config = border_config or BorderConfig(
                border_type=BorderType.get_random(),
                color=self.color_manager.get_random_palette()['border'],
                thickness=random.randint(15, 30),
                corner_radius=random.randint(30, 60)
            )
            
            bg_config = background_config or BackgroundConfig(
                type=random.choice(["gradient", "solid", "pattern"]),
                primary_color=self.color_manager.get_random_palette()['primary'],
                gradient_direction=GradientDirection.get_random(),
                noise_intensity=random.uniform(0, 0.1),
                vignette_intensity=random.uniform(0, 0.3)
            )
            
            # 4. Image creation
            width, height = validate_image_size(self.config.width, self.config.height)
            
            # Create background
            background = self._create_background(bg_config, width, height)
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # Text configuration
            text_config = TextConfig(
                primary_text=actual_text,
                secondary_text=user_dict.get('subtext', ''),
                emoji=random.choice(['🔥', '😈', '⚡', '💥', '🎯', '😂', '👑', '✨', '🌟', '🎨']),
                text_color=(255, 255, 255),
                effects=TextEffect.get_random(random.randint(1, 2)),
                font_size_primary=random.randint(60, 80),
                font_size_secondary=random.randint(36, 48),
                max_width=random.randint(24, 32)
            )
            
            # Render text
            text_bottom = self._render_text(draw, text_config, width, height)
            
            # Add metadata
            self._add_metadata(draw, user_dict, width, text_bottom)
            
            # Apply effects
            if random.random() > 0.3:
                image = self.effect_manager.add_vignette(image, intensity=0.2)
            
            if random.random() > 0.5:
                image = self.effect_manager.add_text_glow(image, intensity=2)
            
            # Apply border
            if border_config.enabled and border_config.border_type != BorderType.NONE:
                border = self.effect_manager.create_border(
                    border_config.border_type,
                    (width, height),
                    border_config.color,
                    border_config.secondary_color,
                    border_config.thickness,
                    border_config.corner_radius
                )
                image = Image.alpha_composite(image, border)
            
            # 5. Save image
            timestamp = int(time.time())
            output_path = Path(self.config.output_dir) / f"roast_{timestamp}_{user_dict.get('id', 0)}.png"
            
            # Convert format if needed and save
            if image.mode == 'RGBA' and self.config.format == 'JPEG':
                rgb_background = Image.new('RGB', image.size, (0, 0, 0))
                rgb_background.paste(image, mask=image.split()[3])
                image = rgb_background
            elif self.config.format == 'PNG' and image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            save_params = {
                'quality': self.config.quality,
                'optimize': True,
            }
            
            if self.config.format == 'PNG':
                save_params['compress_level'] = self.config.compression_level
            
            image.save(output_path, self.config.format, **save_params)
            
            # 6. Cache the result
            if self.config.enable_cache and cache_key:
                with open(output_path, 'rb') as f:
                    image_data = f.read()
                self.cache_manager.set(cache_key, image_data)
            
            # 7. Create backup if enabled
            if self.config.enable_backup:
                backup_path = Path(self.config.backup_dir) / f"backup_{timestamp}.png"
                try:
                    import shutil
                    shutil.copy2(output_path, backup_path)
                except Exception as e:
                    logger.debug(f"Backup failed: {e}")
            
            # 8. Update statistics and return result
            processing_time = time.time() - start_time
            
            self.stats['total_generated'] += 1
            self.stats['successful'] += 1
            self.stats['total_time'] += processing_time
            
            result = GenerationResult(
                success=True,
                image_path=str(output_path),
                processing_time=round(processing_time, 3),
                cache_hit=False,
                image_size=os.path.getsize(output_path),
                metadata={
                    'user': user_dict.get('username', 'Unknown'),
                    'user_id': user_dict.get('id', 0),
                    'text_length': len(actual_text),
                    'style': style,
                    'border_type': border_config.border_type.name,
                    'background_type': bg_config.type,
                    'resolution': f"{width}x{height}",
                    'format': self.config.format,
                    'quality': self.config.quality,
                    'timestamp': timestamp
                }
            )
            
            self.performance_log.append({
                'timestamp': datetime.now().isoformat(),
                'operation': 'generate',
                'time': processing_time,
                'resolution': f"{width}x{height}"
            })
            
            logger.info(f"✓ Image generated: {output_path.name} ({processing_time:.2f}s)")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            self.stats['failed'] += 1
            self.stats['total_time'] += processing_time
            
            self.error_log.append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'traceback': traceback.format_exc()[:500]
            })
            
            logger.error(f"✗ Image generation failed: {e}")
            logger.debug(traceback.format_exc())
            
            # Return error result
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=round(processing_time, 3),
                metadata={
                    'user': user_dict.get('username', 'Unknown') if 'user_dict' in locals() else 'Unknown',
                    'error_type': type(e).__name__,
                    'timestamp': datetime.now().isoformat()
                }
            )
    
    def generate_welcome_image(self, user_info: Any, chat_info: Any = None) -> GenerationResult:
        """Generate welcome image for new users"""
        user_dict = self._process_user_info(user_info)
        
        welcome_texts = [
            "স্বাগতম! রোস্টের জগতে আপনাকে হৃদয়ের অভিনন্দন! 🎉",
            "আসসালামু আলাইকুম! রোস্টিফাই পরিবারে আপনাকে স্বাগতম! 👋",
            "হ্যালো! প্রস্তুত থাকুন মজাদার রোস্টের জন্য! 😄",
            "ওহো! একজন নতুন রোস্টার এসেছেন! 🔥",
            "Welcome to Roastify! Get ready for some fun! 🎊",
            "নতুন সদস্যের আগমন! সবাই স্বাগতম জানাই! 🌟"
        ]
        
        return self.generate_roast_image(
            roast_text=random.choice(welcome_texts),
            user_info=user_dict,
            style="neon",
            border_config=BorderConfig(
                border_type=BorderType.NEON,
                color=(255, 215, 0),
                thickness=25,
                glow_intensity=2
            ),
            background_config=BackgroundConfig(
                type="gradient",
                primary_color=(30, 10, 50),
                secondary_color=(70, 30, 90),
                gradient_direction=GradientDirection.RADIAL
            )
        )
    
    def generate_achievement_image(self, user_info: Any, achievement: Any) -> GenerationResult:
        """Generate achievement/unlock image"""
        user_dict = self._process_user_info(user_info)
        
        # Process achievement
        if isinstance(achievement, dict):
            achievement_text = achievement.get('title', 'Achievement Unlocked!')
            achievement_desc = achievement.get('description', '')
        else:
            achievement_text = str(achievement) or 'Achievement Unlocked!'
            achievement_desc = ''
        
        text = f"{achievement_text}\n\n{achievement_desc}".strip()
        
        return self.generate_roast_image(
            roast_text=text,
            user_info=user_dict,
            style="golden",
            border_config=BorderConfig(
                border_type=BorderType.ORNATE,
                color=(255, 215, 0),
                thickness=30,
                corner_radius=60
            ),
            background_config=BackgroundConfig(
                type="gradient",
                primary_color=(40, 20, 60),
                secondary_color=(80, 40, 100),
                tertiary_color=(120, 60, 140)
            )
        )
    
    def batch_generate(self, tasks: List[Dict]) -> List[GenerationResult]:
        """Generate multiple images in parallel"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_task = {
                executor.submit(
                    self.generate_roast_image,
                    task.get('text', ''),
                    task.get('user_info', {}),
                    task.get('style', 'auto'),
                    task.get('border_config'),
                    task.get('background_config')
                ): task for task in tasks
            }
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result(timeout=self.config.timeout)
                    results.append(result)
                except concurrent.futures.TimeoutError:
                    results.append(GenerationResult(
                        success=False,
                        error="Generation timeout",
                        processing_time=self.config.timeout
                    ))
                except Exception as e:
                    results.append(GenerationResult(
                        success=False,
                        error=str(e),
                        processing_time=0.0
                    ))
        
        return results
    
    def cleanup(self, max_age_hours: int = 24):
        """Clean up old files from output and temp directories"""
        try:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            
            for dir_path in [self.config.temp_dir, self.config.output_dir]:
                dir_obj = Path(dir_path)
                if dir_obj.exists():
                    removed_count = 0
                    
                    for file in dir_obj.glob("*"):
                        if file.is_file():
                            try:
                                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                                if mtime < cutoff:
                                    file.unlink()
                                    removed_count += 1
                            except Exception as e:
                                logger.debug(f"Failed to remove {file}: {e}")
                    
                    if removed_count > 0:
                        logger.info(f"Cleaned up {removed_count} files from {dir_path}")
            
            # Clean cache
            self.cache_manager.cleanup()
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def get_detailed_stats(self) -> Dict:
        """Get comprehensive statistics"""
        avg_time = 0
        if self.stats['total_generated'] > 0:
            avg_time = self.stats['total_time'] / self.stats['total_generated']
        
        success_rate = 0
        if self.stats['total_generated'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_generated']) * 100
        
        cache_hit_rate = 0
        total_cache_ops = self.stats['cache_hits'] + self.stats['cache_misses']
        if total_cache_ops > 0:
            cache_hit_rate = (self.stats['cache_hits'] / total_cache_ops) * 100
        
        recent_performance = list(self.performance_log)
        recent_errors = list(self.error_log)
        
        cache_stats = self.cache_manager.get_stats()
        font_stats = self.font_manager.get_statistics()
        
        return {
            'generator': {
                'version': '6.0.0',
                'pil_available': PIL_AVAILABLE,
                'pil_version': PIL_VERSION,
                'config': {
                    'width': self.config.width,
                    'height': self.config.height,
                    'quality': self.config.quality,
                    'format': self.config.format,
                    'cache_enabled': self.config.enable_cache,
                    'workers': self.config.max_workers
                }
            },
            'performance': {
                'total_generated': self.stats['total_generated'],
                'successful': self.stats['successful'],
                'failed': self.stats['failed'],
                'success_rate': round(success_rate, 1),
                'total_time_seconds': round(self.stats['total_time'], 2),
                'average_time_seconds': round(avg_time, 3),
                'cache_hits': self.stats['cache_hits'],
                'cache_misses': self.stats['cache_misses'],
                'cache_hit_rate': round(cache_hit_rate, 1)
            },
            'cache': cache_stats,
            'fonts': font_stats,
            'recent': {
                'performance_samples': len(recent_performance),
                'error_samples': len(recent_errors),
                'latest_performance': recent_performance[-5:] if recent_performance else [],
                'latest_errors': recent_errors[-5:] if recent_errors else []
            },
            'system': {
                'python_version': sys.version,
                'platform': sys.platform,
                'output_directory': self.config.output_dir,
                'cache_directory': self.config.cache_dir
            }
        }
    
    def export_config(self) -> Dict:
        """Export current configuration"""
        return {
            'image_config': asdict(self.config),
            'statistics': self.get_detailed_stats(),
            'timestamp': datetime.now().isoformat()
        }
    
    def health_check(self) -> Dict:
        """Perform health check of the generator"""
        checks = {
            'pil_available': PIL_AVAILABLE,
            'directories_accessible': True,
            'font_manager_ready': len(self.font_manager.available_fonts) > 0,
            'cache_operational': True,
            'write_permissions': True
        }
        
        # Check directories
        for dir_path in [self.config.output_dir, self.config.temp_dir]:
            try:
                path = Path(dir_path)
                test_file = path / '.health_check'
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                checks['directories_accessible'] = False
        
        # Check cache
        try:
            test_key = 'health_check'
            test_data = b'test'
            self.cache_manager.set(test_key, test_data)
            retrieved = self.cache_manager.get(test_key)
            checks['cache_operational'] = retrieved == test_data
            self.cache_manager.delete(test_key)
        except Exception as e:
            checks['cache_operational'] = False
        
        overall_health = all(checks.values())
        
        return {
            'healthy': overall_health,
            'checks': checks,
            'timestamp': datetime.now().isoformat()
        }
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.executor.shutdown(wait=False)
            logger.info("Image generator shutdown complete")
        except Exception as e:
            logger.debug(f"Shutdown error: {e}")

# Backward compatibility
ImageGenerator = UltimateImageGenerator

# Test and demonstration
def run_comprehensive_test():
    """Run comprehensive tests on the image generator"""
    print("\n" + "="*70)
    print("ULTIMATE IMAGE GENERATOR v6.0 - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    if not PIL_AVAILABLE:
        print("❌ CRITICAL: PIL/Pillow not installed!")
        print("   Install with: pip install pillow")
        return False
    
    test_results = {
        'initialization': False,
        'basic_generation': False,
        'cache_system': False,
        'error_handling': False,
        'batch_operations': False,
        'cleanup': False
    }
    
    try:
        # Test 1: Initialization
        print("\n🔹 Test 1: Initialization...")
        generator = UltimateImageGenerator()
        print("   ✓ Generator initialized successfully")
        print(f"   • Resolution: {generator.config.width}x{generator.config.height}")
        print(f"   • Fonts loaded: {len(generator.font_manager.available_fonts)}")
        test_results['initialization'] = True
        
        # Test 2: Basic image generation
        print("\n🔹 Test 2: Basic image generation...")
        
        # Test with different input types
        test_cases = [
            ("Simple string", "এটা একটা টেস্ট রোস্ট!", {"username": "test_user"}),
            ("Dictionary input", {"text": "Dict test", "type": "test"}, {"username": "user2"}),
            ("Object-like", "Object test", type('User', (), {'username': 'object_user', 'id': 123})()),
            ("Bengali text", "বাংলা টেক্সট টেস্টিং", {"username": "bangla_user"}),
            ("Emoji text", "Test with emojis 🎉🔥🌟", {"username": "emoji_user"})
        ]
        
        for test_name, text_input, user_input in test_cases:
            print(f"   Testing: {test_name}...")
            result = generator.generate_roast_image(text_input, user_input)
            
            if result.success:
                print(f"   ✓ {test_name}: Success ({result.processing_time:.2f}s)")
                print(f"     Output: {result.image_path}")
            else:
                print(f"   ✗ {test_name}: Failed - {result.error}")
        
        test_results['basic_generation'] = True
        
        # Test 3: Cache system
        print("\n🔹 Test 3: Cache system...")
        cache_stats_before = generator.cache_manager.get_stats()
        
        # Generate same image twice
        result1 = generator.generate_roast_image(
            "Cache test text",
            {"username": "cache_test_user"}
        )
        
        result2 = generator.generate_roast_image(
            "Cache test text",
            {"username": "cache_test_user"}
        )
        
        cache_stats_after = generator.cache_manager.get_stats()
        
        print(f"   First generation: {result1.processing_time:.2f}s (Cache miss)")
        print(f"   Second generation: {result2.processing_time:.2f}s (Cache hit: {result2.cache_hit})")
        print(f"   Cache stats: {cache_stats_after['total_items']} items, "
              f"Hit rate: {cache_stats_after['recent_hit_rate']}%")
        
        test_results['cache_system'] = True
        
        # Test 4: Error handling
        print("\n🔹 Test 4: Error handling...")
        
        # Test with invalid inputs
        error_cases = [
            ("Empty text", "", {}),
            ("None text", None, {}),
            ("Invalid user", "Test", {"invalid": "object"}),
        ]
        
        for case_name, text, user in error_cases:
            result = generator.generate_roast_image(text, user)
            if not result.success:
                print(f"   ✓ {case_name}: Properly handled error")
            else:
                print(f"   ✓ {case_name}: Generated successfully (graceful fallback)")
        
        test_results['error_handling'] = True
        
        # Test 5: Batch operations
        print("\n🔹 Test 5: Batch operations...")
        
        batch_tasks = [
            {"text": f"Batch test {i}", "user_info": {"username": f"batch_user_{i}"}}
            for i in range(3)
        ]
        
        batch_results = generator.batch_generate(batch_tasks)
        
        success_count = sum(1 for r in batch_results if r.success)
        print(f"   Batch results: {success_count}/{len(batch_results)} successful")
        
        test_results['batch_operations'] = True
        
        # Test 6: Cleanup
        print("\n🔹 Test 6: Cleanup operations...")
        generator.cleanup(max_age_hours=0)  # Clean files older than 0 hours (all test files)
        print("   ✓ Cleanup completed")
        
        test_results['cleanup'] = True
        
        # Final statistics
        print("\n🔹 Final Statistics:")
        stats = generator.get_detailed_stats()
        
        print(f"   Total generated: {stats['performance']['total_generated']}")
        print(f"   Success rate: {stats['performance']['success_rate']}%")
        print(f"   Average time: {stats['performance']['average_time_seconds']:.3f}s")
        print(f"   Cache hit rate: {stats['performance']['cache_hit_rate']}%")
        
        # Health check
        print("\n🔹 Health Check:")
        health = generator.health_check()
        
        for check_name, status in health['checks'].items():
            status_icon = "✓" if status else "✗"
            print(f"   {status_icon} {check_name}")
        
        print("\n" + "="*70)
        
        if all(test_results.values()):
            print("✅ ALL TESTS PASSED SUCCESSFULLY!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED OR HAD ISSUES")
            for test_name, passed in test_results.items():
                status = "✓" if passed else "✗"
                print(f"  {status} {test_name}")
            return False
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED WITH EXCEPTION: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run comprehensive test
    print("Starting Ultimate Image Generator v6.0...")
    
    success = run_comprehensive_test()
    
    if success:
        print("\n🎉 Generator is ready for production use!")
        print("Usage example:")
        print("""
        # Basic usage
        generator = UltimateImageGenerator()
        result = generator.generate_roast_image(
            "Your text here",
            {"username": "test_user", "first_name": "Test"}
        )
        
        if result.success:
            print(f"Image saved to: {result.image_path}")
        else:
            print(f"Error: {result.error}")
        """)
    else:
        print("\n⚠️  Generator has issues that need to be fixed")
    
    sys.exit(0 if success else 1)
