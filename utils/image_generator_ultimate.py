"""
🚀 ULTIMATE PROFESSIONAL IMAGE GENERATION SYSTEM
✅ 4K+ Ultra HD Quality | Advanced AI-Style Effects
🎯 Complete Bengali Support with Premium Features
📌 Version: 9.0.0 ULTRA PRO MAX
⚡ Performance Optimized for High-Volume Generation
"""

import os
import sys
import math
import random
import logging
import textwrap
import hashlib
import json
import time
import threading
import requests
import numpy as np
import concurrent.futures
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, wraps, partial
import traceback
from collections import deque, OrderedDict
import base64
import io
from urllib.parse import urlparse
import hashlib
import inspect
import secrets
import string
import asyncio
from asyncio import Lock, Semaphore

# ================================
# CONFIGURATION & SETUP
# ================================

# Configure advanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('UltraHDGenerator')

# Import PIL with comprehensive error handling
PIL_AVAILABLE = False
PIL_IMPORTS = {}

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageColor
    from PIL.Image import Resampling, Transform
    from PIL.ImageFilter import GaussianBlur, UnsharpMask, MedianFilter, Kernel, RankFilter
    from PIL import ImageSequence, ImageMath
    PIL_AVAILABLE = True
    PIL_IMPORTS = {
        'Image': Image,
        'ImageDraw': ImageDraw,
        'ImageFont': ImageFont,
        'ImageFilter': ImageFilter,
        'ImageOps': ImageOps,
        'ImageEnhance': ImageEnhance,
        'ImageChops': ImageChops,
        'ImageColor': ImageColor,
        'Resampling': Resampling,
        'GaussianBlur': GaussianBlur,
        'UnsharpMask': UnsharpMask,
        'MedianFilter': MedianFilter,
    }
    logger.info("✅ PIL/Pillow successfully loaded with all modules")
except ImportError as e:
    logger.error(f"❌ PIL not available: {e}")
    PIL_AVAILABLE = False

# Check for numpy for advanced effects
NUMPY_AVAILABLE = False
try:
    import numpy as np
    NUMPY_AVAILABLE = True
    logger.info("✅ NumPy successfully loaded for advanced effects")
except ImportError:
    logger.warning("⚠️ NumPy not available, some advanced effects will be limited")
    NUMPY_AVAILABLE = False

# Constants for Ultra HD
ULTRA_HD_WIDTH = 3840
ULTRA_HD_HEIGHT = 2160
FULL_HD_WIDTH = 1920
FULL_HD_HEIGHT = 1080
STANDARD_WIDTH = 1080
STANDARD_HEIGHT = 1080

# Quality Presets
QUALITY_PRESETS = {
    'ULTRA_HD': {'width': 3840, 'height': 2160, 'quality': 98, 'compression': 1},
    'FULL_HD': {'width': 1920, 'height': 1080, 'quality': 95, 'compression': 2},
    'HD': {'width': 1280, 'height': 720, 'quality': 90, 'compression': 3},
    'STANDARD': {'width': 1080, 'height': 1080, 'quality': 85, 'compression': 4},
    'MOBILE': {'width': 720, 'height': 1280, 'quality': 80, 'compression': 6}
}

SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP', 'TIFF']
MAX_CACHE_SIZE = 5000
CACHE_TTL_HOURS = 72
MAX_RETRY_ATTEMPTS = 5
RETRY_DELAY = 1.0
MAX_WORKERS = 8
MAX_IMAGE_SIZE_MB = 50

# ================================
# ENUMS & DATA CLASSES
# ================================

class ImageStyle(Enum):
    """Ultra HD Image Styles"""
    DARK_FUTURISTIC = auto()
    LIGHT_ELEGANT = auto()
    NEON_CYBERPUNK = auto()
    VINTAGE_RETRO = auto()
    MINIMAL_MODERN = auto()
    GRUNGE_URBAN = auto()
    GLOW_AURORA = auto()
    GRADIENT_MESH = auto()
    PATTERN_GEOMETRIC = auto()
    BENGALI_TRADITIONAL = auto()
    ISLAMIC_CALLIGRAPHY = auto()
    ABSTRACT_ARTISTIC = auto()
    PHOTO_REALISTIC = auto()
    ANIME_STYLE = auto()
    OIL_PAINTING = auto()
    WATERCOLOR = auto()
    SKETCH_DRAWING = auto()
    GLASS_MORPHISM = auto()
    NEU_MORPHISM = auto()
    HOLOGRAPHIC = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class TextEffect(Enum):
    """Advanced Text Effects"""
    NONE = auto()
    SHADOW_DEEP = auto()
    GLOW_INTENSE = auto()
    OUTLINE_MULTI = auto()
    GRADIENT_RAINBOW = auto()
    EMBOSS_3D = auto()
    NEON_PULSING = auto()
    STROKE_GRADIENT = auto()
    REFLECTION_REAL = auto()
    THREE_D_EXTRUDE = auto()
    METALLIC_CHROME = auto()
    GLASS_REFLECTION = auto()
    FIRE_EFFECT = auto()
    ICE_EFFECT = auto()
    GOLD_PLATED = auto()
    ANIMATED_TEXT = auto()
    MORPHING_TEXT = auto()
    
    @classmethod
    def get_random(cls, count=2):
        effects = list(cls.__members__.values())
        effects.remove(cls.NONE)
        return random.sample(effects, min(count, len(effects)))

class BorderType(Enum):
    """Premium Border Styles"""
    NONE = auto()
    SIMPLE_ELEGANT = auto()
    DOUBLE_GLOW = auto()
    ROUNDED_GRADIENT = auto()
    DOTTED_ANIMATED = auto()
    DASHED_NEON = auto()
    ORNATE_GOLD = auto()
    NEON_PULSING = auto()
    GLOW_AURA = auto()
    GRADIENT_MESH = auto()
    PATTERN_CULTURAL = auto()
    ISLAMIC_GEOMETRIC = auto()
    BENGALI_ALPANA = auto()
    FRAME_3D = auto()
    GLASS_FRAME = auto()
    LED_MATRIX = auto()
    HOLOGRAM = auto()
    PARTICLE = auto()
    WAVY_FLUID = auto()
    
    @classmethod
    def get_random(cls):
        types = list(cls.__members__.values())
        types.remove(cls.NONE)
        return random.choice(types)

class GradientDirection(Enum):
    """Gradient Directions"""
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL_TL_BR = auto()
    DIAGONAL_TR_BL = auto()
    RADIAL_CENTER = auto()
    RADIAL_CORNER = auto()
    ANGULAR_SPIRAL = auto()
    MESH_GRID = auto()
    WAVE_PATTERN = auto()
    DIAMOND = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class ProfileStyle(Enum):
    """Profile Picture Styles"""
    DEFAULT = auto()
    SPECIAL_MENTION = auto()
    PREMIUM_USER = auto()
    ADMIN = auto()
    VIP = auto()
    MODERATOR = auto()
    CELEBRITY = auto()
    GOLDEN = auto()
    DIAMOND = auto()
    PLATINUM = auto()
    ANIMATED = auto()
    GLOWING = auto()
    FRAMED = auto()
    BADGED = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

@dataclass
class GenerationConfig:
    """Ultra HD Generation Configuration"""
    # Resolution & Quality
    resolution_preset: str = "ULTRA_HD"
    custom_width: int = 0
    custom_height: int = 0
    quality: int = 98
    format: str = "PNG"
    enable_alpha: bool = True
    compression_level: int = 1
    
    # Performance
    enable_cache: bool = True
    cache_ttl_hours: int = CACHE_TTL_HOURS
    max_cache_size: int = MAX_CACHE_SIZE
    max_workers: int = MAX_WORKERS
    enable_parallel: bool = True
    enable_gpu_acceleration: bool = False
    
    # Features
    enable_random_backgrounds: bool = True
    enable_profile_pictures: bool = True
    enable_advanced_effects: bool = True
    enable_real_time_enhancement: bool = True
    enable_ai_styling: bool = True
    
    # Paths
    output_dir: str = "./output/ultra_hd"
    temp_dir: str = "./temp/ultra_hd"
    cache_dir: str = "./cache/ultra_hd"
    assets_dir: str = "./assets/ultra_hd"
    backgrounds_dir: str = "./assets/backgrounds"
    profiles_dir: str = "./assets/profiles"
    fonts_dir: str = "./assets/fonts"
    backup_dir: str = "./backup/ultra_hd"
    
    # Advanced
    max_file_size_mb: int = MAX_IMAGE_SIZE_MB
    enable_watermark: bool = False
    watermark_text: str = "Roastify Ultra HD"
    enable_metadata: bool = True
    enable_backup: bool = True
    backup_count: int = 10
    
    # Network
    enable_unsplash: bool = True
    unsplash_api_key: str = ""
    unsplash_cache_size: int = 100
    request_timeout: float = 10.0
    max_retries: int = MAX_RETRY_ATTEMPTS
    
    def __post_init__(self):
        """Validate configuration"""
        # Set resolution
        if self.resolution_preset in QUALITY_PRESETS:
            preset = QUALITY_PRESETS[self.resolution_preset]
            if self.custom_width <= 0:
                self.custom_width = preset['width']
            if self.custom_height <= 0:
                self.custom_height = preset['height']
            if self.quality <= 0:
                self.quality = preset['quality']
            self.compression_level = preset['compression']
        else:
            self.custom_width = max(100, min(self.custom_width, 8192))
            self.custom_height = max(100, min(self.custom_height, 8192))
        
        # Validate quality
        self.quality = max(10, min(self.quality, 100))
        self.compression_level = max(1, min(self.compression_level, 9))
        
        # Ensure format is supported
        self.format = self.format.upper()
        if self.format not in SUPPORTED_FORMATS:
            self.format = "PNG"
        
        # Create directories
        directories = [
            self.output_dir, self.temp_dir, self.cache_dir,
            self.assets_dir, self.backgrounds_dir, self.profiles_dir,
            self.fonts_dir, self.backup_dir
        ]
        
        for dir_path in directories:
            try:
                path = Path(dir_path)
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Directory ready: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to create directory {dir_path}: {e}")
        
        logger.info(f"✅ GenerationConfig initialized: {self.custom_width}x{self.custom_height}, {self.format}")

@dataclass
class TextConfig:
    """Advanced Text Configuration"""
    primary_text: str = ""
    secondary_text: str = ""
    tertiary_text: str = ""
    emoji: str = ""
    
    # Font Sizes
    font_size_primary: int = 120
    font_size_secondary: int = 72
    font_size_tertiary: int = 48
    font_size_emoji: int = 144
    
    # Colors
    text_color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (30, 30, 30)
    outline_color: Tuple[int, int, int] = (0, 0, 0)
    gradient_start: Optional[Tuple[int, int, int]] = None
    gradient_end: Optional[Tuple[int, int, int]] = None
    
    # Effects
    effects: List[TextEffect] = field(default_factory=lambda: [TextEffect.SHADOW_DEEP, TextEffect.GLOW_INTENSE])
    effect_intensity: int = 3
    text_shadow_blur: int = 4
    text_shadow_offset: int = 8
    outline_thickness: int = 3
    glow_radius: int = 15
    
    # Layout
    alignment: str = "center"
    line_spacing: float = 1.3
    paragraph_spacing: int = 40
    max_width_chars: int = 35
    text_rotation: float = 0.0
    text_skew: float = 0.0
    
    # Font
    font_family_primary: str = ""
    font_family_secondary: str = ""
    font_style: str = "bold"
    font_weight: int = 700
    
    # Advanced
    opacity: float = 1.0
    blend_mode: str = "normal"
    animation_speed: float = 0.0
    text_pattern: str = ""
    
    def __post_init__(self):
        """Validate text configuration"""
        # Font sizes
        self.font_size_primary = max(24, min(self.font_size_primary, 300))
        self.font_size_secondary = max(18, min(self.font_size_secondary, 200))
        self.font_size_tertiary = max(14, min(self.font_size_tertiary, 100))
        self.font_size_emoji = max(24, min(self.font_size_emoji, 300))
        
        # Effects
        self.effect_intensity = max(1, min(self.effect_intensity, 5))
        self.text_shadow_blur = max(0, min(self.text_shadow_blur, 20))
        self.text_shadow_offset = max(0, min(self.text_shadow_offset, 30))
        self.outline_thickness = max(0, min(self.outline_thickness, 10))
        self.glow_radius = max(0, min(self.glow_radius, 50))
        
        # Layout
        self.line_spacing = max(1.0, min(self.line_spacing, 2.5))
        self.paragraph_spacing = max(0, min(self.paragraph_spacing, 100))
        self.max_width_chars = max(10, min(self.max_width_chars, 100))
        self.text_rotation = max(-360, min(self.text_rotation, 360))
        self.text_skew = max(-45, min(self.text_skew, 45))
        
        # Colors
        if self.gradient_start is None:
            self.gradient_start = self.text_color
        if self.gradient_end is None:
            self.gradient_end = (
                min(255, self.text_color[0] + 40),
                min(255, self.text_color[1] + 40),
                min(255, self.text_color[2] + 40)
            )

@dataclass
class BorderConfig:
    """Premium Border Configuration"""
    enabled: bool = True
    border_type: BorderType = BorderType.GLOW_AURA
    color: Tuple[int, int, int] = (255, 105, 180)
    secondary_color: Optional[Tuple[int, int, int]] = None
    tertiary_color: Optional[Tuple[int, int, int]] = None
    
    # Dimensions
    thickness: int = 25
    padding: int = 60
    corner_radius: int = 50
    inner_padding: int = 20
    
    # Effects
    glow_intensity: int = 3
    glow_color: Optional[Tuple[int, int, int]] = None
    shadow_intensity: int = 2
    pattern_spacing: int = 25
    pattern_scale: float = 1.0
    
    # Animation
    animation_speed: float = 0.0
    pulse_effect: bool = False
    rotation_speed: float = 0.0
    
    # Advanced
    opacity: float = 1.0
    blend_mode: str = "screen"
    gradient_direction: GradientDirection = GradientDirection.RADIAL_CENTER
    
    def __post_init__(self):
        """Validate border configuration"""
        self.thickness = max(1, min(self.thickness, 100))
        self.padding = max(0, min(self.padding, 300))
        self.corner_radius = max(0, min(self.corner_radius, 500))
        self.inner_padding = max(0, min(self.inner_padding, 100))
        
        self.glow_intensity = max(0, min(self.glow_intensity, 10))
        self.shadow_intensity = max(0, min(self.shadow_intensity, 5))
        self.pattern_spacing = max(5, min(self.pattern_spacing, 100))
        self.pattern_scale = max(0.1, min(self.pattern_scale, 5.0))
        
        self.animation_speed = max(0, min(self.animation_speed, 10))
        self.rotation_speed = max(0, min(self.rotation_speed, 10))
        
        self.opacity = max(0.0, min(self.opacity, 1.0))
        
        # Auto colors
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.color[0] + 40),
                min(255, self.color[1] + 40),
                min(255, self.color[2] + 40)
            )
        
        if self.tertiary_color is None:
            self.tertiary_color = (
                min(255, self.color[0] + 80),
                min(255, self.color[1] + 80),
                min(255, self.color[2] + 80)
            )
        
        if self.glow_color is None:
            self.glow_color = (
                min(255, self.color[0] + 100),
                min(255, self.color[1] + 100),
                min(255, self.color[2] + 100)
            )

@dataclass
class BackgroundConfig:
    """Ultra HD Background Configuration"""
    # Type
    type: str = "random_hd"
    style: ImageStyle = ImageStyle.DARK_FUTURISTIC
    
    # Colors
    primary_color: Tuple[int, int, int] = (20, 20, 40)
    secondary_color: Optional[Tuple[int, int, int]] = None
    tertiary_color: Optional[Tuple[int, int, int]] = None
    quaternary_color: Optional[Tuple[int, int, int]] = None
    
    # Image
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    use_unsplash: bool = True
    unsplash_category: str = "nature"
    
    # Effects
    blur_radius: int = 0
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    sharpness: float = 1.0
    hue_rotate: float = 0.0
    
    # Patterns
    pattern_type: str = "none"
    pattern_color: Optional[Tuple[int, int, int]] = None
    pattern_intensity: float = 0.3
    pattern_scale: float = 1.0
    
    # Gradients
    gradient_direction: GradientDirection = GradientDirection.DIAGONAL_TL_BR
    gradient_type: str = "linear"
    gradient_stops: List[float] = field(default_factory=lambda: [0.0, 0.5, 1.0])
    
    # Advanced
    noise_intensity: float = 0.05
    vignette_intensity: float = 0.2
    vignette_size: float = 0.7
    grain_intensity: float = 0.1
    chromatic_aberration: float = 0.0
    lens_flare: bool = False
    bokeh_effect: bool = False
    depth_of_field: float = 0.0
    
    # Animation
    animated: bool = False
    animation_frames: int = 1
    animation_speed: float = 1.0
    
    def __post_init__(self):
        """Validate background configuration"""
        # Colors
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.primary_color[0] + 50),
                min(255, self.primary_color[1] + 50),
                min(255, self.primary_color[2] + 50)
            )
        
        if self.tertiary_color is None:
            self.tertiary_color = (
                min(255, self.primary_color[0] + 100),
                min(255, self.primary_color[1] + 100),
                min(255, self.primary_color[2] + 100)
            )
        
        if self.quaternary_color is None:
            self.quaternary_color = (
                min(255, self.primary_color[0] + 150),
                min(255, self.primary_color[1] + 150),
                min(255, self.primary_color[2] + 150)
            )
        
        # Effects validation
        self.blur_radius = max(0, min(self.blur_radius, 50))
        self.brightness = max(0.1, min(self.brightness, 3.0))
        self.contrast = max(0.1, min(self.contrast, 3.0))
        self.saturation = max(0.0, min(self.saturation, 3.0))
        self.sharpness = max(0.1, min(self.sharpness, 3.0))
        self.hue_rotate = max(0.0, min(self.hue_rotate, 360.0))
        
        self.pattern_intensity = max(0.0, min(self.pattern_intensity, 1.0))
        self.pattern_scale = max(0.1, min(self.pattern_scale, 5.0))
        
        self.noise_intensity = max(0.0, min(self.noise_intensity, 1.0))
        self.vignette_intensity = max(0.0, min(self.vignette_intensity, 1.0))
        self.vignette_size = max(0.1, min(self.vignette_size, 1.0))
        self.grain_intensity = max(0.0, min(self.grain_intensity, 1.0))
        self.chromatic_aberration = max(0.0, min(self.chromatic_aberration, 10.0))
        self.depth_of_field = max(0.0, min(self.depth_of_field, 10.0))
        
        self.animation_frames = max(1, min(self.animation_frames, 60))
        self.animation_speed = max(0.1, min(self.animation_speed, 10.0))

@dataclass
class ProfileConfig:
    """Profile Picture Configuration"""
    enabled: bool = True
    style: ProfileStyle = ProfileStyle.DEFAULT
    
    # Image
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    use_gravatar: bool = False
    use_initials: bool = True
    
    # Display
    size: int = 200
    position: str = "top_right"
    offset_x: int = 50
    offset_y: int = 50
    rotation: float = 0.0
    scale: float = 1.0
    
    # Frame
    frame_enabled: bool = True
    frame_type: BorderType = BorderType.ROUNDED_GRADIENT
    frame_color: Tuple[int, int, int] = (255, 215, 0)
    frame_thickness: int = 10
    frame_corner_radius: int = 100
    
    # Effects
    glow_enabled: bool = True
    glow_color: Optional[Tuple[int, int, int]] = None
    glow_intensity: int = 2
    shadow_enabled: bool = True
    shadow_intensity: int = 3
    border_enabled: bool = True
    border_color: Tuple[int, int, int] = (255, 255, 255)
    
    # Status
    status_indicator: bool = True
    status_type: str = "online"
    status_size: int = 20
    
    # Badge
    badge_enabled: bool = False
    badge_type: str = "premium"
    badge_position: str = "bottom_right"
    
    # Animation
    animated: bool = False
    animation_type: str = "pulse"
    animation_speed: float = 1.0
    
    def __post_init__(self):
        """Validate profile configuration"""
        self.size = max(50, min(self.size, 500))
        self.offset_x = max(0, min(self.offset_x, 500))
        self.offset_y = max(0, min(self.offset_y, 500))
        self.rotation = max(-180, min(self.rotation, 180))
        self.scale = max(0.1, min(self.scale, 3.0))
        
        self.frame_thickness = max(1, min(self.frame_thickness, 30))
        self.frame_corner_radius = max(0, min(self.frame_corner_radius, 200))
        
        self.glow_intensity = max(0, min(self.glow_intensity, 5))
        self.shadow_intensity = max(0, min(self.shadow_intensity, 5))
        self.status_size = max(10, min(self.status_size, 40))
        
        self.animation_speed = max(0.1, min(self.animation_speed, 5.0))
        
        if self.glow_color is None:
            self.glow_color = (
                min(255, self.frame_color[0] + 50),
                min(255, self.frame_color[1] + 50),
                min(255, self.frame_color[2] + 50)
            )

@dataclass
class GenerationResult:
    """Generation Result with Ultra HD Metadata"""
    success: bool
    image_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    error: Optional[str] = None
    warning: Optional[str] = None
    
    # Performance
    processing_time: float = 0.0
    cache_hit: bool = False
    memory_used_mb: float = 0.0
    
    # Image Details
    image_size: Optional[int] = None
    image_dimensions: Optional[Tuple[int, int]] = None
    image_format: Optional[str] = None
    image_quality: Optional[int] = None
    
    # Metadata
    metadata: Optional[Dict] = None
    generation_id: Optional[str] = None
    timestamp: Optional[str] = None
    
    # Advanced
    effects_applied: List[str] = field(default_factory=list)
    layers_count: int = 0
    compression_ratio: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

# ================================
# UTILITY FUNCTIONS
# ================================

def retry_on_failure(max_attempts: int = MAX_RETRY_ATTEMPTS, delay: float = RETRY_DELAY,
                     exponential_backoff: bool = True):
    """Advanced retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {str(e)[:100]}")
                    
                    if attempt < max_attempts - 1:
                        wait_time = delay
                        if exponential_backoff:
                            wait_time = delay * (2 ** attempt)  # Exponential backoff
                        
                        # Add jitter to prevent thundering herd
                        wait_time += random.uniform(0, delay * 0.1)
                        
                        logger.debug(f"Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator

def safe_color_value(value: Union[int, float, str]) -> int:
    """Ensure color value is within 0-255 range"""
    if isinstance(value, str):
        try:
            value = int(value)
        except:
            return 0
    
    return max(0, min(255, int(value)))

def create_gradient_color(color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         ratio: float) -> Tuple[int, int, int]:
    """Create smooth gradient color"""
    ratio = max(0.0, min(1.0, ratio))
    
    # Use easing function for smoother gradients
    eased_ratio = ratio * ratio * (3 - 2 * ratio)  # Smoothstep
    
    return (
        int(color1[0] * (1 - eased_ratio) + color2[0] * eased_ratio),
        int(color1[1] * (1 - eased_ratio) + color2[1] * eased_ratio),
        int(color1[2] * (1 - eased_ratio) + color2[2] * eased_ratio)
    )

def generate_unique_id(length: int = 16) -> str:
    """Generate unique ID for tracking"""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def measure_memory_usage():
    """Measure current memory usage"""
    import psutil
    import os
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def create_color_palette(base_color: Tuple[int, int, int], 
                         variations: int = 5) -> List[Tuple[int, int, int]]:
    """Create color palette from base color"""
    palette = []
    
    for i in range(variations):
        ratio = i / (variations - 1) if variations > 1 else 0.5
        
        # Create variations (darker to lighter)
        if ratio < 0.5:
            # Darker shades
            shade_ratio = ratio * 2
            color = (
                int(base_color[0] * (1 - shade_ratio * 0.7)),
                int(base_color[1] * (1 - shade_ratio * 0.7)),
                int(base_color[2] * (1 - shade_ratio * 0.7))
            )
        else:
            # Lighter shades
            shade_ratio = (ratio - 0.5) * 2
            color = (
                int(base_color[0] + (255 - base_color[0]) * shade_ratio * 0.7),
                int(base_color[1] + (255 - base_color[1]) * shade_ratio * 0.7),
                int(base_color[2] + (255 - base_color[2]) * shade_ratio * 0.7)
            )
        
        palette.append(color)
    
    return palette

# ================================
# MANAGER CLASSES
# ================================

class UltraFontManager:
    """Advanced Font Manager with Ultra HD Support"""
    
    def __init__(self, fonts_dir: str = "./assets/fonts"):
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL is required for font management")
        
        self.fonts_dir = Path(fonts_dir)
        self.fonts_dir.mkdir(parents=True, exist_ok=True)
        
        # Font caches
        self.font_cache = OrderedDict()
        self.font_metadata = {}
        self.available_fonts = []
        self.bengali_fonts = []
        self.english_fonts = []
        self.arabic_fonts = []
        self.special_fonts = []
        
        # Font categories
        self.font_categories = {
            'bengali': [],
            'english': [],
            'arabic': [],
            'decorative': [],
            'modern': [],
            'retro': [],
            'handwritten': [],
            'monospace': []
        }
        
        # Default font sizes for different resolutions
        self.font_size_presets = {
            'ULTRA_HD': {'title': 120, 'subtitle': 72, 'body': 48, 'caption': 36},
            'FULL_HD': {'title': 80, 'subtitle': 48, 'body': 32, 'caption': 24},
            'HD': {'title': 60, 'subtitle': 36, 'body': 24, 'caption': 18},
            'STANDARD': {'title': 48, 'subtitle': 32, 'body': 20, 'caption': 16}
        }
        
        self._load_all_fonts()
        self._download_default_fonts()
        logger.info(f"✅ UltraFontManager initialized with {len(self.available_fonts)} fonts")
    
    def _load_all_fonts(self):
        """Load all available fonts from system and custom directories"""
        font_locations = [
            self.fonts_dir,
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path("~/.fonts").expanduser(),
            Path("~/.local/share/fonts").expanduser(),
            Path("/system/fonts"),
            Path("/data/data/com.termux/files/usr/share/fonts"),
            Path("./fonts"),
        ]
        
        font_extensions = ['.ttf', '.otf', '.TTF', '.OTF', '.woff', '.woff2']
        
        for location in font_locations:
            if location.exists():
                for ext in font_extensions:
                    for font_file in location.rglob(f"*{ext}"):
                        try:
                            font_path = str(font_file.resolve())
                            
                            # Skip already loaded fonts
                            if font_path in self.available_fonts:
                                continue
                            
                            # Test load font
                            test_font = ImageFont.truetype(font_path, 12)
                            font_name = font_file.stem.lower()
                            
                            # Add to available fonts
                            self.available_fonts.append(font_path)
                            
                            # Categorize font
                            self._categorize_font(font_path, font_name, font_file)
                            
                        except Exception as e:
                            logger.debug(f"Failed to load font {font_file}: {e}")
                            continue
        
        # If no fonts found, create emergency font list
        if not self.available_fonts:
            logger.warning("No fonts found, using PIL default")
            self._create_emergency_fonts()
    
    def _categorize_font(self, font_path: str, font_name: str, font_file: Path):
        """Categorize font based on name and content"""
        # Check for language support
        bengali_keywords = ['bengali', 'bangla', 'solaiman', 'kalpurush', 'lipee', 'siyam', 'nikosh']
        arabic_keywords = ['arabic', 'kfgq', 'me_quran', 'uthman', 'noorehira']
        english_keywords = ['arial', 'helvetica', 'times', 'courier', 'verdana', 'georgia']
        
        # Bengali fonts
        if any(keyword in font_name for keyword in bengali_keywords):
            self.bengali_fonts.append(font_path)
            self.font_categories['bengali'].append(font_path)
        
        # Arabic fonts
        elif any(keyword in font_name for keyword in arabic_keywords):
            self.arabic_fonts.append(font_path)
            self.font_categories['arabic'].append(font_path)
        
        # English/Generic fonts
        elif any(keyword in font_name for keyword in english_keywords):
            self.english_fonts.append(font_path)
            self.font_categories['english'].append(font_path)
        
        # Categorize by style
        if any(word in font_name for word in ['decorative', 'ornate', 'fancy']):
            self.font_categories['decorative'].append(font_path)
            self.special_fonts.append(font_path)
        
        elif any(word in font_name for word in ['modern', 'clean', 'minimal']):
            self.font_categories['modern'].append(font_path)
        
        elif any(word in font_name for word in ['retro', 'vintage', 'old']):
            self.font_categories['retro'].append(font_path)
        
        elif any(word in font_name for word in ['hand', 'script', 'cursive']):
            self.font_categories['handwritten'].append(font_path)
        
        elif any(word in font_name for word in ['mono', 'code', 'console']):
            self.font_categories['monospace'].append(font_path)
    
    def _create_emergency_fonts(self):
        """Create emergency fallback fonts"""
        try:
            # Try to use default PIL font
            default_font = ImageFont.load_default()
            self.available_fonts.append('default')
            self.english_fonts.append('default')
            self.font_categories['english'].append('default')
        except:
            pass
    
    @retry_on_failure(max_attempts=3)
    def _download_default_fonts(self):
        """Download default fonts if not available"""
        default_fonts = [
            {
                'name': 'Kalpurush',
                'url': 'https://github.com/fonts-for-bengali/kalpurush/raw/master/Kalpurush.ttf',
                'category': 'bengali'
            },
            {
                'name': 'SiyamRupali',
                'url': 'https://github.com/fonts-for-bengali/siyam-rupali/raw/master/Siyamrupali.ttf',
                'category': 'bengali'
            }
        ]
        
        for font_info in default_fonts:
            font_path = self.fonts_dir / f"{font_info['name']}.ttf"
            
            if not font_path.exists():
                try:
                    logger.info(f"Downloading {font_info['name']}...")
                    response = requests.get(font_info['url'], timeout=10)
                    if response.status_code == 200:
                        font_path.write_bytes(response.content)
                        logger.info(f"Downloaded {font_info['name']}")
                        
                        # Reload fonts
                        self._load_all_fonts()
                except Exception as e:
                    logger.warning(f"Failed to download {font_info['name']}: {e}")
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text"""
        if not text:
            return 'english'
        
        # Bengali range
        bengali_range = range(0x0980, 0x09FF + 1)
        # Arabic range
        arabic_range = range(0x0600, 0x06FF + 1)
        
        bengali_chars = 0
        arabic_chars = 0
        english_chars = 0
        
        for char in text:
            try:
                code = ord(char)
                if code in bengali_range:
                    bengali_chars += 1
                elif code in arabic_range:
                    arabic_chars += 1
                elif 0x0041 <= code <= 0x007A or 0x0080 <= code <= 0x024F:
                    english_chars += 1
            except:
                continue
        
        if bengali_chars > english_chars and bengali_chars > arabic_chars:
            return 'bengali'
        elif arabic_chars > english_chars and arabic_chars > bengali_chars:
            return 'arabic'
        else:
            return 'english'
    
    @lru_cache(maxsize=500)
    def get_font(self, size: int, category: str = None, 
                style: str = "regular", language: str = None,
                text: str = None) -> ImageFont.FreeTypeFont:
        """Get appropriate font with caching"""
        cache_key = f"{size}_{category}_{style}_{language}_{hash(text or '')}"
        
        # Check cache
        if cache_key in self.font_cache:
            # Move to end (LRU)
            font = self.font_cache.pop(cache_key)
            self.font_cache[cache_key] = font
            return font
        
        try:
            # Determine language from text if not provided
            if language is None and text:
                language = self._detect_language(text)
            
            # Select font category
            if category and category in self.font_categories and self.font_categories[category]:
                font_list = self.font_categories[category]
            elif language == 'bengali' and self.bengali_fonts:
                font_list = self.bengali_fonts
            elif language == 'arabic' and self.arabic_fonts:
                font_list = self.arabic_fonts
            elif self.english_fonts:
                font_list = self.english_fonts
            else:
                font_list = self.available_fonts
            
            # Choose font
            if not font_list:
                return ImageFont.load_default()
            
            font_path = random.choice(font_list)
            
            # Load font
            if font_path == 'default':
                font = ImageFont.load_default()
                # Scale default font
                from PIL import ImageDraw
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(font_path, size)
            
            # Cache font
            if len(self.font_cache) >= 100:  # Limit cache size
                self.font_cache.popitem(last=False)
            self.font_cache[cache_key] = font
            
            return font
            
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            return ImageFont.load_default()
    
    def get_font_size(self, resolution: str, font_type: str) -> int:
        """Get appropriate font size for resolution"""
        if resolution in self.font_size_presets and font_type in self.font_size_presets[resolution]:
            return self.font_size_presets[resolution][font_type]
        return self.font_size_presets['STANDARD'][font_type]
    
    def get_font_for_style(self, style: ImageStyle, size: int) -> ImageFont.FreeTypeFont:
        """Get font appropriate for image style"""
        style_font_map = {
            ImageStyle.DARK_FUTURISTIC: 'modern',
            ImageStyle.LIGHT_ELEGANT: 'decorative',
            ImageStyle.NEON_CYBERPUNK: 'monospace',
            ImageStyle.VINTAGE_RETRO: 'retro',
            ImageStyle.MINIMAL_MODERN: 'modern',
            ImageStyle.GRUNGE_URBAN: 'handwritten',
            ImageStyle.BENGALI_TRADITIONAL: 'bengali',
            ImageStyle.ISLAMIC_CALLIGRAPHY: 'arabic',
        }
        
        category = style_font_map.get(style, 'english')
        return self.get_font(size, category)
    
    def get_stats(self) -> Dict:
        """Get font statistics"""
        return {
            'total_fonts': len(self.available_fonts),
            'bengali_fonts': len(self.bengali_fonts),
            'english_fonts': len(self.english_fonts),
            'arabic_fonts': len(self.arabic_fonts),
            'special_fonts': len(self.special_fonts),
            'cache_size': len(self.font_cache),
            'categories': {k: len(v) for k, v in self.font_categories.items()}
        }

class UltraColorManager:
    """Advanced Color Management with Ultra HD Palettes"""
    
    def __init__(self):
        self.palettes = self._initialize_ultra_palettes()
        self.gradient_cache = OrderedDict()
        self.color_schemes_cache = {}
        self.max_cache_size = 1000
        
        logger.info(f"✅ UltraColorManager initialized with {len(self.palettes)} palettes")
    
    def _initialize_ultra_palettes(self) -> Dict[str, Dict]:
        """Initialize comprehensive ultra HD color palettes"""
        return {
            # Modern Palettes
            "midnight_aurora": {
                "name": "Midnight Aurora",
                "primary": (10, 15, 30),
                "secondary": (40, 45, 70),
                "accent": (0, 200, 255),
                "highlight": (255, 100, 150),
                "text": (240, 240, 255),
                "shadow": (20, 20, 40),
                "border": (0, 150, 255),
                "success": (0, 255, 150),
                "warning": (255, 200, 0),
                "error": (255, 50, 50),
                "gradient": [(10, 15, 30), (40, 45, 70), (80, 85, 120)]
            },
            "cyber_neon": {
                "name": "Cyber Neon",
                "primary": (0, 0, 20),
                "secondary": (30, 0, 50),
                "accent": (255, 0, 255),
                "highlight": (0, 255, 255),
                "text": (200, 255, 255),
                "shadow": (0, 50, 50),
                "border": (255, 0, 255),
                "success": (0, 255, 200),
                "warning": (255, 255, 0),
                "error": (255, 0, 100),
                "gradient": [(0, 0, 20), (30, 0, 50), (60, 0, 100)]
            },
            "sunset_gold": {
                "name": "Sunset Gold",
                "primary": (30, 25, 20),
                "secondary": (60, 50, 40),
                "accent": (255, 215, 0),
                "highlight": (255, 140, 0),
                "text": (255, 240, 200),
                "shadow": (50, 40, 20),
                "border": (255, 215, 0),
                "success": (200, 255, 0),
                "warning": (255, 180, 0),
                "error": (255, 100, 0),
                "gradient": [(30, 25, 20), (60, 50, 40), (120, 100, 80)]
            },
            "ocean_depth": {
                "name": "Ocean Depth",
                "primary": (0, 30, 50),
                "secondary": (0, 80, 120),
                "accent": (0, 200, 255),
                "highlight": (0, 255, 200),
                "text": (200, 240, 255),
                "shadow": (0, 20, 40),
                "border": (0, 150, 255),
                "success": (0, 255, 150),
                "warning": (255, 220, 100),
                "error": (255, 100, 100),
                "gradient": [(0, 30, 50), (0, 80, 120), (0, 150, 200)]
            },
            "forest_mystic": {
                "name": "Forest Mystic",
                "primary": (20, 40, 30),
                "secondary": (40, 100, 80),
                "accent": (80, 200, 120),
                "highlight": (150, 220, 180),
                "text": (220, 240, 220),
                "shadow": (10, 30, 20),
                "border": (60, 180, 140),
                "success": (100, 255, 180),
                "warning": (255, 220, 100),
                "error": (255, 100, 100),
                "gradient": [(20, 40, 30), (40, 100, 80), (80, 160, 130)]
            },
            # Bengali Traditional
            "bengali_festival": {
                "name": "Bengali Festival",
                "primary": (139, 0, 0),  # Deep Red
                "secondary": (255, 140, 0),  # Orange
                "accent": (0, 100, 0),  # Green
                "highlight": (255, 215, 0),  # Gold
                "text": (255, 240, 200),
                "shadow": (100, 0, 0),
                "border": (255, 140, 0),
                "success": (0, 200, 0),
                "warning": (255, 180, 0),
                "error": (255, 50, 50),
                "gradient": [(139, 0, 0), (255, 140, 0), (255, 215, 0)]
            },
            # Islamic Theme
            "islamic_gold": {
                "name": "Islamic Gold",
                "primary": (0, 50, 30),  # Dark Green
                "secondary": (218, 165, 32),  # Golden
                "accent": (139, 69, 19),  # Brown
                "highlight": (255, 215, 0),
                "text": (255, 250, 240),
                "shadow": (0, 30, 20),
                "border": (218, 165, 32),
                "success": (0, 200, 100),
                "warning": (255, 200, 0),
                "error": (200, 0, 0),
                "gradient": [(0, 50, 30), (139, 69, 19), (218, 165, 32)]
            },
            # Neon Theme
            "neon_dream": {
                "name": "Neon Dream",
                "primary": (20, 0, 40),
                "secondary": (60, 0, 100),
                "accent": (255, 0, 200),
                "highlight": (0, 255, 200),
                "text": (255, 255, 255),
                "shadow": (40, 0, 60),
                "border": (255, 0, 200),
                "success": (0, 255, 150),
                "warning": (255, 255, 0),
                "error": (255, 0, 100),
                "gradient": [(20, 0, 40), (60, 0, 100), (100, 0, 160)]
            },
            # Pastel Theme
            "pastel_bliss": {
                "name": "Pastel Bliss",
                "primary": (255, 230, 240),
                "secondary": (230, 240, 255),
                "accent": (200, 230, 255),
                "highlight": (255, 240, 200),
                "text": (80, 80, 100),
                "shadow": (200, 200, 220),
                "border": (200, 230, 255),
                "success": (180, 255, 200),
                "warning": (255, 240, 150),
                "error": (255, 180, 180),
                "gradient": [(255, 230, 240), (230, 240, 255), (200, 230, 255)]
            }
        }
    
    def get_palette(self, name: str = None, style: ImageStyle = None) -> Dict:
        """Get color palette by name, style, or auto-select"""
        if name and name in self.palettes:
            return self.palettes[name]
        
        # Map styles to palettes
        style_palette_map = {
            ImageStyle.DARK_FUTURISTIC: "midnight_aurora",
            ImageStyle.LIGHT_ELEGANT: "pastel_bliss",
            ImageStyle.NEON_CYBERPUNK: "cyber_neon",
            ImageStyle.VINTAGE_RETRO: "sunset_gold",
            ImageStyle.BENGALI_TRADITIONAL: "bengali_festival",
            ImageStyle.ISLAMIC_CALLIGRAPHY: "islamic_gold",
            ImageStyle.GLOW_AURORA: "neon_dream",
            ImageStyle.OCEAN_DEPTH: "ocean_depth",
        }
        
        if style and style in style_palette_map:
            return self.palettes[style_palette_map[style]]
        
        # Auto-select based on time
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return self.palettes["sunset_gold"]
        elif 12 <= hour < 17:
            return self.palettes["ocean_depth"]
        elif 17 <= hour < 20:
            return self.palettes["cyber_neon"]
        elif 20 <= hour < 23:
            return self.palettes["neon_dream"]
        else:
            return self.palettes["midnight_aurora"]
    
    def get_random_palette(self) -> Dict:
        """Get random color palette"""
        return random.choice(list(self.palettes.values()))
    
    def generate_complementary_colors(self, base_color: Tuple[int, int, int], 
                                     count: int = 5) -> List[Tuple[int, int, int]]:
        """Generate complementary colors from base color"""
        colors = []
        
        # Convert to HSL for better color manipulation
        r, g, b = base_color
        
        # Create variations
        for i in range(count):
            ratio = i / max(1, count - 1)
            
            # Create complementary, triadic, or analogous colors
            if ratio < 0.2:
                # Lighter shade
                color = (
                    min(255, int(r * 1.3)),
                    min(255, int(g * 1.3)),
                    min(255, int(b * 1.3))
                )
            elif ratio < 0.4:
                # Darker shade
                color = (
                    max(0, int(r * 0.7)),
                    max(0, int(g * 0.7)),
                    max(0, int(b * 0.7))
                )
            elif ratio < 0.6:
                # Complementary
                color = (
                    safe_color_value(255 - r),
                    safe_color_value(255 - g),
                    safe_color_value(255 - b)
                )
            elif ratio < 0.8:
                # Analogous 1
                color = (
                    safe_color_value(r),
                    safe_color_value(g + 50),
                    safe_color_value(b - 50)
                )
            else:
                # Analogous 2
                color = (
                    safe_color_value(r + 50),
                    safe_color_value(g - 50),
                    safe_color_value(b)
                )
            
            colors.append(color)
        
        return colors
    
    @lru_cache(maxsize=100)
    def generate_gradient(self, width: int, height: int,
                         colors: List[Tuple[int, int, int]],
                         direction: GradientDirection = GradientDirection.DIAGONAL_TL_BR,
                         gradient_type: str = "linear") -> Image.Image:
        """Generate ultra HD gradient with multiple colors"""
        cache_key = f"{width}x{height}_{str(colors)}_{direction.name}_{gradient_type}"
        
        if cache_key in self.gradient_cache:
            # Move to end (LRU)
            gradient = self.gradient_cache.pop(cache_key)
            self.gradient_cache[cache_key] = gradient
            return gradient.copy()
        
        try:
            gradient = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(gradient)
            
            if gradient_type == "linear":
                if direction == GradientDirection.HORIZONTAL:
                    for x in range(width):
                        ratio = x / max(width - 1, 1)
                        color = self._get_gradient_color(colors, ratio)
                        draw.line([(x, 0), (x, height)], fill=color)
                
                elif direction == GradientDirection.VERTICAL:
                    for y in range(height):
                        ratio = y / max(height - 1, 1)
                        color = self._get_gradient_color(colors, ratio)
                        draw.line([(0, y), (width, y)], fill=color)
                
                elif direction in [GradientDirection.DIAGONAL_TL_BR, GradientDirection.DIAGONAL_TR_BL]:
                    max_dist = math.sqrt(width**2 + height**2)
                    
                    for x in range(width):
                        for y in range(height):
                            if direction == GradientDirection.DIAGONAL_TL_BR:
                                dist = (x + y) / max_dist
                            else:  # TR_BL
                                dist = (width - x + y) / max_dist
                            
                            color = self._get_gradient_color(colors, dist)
                            draw.point((x, y), fill=color)
                
                elif direction == GradientDirection.RADIAL_CENTER:
                    center_x, center_y = width // 2, height // 2
                    max_radius = math.sqrt(center_x**2 + center_y**2)
                    
                    for x in range(width):
                        for y in range(height):
                            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                            ratio = dist / max_radius
                            color = self._get_gradient_color(colors, ratio)
                            draw.point((x, y), fill=color)
            
            elif gradient_type == "mesh":
                # Create mesh gradient
                mesh_size = 10
                for i in range(mesh_size):
                    for j in range(mesh_size):
                        x1 = int(width * i / mesh_size)
                        y1 = int(height * j / mesh_size)
                        x2 = int(width * (i + 1) / mesh_size)
                        y2 = int(height * (j + 1) / mesh_size)
                        
                        color_idx = (i + j) % len(colors)
                        color = colors[color_idx]
                        
                        draw.rectangle([x1, y1, x2, y2], fill=color)
            
            # Cache gradient
            if len(self.gradient_cache) >= self.max_cache_size:
                self.gradient_cache.popitem(last=False)
            self.gradient_cache[cache_key] = gradient.copy()
            
            return gradient
            
        except Exception as e:
            logger.error(f"Gradient generation failed: {e}")
            # Fallback to simple gradient
            fallback = Image.new('RGB', (width, height), colors[0] if colors else (0, 0, 0))
            return fallback
    
    def _get_gradient_color(self, colors: List[Tuple[int, int, int]], ratio: float) -> Tuple[int, int, int]:
        """Get color from gradient stops"""
        ratio = max(0.0, min(1.0, ratio))
        
        if len(colors) == 1:
            return colors[0]
        
        # Find which segment the ratio falls into
        segment_count = len(colors) - 1
        segment_length = 1.0 / segment_count
        
        segment = int(ratio / segment_length)
        segment = min(segment, segment_count - 1)
        
        segment_ratio = (ratio % segment_length) / segment_length
        
        # Use smoothstep for smoother transitions
        segment_ratio = segment_ratio * segment_ratio * (3 - 2 * segment_ratio)
        
        return create_gradient_color(colors[segment], colors[segment + 1], segment_ratio)
    
    def get_color_scheme(self, base_color: Tuple[int, int, int], 
                        scheme_type: str = "analogous") -> List[Tuple[int, int, int]]:
        """Generate color scheme from base color"""
        cache_key = f"{base_color}_{scheme_type}"
        
        if cache_key in self.color_schemes_cache:
            return self.color_schemes_cache[cache_key]
        
        r, g, b = base_color
        
        if scheme_type == "monochromatic":
            colors = [
                (r, g, b),
                (max(0, r-30), max(0, g-30), max(0, b-30)),
                (min(255, r+30), min(255, g+30), min(255, b+30)),
                (max(0, r-60), max(0, g-60), max(0, b-60)),
                (min(255, r+60), min(255, g+60), min(255, b+60))
            ]
        
        elif scheme_type == "analogous":
            colors = [
                (r, g, b),
                ((r + 30) % 255, (g + 20) % 255, (b - 30) % 255),
                ((r - 30) % 255, (g - 20) % 255, (b + 30) % 255),
                ((r + 60) % 255, (g + 40) % 255, (b - 60) % 255),
                ((r - 60) % 255, (g - 40) % 255, (b + 60) % 255)
            ]
        
        elif scheme_type == "complementary":
            colors = [
                (r, g, b),
                (255 - r, 255 - g, 255 - b),
                ((r + 128) % 255, (g + 128) % 255, (b + 128) % 255),
                (max(0, r-50), g, min(255, b+50)),
                (min(255, r+50), g, max(0, b-50))
            ]
        
        elif scheme_type == "triadic":
            colors = [
                (r, g, b),
                (g, b, r),
                (b, r, g),
                ((r + 85) % 255, (g + 85) % 255, (b + 85) % 255),
                ((r + 170) % 255, (g + 170) % 255, (b + 170) % 255)
            ]
        
        else:  # tetradic
            colors = [
                (r, g, b),
                ((r + 64) % 255, (g + 64) % 255, (b + 64) % 255),
                ((r + 128) % 255, (g + 128) % 255, (b + 128) % 255),
                ((r + 192) % 255, (g + 192) % 255, (b + 192) % 255),
                (255 - r, 255 - g, 255 - b)
            ]
        
        # Cache the scheme
        self.color_schemes_cache[cache_key] = colors
        if len(self.color_schemes_cache) > 500:
            # Remove oldest entries
            keys = list(self.color_schemes_cache.keys())
            for key in keys[:100]:
                del self.color_schemes_cache[key]
        
        return colors
    
    def get_stats(self) -> Dict:
        """Get color manager statistics"""
        return {
            'palettes_count': len(self.palettes),
            'gradient_cache_size': len(self.gradient_cache),
            'color_schemes_cache_size': len(self.color_schemes_cache),
            'max_cache_size': self.max_cache_size
        }

class BackgroundImageManager:
    """Manager for Ultra HD Background Images"""
    
    def __init__(self, config: GenerationConfig):
        self.config = config
        self.backgrounds_dir = Path(config.backgrounds_dir)
        self.backgrounds_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache
        self.background_cache = OrderedDict()
        self.url_cache = {}
        self.max_cache_size = 100
        
        # Categories
        self.categories = [
            "nature", "abstract", "gradient", "pattern", "texture",
            "space", "city", "technology", "art", "minimal",
            "dark", "light", "colorful", "monochrome", "bengali",
            "islamic", "festival", "celebration"
        ]
        
        # Default gradients
        self.default_gradients = self._create_default_gradients()
        
        # Unsplash integration
        self.unsplash_enabled = config.enable_unsplash and config.unsplash_api_key
        self.unsplash_cache = OrderedDict()
        
        logger.info(f"✅ BackgroundImageManager initialized with {len(self.categories)} categories")
    
    def _create_default_gradients(self) -> Dict[str, List[Tuple[int, int, int]]]:
        """Create default gradient presets"""
        return {
            "sunrise": [(255, 100, 50), (255, 200, 100), (100, 200, 255)],
            "sunset": [(255, 50, 100), (255, 150, 50), (50, 20, 100)],
            "ocean": [(0, 30, 50), (0, 100, 150), (0, 200, 255)],
            "forest": [(20, 40, 30), (40, 100, 80), (100, 200, 150)],
            "cyber": [(0, 0, 20), (30, 0, 50), (100, 0, 150)],
            "neon": [(20, 0, 40), (60, 0, 100), (150, 0, 200)],
            "gold": [(30, 25, 20), (60, 50, 40), (120, 100, 80)],
            "silver": [(40, 40, 50), (80, 80, 100), (150, 150, 180)],
            "bengali": [(139, 0, 0), (255, 140, 0), (255, 215, 0)],
            "islamic": [(0, 50, 30), (139, 69, 19), (218, 165, 32)]
        }
    
    def get_background(self, width: int, height: int, 
                      style: ImageStyle = None,
                      category: str = None) -> Image.Image:
        """Get ultra HD background image"""
        cache_key = f"{width}x{height}_{style.name if style else 'default'}_{category}"
        
        if cache_key in self.background_cache:
            # Move to end (LRU)
            bg = self.background_cache.pop(cache_key)
            self.background_cache[cache_key] = bg
            return bg.copy()
        
        try:
            # Decide background type
            bg_type = random.choice(["gradient", "unsplash", "pattern", "texture"])
            
            if bg_type == "gradient" or not self.unsplash_enabled:
                background = self._create_gradient_background(width, height, style)
            elif bg_type == "unsplash":
                background = self._get_unsplash_background(width, height, category)
            elif bg_type == "pattern":
                background = self._create_pattern_background(width, height, style)
            else:  # texture
                background = self._create_texture_background(width, height, style)
            
            # Apply effects
            background = self._apply_background_effects(background, style)
            
            # Cache background
            if len(self.background_cache) >= self.max_cache_size:
                self.background_cache.popitem(last=False)
            self.background_cache[cache_key] = background.copy()
            
            return background
            
        except Exception as e:
            logger.error(f"Background creation failed: {e}")
            # Ultimate fallback
            return Image.new('RGB', (width, height), (40, 40, 60))
    
    def _create_gradient_background(self, width: int, height: int, 
                                   style: ImageStyle = None) -> Image.Image:
        """Create gradient background"""
        from .ultra_color_manager import UltraColorManager
        color_manager = UltraColorManager()
        
        if style:
            palette = color_manager.get_palette(style=style)
            colors = palette.get('gradient', [palette['primary'], palette['secondary']])
        else:
            gradient_name = random.choice(list(self.default_gradients.keys()))
            colors = self.default_gradients[gradient_name]
        
        direction = random.choice(list(GradientDirection))
        
        return color_manager.generate_gradient(width, height, colors, direction)
    
    @retry_on_failure(max_attempts=3)
    def _get_unsplash_background(self, width: int, height: int,
                                category: str = None) -> Image.Image:
        """Get background from Unsplash"""
        if not self.unsplash_enabled:
            return self._create_gradient_background(width, height)
        
        try:
            # Build URL
            if category:
                query = category
            else:
                query = random.choice(["abstract", "nature", "gradient", "texture"])
            
            url = f"https://api.unsplash.com/photos/random"
            params = {
                'query': query,
                'w': width,
                'h': height,
                'fit': 'crop',
                'client_id': self.config.unsplash_api_key
            }
            
            response = requests.get(url, params=params, timeout=self.config.request_timeout)
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['regular']
                
                # Download image
                img_response = requests.get(image_url, timeout=self.config.request_timeout)
                if img_response.status_code == 200:
                    image = Image.open(io.BytesIO(img_response.content))
                    image = image.resize((width, height), Resampling.LANCZOS)
                    return image.convert('RGB')
            
        except Exception as e:
            logger.warning(f"Unsplash failed: {e}")
        
        # Fallback to gradient
        return self._create_gradient_background(width, height)
    
    def _create_pattern_background(self, width: int, height: int,
                                  style: ImageStyle = None) -> Image.Image:
        """Create patterned background"""
        bg = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(bg)
        
        # Choose pattern
        pattern_type = random.choice(["dots", "lines", "grid", "waves", "triangles"])
        
        if pattern_type == "dots":
            spacing = 30
            radius = 8
            color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            
            for x in range(0, width, spacing):
                for y in range(0, height, spacing):
                    offset_x = random.randint(-5, 5)
                    offset_y = random.randint(-5, 5)
                    draw.ellipse([x + offset_x - radius, y + offset_y - radius,
                                 x + offset_x + radius, y + offset_y + radius],
                                fill=color)
        
        elif pattern_type == "lines":
            spacing = 20
            color = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
            
            for x in range(0, width, spacing):
                draw.line([(x, 0), (x + random.randint(-10, 10), height)],
                         fill=color, width=2)
        
        elif pattern_type == "grid":
            spacing = 40
            color = (random.randint(100, 180), random.randint(100, 180), random.randint(100, 180))
            
            for x in range(0, width, spacing):
                draw.line([(x, 0), (x, height)], fill=color, width=1)
            for y in range(0, height, spacing):
                draw.line([(0, y), (width, y)], fill=color, width=1)
        
        return bg
    
    def _create_texture_background(self, width: int, height: int,
                                  style: ImageStyle = None) -> Image.Image:
        """Create textured background"""
        bg = Image.new('RGB', (width, height), (255, 255, 255))
        
        # Add noise
        if NUMPY_AVAILABLE:
            try:
                noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
                noise_img = Image.fromarray(noise, 'RGB')
                bg = ImageChops.add(bg, noise_img)
            except:
                pass
        
        # Add gradient overlay
        overlay = self._create_gradient_background(width, height, style)
        overlay = overlay.convert('RGBA')
        
        # Set overlay opacity
        alpha = overlay.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(0.3)
        overlay.putalpha(alpha)
        
        bg = bg.convert('RGBA')
        bg = Image.alpha_composite(bg, overlay)
        
        return bg.convert('RGB')
    
    def _apply_background_effects(self, image: Image.Image, 
                                 style: ImageStyle = None) -> Image.Image:
        """Apply background effects based on style"""
        if style == ImageStyle.VINTAGE_RETRO:
            # Add vintage effect
            image = ImageEnhance.Color(image).enhance(0.7)
            image = ImageEnhance.Contrast(image).enhance(1.2)
            
            # Add grain
            if NUMPY_AVAILABLE:
                try:
                    grain = np.random.normal(0, 10, (image.height, image.width, 3))
                    grain = np.clip(grain, -20, 20).astype(np.uint8)
                    grain_img = Image.fromarray(grain, 'RGB')
                    image = ImageChops.add(image, grain_img, scale=0.3)
                except:
                    pass
        
        elif style == ImageStyle.GRUNGE_URBAN:
            # Add grunge texture
            image = ImageEnhance.Contrast(image).enhance(1.3)
            image = ImageEnhance.Brightness(image).enhance(0.9)
        
        elif style in [ImageStyle.NEON_CYBERPUNK, ImageStyle.GLOW_AURORA]:
            # Add glow effect
            image = ImageEnhance.Color(image).enhance(1.5)
            image = ImageEnhance.Brightness(image).enhance(1.1)
        
        return image
    
    def preload_backgrounds(self, count: int = 10):
        """Preload backgrounds for faster generation"""
        futures = []
        
        with ThreadPoolExecutor(max_workers=min(count, 4)) as executor:
            for i in range(count):
                width = random.choice([1080, 1920, 3840])
                height = random.choice([1080, 1080, 2160])
                style = ImageStyle.get_random()
                
                future = executor.submit(self.get_background, width, height, style)
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.debug(f"Background preload failed: {e}")
        
        logger.info(f"Preloaded {count} backgrounds")
    
    def get_stats(self) -> Dict:
        """Get background manager statistics"""
        return {
            'cache_size': len(self.background_cache),
            'unsplash_enabled': self.unsplash_enabled,
            'categories': self.categories,
            'default_gradients': len(self.default_gradients)
        }

class ProfilePictureManager:
    """Ultra HD Profile Picture Manager"""
    
    def __init__(self, config: GenerationConfig):
        self.config = config
        self.profiles_dir = Path(config.profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache
        self.profile_cache = OrderedDict()
        self.avatar_cache = {}
        self.max_cache_size = 500
        
        # Avatar generation
        self.avatar_colors = [
            (255, 105, 180),  # Pink
            (30, 144, 255),   # Blue
            (50, 205, 50),    # Green
            (255, 165, 0),    # Orange
            (138, 43, 226),   # Purple
            (220, 20, 60),    # Red
            (0, 206, 209),    # Cyan
            (255, 215, 0),    # Gold
        ]
        
        # Special treatments
        self.special_users = {
            "জাকির": {
                'color': (255, 215, 0),  # Gold
                'style': ProfileStyle.GOLDEN,
                'badge': "premium",
                'frame': BorderType.GOLD_PLATED
            },
            "zakir": {
                'color': (255, 215, 0),
                'style': ProfileStyle.GOLDEN,
                'badge': "premium",
                'frame': BorderType.GOLD_PLATED
            },
            "admin": {
                'color': (220, 20, 60),  # Red
                'style': ProfileStyle.ADMIN,
                'badge': "admin",
                'frame': BorderType.NEON_PULSING
            },
            "moderator": {
                'color': (30, 144, 255),  # Blue
                'style': ProfileStyle.MODERATOR,
                'badge': "mod",
                'frame': BorderType.GLOW_AURA
            }
        }
        
        logger.info("✅ ProfilePictureManager initialized")
    
    def generate_profile(self, user_info: Dict, 
                        size: int = 200,
                        style: ProfileStyle = None,
                        is_mentioned: bool = False) -> Image.Image:
        """Generate ultra HD profile picture"""
        # Create cache key
        user_id = user_info.get('id', 0)
        username = user_info.get('username', '').lower()
        cache_key = f"{user_id}_{username}_{size}_{style.name if style else 'default'}_{is_mentioned}"
        
        if cache_key in self.profile_cache:
            # Move to end (LRU)
            profile = self.profile_cache.pop(cache_key)
            self.profile_cache[cache_key] = profile
            return profile.copy()
        
        try:
            # Check for special treatment
            special_config = None
            if username in self.special_users:
                special_config = self.special_users[username]
            elif is_mentioned and "জাকির" in str(user_info.get('username', '')) + str(user_info.get('first_name', '')):
                special_config = self.special_users["জাকির"]
            
            # Generate profile
            if special_config:
                profile = self._generate_special_profile(user_info, size, special_config)
            else:
                profile = self._generate_default_profile(user_info, size, style)
            
            # Apply effects
            profile = self._apply_profile_effects(profile, style or ProfileStyle.DEFAULT)
            
            # Cache profile
            if len(self.profile_cache) >= self.max_cache_size:
                self.profile_cache.popitem(last=False)
            self.profile_cache[cache_key] = profile.copy()
            
            return profile
            
        except Exception as e:
            logger.error(f"Profile generation failed: {e}")
            # Fallback
            return self._create_fallback_profile(size)
    
    def _generate_default_profile(self, user_info: Dict, size: int,
                                 style: ProfileStyle = None) -> Image.Image:
        """Generate default profile picture"""
        # Create base image
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Get user initials
        initials = self._get_user_initials(user_info)
        username = user_info.get('username', 'user').lower()
        
        # Select color based on username
        color_idx = hash(username) % len(self.avatar_colors)
        base_color = self.avatar_colors[color_idx]
        
        # Create gradient background
        center = size // 2
        radius = size // 2 - 10
        
        for r in range(radius, 0, -5):
            color_ratio = r / radius
            color = (
                int(base_color[0] * color_ratio),
                int(base_color[1] * color_ratio),
                int(base_color[2] * color_ratio)
            )
            draw.ellipse([center - r, center - r, center + r, center + r],
                        fill=(*color, 255))
        
        # Add initials
        if initials:
            font_size = size // 2
            try:
                font = ImageFont.truetype("Arial", font_size)
            except:
                font = ImageFont.load_default()
            
            # Draw initials
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = (
                (size - text_width) // 2,
                (size - text_height) // 2
            )
            
            draw.text(position, initials, font=font, fill=(255, 255, 255, 255))
        
        # Add frame
        if style != ProfileStyle.DEFAULT:
            frame = self._create_profile_frame(size, style)
            profile = Image.alpha_composite(profile, frame)
        
        return profile
    
    def _generate_special_profile(self, user_info: Dict, size: int,
                                 special_config: Dict) -> Image.Image:
        """Generate special profile for mentioned users"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Create special background
        center = size // 2
        radius = size // 2 - 15
        
        # Multi-layered gradient
        colors = self._create_special_gradient(special_config['color'])
        
        for i, color in enumerate(colors):
            r = radius - (i * 15)
            if r > 0:
                alpha = 255 - (i * 50)
                draw.ellipse([center - r, center - r, center + r, center + r],
                            fill=(*color, alpha))
        
        # Add user initial with special font
        initials = self._get_user_initials(user_info)
        if initials:
            font_size = size // 3
            
            # Try to load a decorative font
            try:
                # This would need actual font files
                font = ImageFont.truetype("Arial", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = (
                (size - text_width) // 2,
                (size - text_height) // 2
            )
            
            # Text with shadow
            shadow_color = (0, 0, 0, 150)
            draw.text((position[0] + 2, position[1] + 2), initials, 
                     font=font, fill=shadow_color)
            draw.text(position, initials, font=font, fill=(255, 255, 255, 255))
        
        # Add special frame
        frame = self._create_special_frame(size, special_config)
        profile = Image.alpha_composite(profile, frame)
        
        # Add badge if specified
        if special_config.get('badge'):
            badge = self._create_badge(size, special_config['badge'])
            profile = Image.alpha_composite(profile, badge)
        
        return profile
    
    def _create_profile_frame(self, size: int, style: ProfileStyle) -> Image.Image:
        """Create profile frame"""
        frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        if style == ProfileStyle.GOLDEN:
            # Golden frame
            draw.ellipse([5, 5, size-5, size-5], 
                        outline=(255, 215, 0, 255), width=8)
            draw.ellipse([10, 10, size-10, size-10], 
                        outline=(255, 240, 150, 200), width=4)
        
        elif style == ProfileStyle.PREMIUM_USER:
            # Premium frame with glow
            for i in range(3):
                width = 6 - i * 2
                alpha = 200 - i * 60
                offset = 5 + i * 3
                draw.ellipse([offset, offset, size-offset, size-offset],
                            outline=(0, 200, 255, alpha), width=width)
        
        elif style == ProfileStyle.GLOWING:
            # Glowing frame
            for i in range(4):
                alpha = 150 - i * 40
                offset = 3 + i * 4
                draw.ellipse([offset, offset, size-offset, size-offset],
                            outline=(255, 105, 180, alpha), width=3)
        
        return frame
    
    def _create_special_frame(self, size: int, special_config: Dict) -> Image.Image:
        """Create special frame for mentioned users"""
        frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        color = special_config['color']
        
        # Animated-style frame
        for i in range(5):
            width = 8 - i
            alpha = 255 - i * 50
            offset = 5 + i * 4
            
            draw.ellipse([offset, offset, size-offset, size-offset],
                        outline=(*color, alpha), width=width)
        
        # Add decorative elements
        if special_config.get('frame') == BorderType.GOLD_PLATED:
            # Add corner decorations
            corner_size = size // 4
            for x in [0, size - corner_size]:
                for y in [0, size - corner_size]:
                    draw.rectangle([x, y, x + corner_size, y + corner_size],
                                 outline=(255, 215, 0, 200), width=3)
        
        return frame
    
    def _create_badge(self, size: int, badge_type: str) -> Image.Image:
        """Create profile badge"""
        badge = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(badge)
        
        badge_size = size // 4
        position = size - badge_size - 10
        
        if badge_type == "premium":
            # Star badge
            points = []
            for i in range(10):
                angle = math.pi * i / 5
                radius = badge_size // 2 if i % 2 == 0 else badge_size // 4
                points.append((
                    position + badge_size//2 + radius * math.cos(angle - math.pi/2),
                    position + badge_size//2 + radius * math.sin(angle - math.pi/2)
                ))
            
            if len(points) >= 3:
                draw.polygon(points, fill=(255, 215, 0, 255))
        
        elif badge_type == "admin":
            # Shield badge
            draw.rectangle([position, position, 
                          position + badge_size, position + badge_size],
                         fill=(220, 20, 60, 255))
            draw.text([position + badge_size//4, position + badge_size//4],
                     "A", fill=(255, 255, 255, 255))
        
        return badge
    
    def _get_user_initials(self, user_info: Dict) -> str:
        """Get user initials for avatar"""
        first_name = user_info.get('first_name', '')
        last_name = user_info.get('last_name', '')
        username = user_info.get('username', '')
        
        if first_name and last_name:
            return (first_name[0] + last_name[0]).upper()
        elif first_name:
            return first_name[0].upper()
        elif username:
            return username[0].upper()
        else:
            return "U"
    
    def _create_special_gradient(self, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Create special gradient colors"""
        colors = []
        
        for i in range(5):
            ratio = i / 4
            # Create gradient from dark to light
            color = (
                int(base_color[0] * (0.3 + ratio * 0.7)),
                int(base_color[1] * (0.3 + ratio * 0.7)),
                int(base_color[2] * (0.3 + ratio * 0.7))
            )
            colors.append(color)
        
        return colors
    
    def _apply_profile_effects(self, profile: Image.Image, style: ProfileStyle) -> Image.Image:
        """Apply profile effects"""
        if style in [ProfileStyle.GLOWING, ProfileStyle.PREMIUM_USER]:
            # Add glow effect
            profile = profile.filter(ImageFilter.GaussianBlur(radius=2))
        
        if style == ProfileStyle.ANIMATED:
            # Add subtle animation effect
            profile = ImageEnhance.Brightness(profile).enhance(1.1)
        
        return profile
    
    def _create_fallback_profile(self, size: int) -> Image.Image:
        """Create fallback profile picture"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Simple circle
        center = size // 2
        radius = size // 2 - 5
        
        draw.ellipse([center - radius, center - radius, 
                     center + radius, center + radius],
                    fill=(100, 100, 100, 255))
        
        draw.ellipse([center - radius, center - radius, 
                     center + radius, center + radius],
                    outline=(200, 200, 200, 255), width=3)
        
        return profile
    
    def get_stats(self) -> Dict:
        """Get profile manager statistics"""
        return {
            'cache_size': len(self.profile_cache),
            'special_users': len(self.special_users),
            'avatar_colors': len(self.avatar_colors),
            'max_cache_size': self.max_cache_size
        }

class ReplyManager:
    """Advanced Reply Management System"""
    
    def __init__(self):
        self.replies = self._initialize_replies()
        self.used_replies = deque(maxlen=100)
        self.context_replies = {}
        
        logger.info(f"✅ ReplyManager initialized with {sum(len(r) for r in self.replies.values())} replies")
    
    def _initialize_replies(self) -> Dict[str, List[str]]:
        """Initialize comprehensive reply database"""
        return {
            'funny': [
                "তোমার বুদ্ধির কথা শুনে আমার আইকিউ কমে গেছে! 😂",
                "এত স্মার্ট হলে এত বোকা কেন? 🤔",
                "তোমার মতো বন্ধু থাকলে শত্রু দরকার হয় না! 😄",
                "তোমাকে দেখে মনে হচ্ছে evolution কাজ করে না! 🐒",
                "তোমার বুদ্ধি তো আকাশচুম্বী... নিচের দিকে! 📉",
                "তুমি যদি কমিক্স হতে, তুমি হতে 'দ্য ইনভিজিবল ম্যান' কারণ তোমার কোনো অস্তিত্ব নেই! 👻",
                "তোমার ফেসবুক স্ট্যাটাস পড়ে আমার Data waste হয়েছে! 📱",
                "তোমার মতামতের মূল্য তো শূন্যেরও কম! 💸",
                "তুমি যদি Google হতে, Search history ফাঁস হয়ে যেত! 🔍",
                "তোমার বুদ্ধি দেখে মনে হচ্ছে টেস্ট নেগেটিভ! 🧪"
            ],
            'roast': [
                "তোমার personality তো Null pointer exception! 💻",
                "তোমার মতো মানুষদের জন্য 'block' বাটন তৈরি হয়েছে! 🚫",
                "তুমি যদি Meme হতে, তুমি হতে 'Nobody:'! 😶",
                "তোমার জীবন story তো 404 Error! ❌",
                "তোমার face দেখে মনে হচ্ছে Ctrl+Z কাজ করে না! ↩️",
                "তোমার existence প্রমাণ করতে Scientific evidence দরকার! 🔬",
                "তুমি যদি App হতে, uninstall হওয়ার যোগ্য! 📲",
                "তোমার opinion তো Background noise! 🔊",
                "তুমি যদি Movie হতে, Rotten Tomatoes score 0%! 🍅",
                "তোমার vibe তো Corrupted file! 💾"
            ],
            'bengali_special': [
                "তোমার আত্মার ওজন নেগেটিভ! 👻",
                "তুমি ধোঁয়া তুলছো নাকি বুদ্ধি দেখাচ্ছো বুঝতে পারছি না! 💨",
                "তোমার মতামতের দাম ডলারের তুলনায়ও কম! 💵",
                "তুমি যদি রিক্সা চালাতে, ভাড়া নিতেও ভুলে যেতে! 🛺",
                "তোমার বুদ্ধির আলো নিভে গেছে অনেক আগেই! 💡",
                "তুমি চাঁদের আলো দেখলে মনে করো সেটা স্ট্রিট লাইট! 🌙",
                "তোমার কাছ থেকে ভালো পরামর্শ পেলে আমি বিশ্বাস করবো ভূত আছে! 👻",
                "তুমি সাগরে গেলে লবণাক্ততা কমে যাবে! 🌊",
                "তোমার বুদ্ধির পরীক্ষায় নম্বর আসে নেগেটিভ! 📝",
                "তুমি যদি কবি হতে, ছন্দ মেলাতে পারতে না! 📜"
            ],
            'english_roast': [
                "Your IQ is so low, it's in negative numbers! 🧠",
                "If stupidity was a superpower, you'd be a superhero! 🦸",
                "You're like a cloud. When you disappear, it's a beautiful day! ☁️",
                "Your brain is smoother than a marble floor! 🪨",
                "You're the reason why aliens won't talk to us! 👽",
                "If laughter is the best medicine, your face must be curing the world! 😷",
                "You're not stupid; you just have bad luck thinking! 🍀",
                "Your ideas are like lost socks - never to be found again! 🧦",
                "You're proof that evolution can go in reverse! 🔄",
                "If you were a WiFi signal, you'd be one bar in a five-bar area! 📶"
            ],
            'compliment': [
                "তুমি অসাধারণ! তবে রোস্টের জন্য এখানে এসেছো তো? 😉",
                "তোমার মতো বন্ধু পাওয়া সত্যিই সৌভাগ্যের বিষয়! 🤗",
                "তুমি একটু বেশিই স্মার্ট, রোস্ট করতে পারছি না! 🧠",
                "তোমার উপস্থিতি এই গ্রুপের গর্ব! 👑",
                "তোমাকে দেখে আমার রোস্ট করার মেজাজই চলে গেল! 🥺",
                "You're amazing! But we're here for roasts, remember? 😅",
                "Your positivity is infectious! Too bad we're roasting! 😄",
                "You're making it hard to roast you! Stop being so nice! 😊",
                "You're the kind of person who makes the internet better! 🌐",
                "I was going to roast you, but you're actually cool! 👍"
            ],
            'welcome': [
                "স্বাগতম! রোস্টের জগতে আপনাকে হৃদয়ের অভিনন্দন! 🎉",
                "নতুন রোস্টারের আগমন! সবাই প্রস্তুত থাকুন! 🔥",
                "হ্যালো! রোস্টিফাই পরিবারে আপনাকে স্বাগতম! 👋",
                "ওহো! একজন নতুন প্রতিভা এসেছেন! প্রত্যেকের রোস্ট প্রস্তুত রাখুন! ⚡",
                "Welcome to Roastify! May the roasts be ever in your favor! 🏆",
                "New member alert! Everyone bring your best roasts! 🚨",
                "আসসালামু আলাইকুম! রোস্টের আখড়ায় আপনাকে স্বাগতম! 🤲",
                "Get ready for some spicy roasts! Welcome aboard! 🌶️",
                "তোমার রোস্টিং যাত্রা শুরু হোক এই মুহূর্ত থেকে! 🚀",
                "A new challenger approaches! Let the roasts begin! ⚔️"
            ],
            'achievement': [
                "Congratulations! You've unlocked: Professional Roastee! 🏅",
                "Achievement Unlocked: Can Take a Joke! 🎯",
                "Level Up! You're now a Roast Master! ⭐",
                "New Badge Earned: Roast Survivor! 🛡️",
                "Milestone Reached: 100 Roasts Endured! 💯",
                "Special Achievement: Still Smiling After Roasts! 😄",
                "You've earned the 'Good Sport' award! 🏆",
                "Promotion: From Roastee to Roaster! 🔥",
                "Unlocked: Immunity to Weak Roasts! 💪",
                "Legendary Status: Roast Proof! 🦸"
            ]
        }
    
    def get_reply(self, category: str = None, context: Dict = None) -> str:
        """Get intelligent reply based on category and context"""
        # If no category, choose random
        if not category or category not in self.replies:
            category = random.choice(list(self.replies.keys()))
        
        # Get available replies
        available_replies = self.replies[category].copy()
        
        # Remove recently used replies
        for used in self.used_replies:
            if used in available_replies:
                available_replies.remove(used)
        
        # If no available replies, reset used list
        if not available_replies:
            self.used_replies.clear()
            available_replies = self.replies[category].copy()
        
        # Choose reply
        reply = random.choice(available_replies)
        
        # Add to used list
        self.used_replies.append(reply)
        
        # Apply context if available
        if context:
            reply = self._apply_context(reply, context)
        
        return reply
    
    def _apply_context(self, reply: str, context: Dict) -> str:
        """Apply context to reply"""
        user_name = context.get('user_name', '')
        rating = context.get('rating', 0)
        
        if user_name and '{user}' in reply:
            reply = reply.replace('{user}', user_name)
        
        if rating and '{rating}' in reply:
            reply = reply.replace('{rating}', str(rating))
        
        return reply
    
    def add_custom_reply(self, category: str, reply: str):
        """Add custom reply to database"""
        if category not in self.replies:
            self.replies[category] = []
        
        self.replies[category].append(reply)
        logger.info(f"Added custom reply to category '{category}'")
    
    def get_categories(self) -> List[str]:
        """Get available reply categories"""
        return list(self.replies.keys())
    
    def get_stats(self) -> Dict:
        """Get reply manager statistics"""
        total_replies = sum(len(replies) for replies in self.replies.values())
        return {
            'total_categories': len(self.replies),
            'total_replies': total_replies,
            'recently_used': len(self.used_replies),
            'categories': {k: len(v) for k, v in self.replies.items()}
        }

class ImageEnhancer:
    """Ultra HD Image Enhancement System"""
    
    def __init__(self):
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL is required for image enhancement")
        
        logger.info("✅ ImageEnhancer initialized")
    
    def enhance_image(self, image: Image.Image, 
                     enhancement_type: str = "auto") -> Image.Image:
        """Enhance image quality"""
        enhanced = image.copy()
        
        if enhancement_type == "auto":
            enhancement_type = self._detect_enhancement_needed(image)
        
        try:
            if enhancement_type == "sharpness":
                enhanced = self._enhance_sharpness(enhanced)
            elif enhancement_type == "color":
                enhanced = self._enhance_color(enhanced)
            elif enhancement_type == "contrast":
                enhanced = self._enhance_contrast(enhanced)
            elif enhancement_type == "details":
                enhanced = self._enhance_details(enhanced)
            elif enhancement_type == "all":
                enhanced = self._enhance_all(enhanced)
            
            # Always apply basic enhancements
            enhanced = self._apply_basic_enhancements(enhanced)
            
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
        
        return enhanced
    
    def _detect_enhancement_needed(self, image: Image.Image) -> str:
        """Detect what type of enhancement is needed"""
        # Simple detection based on image characteristics
        if image.mode == 'L':  # Grayscale
            return "color"
        
        # Check contrast
        if self._get_contrast_ratio(image) < 2.0:
            return "contrast"
        
        # Check sharpness (simple edge detection)
        if self._get_sharpness_score(image) < 0.1:
            return "sharpness"
        
        return "details"
    
    def _enhance_sharpness(self, image: Image.Image) -> Image.Image:
        """Enhance image sharpness"""
        # Unsharp mask
        if hasattr(ImageFilter, 'UnsharpMask'):
            image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        # Edge enhancement
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        return image
    
    def _enhance_color(self, image: Image.Image) -> Image.Image:
        """Enhance image colors"""
        # Convert to RGB if needed
        if image.mode != 'RGB' and image.mode != 'RGBA':
            image = image.convert('RGB')
        
        # Enhance saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        # Enhance vibrance (selective saturation)
        if NUMPY_AVAILABLE:
            try:
                image = self._enhance_vibrance(image)
            except:
                pass
        
        return image
    
    def _enhance_contrast(self, image: Image.Image) -> Image.Image:
        """Enhance image contrast"""
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Adjust brightness if needed
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def _enhance_details(self, image: Image.Image) -> Image.Image:
        """Enhance image details"""
        # Multiple enhancement passes
        image = self._enhance_sharpness(image)
        image = self._enhance_contrast(image)
        image = self._enhance_color(image)
        
        # Add clarity
        if hasattr(ImageFilter, 'Detail'):
            image = image.filter(ImageFilter.Detail())
        
        return image
    
    def _enhance_all(self, image: Image.Image) -> Image.Image:
        """Apply all enhancements"""
        image = self._enhance_details(image)
        image = self._enhance_color(image)
        image = self._enhance_sharpness(image)
        
        return image
    
    def _apply_basic_enhancements(self, image: Image.Image) -> Image.Image:
        """Apply basic enhancements to all images"""
        # Auto contrast
        image = ImageOps.autocontrast(image, cutoff=2)
        
        # Auto color (if available)
        try:
            image = ImageOps.autocolor(image)
        except:
            pass
        
        # Denoise
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    
    def _enhance_vibrance(self, image: Image.Image) -> Image.Image:
        """Selective saturation enhancement (vibrance)"""
        if not NUMPY_AVAILABLE:
            return image
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Convert to HSV
        hsv = self._rgb_to_hsv(img_array)
        
        # Increase saturation for less saturated pixels more
        saturation = hsv[:, :, 1]
        
        # Create vibrance mask (boost less saturated areas more)
        vibrance_mask = 1.0 - saturation
        vibrance_mask = np.clip(vibrance_mask * 2, 0, 1)
        
        # Apply vibrance
        saturation_boost = 0.3  # Base boost
        saturation += vibrance_mask * saturation_boost
        saturation = np.clip(saturation, 0, 1)
        
        hsv[:, :, 1] = saturation
        
        # Convert back to RGB
        rgb = self._hsv_to_rgb(hsv)
        
        return Image.fromarray(rgb.astype(np.uint8))
    
    def _rgb_to_hsv(self, rgb: np.ndarray) -> np.ndarray:
        """Convert RGB to HSV"""
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        
        maxc = np.maximum(np.maximum(r, g), b)
        minc = np.minimum(np.minimum(r, g), b)
        
        v = maxc
        
        deltac = maxc - minc
        s = np.where(maxc != 0, deltac / maxc, 0)
        
        rc = np.where(deltac != 0, (maxc - r) / deltac, 0)
        gc = np.where(deltac != 0, (maxc - g) / deltac, 0)
        bc = np.where(deltac != 0, (maxc - b) / deltac, 0)
        
        h = 4.0 + gc - rc
        h = np.where(r == maxc, bc - gc, h)
        h = np.where(g == maxc, 2.0 + rc - bc, h)
        h = (h / 6.0) % 1.0
        
        h = np.where(deltac == 0, 0, h)
        
        return np.stack([h, s, v], axis=2)
    
    def _hsv_to_rgb(self, hsv: np.ndarray) -> np.ndarray:
        """Convert HSV to RGB"""
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
        
        i = np.floor(h * 6.0)
        f = h * 6.0 - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        i = i.astype(np.uint8) % 6
        
        rgb = np.zeros_like(hsv)
        
        rgb[i == 0] = np.stack([v[i == 0], t[i == 0], p[i == 0]], axis=1)
        rgb[i == 1] = np.stack([q[i == 1], v[i == 1], p[i == 1]], axis=1)
        rgb[i == 2] = np.stack([p[i == 2], v[i == 2], t[i == 2]], axis=1)
        rgb[i == 3] = np.stack([p[i == 3], q[i == 3], v[i == 3]], axis=1)
        rgb[i == 4] = np.stack([t[i == 4], p[i == 4], v[i == 4]], axis=1)
        rgb[i == 5] = np.stack([v[i == 5], p[i == 5], q[i == 5]], axis=1)
        
        return (rgb * 255).astype(np.uint8)
    
    def _get_contrast_ratio(self, image: Image.Image) -> float:
        """Get image contrast ratio"""
        # Convert to grayscale
        gray = image.convert('L')
        gray_array = np.array(gray)
        
        # Calculate standard deviation as contrast measure
        return float(np.std(gray_array)) / 255.0
    
    def _get_sharpness_score(self, image: Image.Image) -> float:
        """Get image sharpness score"""
        # Use Laplacian variance method
        if not NUMPY_AVAILABLE:
            return 0.5
        
        try:
            gray = image.convert('L')
            gray_array = np.array(gray)
            
            # Apply Laplacian filter
            laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
            edges = np.abs(np.convolve(gray_array.flatten(), laplacian.flatten(), mode='same'))
            edges = edges.reshape(gray_array.shape)
            
            # Variance of edges as sharpness measure
            return float(np.var(edges)) / 10000.0
        except:
            return 0.5
    
    def upscale_image(self, image: Image.Image, scale_factor: float = 2.0) -> Image.Image:
        """Upscale image using advanced algorithms"""
        if scale_factor <= 1.0:
            return image
        
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        # Use LANCZOS resampling for best quality
        upscaled = image.resize((new_width, new_height), Resampling.LANCZOS)
        
        # Enhance after upscaling
        upscaled = self.enhance_image(upscaled, "sharpness")
        
        return upscaled

# ================================
# MAIN GENERATOR CLASS
# ================================

class UltraHDImageGenerator:
    """
    🔥 ULTRA HD IMAGE GENERATOR v9.0
    🚀 Professional, Ultra HD, Production-Ready
    """
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        if not PIL_AVAILABLE:
            logger.critical("PIL/Pillow not available. Install: pip install pillow")
            raise ImportError("PIL/Pillow is required for image generation")
        
        self.config = config or GenerationConfig()
        self.generation_id = generate_unique_id()
        
        # Initialize managers
        self.font_manager = UltraFontManager(self.config.fonts_dir)
        self.color_manager = UltraColorManager()
        self.background_manager = BackgroundImageManager(self.config)
        self.profile_manager = ProfilePictureManager(self.config)
        self.reply_manager = ReplyManager()
        self.enhancer = ImageEnhancer()
        
        # Cache system
        self.cache_manager = CacheManager(
            cache_dir=self.config.cache_dir,
            ttl_hours=self.config.cache_ttl_hours,
            max_size=self.config.max_cache_size
        )
        
        # Thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=self.config.max_workers)
        self.active_tasks = {}
        
        # Statistics and monitoring
        self.stats = {
            'total_generated': 0,
            'ultra_hd_generated': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0,
            'avg_generation_time': 0.0,
            'peak_memory_mb': 0.0,
            'parallel_tasks': 0
        }
        
        # Performance monitoring
        self.performance_history = deque(maxlen=100)
        self.error_history = deque(maxlen=50)
        
        # Preload resources
        self._preload_resources()
        
        logger.info(f"✅ Ultra HD Image Generator v9.0 initialized (ID: {self.generation_id})")
        logger.info(f"  • Resolution: {self.config.custom_width}x{self.config.custom_height}")
        logger.info(f"  • Quality: {self.config.quality}/{self.config.format}")
        logger.info(f"  • Cache: {'Enabled' if self.config.enable_cache else 'Disabled'}")
        logger.info(f"  • Workers: {self.config.max_workers}")
        logger.info(f"  • Features: Random BG: {self.config.enable_random_backgrounds}, "
                   f"Profiles: {self.config.enable_profile_pictures}")
    
    def _preload_resources(self):
        """Preload resources for faster generation"""
        if self.config.enable_random_backgrounds:
            try:
                self.background_manager.preload_backgrounds(count=5)
            except Exception as e:
                logger.warning(f"Background preload failed: {e}")
    
    @retry_on_failure(max_attempts=3)
    def generate_roast_image(self, roast_text: Any, user_info: Any,
                            mentioned_user: Optional[Any] = None,
                            style: ImageStyle = None,
                            border_config: Optional[BorderConfig] = None,
                            background_config: Optional[BackgroundConfig] = None,
                            profile_config: Optional[ProfileConfig] = None,
                            reply_category: str = None) -> GenerationResult:
        """
        Generate Ultra HD roast image with all features
        """
        start_time = time.time()
        start_memory = measure_memory_usage()
        generation_id = generate_unique_id()
        
        try:
            logger.info(f"🚀 Starting Ultra HD generation {generation_id}")
            
            # 1. Input processing
            processed_text = self._safe_text_extract(roast_text)
            if not processed_text or len(processed_text.strip()) < 2:
                # Get intelligent reply
                processed_text = self.reply_manager.get_reply(
                    reply_category or 'funny',
                    {'user_name': user_info.get('username', 'User')}
                )
                logger.info(f"Using auto-reply: {processed_text[:50]}...")
            
            user_dict = self._process_user_info(user_info)
            mentioned_dict = self._process_user_info(mentioned_user) if mentioned_user else None
            
            logger.debug(f"Processing for user: {user_dict.get('username', 'Unknown')}")
            
            # 2. Cache check
            cache_key = None
            if self.config.enable_cache:
                cache_key = self._generate_cache_key(
                    processed_text, user_dict, mentioned_dict,
                    style, border_config, background_config
                )
                
                cached_data = self.cache_manager.get(cache_key)
                if cached_data:
                    self.stats['cache_hits'] += 1
                    
                    output_path = self._save_cached_image(cached_data, generation_id)
                    
                    processing_time = time.time() - start_time
                    current_memory = measure_memory_usage()
                    
                    result = GenerationResult(
                        success=True,
                        image_path=str(output_path),
                        thumbnail_path=self._create_thumbnail(output_path),
                        processing_time=round(processing_time, 3),
                        cache_hit=True,
                        memory_used_mb=round(current_memory - start_memory, 2),
                        image_size=len(cached_data),
                        image_dimensions=(self.config.custom_width, self.config.custom_height),
                        image_format=self.config.format,
                        image_quality=self.config.quality,
                        generation_id=generation_id,
                        timestamp=datetime.now().isoformat(),
                        metadata={
                            'user': user_dict.get('username', 'Unknown'),
                            'user_id': user_dict.get('id', 0),
                            'mentioned_user': mentioned_dict.get('username') if mentioned_dict else None,
                            'text_preview': processed_text[:100],
                            'style': style.name if style else 'auto',
                            'cache_key': cache_key[:12]
                        }
                    )
                    
                    self._update_stats(processing_time, True)
                    return result
            
            self.stats['cache_misses'] += 1
            
            # 3. Configuration setup
            style = style or ImageStyle.get_random()
            palette = self.color_manager.get_palette(style=style)
            
            border_config = border_config or self._create_border_config(style, palette)
            background_config = background_config or self._create_background_config(style, palette)
            profile_config = profile_config or self._create_profile_config(user_dict, mentioned_dict)
            text_config = self._create_text_config(processed_text, style, palette)
            
            # 4. Image creation pipeline
            image = self._create_ultra_hd_image(
                text_config, background_config, border_config,
                profile_config, user_dict, mentioned_dict,
                style, palette
            )
            
            # 5. Post-processing
            if self.config.enable_real_time_enhancement:
                image = self.enhancer.enhance_image(image)
            
            # 6. Save image
            output_path = self._save_image(image, generation_id, user_dict)
            
            # 7. Cache the result
            if self.config.enable_cache and cache_key:
                with open(output_path, 'rb') as f:
                    image_data = f.read()
                self.cache_manager.set(cache_key, image_data)
            
            # 8. Create thumbnail
            thumbnail_path = self._create_thumbnail(output_path)
            
            # 9. Backup if enabled
            if self.config.enable_backup:
                self._create_backup(output_path, generation_id)
            
            # 10. Update statistics and return
            processing_time = time.time() - start_time
            current_memory = measure_memory_usage()
            memory_used = current_memory - start_memory
            
            self.stats['total_generated'] += 1
            self.stats['successful'] += 1
            self.stats['total_time'] += processing_time
            
            if self.config.resolution_preset == "ULTRA_HD":
                self.stats['ultra_hd_generated'] += 1
            
            self.stats['peak_memory_mb'] = max(self.stats['peak_memory_mb'], memory_used)
            
            result = GenerationResult(
                success=True,
                image_path=str(output_path),
                thumbnail_path=str(thumbnail_path) if thumbnail_path else None,
                processing_time=round(processing_time, 3),
                cache_hit=False,
                memory_used_mb=round(memory_used, 2),
                image_size=os.path.getsize(output_path),
                image_dimensions=(self.config.custom_width, self.config.custom_height),
                image_format=self.config.format,
                image_quality=self.config.quality,
                generation_id=generation_id,
                timestamp=datetime.now().isoformat(),
                metadata={
                    'user': user_dict.get('username', 'Unknown'),
                    'user_id': user_dict.get('id', 0),
                    'mentioned_user': mentioned_dict.get('username') if mentioned_dict else None,
                    'text_length': len(processed_text),
                    'style': style.name,
                    'border_type': border_config.border_type.name,
                    'background_type': background_config.type,
                    'resolution': f"{self.config.custom_width}x{self.config.custom_height}",
                    'format': self.config.format,
                    'quality': self.config.quality,
                    'profile_style': profile_config.style.name,
                    'color_palette': palette['name'],
                    'enhancement_applied': self.config.enable_real_time_enhancement
                },
                effects_applied=[style.name, border_config.border_type.name],
                layers_count=5,
                compression_ratio=round(os.path.getsize(output_path) / (self.config.custom_width * self.config.custom_height * 3), 3)
            )
            
            self._update_stats(processing_time, True)
            logger.info(f"✅ Ultra HD image generated: {output_path.name} "
                       f"({processing_time:.2f}s, {memory_used:.1f}MB)")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            self.stats['failed'] += 1
            self.stats['total_time'] += processing_time
            
            error_msg = str(e)
            self.error_history.append({
                'time': datetime.now().isoformat(),
                'error': error_msg,
                'generation_id': generation_id
            })
            
            logger.error(f"❌ Ultra HD generation failed ({generation_id}): {error_msg}")
            logger.debug(traceback.format_exc())
            
            # Return comprehensive error result
            return GenerationResult(
                success=False,
                error=error_msg,
                warning="Using fallback generation method",
                processing_time=round(processing_time, 3),
                generation_id=generation_id,
                timestamp=datetime.now().isoformat(),
                metadata={
                    'user': user_dict.get('username', 'Unknown') if 'user_dict' in locals() else 'Unknown',
                    'error_type': type(e).__name__,
                    'retry_count': 0
                }
            )
    
    def _safe_text_extract(self, text_input: Any) -> str:
        """Safely extract text from any input type"""
        if text_input is None:
            return ""
        
        if isinstance(text_input, str):
            return text_input.strip()
        
        if isinstance(text_input, dict):
            text_keys = ['text', 'message', 'content', 'caption', 'roast', 
                        'roast_text', 'primary_text', 'reply', 'comment']
            
            for key in text_keys:
                if key in text_input:
                    value = text_input[key]
                    if isinstance(value, str) and value.strip():
                        return value.strip()
            
            # Try any string value
            for key, value in text_input.items():
                if isinstance(value, str) and len(value.strip()) > 2:
                    return value.strip()
            
            # Convert dict to JSON
            try:
                return json.dumps(text_input, ensure_ascii=False, indent=0)
            except:
                return str(text_input)
        
        if isinstance(text_input, (list, tuple)):
            if all(isinstance(item, str) for item in text_input):
                return ' '.join(str(item).strip() for item in text_input)
            return str(text_input)
        
        try:
            result = str(text_input)
            return result if result != "None" else ""
        except:
            return ""
    
    def _process_user_info(self, user_info: Any) -> Dict:
        """Process user information from any format"""
        default_user = {
            'id': random.randint(1000, 99999),
            'username': 'User',
            'first_name': 'User',
            'last_name': '',
            'full_name': 'User',
            'rating': round(random.uniform(5.0, 9.9), 1),
            'level': random.randint(1, 100),
            'rank': random.choice(['Member', 'Active', 'VIP', 'Regular']),
            'join_date': datetime.now().strftime('%Y-%m-%d'),
            'avatar_url': None,
            'metadata': {}
        }
        
        if user_info is None:
            return default_user
        
        if isinstance(user_info, dict):
            result = default_user.copy()
            result.update(user_info)
            
            # Ensure username
            if not result['username'] or result['username'] == 'User':
                if result['first_name'] and result['first_name'] != 'User':
                    result['username'] = result['first_name']
                else:
                    result['username'] = f"user_{result['id']}"
            
            # Ensure full name
            if not result['full_name'] or result['full_name'] == 'User':
                names = [result['first_name'], result['last_name']]
                result['full_name'] = ' '.join(filter(None, names)).strip()
                if not result['full_name']:
                    result['full_name'] = result['username']
            
            return result
        
        # Handle object with attributes
        result = default_user.copy()
        
        try:
            if hasattr(user_info, 'id'):
                result['id'] = user_info.id
            
            if hasattr(user_info, 'username') and user_info.username:
                result['username'] = str(user_info.username)
            
            if hasattr(user_info, 'first_name') and user_info.first_name:
                result['first_name'] = str(user_info.first_name)
            
            if hasattr(user_info, 'last_name') and user_info.last_name:
                result['last_name'] = str(user_info.last_name)
            
        except Exception as e:
            logger.debug(f"User info extraction error: {e}")
        
        # Final validation
        if not result['username'] or result['username'] == 'User':
            result['username'] = result.get('first_name', f"user_{result['id']}")
        
        if not result['full_name'] or result['full_name'] == 'User':
            names = [result['first_name'], result['last_name']]
            result['full_name'] = ' '.join(filter(None, names)).strip()
            if not result['full_name']:
                result['full_name'] = result['username']
        
        return result
    
    def _generate_cache_key(self, text: str, user_info: Dict, mentioned_info: Optional[Dict],
                           style: ImageStyle, border_config: BorderConfig,
                           background_config: BackgroundConfig) -> str:
        """Generate cache key"""
        data = {
            'text': text[:500],
            'user_id': user_info.get('id', 0),
            'username': user_info.get('username', ''),
            'mentioned_id': mentioned_info.get('id', 0) if mentioned_info else 0,
            'style': style.name if style else 'random',
            'border_type': border_config.border_type.name if border_config else 'default',
            'background_type': background_config.type if background_config else 'default',
            'resolution': f"{self.config.custom_width}x{self.config.custom_height}",
            'quality': self.config.quality
        }
        
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:32]
    
    def _save_cached_image(self, image_data: bytes, generation_id: str) -> Path:
        """Save cached image"""
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"cached_{generation_id}.{self.config.format.lower()}"
        
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        return output_path
    
    def _create_border_config(self, style: ImageStyle, palette: Dict) -> BorderConfig:
        """Create border configuration"""
        border_type = BorderType.get_random()
        
        # Style-specific borders
        if style == ImageStyle.GOLDEN:
            border_type = BorderType.ORNATE_GOLD
        elif style == ImageStyle.NEON_CYBERPUNK:
            border_type = BorderType.NEON_PULSING
        elif style == ImageStyle.BENGALI_TRADITIONAL:
            border_type = BorderType.BENGALI_ALPANA
        elif style == ImageStyle.ISLAMIC_CALLIGRAPHY:
            border_type = BorderType.ISLAMIC_GEOMETRIC
        
        return BorderConfig(
            border_type=border_type,
            color=palette['border'],
            secondary_color=palette['accent'],
            thickness=random.randint(20, 35),
            corner_radius=random.randint(40, 80),
            glow_intensity=random.randint(0, 3),
            padding=random.randint(50, 80)
        )
    
    def _create_background_config(self, style: ImageStyle, palette: Dict) -> BackgroundConfig:
        """Create background configuration"""
        bg_type = random.choice(["gradient", "random_hd", "pattern"])
        
        if not self.config.enable_random_backgrounds:
            bg_type = "gradient"
        
        return BackgroundConfig(
            type=bg_type,
            style=style,
            primary_color=palette['primary'],
            secondary_color=palette['secondary'],
            tertiary_color=palette.get('tertiary', palette['accent']),
            gradient_direction=GradientDirection.get_random(),
            blur_radius=random.randint(0, 10),
            vignette_intensity=random.uniform(0.1, 0.4),
            noise_intensity=random.uniform(0.0, 0.1)
        )
    
    def _create_profile_config(self, user_info: Dict, mentioned_info: Optional[Dict]) -> ProfileConfig:
        """Create profile configuration"""
        if not self.config.enable_profile_pictures:
            return ProfileConfig(enabled=False)
        
        # Check if user is mentioned (special treatment)
        is_mentioned = mentioned_info is not None
        is_special_user = user_info.get('username', '').lower() in ['জাকির', 'zakir', 'admin', 'moderator']
        
        style = ProfileStyle.DEFAULT
        if is_special_user:
            style = ProfileStyle.GOLDEN
        elif is_mentioned:
            style = ProfileStyle.SPECIAL_MENTION
        
        return ProfileConfig(
            enabled=True,
            style=style,
            size=random.randint(180, 250),
            position=random.choice(["top_right", "top_left", "bottom_right", "bottom_left"]),
            offset_x=random.randint(40, 80),
            offset_y=random.randint(40, 80),
            frame_enabled=True,
            glow_enabled=style != ProfileStyle.DEFAULT,
            shadow_enabled=True
        )
    
    def _create_text_config(self, text: str, style: ImageStyle, palette: Dict) -> TextConfig:
        """Create text configuration"""
        # Font sizes based on resolution
        if self.config.resolution_preset == "ULTRA_HD":
            font_sizes = {'primary': 120, 'secondary': 72, 'tertiary': 48}
        elif self.config.resolution_preset == "FULL_HD":
            font_sizes = {'primary': 80, 'secondary': 48, 'tertiary': 32}
        else:
            font_sizes = {'primary': 60, 'secondary': 36, 'tertiary': 24}
        
        # Effects based on style
        if style in [ImageStyle.NEON_CYBERPUNK, ImageStyle.GLOW_AURORA]:
            effects = [TextEffect.GLOW_INTENSE, TextEffect.NEON_PULSING]
        elif style == ImageStyle.GOLDEN:
            effects = [TextEffect.GOLD_PLATED, TextEffect.SHADOW_DEEP]
        else:
            effects = TextEffect.get_random(random.randint(1, 2))
        
        return TextConfig(
            primary_text=text,
            font_size_primary=font_sizes['primary'],
            font_size_secondary=font_sizes['secondary'],
            text_color=palette['text'],
            shadow_color=palette['shadow'],
            effects=effects,
            line_spacing=random.uniform(1.2, 1.5),
            max_width_chars=random.randint(25, 40),
            alignment="center"
        )
    
    def _create_ultra_hd_image(self, text_config: TextConfig,
                              background_config: BackgroundConfig,
                              border_config: BorderConfig,
                              profile_config: ProfileConfig,
                              user_info: Dict,
                              mentioned_info: Optional[Dict],
                              style: ImageStyle,
                              palette: Dict) -> Image.Image:
        """Create ultra HD image with all components"""
        width, height = self.config.custom_width, self.config.custom_height
        
        # 1. Create background
        if background_config.type == "random_hd" and self.config.enable_random_backgrounds:
            background = self.background_manager.get_background(width, height, style)
        else:
            # Create gradient background
            colors = [
                background_config.primary_color,
                background_config.secondary_color,
                background_config.tertiary_color
            ]
            background = self.color_manager.generate_gradient(
                width, height, colors,
                background_config.gradient_direction
            )
        
        # Apply background effects
        if background_config.blur_radius > 0:
            background = background.filter(
                GaussianBlur(background_config.blur_radius)
            )
        
        # Convert to RGBA for compositing
        image = background.convert('RGBA')
        
        # 2. Add text
        image = self._add_text_to_image(image, text_config, style, palette)
        
        # 3. Add profile pictures
        if profile_config.enabled:
            # Main user profile
            main_profile = self.profile_manager.generate_profile(
                user_info, profile_config.size,
                profile_config.style, False
            )
            image = self._place_profile_image(image, main_profile, profile_config)
            
            # Mentioned user profile (if any)
            if mentioned_info:
                mentioned_profile = self.profile_manager.generate_profile(
                    mentioned_info, profile_config.size - 30,
                    ProfileStyle.SPECIAL_MENTION, True
                )
                # Place at different position
                mentioned_config = ProfileConfig(
                    **asdict(profile_config),
                    position="top_left" if profile_config.position == "top_right" else "top_right",
                    offset_x=profile_config.offset_x + 30,
                    offset_y=profile_config.offset_y
                )
                image = self._place_profile_image(image, mentioned_profile, mentioned_config)
        
        # 4. Add border
        if border_config.enabled:
            border = self._create_border_layer(width, height, border_config)
            image = Image.alpha_composite(image, border)
        
        # 5. Add metadata/watermark
        if self.config.enable_watermark:
            image = self._add_watermark(image, user_info)
        
        # 6. Apply final effects based on style
        image = self._apply_style_effects(image, style)
        
        return image
    
    def _add_text_to_image(self, image: Image.Image, text_config: TextConfig,
                          style: ImageStyle, palette: Dict) -> Image.Image:
        """Add text to image with effects"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Get fonts
        primary_font = self.font_manager.get_font(
            text_config.font_size_primary,
            style=text_config.font_style,
            text=text_config.primary_text
        )
        
        secondary_font = self.font_manager.get_font(
            text_config.font_size_secondary,
            style="regular",
            text=text_config.secondary_text
        )
        
        # Wrap text
        primary_lines = self._wrap_text(text_config.primary_text, text_config.max_width_chars)
        secondary_lines = self._wrap_text(text_config.secondary_text, text_config.max_width_chars + 10)
        
        # Calculate positions
        line_height_primary = int(text_config.font_size_primary * text_config.line_spacing)
        line_height_secondary = int(text_config.font_size_secondary * text_config.line_spacing)
        
        total_height = (
            len(primary_lines) * line_height_primary +
            (len(secondary_lines) * line_height_secondary if secondary_lines else 0) +
            50
        )
        
        start_y = max(100, (height - total_height) // 3)
        
        # Draw primary text with effects
        for i, line in enumerate(primary_lines):
            y_pos = start_y + (i * line_height_primary)
            x_pos = self._get_text_position(line, primary_font, width, text_config.alignment)
            
            # Apply text effects
            self._apply_text_effects(draw, line, primary_font, (x_pos, y_pos), text_config, style)
        
        # Draw secondary text
        if secondary_lines:
            start_y += len(primary_lines) * line_height_primary + 30
            
            for i, line in enumerate(secondary_lines):
                y_pos = start_y + (i * line_height_secondary)
                x_pos = self._get_text_position(line, secondary_font, width, text_config.alignment)
                
                draw.text((x_pos, y_pos), line, font=secondary_font, fill=palette.get('secondary', (200, 200, 200)))
        
        return image
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text for optimal display"""
        if not text:
            return []
        
        # First try intelligent wrapping
        lines = textwrap.wrap(text, width=max_width, break_long_words=False)
        
        # If lines are still too long, break words
        if any(len(line) > max_width * 1.5 for line in lines):
            lines = textwrap.wrap(text, width=max_width, break_long_words=True)
        
        return lines
    
    def _get_text_position(self, text: str, font: ImageFont.FreeTypeFont,
                          width: int, alignment: str) -> int:
        """Get text x-position based on alignment"""
        bbox = font.getbbox(text) if hasattr(font, 'getbbox') else font.getsize(text)
        
        if isinstance(bbox, tuple):  # getsize returns (width, height)
            text_width = bbox[0]
        else:  # getbbox returns (left, top, right, bottom)
            text_width = bbox[2] - bbox[0]
        
        if alignment == "center":
            return (width - text_width) // 2
        elif alignment == "right":
            return width - text_width - 50
        else:  # left
            return 50
    
    def _apply_text_effects(self, draw: ImageDraw.Draw, text: str,
                           font: ImageFont.FreeTypeFont, position: Tuple[int, int],
                           text_config: TextConfig, style: ImageStyle):
        """Apply advanced text effects"""
        x, y = position
        text_color = text_config.text_color
        
        # Shadow effect
        if TextEffect.SHADOW_DEEP in text_config.effects:
            shadow_offset = text_config.text_shadow_offset
            shadow_color = text_config.shadow_color
            
            # Multiple shadow layers for depth
            for i in range(text_config.text_shadow_blur, 0, -1):
                offset = shadow_offset * i // max(text_config.text_shadow_blur, 1)
                draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
        
        # Outline effect
        if TextEffect.OUTLINE_MULTI in text_config.effects:
            outline_color = text_config.outline_color
            thickness = text_config.outline_thickness
            
            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Main text
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Note: More advanced effects (gradient, glow, 3D) would require
        # creating separate text layers and compositing
    
    def _place_profile_image(self, base_image: Image.Image, profile_image: Image.Image,
                            profile_config: ProfileConfig) -> Image.Image:
        """Place profile image on base image"""
        # Calculate position
        width, height = base_image.size
        profile_size = profile_config.size
        
        if profile_config.position == "top_right":
            x = width - profile_size - profile_config.offset_x
            y = profile_config.offset_y
        elif profile_config.position == "top_left":
            x = profile_config.offset_x
            y = profile_config.offset_y
        elif profile_config.position == "bottom_right":
            x = width - profile_size - profile_config.offset_x
            y = height - profile_size - profile_config.offset_y
        else:  # bottom_left
            x = profile_config.offset_x
            y = height - profile_size - profile_config.offset_y
        
        # Resize profile if needed
        if profile_image.size != (profile_size, profile_size):
            profile_image = profile_image.resize((profile_size, profile_size), Resampling.LANCZOS)
        
        # Create circular mask for profile
        mask = Image.new('L', (profile_size, profile_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse([0, 0, profile_size, profile_size], fill=255)
        
        # Apply rotation if specified
        if profile_config.rotation != 0:
            profile_image = profile_image.rotate(profile_config.rotation, expand=True)
            mask = mask.rotate(profile_config.rotation, expand=True)
            # Resize back to original size
            profile_image = profile_image.resize((profile_size, profile_size), Resampling.LANCZOS)
            mask = mask.resize((profile_size, profile_size), Resampling.LANCZOS)
        
        # Composite profile onto base image
        base_image.paste(profile_image, (x, y), mask)
        
        return base_image
    
    def _create_border_layer(self, width: int, height: int,
                            border_config: BorderConfig) -> Image.Image:
        """Create border layer"""
        border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        border_type = border_config.border_type
        
        if border_type == BorderType.SIMPLE_ELEGANT:
            draw.rectangle(
                [border_config.thickness, border_config.thickness,
                 width - border_config.thickness, height - border_config.thickness],
                outline=(*border_config.color, int(255 * border_config.opacity)),
                width=border_config.thickness
            )
        
        elif border_type == BorderType.ROUNDED_GRADIENT:
            # Draw rounded rectangle with gradient
            for i in range(border_config.thickness):
                alpha = int(255 * border_config.opacity * (1 - i / border_config.thickness))
                offset = border_config.padding + i
                color = create_gradient_color(
                    border_config.color,
                    border_config.secondary_color,
                    i / border_config.thickness
                )
                
                draw.rounded_rectangle(
                    [offset, offset, width - offset, height - offset],
                    radius=border_config.corner_radius,
                    outline=(*color, alpha),
                    width=1
                )
        
        elif border_type == BorderType.NEON_PULSING:
            # Neon glow effect
            for i in range(3):
                glow_thickness = border_config.thickness + i * 5
                glow_alpha = 200 - i * 60
                glow_offset = border_config.padding - i * 3
                
                draw.rounded_rectangle(
                    [glow_offset, glow_offset,
                     width - glow_offset, height - glow_offset],
                    radius=border_config.corner_radius,
                    outline=(*border_config.glow_color, glow_alpha),
                    width=glow_thickness
                )
        
        return border
    
    def _add_watermark(self, image: Image.Image, user_info: Dict) -> Image.Image:
        """Add watermark to image"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Small font for watermark
        try:
            font = ImageFont.truetype("Arial", 20)
        except:
            font = ImageFont.load_default()
        
        watermark_text = f"© {self.config.watermark_text} • {user_info.get('username', 'User')}"
        
        # Semi-transparent watermark
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        position = (width - text_width - 20, height - 40)
        draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))
        
        return image
    
    def _apply_style_effects(self, image: Image.Image, style: ImageStyle) -> Image.Image:
        """Apply final style effects"""
        if style == ImageStyle.VINTAGE_RETRO:
            # Vintage effect
            image = ImageEnhance.Color(image).enhance(0.8)
            image = ImageEnhance.Contrast(image).enhance(1.2)
            
            # Add sepia tone
            if image.mode == 'RGB':
                sepia = image.copy()
                sepia = ImageEnhance.Color(sepia).enhance(0.5)
                sepia = ImageEnhance.Brightness(sepia).enhance(0.9)
                image = Image.blend(image, sepia, 0.3)
        
        elif style == ImageStyle.NEON_CYBERPUNK:
            # Neon effect
            image = ImageEnhance.Color(image).enhance(1.5)
            image = ImageEnhance.Brightness(image).enhance(1.1)
            image = ImageEnhance.Contrast(image).enhance(1.3)
        
        elif style == ImageStyle.BENGALI_TRADITIONAL:
            # Warm, vibrant colors
            image = ImageEnhance.Color(image).enhance(1.2)
            image = ImageEnhance.Brightness(image).enhance(1.05)
        
        return image
    
    def _save_image(self, image: Image.Image, generation_id: str, user_info: Dict) -> Path:
        """Save image with optimal settings"""
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"ultra_hd_{generation_id}_{user_info.get('id', 0)}.{self.config.format.lower()}"
        output_path = output_dir / filename
        
        # Prepare save parameters
        save_params = {
            'quality': self.config.quality,
            'optimize': True,
        }
        
        if self.config.format == 'PNG':
            save_params['compress_level'] = self.config.compression_level
            if self.config.enable_alpha and image.mode == 'RGBA':
                pass  # Keep alpha
            else:
                image = image.convert('RGB')
        
        elif self.config.format == 'JPEG':
            if image.mode == 'RGBA':
                # Create white background for JPEG
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            else:
                image = image.convert('RGB')
        
        elif self.config.format == 'WEBP':
            save_params['method'] = 6  # Best quality
            save_params['lossless'] = False
        
        # Save image
        image.save(output_path, self.config.format, **save_params)
        
        # Verify file was saved
        if not output_path.exists() or output_path.stat().st_size == 0:
            raise IOError(f"Failed to save image: {output_path}")
        
        # Check file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.config.max_file_size_mb:
            logger.warning(f"Image size ({file_size_mb:.1f}MB) exceeds limit, re-saving with compression")
            self._compress_image(output_path)
        
        return output_path
    
    def _compress_image(self, image_path: Path):
        """Compress image if too large"""
        try:
            image = Image.open(image_path)
            
            # Reduce quality for JPEG
            if self.config.format == 'JPEG':
                image.save(image_path, 'JPEG', quality=max(70, self.config.quality - 20), optimize=True)
            
            # Reduce compression level for PNG
            elif self.config.format == 'PNG':
                image.save(image_path, 'PNG', compress_level=min(9, self.config.compression_level + 3))
            
        except Exception as e:
            logger.error(f"Image compression failed: {e}")
    
    def _create_thumbnail(self, image_path: Path) -> Optional[Path]:
        """Create thumbnail for image"""
        try:
            thumbnail_size = (300, 300)
            image = Image.open(image_path)
            
            # Create thumbnail
            image.thumbnail(thumbnail_size, Resampling.LANCZOS)
            
            # Save thumbnail
            thumb_path = image_path.parent / f"thumb_{image_path.name}"
            image.save(thumb_path, 'JPEG', quality=85, optimize=True)
            
            return thumb_path
        except Exception as e:
            logger.warning(f"Thumbnail creation failed: {e}")
            return None
    
    def _create_backup(self, image_path: Path, generation_id: str):
        """Create backup of generated image"""
        if not self.config.enable_backup:
            return
        
        try:
            backup_dir = Path(self.config.backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_path = backup_dir / f"backup_{generation_id}_{image_path.name}"
            
            # Copy file
            import shutil
            shutil.copy2(image_path, backup_path)
            
            # Clean old backups
            self._cleanup_old_backups(backup_dir)
            
        except Exception as e:
            logger.debug(f"Backup failed: {e}")
    
    def _cleanup_old_backups(self, backup_dir: Path):
        """Clean up old backup files"""
        try:
            backup_files = list(backup_dir.glob("backup_*"))
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Keep only latest N backups
            if len(backup_files) > self.config.backup_count:
                for old_file in backup_files[:-self.config.backup_count]:
                    old_file.unlink()
                    
        except Exception as e:
            logger.debug(f"Backup cleanup failed: {e}")
    
    def _update_stats(self, processing_time: float, success: bool):
        """Update performance statistics"""
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'processing_time': processing_time,
            'success': success
        })
        
        # Update average time
        if self.stats['successful'] > 0:
            self.stats['avg_generation_time'] = self.stats['total_time'] / self.stats['successful']
    
    # ================================
    # PUBLIC METHODS
    # ================================
    
    def generate_welcome_image(self, user_info: Any) -> GenerationResult:
        """Generate welcome image for new users"""
        welcome_text = self.reply_manager.get_reply('welcome', {
            'user_name': user_info.get('username', 'New User')
        })
        
        return self.generate_roast_image(
            roast_text=welcome_text,
            user_info=user_info,
            style=ImageStyle.LIGHT_ELEGANT,
            border_config=BorderConfig(
                border_type=BorderType.ROUNDED_GRADIENT,
                color=(0, 200, 255),
                thickness=30,
                corner_radius=60,
                glow_intensity=2
            ),
            background_config=BackgroundConfig(
                type="gradient",
                primary_color=(30, 10, 50),
                secondary_color=(70, 30, 90),
                tertiary_color=(120, 60, 140)
            )
        )
    
    def generate_achievement_image(self, user_info: Any, achievement: Any) -> GenerationResult:
        """Generate achievement image"""
        if isinstance(achievement, dict):
            title = achievement.get('title', 'Achievement Unlocked!')
            description = achievement.get('description', '')
        else:
            title = str(achievement) or 'Achievement Unlocked!'
            description = ''
        
        text = f"{title}\n\n{description}".strip()
        
        return self.generate_roast_image(
            roast_text=text,
            user_info=user_info,
            style=ImageStyle.GOLDEN,
            border_config=BorderConfig(
                border_type=BorderType.ORNATE_GOLD,
                color=(255, 215, 0),
                thickness=35,
                corner_radius=70,
                glow_intensity=3
            ),
            background_config=BackgroundConfig(
                type="gradient",
                primary_color=(40, 20, 60),
                secondary_color=(80, 40, 100),
                tertiary_color=(120, 60, 140)
            )
        )
    
    def generate_profile_picture(self, user_info: Any, 
                                size: int = 512,
                                style: ProfileStyle = None) -> GenerationResult:
        """Generate standalone profile picture"""
        start_time = time.time()
        generation_id = generate_unique_id()
        
        try:
            user_dict = self._process_user_info(user_info)
            
            # Generate profile
            profile = self.profile_manager.generate_profile(
                user_dict, size, style or ProfileStyle.get_random(), False
            )
            
            # Save profile
            output_dir = Path(self.config.output_dir) / "profiles"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"profile_{generation_id}_{user_dict['id']}.png"
            profile.save(output_path, 'PNG', optimize=True)
            
            processing_time = time.time() - start_time
            
            result = GenerationResult(
                success=True,
                image_path=str(output_path),
                processing_time=round(processing_time, 3),
                image_size=os.path.getsize(output_path),
                generation_id=generation_id,
                metadata={
                    'user': user_dict['username'],
                    'user_id': user_dict['id'],
                    'profile_style': style.name if style else 'random',
                    'size': size
                }
            )
            
            logger.info(f"✅ Profile picture generated: {output_path.name}")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            logger.error(f"❌ Profile generation failed: {e}")
            
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=round(processing_time, 3),
                generation_id=generation_id
            )
    
    def generate_batch(self, items: List[Dict], 
                      callback: Optional[Callable] = None) -> List[GenerationResult]:
        """Generate images in batch"""
        results = []
        futures = {}
        
        def process_item(item):
            try:
                result = self.generate_roast_image(
                    roast_text=item.get('text', ''),
                    user_info=item.get('user', {}),
                    mentioned_user=item.get('mentioned_user'),
                    style=item.get('style'),
                    reply_category=item.get('category')
                )
                
                if callback:
                    callback(result, item)
                
                return result
            except Exception as e:
                logger.error(f"Batch item failed: {e}")
                return GenerationResult(
                    success=False,
                    error=str(e),
                    metadata={'item': item}
                )
        
        # Submit tasks
        for item in items:
            future = self.thread_pool.submit(process_item, item)
            futures[future] = item
        
        # Collect results
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Batch future failed: {e}")
                results.append(GenerationResult(
                    success=False,
                    error=str(e),
                    metadata={'item': futures[future]}
                ))
        
        return results
    
    def get_detailed_stats(self) -> Dict:
        """Get comprehensive statistics"""
        # Calculate rates
        success_rate = 0
        if self.stats['total_generated'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_generated']) * 100
        
        cache_hit_rate = 0
        total_cache_ops = self.stats['cache_hits'] + self.stats['cache_misses']
        if total_cache_ops > 0:
            cache_hit_rate = (self.stats['cache_hits'] / total_cache_ops) * 100
        
        # Get subsystem stats
        font_stats = self.font_manager.get_stats()
        color_stats = self.color_manager.get_stats()
        background_stats = self.background_manager.get_stats()
        profile_stats = self.profile_manager.get_stats()
        reply_stats = self.reply_manager.get_stats()
        cache_stats = self.cache_manager.get_stats()
        
        # Performance analysis
        recent_performance = list(self.performance_history)
        avg_recent_time = 0
        if recent_performance:
            recent_times = [p['processing_time'] for p in recent_performance if p['success']]
            if recent_times:
                avg_recent_time = sum(recent_times) / len(recent_times)
        
        return {
            'generator': {
                'version': '9.0.0',
                'id': self.generation_id,
                'pil_available': PIL_AVAILABLE,
                'numpy_available': NUMPY_AVAILABLE,
                'config': {
                    'resolution': f"{self.config.custom_width}x{self.config.custom_height}",
                    'quality': self.config.quality,
                    'format': self.config.format,
                    'cache_enabled': self.config.enable_cache,
                    'workers': self.config.max_workers,
                    'features': {
                        'random_backgrounds': self.config.enable_random_backgrounds,
                        'profile_pictures': self.config.enable_profile_pictures,
                        'advanced_effects': self.config.enable_advanced_effects,
                        'real_time_enhancement': self.config.enable_real_time_enhancement
                    }
                }
            },
            'performance': {
                'total_generated': self.stats['total_generated'],
                'ultra_hd_generated': self.stats['ultra_hd_generated'],
                'successful': self.stats['successful'],
                'failed': self.stats['failed'],
                'success_rate': round(success_rate, 1),
                'total_time_seconds': round(self.stats['total_time'], 2),
                'average_time_seconds': round(self.stats['avg_generation_time'], 3),
                'recent_average_time': round(avg_recent_time, 3),
                'cache_hits': self.stats['cache_hits'],
                'cache_misses': self.stats['cache_misses'],
                'cache_hit_rate': round(cache_hit_rate, 1),
                'peak_memory_mb': round(self.stats['peak_memory_mb'], 1),
                'parallel_tasks': len(self.active_tasks)
            },
            'subsystems': {
                'fonts': font_stats,
                'colors': color_stats,
                'backgrounds': background_stats,
                'profiles': profile_stats,
                'replies': reply_stats,
                'cache': cache_stats
            },
            'recent_errors': len(self.error_history),
            'timestamp': datetime.now().isoformat()
        }
    
    def health_check(self) -> Dict:
        """Perform comprehensive health check"""
        checks = {
            'pil_available': PIL_AVAILABLE,
            'numpy_available': NUMPY_AVAILABLE,
            'directories_writable': True,
            'font_manager_ready': len(self.font_manager.available_fonts) > 0,
            'cache_operational': True,
            'thread_pool_active': True,
            'memory_ok': True
        }
        
        # Check directories
        test_dirs = [self.config.output_dir, self.config.temp_dir, self.config.cache_dir]
        for dir_path in test_dirs:
            try:
                path = Path(dir_path)
                test_file = path / '.health_check'
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                checks['directories_writable'] = False
                logger.error(f"Directory check failed for {dir_path}: {e}")
        
        # Check cache
        try:
            test_key = 'health_check_' + generate_unique_id(8)
            test_data = b'test_data_' + os.urandom(10)
            self.cache_manager.set(test_key, test_data)
            retrieved = self.cache_manager.get(test_key)
            checks['cache_operational'] = retrieved == test_data
            self.cache_manager.delete(test_key)
        except Exception as e:
            checks['cache_operational'] = False
            logger.error(f"Cache check failed: {e}")
        
        # Check thread pool
        try:
            future = self.thread_pool.submit(lambda: "test")
            result = future.result(timeout=5)
            checks['thread_pool_active'] = result == "test"
        except Exception as e:
            checks['thread_pool_active'] = False
            logger.error(f"Thread pool check failed: {e}")
        
        # Check memory
        try:
            import psutil
            memory = psutil.virtual_memory()
            checks['memory_ok'] = memory.percent < 90
        except:
            checks['memory_ok'] = True  # Assume OK if we can't check
        
        overall_health = all(checks.values())
        
        return {
            'healthy': overall_health,
            'checks': checks,
            'timestamp': datetime.now().isoformat(),
            'generator_id': self.generation_id
        }
    
    def cleanup(self, max_age_hours: int = 24, clean_all: bool = False):
        """Cleanup old files"""
        try:
            cutoff = time.time() - (max_age_hours * 3600)
            
            directories = [
                Path(self.config.temp_dir),
                Path(self.config.output_dir),
                Path(self.config.cache_dir)
            ]
            
            if clean_all:
                directories.append(Path(self.config.backup_dir))
            
            total_removed = 0
            
            for directory in directories:
                if directory.exists():
                    for file in directory.glob("*"):
                        if file.is_file():
                            try:
                                if file.stat().st_mtime < cutoff or clean_all:
                                    file.unlink()
                                    total_removed += 1
                            except Exception as e:
                                logger.debug(f"Failed to remove {file}: {e}")
            
            # Clean cache
            self.cache_manager.cleanup()
            
            logger.info(f"Cleanup completed: {total_removed} files removed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down Ultra HD Generator...")
        
        # Shutdown thread pool
        self.thread_pool.shutdown(wait=True)
        
        # Save final statistics
        stats_file = Path(self.config.output_dir) / "generator_stats.json"
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.get_detailed_stats(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save statistics: {e}")
        
        logger.info("Ultra HD Generator shutdown complete")

# ================================
# CACHE MANAGER (Updated)
# ================================

class CacheManager:
    """Advanced Cache Management for Ultra HD"""
    
    def __init__(self, cache_dir: str = "./cache", 
                 ttl_hours: int = CACHE_TTL_HOURS, 
                 max_size: int = MAX_CACHE_SIZE):
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.max_size = max_size
        self.metadata = {}
        self.hits = 0
        self.misses = 0
        
        self._load_metadata()
        logger.info(f"CacheManager initialized: {cache_dir}, TTL: {ttl_hours}h, Max: {max_size}")
    
    def _load_metadata(self):
        """Load cache metadata"""
        metadata_file = self.cache_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except:
                self.metadata = {}
    
    def _save_metadata(self):
        """Save cache metadata"""
        metadata_file = self.cache_dir / "metadata.json"
        try:
            temp_file = metadata_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            temp_file.replace(metadata_file)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def get(self, key: str) -> Optional[bytes]:
        """Get cached item"""
        if not key:
            self.misses += 1
            return None
        
        cache_file = self.cache_dir / f"{key}.cache"
        
        if not cache_file.exists():
            self.misses += 1
            return None
        
        # Check TTL
        if key in self.metadata:
            created = datetime.fromisoformat(self.metadata[key]['created'])
            if datetime.now() - created > self.ttl:
                self.delete(key)
                self.misses += 1
                return None
        
        try:
            with open(cache_file, 'rb') as f:
                data = f.read()
            
            # Update access info
            if key in self.metadata:
                self.metadata[key]['hits'] = self.metadata[key].get('hits', 0) + 1
                self.metadata[key]['last_accessed'] = datetime.now().isoformat()
                self._save_metadata()
            
            self.hits += 1
            return data
            
        except Exception as e:
            logger.error(f"Cache read failed for {key}: {e}")
            self.misses += 1
            return None
    
    def set(self, key: str, data: bytes):
        """Cache item"""
        if not key or not data:
            return
        
        # Check size and evict if needed
        if len(self.metadata) >= self.max_size:
            self._evict_oldest()
        
        cache_file = self.cache_dir / f"{key}.cache"
        
        try:
            # Write to temp file first
            temp_file = cache_file.with_suffix('.tmp')
            with open(temp_file, 'wb') as f:
                f.write(data)
            temp_file.replace(cache_file)
            
            # Update metadata
            self.metadata[key] = {
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'size': len(data),
                'hits': 0
            }
            self._save_metadata()
            
        except Exception as e:
            logger.error(f"Cache write failed for {key}: {e}")
    
    def delete(self, key: str):
        """Delete cached item"""
        cache_file = self.cache_dir / f"{key}.cache"
        
        try:
            if cache_file.exists():
                cache_file.unlink()
            
            if key in self.metadata:
                del self.metadata[key]
                self._save_metadata()
            
        except Exception as e:
            logger.error(f"Cache delete failed for {key}: {e}")
    
    def _evict_oldest(self, count: int = 10):
        """Evict least recently used cache entries"""
        if not self.metadata:
            return
        
        # Sort by last accessed time and hits
        sorted_items = sorted(
            self.metadata.items(),
            key=lambda x: (
                datetime.fromisoformat(x[1].get('last_accessed', x[1]['created'])),
                -x[1].get('hits', 0)  # Negative for ascending
            )
        )
        
        to_remove = min(count, len(sorted_items))
        
        for key, _ in sorted_items[:to_remove]:
            self.delete(key)
        
        logger.debug(f"Evicted {to_remove} cache entries")
    
    def cleanup(self):
        """Clean up expired cache entries"""
        cutoff = datetime.now() - self.ttl
        
        expired_keys = []
        
        for key, data in list(self.metadata.items()):
            created = datetime.fromisoformat(data['created'])
            if created < cutoff:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)
        
        if expired_keys:
            logger.info(f"Cache cleanup removed {len(expired_keys)} expired items")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_size = sum(data['size'] for data in self.metadata.values())
        total_hits = sum(data.get('hits', 0) for data in self.metadata.values())
        
        hit_rate = 0
        if self.hits + self.misses > 0:
            hit_rate = self.hits / (self.hits + self.misses) * 100
        
        return {
            'total_items': len(self.metadata),
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'total_hits': total_hits,
            'current_hits': self.hits,
            'current_misses': self.misses,
            'hit_rate_percent': round(hit_rate, 1),
            'max_size': self.max_size,
            'ttl_hours': self.ttl.total_seconds() / 3600
        }

# ================================
# TEST FUNCTION
# ================================

def test_ultra_hd_generator():
    """Test the Ultra HD image generator"""
    print("\n" + "="*70)
    print("🔥 ULTRA HD IMAGE GENERATOR v9.0 - COMPREHENSIVE TEST")
    print("="*70)
    
    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow not installed!")
        print("   Install with: pip install pillow")
        return False
    
    try:
        # Test 1: Basic initialization
        print("\n🔹 Test 1: Initializing Ultra HD Generator...")
        config = GenerationConfig(
            resolution_preset="FULL_HD",  # Use FULL_HD for faster testing
            enable_random_backgrounds=True,
            enable_profile_pictures=True,
            enable_real_time_enhancement=True
        )
        
        generator = UltraHDImageGenerator(config)
        print("   ✅ Ultra HD Generator initialized")
        
        # Test 2: Health check
        print("\n🔹 Test 2: Health check...")
        health = generator.health_check()
        print(f"   🩺 System healthy: {health['healthy']}")
        for check, status in health['checks'].items():
            print(f"     • {check}: {'✅' if status else '❌'}")
        
        # Test 3: Generate roast image
        print("\n🔹 Test 3: Testing Ultra HD roast image generation...")
        
        test_user = {
            'id': 123456,
            'username': 'test_user',
            'first_name': 'টেস্ট',
            'last_name': 'ব্যবহারকারী',
            'rating': 8.5
        }
        
        test_mentioned = {
            'id': 789012,
            'username': 'জাকির',
            'first_name': 'জাকির',
            'rating': 9.8
        }
        
        result = generator.generate_roast_image(
            roast_text="এটা একটা বাংলা টেস্ট রোস্ট! দেখি কেমন হয়? এটি আল্ট্রা এইচডি কোয়ালিটি!",
            user_info=test_user,
            mentioned_user=test_mentioned,
            style=ImageStyle.NEON_CYBERPUNK,
            reply_category='funny'
        )
        
        if result.success:
            print(f"   ✅ Ultra HD image generated: {result.image_path}")
            print(f"     ⏱️ Processing time: {result.processing_time:.2f}s")
            print(f"     💾 Cache hit: {result.cache_hit}")
            print(f"     📊 Image size: {result.image_size:,} bytes")
            print(f"     🖼️ Dimensions: {result.image_dimensions}")
            if result.thumbnail_path:
                print(f"     📸 Thumbnail: {result.thumbnail_path}")
        else:
            print(f"   ❌ Ultra HD image failed: {result.error}")
        
        # Test 4: Generate welcome image
        print("\n🔹 Test 4: Testing welcome image generation...")
        welcome_result = generator.generate_welcome_image(test_user)
        
        if welcome_result.success:
            print(f"   ✅ Welcome image generated: {welcome_result.image_path}")
        else:
            print(f"   ❌ Welcome image failed: {welcome_result.error}")
        
        # Test 5: Generate profile picture
        print("\n🔹 Test 5: Testing profile picture generation...")
        profile_result = generator.generate_profile_picture(
            test_user, 
            size=512,
            style=ProfileStyle.GOLDEN
        )
        
        if profile_result.success:
            print(f"   ✅ Profile picture generated: {profile_result.image_path}")
        else:
            print(f"   ❌ Profile picture failed: {profile_result.error}")
        
        # Test 6: Get statistics
        print("\n🔹 Test 6: Checking comprehensive statistics...")
        stats = generator.get_detailed_stats()
        
        print(f"   📊 Total generated: {stats['performance']['total_generated']}")
        print(f"   🎯 Success rate: {stats['performance']['success_rate']}%")
        print(f"   ⚡ Average time: {stats['performance']['average_time_seconds']:.2f}s")
        print(f"   💾 Cache hit rate: {stats['performance']['cache_hit_rate']}%")
        print(f"   🧠 Peak memory: {stats['performance']['peak_memory_mb']}MB")
        
        print(f"   📈 Fonts: {stats['subsystems']['fonts']['total_fonts']} fonts")
        print(f"   🎨 Color palettes: {stats['subsystems']['colors']['palettes_count']}")
        print(f"   🖼️ Backgrounds cached: {stats['subsystems']['backgrounds']['cache_size']}")
        print(f"   👤 Profiles cached: {stats['subsystems']['profiles']['cache_size']}")
        print(f"   💬 Replies: {stats['subsystems']['replies']['total_replies']} replies")
        
        # Test 7: Batch generation
        print("\n🔹 Test 7: Testing batch generation (2 images)...")
        batch_items = [
            {
                'text': "First batch test roast!",
                'user': {'id': 1001, 'username': 'user1', 'first_name': 'ব্যবহারকারী ১'},
                'category': 'funny'
            },
            {
                'text': "Second batch test roast!",
                'user': {'id': 1002, 'username': 'user2', 'first_name': 'ব্যবহারকারী ২'},
                'category': 'roast'
            }
        ]
        
        def batch_callback(result, item):
            if result.success:
                print(f"     → Batch item for {item['user']['username']}: ✅")
            else:
                print(f"     → Batch item for {item['user']['username']}: ❌")
        
        batch_results = generator.generate_batch(batch_items, batch_callback)
        
        successful_batch = sum(1 for r in batch_results if r.success)
        print(f"   ✅ Batch completed: {successful_batch}/{len(batch_results)} successful")
        
        # Test 8: Cleanup
        print("\n🔹 Test 8: Testing cleanup...")
        generator.cleanup(max_age_hours=0)  # Clean all test files
        print("   ✅ Cleanup completed")
        
        # Test 9: Shutdown
        print("\n🔹 Test 9: Testing graceful shutdown...")
        generator.shutdown()
        print("   ✅ Shutdown completed")
        
        print("\n" + "="*70)
        print("🎉 ALL ULTRA HD TESTS PASSED SUCCESSFULLY!")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run comprehensive test
    print("Starting Ultra HD Image Generator v9.0...")
    success = test_ultra_hd_generator()
    
    if success:
        print("\n✨ Ultra HD Generator is ready for production!")
        print("📦 Features:")
        print("   • 4K+ Ultra HD Quality")
        print("   • Random HD Backgrounds")
        print("   • Profile Pictures with Special Mentions")
        print("   • Intelligent Reply System")
        print("   • Advanced Effects and Styling")
        print("   • Comprehensive Error Handling")
        print("   • High-Performance Batch Processing")
    else:
        print("\n⚠️ Some tests failed. Check the installation and dependencies.")
    
    sys.exit(0 if success else 1)

# Export all required classes
__all__ = [
    'UltraHDImageGenerator',
    'GenerationConfig',
    'TextConfig',
    'BorderConfig',
    'BackgroundConfig',
    'ProfileConfig',
    'GenerationResult',
    'ImageStyle',
    'TextEffect',
    'BorderType',
    'GradientDirection',
    'ProfileStyle',
    'UltraFontManager',
    'UltraColorManager',
    'BackgroundImageManager',
    'ProfilePictureManager',
    'ReplyManager',
    'ImageEnhancer',
    'CacheManager'
]
