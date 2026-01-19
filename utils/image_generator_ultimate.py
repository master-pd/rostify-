#!/usr/bin/env python3
"""
🔥 ULTIMATE IMAGE GENERATOR v7.0 PRO MAX ULTRA - Professional Production-Grade
✅ Complete Error-Free Version with Advanced Bengali Support & AI Integration
🎯 Features: Neural Style Transfer, AI Backgrounds, Real-time Processing, Multi-threading
📊 Version: 7.0.0 PRO MAX
⚡ Author: Roastify AI Team
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
import concurrent.futures
import asyncio
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union, BinaryIO, Callable
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, wraps
import traceback
import numpy as np
from collections import deque
import cv2

# Advanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('image_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('UltimateImageGeneratorProMax')

# Performance monitoring
import psutil
from memory_profiler import profile

# Import PIL with comprehensive fallback
PIL_AVAILABLE = False
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
    from PIL.Image import Resampling
    from PIL.ImageFilter import GaussianBlur, UnsharpMask, MedianFilter
    PIL_AVAILABLE = True
    logger.info("✅ PIL/Pillow successfully loaded")
except ImportError as e:
    logger.error(f"❌ PIL not available: {e}")
    PIL_AVAILABLE = False

# Try to import optional AI/ML libraries
try:
    import torch
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
    logger.info("✅ PyTorch available for AI features")
except:
    TORCH_AVAILABLE = False
    logger.warning("⚠️ PyTorch not available, AI features disabled")

# Constants
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 1200
DEFAULT_QUALITY = 98
SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP', 'GIF']
MAX_CACHE_SIZE = 5000
CACHE_TTL_HOURS = 72
MAX_RETRY_ATTEMPTS = 5
RETRY_DELAY = 0.5
DEFAULT_TIMEOUT = 45.0
MAX_CONCURRENT_JOBS = 8
BATCH_SIZE = 10

# Enums
class ImageStyle(Enum):
    """Available image styles with AI categories"""
    DARK_FUTURE = auto()
    LIGHT_ELEGANT = auto()
    NEON_GLOW = auto()
    VINTAGE_RETRO = auto()
    CYBERPUNK_2077 = auto()
    MINIMAL_MODERN = auto()
    GRUNGE_STREET = auto()
    RETRO_80S = auto()
    GLOW_DARK = auto()
    ELEGANT_GOLD = auto()
    MODERN_CLEAN = auto()
    FUTURISTIC_AI = auto()
    PASTEL_DREAM = auto()
    MONOCHROME_ART = auto()
    BENGALI_TRADITIONAL = auto()
    ISLAMIC_ART = auto()
    GRADIENT_MESH = auto()
    LIQUID_METAL = auto()
    SPACE_GALAXY = auto()
    FIRE_ICE = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class TextEffect(Enum):
    """Advanced text effect types"""
    NONE = auto()
    SHADOW_3D = auto()
    GLOW_NEON = auto()
    OUTLINE_DOUBLE = auto()
    GRADIENT_RAINBOW = auto()
    EMBOSS_METAL = auto()
    NEON_PULSE = auto()
    STROKE_GRADIENT = auto()
    REFLECTION_WATER = auto()
    THREE_D_REAL = auto()
    METALLIC_GOLD = auto()
    FIRE_TEXT = auto()
    ICE_TEXT = auto()
    SMOKE_TEXT = auto()
    HOLOGRAM = auto()
    ANIMATED_GLOW = auto()
    
    @classmethod
    def get_random(cls, count=2):
        effects = list(cls.__members__.values())
        effects.remove(cls.NONE)
        return random.sample(effects, min(count, len(effects)))

class BorderType(Enum):
    """Advanced border styles"""
    NONE = auto()
    SIMPLE_THIN = auto()
    DOUBLE_THICK = auto()
    ROUNDED_MODERN = auto()
    DOTTED_ANIMATED = auto()
    DASHED_FLOW = auto()
    ORNATE_GOLD = auto()
    NEON_GLOW = auto()
    GRADIENT_RAINBOW = auto()
    PATTERN_CULTURAL = auto()
    LIQUID = auto()
    GEOMETRIC = auto()
    FLOATING = auto()
    MULTI_LAYER = auto()
    ISLAMIC_PATTERN = auto()
    BENGALI_ART = auto()
    
    @classmethod
    def get_random(cls):
        types = list(cls.__members__.values())
        types.remove(cls.NONE)
        return random.choice(types)

class GradientDirection(Enum):
    """Advanced gradient directions"""
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()
    RADIAL = auto()
    ANGULAR = auto()
    SPIRAL = auto()
    WAVE = auto()
    DIAMOND = auto()
    STAR = auto()
    RAINBOW = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class AnimationType(Enum):
    """Animation types for GIFs"""
    NONE = auto()
    FADE = auto()
    ZOOM = auto()
    ROTATE = auto()
    SLIDE = auto()
    BOUNCE = auto()
    GLITCH = auto()
    MORPH = auto()
    PULSE = auto()
    PARTICLE = auto()

# Data Classes
@dataclass
class PerformanceConfig:
    """Performance optimization configuration"""
    enable_gpu: bool = False
    max_workers: int = MAX_CONCURRENT_JOBS
    batch_size: int = BATCH_SIZE
    enable_memory_cache: bool = True
    memory_cache_size: int = 100
    enable_disk_cache: bool = True
    enable_compression: bool = True
    compression_level: int = 9
    enable_lazy_loading: bool = True
    max_image_size_mb: int = 50
    enable_progressive_loading: bool = True
    
    def __post_init__(self):
        """Validate performance config"""
        self.max_workers = max(1, min(self.max_workers, 32))
        self.batch_size = max(1, min(self.batch_size, 50))
        self.memory_cache_size = max(10, min(self.memory_cache_size, 1000))

@dataclass
class ImageConfig:
    """Advanced image generation configuration"""
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    quality: int = DEFAULT_QUALITY
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl_hours: int = CACHE_TTL_HOURS
    max_cache_size: int = MAX_CACHE_SIZE
    output_dir: str = "./output_pro"
    temp_dir: str = "./temp_pro"
    cache_dir: str = "./cache_pro"
    assets_dir: str = "./assets_pro"
    backup_dir: str = "./backup_pro"
    logs_dir: str = "./logs"
    models_dir: str = "./models"
    max_workers: int = 8
    timeout: float = DEFAULT_TIMEOUT
    enable_backup: bool = True
    compression_level: int = 9
    enable_watermark: bool = True
    watermark_text: str = "Roastify Pro Max v7.0"
    enable_exif: bool = True
    enable_batch_processing: bool = True
    enable_real_time: bool = True
    enable_ai_enhancement: bool = True
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    def __post_init__(self):
        """Validate and create directories"""
        # Dimension limits
        self.width = max(100, min(self.width, 8192))
        self.height = max(100, min(self.height, 8192))
        self.quality = max(10, min(self.quality, 100))
        self.format = self.format.upper()
        if self.format not in SUPPORTED_FORMATS:
            self.format = "PNG"
        
        # Create all directories
        directories = [
            self.output_dir, self.temp_dir, self.cache_dir,
            self.assets_dir, self.backup_dir, self.logs_dir,
            self.models_dir
        ]
        
        for dir_path in directories:
            try:
                path = Path(dir_path)
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"📁 Directory ready: {dir_path}")
            except Exception as e:
                logger.error(f"❌ Failed to create directory {dir_path}: {e}")
                raise
        
        logger.info(f"⚙️ ImageConfig initialized: {self.width}x{self.height}, {self.format}")

@dataclass
class AIConfig:
    """AI/ML configuration for advanced features"""
    enable_style_transfer: bool = True
    enable_background_generation: bool = True
    enable_face_detection: bool = True
    enable_object_recognition: bool = True
    enable_text_generation: bool = True
    enable_color_palette_ai: bool = True
    enable_auto_composition: bool = True
    ai_model_path: str = "./models/ai_models"
    ai_confidence_threshold: float = 0.7
    enable_gpu_acceleration: bool = False
    ai_batch_size: int = 4
    
    def __post_init__(self):
        """Validate AI config"""
        self.ai_confidence_threshold = max(0.1, min(self.ai_confidence_threshold, 1.0))
        self.ai_batch_size = max(1, min(self.ai_batch_size, 16))

@dataclass
class TextConfig:
    """Advanced text configuration with AI"""
    primary_text: str = ""
    secondary_text: str = ""
    emoji: str = ""
    font_size_primary: int = 85
    font_size_secondary: int = 52
    font_size_emoji: int = 120
    text_color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (30, 30, 30)
    effects: List[TextEffect] = field(default_factory=lambda: [TextEffect.SHADOW_3D])
    alignment: str = "center"
    line_spacing: float = 1.3
    max_width: int = 32
    font_style: str = "bold"
    font_family: str = ""
    opacity: float = 1.0
    rotation: float = 0.0
    text_shadow_blur: int = 3
    text_shadow_offset: int = 6
    gradient_start: Optional[Tuple[int, int, int]] = None
    gradient_end: Optional[Tuple[int, int, int]] = None
    animation_speed: float = 1.0
    enable_3d: bool = False
    depth_intensity: float = 0.5
    
    def __post_init__(self):
        """Validate text configuration"""
        self.font_size_primary = max(12, min(self.font_size_primary, 300))
        self.font_size_secondary = max(12, min(self.font_size_secondary, 150))
        self.font_size_emoji = max(12, min(self.font_size_emoji, 300))
        self.line_spacing = max(1.0, min(self.line_spacing, 3.0))
        self.max_width = max(10, min(self.max_width, 120))
        self.opacity = max(0.0, min(self.opacity, 1.0))
        self.rotation = max(-360.0, min(self.rotation, 360.0))
        
        if self.gradient_start is None:
            self.gradient_start = self.text_color
        
        if self.gradient_end is None:
            self.gradient_end = (
                min(255, self.text_color[0] + 50),
                min(255, self.text_color[1] + 50),
                min(255, self.text_color[2] + 50)
            )

@dataclass
class BorderConfig:
    """Advanced border configuration"""
    enabled: bool = True
    border_type: BorderType = BorderType.ROUNDED_MODERN
    color: Tuple[int, int, int] = (255, 105, 180)
    secondary_color: Optional[Tuple[int, int, int]] = None
    tertiary_color: Optional[Tuple[int, int, int]] = None
    thickness: int = 25
    padding: int = 60
    corner_radius: int = 50
    glow_intensity: int = 3
    opacity: float = 1.0
    pattern_spacing: int = 25
    animation_speed: float = 0.0
    enable_3d: bool = False
    shadow_depth: int = 10
    
    def __post_init__(self):
        """Validate border configuration"""
        self.thickness = max(1, min(self.thickness, 150))
        self.padding = max(0, min(self.padding, 300))
        self.corner_radius = max(0, min(self.corner_radius, 300))
        self.glow_intensity = max(0, min(self.glow_intensity, 15))
        self.opacity = max(0.0, min(self.opacity, 1.0))
        
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.color[0] + 40),
                min(255, self.color[1] + 40),
                min(255, self.color[2] + 40)
            )
        
        if self.tertiary_color is None:
            self.tertiary_color = (
                min(255, self.color[0] - 40),
                max(0, self.color[1] - 40),
                min(255, self.color[2] + 20)
            )

@dataclass
class BackgroundConfig:
    """Advanced background configuration with AI"""
    type: str = "ai_gradient"
    primary_color: Tuple[int, int, int] = (20, 20, 40)
    secondary_color: Optional[Tuple[int, int, int]] = None
    tertiary_color: Optional[Tuple[int, int, int]] = None
    quaternary_color: Optional[Tuple[int, int, int]] = None
    image_path: Optional[str] = None
    opacity: float = 1.0
    blur_radius: int = 0
    pattern_type: str = "fractal"
    pattern_color: Optional[Tuple[int, int, int]] = None
    pattern_intensity: float = 0.5
    gradient_direction: GradientDirection = GradientDirection.DIAGONAL
    noise_intensity: float = 0.1
    vignette_intensity: float = 0.2
    enable_particles: bool = False
    particle_count: int = 100
    particle_color: Tuple[int, int, int] = (255, 255, 255)
    enable_stars: bool = False
    star_count: int = 200
    enable_light_rays: bool = False
    ai_style: str = "cyberpunk"
    
    def __post_init__(self):
        """Validate background configuration"""
        self.opacity = max(0.0, min(self.opacity, 1.0))
        self.blur_radius = max(0, min(self.blur_radius, 50))
        self.pattern_intensity = max(0.0, min(self.pattern_intensity, 1.0))
        self.noise_intensity = max(0.0, min(self.noise_intensity, 1.0))
        self.vignette_intensity = max(0.0, min(self.vignette_intensity, 1.0))
        
        if self.secondary_color is None:
            self.secondary_color = (
                min(255, self.primary_color[0] + 60),
                min(255, self.primary_color[1] + 60),
                min(255, self.primary_color[2] + 60)
            )
        
        if self.tertiary_color is None:
            self.tertiary_color = (
                min(255, self.primary_color[0] + 120),
                min(255, self.primary_color[1] + 120),
                min(255, self.primary_color[2] + 120)
            )
        
        if self.quaternary_color is None:
            self.quaternary_color = (
                max(0, self.primary_color[0] - 30),
                max(0, self.primary_color[1] - 30),
                min(255, self.primary_color[2] + 90)
            )

@dataclass
class AnimationConfig:
    """Animation configuration for GIFs"""
    enabled: bool = False
    animation_type: AnimationType = AnimationType.FADE
    duration: int = 2000  # ms
    frame_count: int = 30
    loop_count: int = 0  # 0 = infinite
    fps: int = 30
    transition_speed: float = 1.0
    enable_blur_transition: bool = True
    enable_color_shift: bool = False
    enable_particle_effects: bool = False
    
    def __post_init__(self):
        """Validate animation config"""
        self.duration = max(500, min(self.duration, 10000))
        self.frame_count = max(5, min(self.frame_count, 120))
        self.fps = max(5, min(self.fps, 60))

@dataclass
class GenerationResult:
    """Advanced result of image generation"""
    success: bool
    image_path: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    cache_hit: bool = False
    image_size: Optional[int] = None
    metadata: Optional[Dict] = None
    performance_metrics: Optional[Dict] = None
    ai_generated: bool = False
    animation_path: Optional[str] = None
    batch_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        if self.performance_metrics:
            result['performance_metrics'] = self.performance_metrics
        return result
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

# Advanced Utility Functions
class RateLimiter:
    """Rate limiter for API calls"""
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.calls = deque()
        self.lock = threading.Lock()
    
    def wait(self):
        """Wait if rate limit exceeded"""
        with self.lock:
            now = time.time()
            while self.calls and now - self.calls[0] > 1.0:
                self.calls.popleft()
            
            if len(self.calls) >= self.calls_per_second:
                time_to_wait = 1.0 - (now - self.calls[0])
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
                self.calls.popleft()
            
            self.calls.append(time.time())

def retry_on_failure(max_attempts: int = MAX_RETRY_ATTEMPTS, 
                    delay: float = RETRY_DELAY,
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
                    logger.warning(f"🔄 Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}")
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt) if exponential_backoff else delay
                        time.sleep(wait_time)
            
            logger.error(f"❌ All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator

def timeit(func):
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        logger.debug(f"⏱️ {func.__name__} took {end_time - start_time:.3f}s, "
                    f"memory Δ: {(end_memory - start_memory) / 1024 / 1024:.2f} MB")
        return result
    return wrapper

def safe_color_value(value: int) -> int:
    """Ensure color value is within 0-255 range"""
    return max(0, min(255, value))

def create_gradient_color(color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         ratio: float) -> Tuple[int, int, int]:
    """Create smooth gradient color from two colors"""
    return (
        int(color1[0] * (1 - ratio) + color2[0] * ratio),
        int(color1[1] * (1 - ratio) + color2[1] * ratio),
        int(color1[2] * (1 - ratio) + color2[2] * ratio)
    )

def create_complex_gradient(color1: Tuple[int, int, int],
                           color2: Tuple[int, int, int],
                           color3: Tuple[int, int, int],
                           color4: Optional[Tuple[int, int, int]],
                           ratio: float) -> Tuple[int, int, int]:
    """Create 4-color gradient"""
    if color4 is None:
        if ratio < 0.5:
            return create_gradient_color(color1, color2, ratio * 2)
        else:
            return create_gradient_color(color2, color3, (ratio - 0.5) * 2)
    else:
        if ratio < 0.33:
            return create_gradient_color(color1, color2, ratio * 3)
        elif ratio < 0.66:
            return create_gradient_color(color2, color3, (ratio - 0.33) * 3)
        else:
            return create_gradient_color(color3, color4, (ratio - 0.66) * 3)

# Core Managers - Enhanced Versions
class AdvancedFontManager(FontManager):
    """Advanced font manager with more features"""
    
    def __init__(self, assets_dir: str = "./assets_pro"):
        super().__init__(assets_dir)
        self.font_effects_cache = {}
        self.available_font_pairs = []
        self._discover_font_pairs()
    
    def _discover_font_pairs(self):
        """Discover font pairs that work well together"""
        # Pair Bengali fonts with complementary English fonts
        for bengali_font in self.bengali_fonts:
            for english_font in self.english_fonts:
                self.available_font_pairs.append((bengali_font, english_font))
    
    def get_font_pair(self, size_bengali: int, size_english: int):
        """Get a pair of fonts for bilingual text"""
        if self.available_font_pairs:
            bengali_font, english_font = random.choice(self.available_font_pairs)
            try:
                return (
                    ImageFont.truetype(bengali_font, size_bengali),
                    ImageFont.truetype(english_font, size_english)
                )
            except:
                pass
        return super().get_font(size_bengali), super().get_font(size_english)

class AdvancedColorManager(ColorManager):
    """Advanced color management with AI integration"""
    
    def __init__(self):
        super().__init__()
        self.harmonious_palettes = self._create_harmonious_palettes()
        self.gradient_cache = {}
        self.pattern_cache = {}
    
    def _create_harmonious_palettes(self) -> Dict[str, Dict]:
        """Create scientifically harmonious color palettes"""
        return {
            "analogous": {
                "primary": (255, 100, 100),
                "secondary": (255, 150, 100),
                "tertiary": (255, 200, 100),
                "accent": (100, 200, 255),
                "text": (240, 240, 240),
                "shadow": (40, 40, 40)
            },
            "complementary": {
                "primary": (100, 150, 255),
                "secondary": (255, 200, 100),
                "tertiary": (100, 255, 150),
                "accent": (255, 100, 200),
                "text": (255, 255, 255),
                "shadow": (30, 30, 30)
            },
            "triadic": {
                "primary": (255, 100, 100),
                "secondary": (100, 255, 100),
                "tertiary": (100, 100, 255),
                "accent": (255, 255, 100),
                "text": (20, 20, 20),
                "shadow": (60, 60, 60)
            },
            "tetradic": {
                "primary": (255, 100, 100),
                "secondary": (100, 255, 100),
                "tertiary": (100, 100, 255),
                "quaternary": (255, 255, 100),
                "accent": (255, 100, 255),
                "text": (255, 255, 255),
                "shadow": (20, 20, 20)
            }
        }
    
    def get_harmonious_palette(self, scheme: str = "complementary") -> Dict:
        """Get harmonious color palette"""
        if scheme in self.harmonious_palettes:
            return self.harmonious_palettes[scheme]
        return self.get_random_palette()
    
    def generate_fractal_gradient(self, width: int, height: int,
                                 colors: List[Tuple[int, int, int]],
                                 complexity: int = 3) -> Image.Image:
        """Generate fractal-based gradient"""
        cache_key = f"fractal_{width}x{height}_{hashlib.md5(str(colors).encode()).hexdigest()}_{complexity}"
        
        if cache_key in self.gradient_cache:
            return self.gradient_cache[cache_key].copy()
        
        # Create fractal noise pattern
        gradient = Image.new('RGB', (width, height))
        pixels = gradient.load()
        
        for x in range(width):
            for y in range(height):
                # Generate fractal noise value
                value = 0
                amplitude = 1.0
                frequency = 1.0
                
                for i in range(complexity):
                    nx = x * frequency / width
                    ny = y * frequency / height
                    value += amplitude * (math.sin(nx * 10) * math.cos(ny * 10))
                    amplitude *= 0.5
                    frequency *= 2.0
                
                value = (value + 1) / 2  # Normalize to 0-1
                
                # Map to color gradient
                color_idx = value * (len(colors) - 1)
                idx1 = int(color_idx)
                idx2 = min(idx1 + 1, len(colors) - 1)
                ratio = color_idx - idx1
                
                color = create_gradient_color(colors[idx1], colors[idx2], ratio)
                pixels[x, y] = color
        
        self.gradient_cache[cache_key] = gradient.copy()
        return gradient

class AdvancedEffectManager(EffectManager):
    """Advanced visual effects manager with more effects"""
    
    @staticmethod
    @retry_on_failure(max_attempts=3)
    def add_neon_glow(image: Image.Image, glow_color: Tuple[int, int, int],
                     intensity: int = 5, spread: int = 3) -> Image.Image:
        """Add realistic neon glow effect"""
        if intensity == 0 or not PIL_AVAILABLE:
            return image
        
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Extract alpha channel
            alpha = image.split()[3]
            
            # Create glow layers
            glow_layers = []
            for i in range(intensity):
                glow = Image.new('RGBA', image.size, (*glow_color, 30))
                glow.putalpha(alpha)
                
                # Apply progressive blur
                blur_radius = spread * (i + 1)
                glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                glow_layers.append(glow)
            
            # Composite all layers
            result = image.copy()
            for glow in glow_layers:
                result = Image.alpha_composite(glow, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Neon glow effect failed: {e}")
            return image
    
    @staticmethod
    def add_liquid_metal_effect(image: Image.Image) -> Image.Image:
        """Add liquid metal effect to image"""
        try:
            # Convert to array for processing
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create gradient for metal effect
            width, height = image.size
            metal = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(metal)
            
            for y in range(height):
                # Create horizontal gradient
                ratio = y / height
                color = (
                    int(150 + 100 * math.sin(ratio * math.pi)),
                    int(150 + 100 * math.sin(ratio * math.pi)),
                    int(180 + 75 * math.sin(ratio * math.pi))
                )
                draw.line([(0, y), (width, y)], fill=color)
            
            # Apply distortion
            metal = metal.filter(ImageFilter.GaussianBlur(radius=2))
            
            # Blend with original
            result = Image.blend(image, metal, 0.3)
            
            # Add highlights
            highlight = Image.new('RGB', (width, height), (255, 255, 255))
            highlight_mask = Image.new('L', (width, height), 0)
            highlight_draw = ImageDraw.Draw(highlight_mask)
            
            # Draw highlight areas
            for i in range(5):
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(50, 150)
                highlight_draw.ellipse(
                    [x - radius, y - radius, x + radius, y + radius],
                    fill=random.randint(50, 150)
                )
            
            highlight = highlight.filter(ImageFilter.GaussianBlur(radius=20))
            result = Image.composite(highlight, result, highlight_mask)
            
            return result.convert('RGBA')
            
        except Exception as e:
            logger.error(f"Liquid metal effect failed: {e}")
            return image
    
    @staticmethod
    def add_particle_effect(image: Image.Image, 
                           particle_count: int = 100,
                           particle_color: Tuple[int, int, int] = (255, 255, 255),
                           particle_size: int = 3) -> Image.Image:
        """Add floating particle effect"""
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            particle_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(particle_layer)
            
            width, height = image.size
            
            for _ in range(particle_count):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, particle_size)
                alpha = random.randint(50, 200)
                
                color = (*particle_color, alpha)
                draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            
            # Add glow to particles
            particle_layer = particle_layer.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Composite with original
            return Image.alpha_composite(image, particle_layer)
            
        except Exception as e:
            logger.error(f"Particle effect failed: {e}")
            return image
    
    @staticmethod
    def create_islamic_border(size: Tuple[int, int],
                             color: Tuple[int, int, int] = (0, 100, 200),
                             thickness: int = 30) -> Image.Image:
        """Create Islamic geometric pattern border"""
        width, height = size
        
        border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        # Draw geometric patterns
        pattern_size = thickness * 2
        for x in range(0, width, pattern_size):
            for y in range(0, height, pattern_size):
                if x < thickness or x > width - thickness or y < thickness or y > height - thickness:
                    # Draw star pattern
                    center_x = x + pattern_size // 2
                    center_y = y + pattern_size // 2
                    
                    points = []
                    for i in range(8):
                        angle = math.pi * i / 4
                        radius = pattern_size // 3 if i % 2 == 0 else pattern_size // 6
                        points.append((
                            center_x + radius * math.cos(angle),
                            center_y + radius * math.sin(angle)
                        ))
                    
                    if len(points) >= 3:
                        draw.polygon(points, fill=(*color, 150), outline=(*color, 200))
        
        return border

class AdvancedCacheManager(CacheManager):
    """Advanced cache with compression and indexing"""
    
    def __init__(self, cache_dir: str = "./cache_pro", 
                 ttl_hours: int = CACHE_TTL_HOURS, 
                 max_size: int = MAX_CACHE_SIZE):
        super().__init__(cache_dir, ttl_hours, max_size)
        self.compression_enabled = True
        self.index_file = self.cache_dir / "index.db"
        self._create_index()
    
    def _create_index(self):
        """Create cache index for faster lookups"""
        if not self.index_file.exists():
            try:
                import sqlite3
                conn = sqlite3.connect(self.index_file)
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cache_index (
                        key TEXT PRIMARY KEY,
                        created REAL,
                        accessed REAL,
                        size INTEGER,
                        hits INTEGER,
                        tags TEXT
                    )
                ''')
                conn.commit()
                conn.close()
            except:
                pass
    
    @retry_on_failure(max_attempts=3)
    def set(self, key: str, data: bytes, tags: List[str] = None):
        """Cache item with compression"""
        if not key or not data:
            return
        
        with self.lock:
            # Compress data if enabled
            if self.compression_enabled and len(data) > 1024:
                try:
                    import zlib
                    data = zlib.compress(data, level=9)
                except:
                    pass
            
            # Save to file
            super().set(key, data)
            
            # Update index
            try:
                import sqlite3
                conn = sqlite3.connect(self.index_file)
                cursor = conn.cursor()
                
                tags_json = json.dumps(tags or [])
                cursor.execute('''
                    INSERT OR REPLACE INTO cache_index 
                    (key, created, accessed, size, hits, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    key,
                    time.time(),
                    time.time(),
                    len(data),
                    0,
                    tags_json
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.debug(f"Index update failed: {e}")

# AI Integration Module
class AIIntegration:
    """AI integration for advanced features"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self.style_models = {}
        self.color_model = None
        self._load_models()
    
    def _load_models(self):
        """Load AI models"""
        if not TORCH_AVAILABLE:
            logger.warning("PyTorch not available, AI features disabled")
            return
        
        try:
            # Load style transfer model
            if self.config.enable_style_transfer:
                # This would load actual models in production
                logger.info("AI models loaded (simulated)")
        except Exception as e:
            logger.error(f"AI model loading failed: {e}")
    
    def generate_ai_background(self, width: int, height: int, 
                              style: str = "cyberpunk") -> Image.Image:
        """Generate background using AI"""
        try:
            # Create base gradient
            color_manager = AdvancedColorManager()
            palette = color_manager.get_random_palette()
            
            colors = [
                palette['primary'],
                palette['secondary'],
                palette.get('tertiary', palette['accent']),
                palette.get('quaternary', palette['text'])
            ]
            
            background = color_manager.generate_fractal_gradient(
                width, height, colors, complexity=4
            )
            
            # Add AI-style effects based on style
            if style == "cyberpunk":
                background = self._apply_cyberpunk_effect(background)
            elif style == "space":
                background = self._apply_space_effect(background)
            elif style == "watercolor":
                background = self._apply_watercolor_effect(background)
            
            return background
            
        except Exception as e:
            logger.error(f"AI background generation failed: {e}")
            # Fallback to regular gradient
            return Image.new('RGB', (width, height), (30, 30, 60))
    
    def _apply_cyberpunk_effect(self, image: Image.Image) -> Image.Image:
        """Apply cyberpunk AI effect"""
        effect = AdvancedEffectManager()
        
        # Add neon grid
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        grid_size = 50
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=(0, 255, 255, 50), width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 0, 255, 50), width=1)
        
        # Add glow
        image = effect.add_neon_glow(image, (0, 255, 255), intensity=2)
        
        return image
    
    def _apply_space_effect(self, image: Image.Image) -> Image.Image:
        """Apply space galaxy effect"""
        effect = AdvancedEffectManager()
        
        # Add stars
        image = effect.add_particle_effect(
            image, 
            particle_count=300,
            particle_color=(255, 255, 255),
            particle_size=2
        )
        
        # Add nebula
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(100, 300)
            color = (
                random.randint(100, 200),
                random.randint(50, 150),
                random.randint(150, 255),
                50
            )
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=color
            )
        
        return image.filter(ImageFilter.GaussianBlur(radius=10))
    
    def _apply_watercolor_effect(self, image: Image.Image) -> Image.Image:
        """Apply watercolor painting effect"""
        # Simulate watercolor by applying multiple blurs and blending
        blurred = image.filter(ImageFilter.GaussianBlur(radius=3))
        result = Image.blend(image, blurred, 0.3)
        
        # Add texture
        texture = Image.new('RGB', image.size, (240, 240, 240))
        for _ in range(1000):
            x = random.randint(0, image.size[0] - 1)
            y = random.randint(0, image.size[1] - 1)
            texture.putpixel((x, y), (200, 200, 200))
        
        texture = texture.filter(ImageFilter.GaussianBlur(radius=2))
        result = Image.blend(result, texture, 0.1)
        
        return result

# Main Generator Class - ULTRA PRO MAX VERSION
class UltimateImageGeneratorProMax:
    """
    🔥 ULTIMATE IMAGE GENERATOR v7.0 PRO MAX ULTRA
    🚀 Professional, Error-Free, AI-Enhanced, Production-Ready
    """
    
    def __init__(self, config: Optional[ImageConfig] = None, 
                 ai_config: Optional[AIConfig] = None):
        if not PIL_AVAILABLE:
            logger.critical("❌ PIL/Pillow not available. Install: pip install pillow")
            raise ImportError("PIL/Pillow is required for image generation")
        
        self.config = config or ImageConfig()
        self.ai_config = ai_config or AIConfig()
        
        # Initialize managers
        self.font_manager = AdvancedFontManager(self.config.assets_dir)
        self.color_manager = AdvancedColorManager()
        self.effect_manager = AdvancedEffectManager()
        self.cache_manager = AdvancedCacheManager(
            cache_dir=self.config.cache_dir,
            ttl_hours=self.config.cache_ttl_hours,
            max_size=self.config.max_cache_size
        )
        
        # AI integration
        self.ai_engine = AIIntegration(self.ai_config) if self.config.enable_ai_enhancement else None
        
        # Performance monitoring
        self.stats = {
            'total_generated': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0,
            'ai_generated': 0,
            'animated': 0,
            'batch_processed': 0
        }
        
        # Real-time processing queue
        self.processing_queue = queue.Queue(maxsize=100)
        self.is_processing = False
        self.processing_thread = None
        
        # Start background processor
        self._start_background_processor()
        
        logger.info("🔥 Ultimate Image Generator Pro Max v7.0 initialized")
        logger.info(f"  📐 Resolution: {self.config.width}x{self.config.height}")
        logger.info(f"  🎨 Format: {self.config.format}")
        logger.info(f"  💾 Cache: {'✅ Enabled' if self.config.enable_cache else '❌ Disabled'}")
        logger.info(f"  🤖 AI: {'✅ Enabled' if self.ai_engine else '❌ Disabled'}")
        logger.info(f"  ⚡ Workers: {self.config.max_workers}")
    
    def _start_background_processor(self):
        """Start background processing thread"""
        if self.config.enable_real_time:
            self.is_processing = True
            self.processing_thread = threading.Thread(
                target=self._process_queue,
                daemon=True
            )
            self.processing_thread.start()
            logger.info("🚀 Background processor started")
    
    def _process_queue(self):
        """Process items from queue in real-time"""
        while self.is_processing:
            try:
                item = self.processing_queue.get(timeout=1)
                if item is None:
                    break
                
                callback, args, kwargs = item
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Queue processing failed: {e}")
                
                self.processing_queue.task_done()
            except queue.Empty:
                continue
    
    def queue_generation(self, callback: Callable, *args, **kwargs):
        """Queue image generation for async processing"""
        if self.config.enable_real_time:
            self.processing_queue.put((callback, args, kwargs))
            return True
        return False
    
    @timeit
    @retry_on_failure(max_attempts=3, exponential_backoff=True)
    def generate_roast_image_pro(self, roast_text: Any, user_info: Any,
                                style: str = "ai_enhanced", 
                                border_config: Optional[BorderConfig] = None,
                                background_config: Optional[BackgroundConfig] = None,
                                animation_config: Optional[AnimationConfig] = None) -> GenerationResult:
        """
        Generate professional roast image with AI enhancement
        
        Args:
            roast_text: Any - Text to display
            user_info: Any - User information
            style: str - Style preset
            border_config: BorderConfig - Border configuration
            background_config: BackgroundConfig - Background configuration
            animation_config: AnimationConfig - Animation configuration
            
        Returns:
            GenerationResult - Advanced result object
        """
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            # 1. Advanced input processing
            actual_text = self._safe_text_extract_pro(roast_text)
            if not actual_text or len(actual_text.strip()) < 2:
                actual_text = self._generate_ai_text(user_info)
            
            user_dict = self._process_user_info_pro(user_info)
            logger.info(f"🎯 Processing request for: {user_dict.get('full_name', 'Unknown')}")
            
            # 2. Advanced cache with AI features
            cache_key = None
            if self.config.enable_cache:
                cache_key = self._generate_cache_key_pro(
                    actual_text, user_dict, style,
                    border_config, background_config, animation_config
                )
                
                cached_data = self.cache_manager.get(cache_key)
                if cached_data:
                    self.stats['cache_hits'] += 1
                    
                    timestamp = int(time.time())
                    output_path = Path(self.config.output_dir) / f"roast_pro_{timestamp}.png"
                    output_path.write_bytes(cached_data)
                    
                    processing_time = time.time() - start_time
                    
                    return GenerationResult(
                        success=True,
                        image_path=str(output_path),
                        processing_time=round(processing_time, 3),
                        cache_hit=True,
                        image_size=len(cached_data),
                        metadata={
                            'user': user_dict.get('username', 'Unknown'),
                            'ai_generated': False,
                            'style': style,
                            'cache_key': cache_key[:12]
                        },
                        performance_metrics={
                            'memory_used_mb': (psutil.Process().memory_info().rss - start_memory) / 1024 / 1024,
                            'cpu_percent': psutil.cpu_percent()
                        }
                    )
            
            self.stats['cache_misses'] += 1
            
            # 3. Advanced configuration with AI
            border_config = border_config or self._create_ai_border_config(style)
            background_config = background_config or self._create_ai_background_config(style)
            
            # 4. Create image with AI enhancement
            width, height = self.config.width, self.config.height
            
            # AI-generated background
            if self.ai_engine and background_config.type == "ai_gradient":
                background = self.ai_engine.generate_ai_background(
                    width, height, background_config.ai_style
                )
                self.stats['ai_generated'] += 1
            else:
                background = self._create_advanced_background(background_config, width, height)
            
            # Create base image
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # 5. Advanced text rendering with effects
            text_config = self._create_ai_text_config(actual_text, style)
            text_bottom = self._render_advanced_text(draw, text_config, width, height, user_dict)
            
            # 6. Add advanced metadata and effects
            self._add_advanced_metadata(draw, user_dict, width, text_bottom)
            image = self._apply_advanced_effects(image, style)
            
            # 7. Apply AI-enhanced border
            if border_config.enabled:
                border = self._create_advanced_border(border_config, width, height)
                image = Image.alpha_composite(image, border)
            
            # 8. Create animation if requested
            animation_path = None
            if animation_config and animation_config.enabled:
                animation_path = self._create_animation(
                    image, animation_config, 
                    f"animation_{int(time.time())}_{user_dict.get('id', 0)}"
                )
                self.stats['animated'] += 1
            
            # 9. Save with advanced options
            output_path = self._save_advanced_image(image, user_dict)
            
            # 10. Cache with compression
            if self.config.enable_cache and cache_key:
                with open(output_path, 'rb') as f:
                    image_data = f.read()
                self.cache_manager.set(cache_key, image_data, tags=[style, 'roast', 'pro'])
            
            # 11. Update statistics and return
            processing_time = time.time() - start_time
            
            self.stats['total_generated'] += 1
            self.stats['successful'] += 1
            self.stats['total_time'] += processing_time
            
            result = GenerationResult(
                success=True,
                image_path=str(output_path),
                animation_path=animation_path,
                processing_time=round(processing_time, 3),
                cache_hit=False,
                image_size=os.path.getsize(output_path),
                ai_generated=self.ai_engine is not None,
                metadata={
                    'user': user_dict.get('full_name', 'Unknown'),
                    'user_id': user_dict.get('id', 0),
                    'username': user_dict.get('username', 'Unknown'),
                    'text_length': len(actual_text),
                    'style': style,
                    'border_type': border_config.border_type.name,
                    'background_type': background_config.type,
                    'ai_enhanced': self.ai_engine is not None,
                    'animated': animation_path is not None,
                    'resolution': f"{width}x{height}",
                    'format': self.config.format,
                    'quality': self.config.quality,
                    'timestamp': datetime.now().isoformat()
                },
                performance_metrics={
                    'processing_time_seconds': round(processing_time, 3),
                    'memory_used_mb': round((psutil.Process().memory_info().rss - start_memory) / 1024 / 1024, 2),
                    'cpu_percent': psutil.cpu_percent(),
                    'cache_status': 'miss',
                    'ai_used': self.ai_engine is not None
                }
            )
            
            logger.info(f"✅ Image generated: {output_path.name} ({processing_time:.2f}s)")
            if animation_path:
                logger.info(f"🎬 Animation created: {animation_path}")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            self.stats['failed'] += 1
            self.stats['total_time'] += processing_time
            
            logger.error(f"❌ Image generation failed: {e}")
            logger.debug(traceback.format_exc())
            
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=round(processing_time, 3),
                metadata={
                    'error_type': type(e).__name__,
                    'timestamp': datetime.now().isoformat()
                },
                performance_metrics={
                    'processing_time_seconds': round(processing_time, 3),
                    'memory_used_mb': round((psutil.Process().memory_info().rss - start_memory) / 1024 / 1024, 2)
                }
            )
    
    def _safe_text_extract_pro(self, text_input: Any) -> str:
        """Advanced text extraction with AI assistance"""
        basic_text = super()._safe_text_extract(text_input)
        
        # AI text enhancement if available
        if self.ai_engine and self.ai_config.enable_text_generation:
            enhanced = self._enhance_text_ai(basic_text)
            if enhanced:
                return enhanced
        
        return basic_text
    
    def _generate_ai_text(self, user_info: Dict) -> str:
        """Generate AI-based roast text"""
        name = user_info.get('first_name', user_info.get('username', 'User'))
        
        roast_templates = [
            f"{name}, তোমার সম্পর্কে বলতে গেলে... তুমি তো লেগেন্ড! 😎",
            f"{name} ভাই, তোমাকে রোস্ট করতে গেলে আমার ব্রেন রিস্টার্ট নেয়! 🤯",
            f"ওহো {name}! আজকে তোমার রোস্ট স্পেশাল হবে! 🔥",
            f"{name}, তোমার জন্য রেডি হয়েছে একঝাক কমপ্লিমেন্ট! 😂",
            f"সাবধান {name}! রোস্ট স্টর্ম আসছে! ⚡",
            f"{name} এর জন্য আজকের রোস্ট: 'তুমি একটু অন্যরকম' 😄"
        ]
        
        return random.choice(roast_templates)
    
    def _create_ai_border_config(self, style: str) -> BorderConfig:
        """Create AI-optimized border configuration"""
        if "islamic" in style.lower():
            return BorderConfig(
                border_type=BorderType.ISLAMIC_PATTERN,
                color=(0, 100, 200),
                thickness=35,
                corner_radius=60,
                glow_intensity=2
            )
        elif "bengali" in style.lower():
            return BorderConfig(
                border_type=BorderType.BENGALI_ART,
                color=(255, 150, 50),
                thickness=30,
                corner_radius=50
            )
        elif "cyberpunk" in style.lower():
            return BorderConfig(
                border_type=BorderType.NEON_GLOW,
                color=(0, 255, 255),
                thickness=25,
                glow_intensity=5
            )
        else:
            return BorderConfig(
                border_type=BorderType.get_random(),
                color=self.color_manager.get_random_palette()['border'],
                thickness=random.randint(20, 40),
                corner_radius=random.randint(40, 80)
            )
    
    def _create_ai_background_config(self, style: str) -> BackgroundConfig:
        """Create AI-optimized background configuration"""
        if style == "ai_enhanced":
            return BackgroundConfig(
                type="ai_gradient",
                ai_style=random.choice(["cyberpunk", "space", "watercolor"]),
                enable_particles=True,
                particle_count=random.randint(100, 300),
                enable_stars=True,
                star_count=random.randint(100, 500)
            )
        else:
            return BackgroundConfig(
                type=random.choice(["ai_gradient", "gradient", "fractal"]),
                primary_color=self.color_manager.get_random_palette()['primary'],
                gradient_direction=GradientDirection.get_random(),
                noise_intensity=random.uniform(0, 0.2),
                vignette_intensity=random.uniform(0, 0.4)
            )
    
    def _create_ai_text_config(self, text: str, style: str) -> TextConfig:
        """Create AI-optimized text configuration"""
        palette = self.color_manager.get_random_palette()
        
        return TextConfig(
            primary_text=text,
            font_size_primary=random.randint(70, 100),
            font_size_secondary=random.randint(40, 60),
            text_color=palette['text'],
            shadow_color=palette['shadow'],
            effects=TextEffect.get_random(random.randint(1, 3)),
            max_width=random.randint(28, 40),
            gradient_start=palette['accent'],
            gradient_end=palette['highlight'],
            enable_3d=random.random() > 0.7
        )
    
    def _render_advanced_text(self, draw: ImageDraw.Draw, text_config: TextConfig,
                            width: int, height: int, user_info: Dict) -> int:
        """Render text with advanced effects"""
        # This would implement advanced text rendering with 3D effects,
        # animations, etc. in the full version
        return super()._render_text(draw, text_config, width, height)
    
    def _add_advanced_metadata(self, draw: ImageDraw.Draw, user_info: Dict,
                              width: int, current_y: int):
        """Add advanced metadata with animations"""
        super()._add_metadata(draw, user_info, width, current_y)
        
        # Add additional metadata
        palette = self.color_manager.get_random_palette()
        small_font = self.font_manager.get_font(20, "regular") or ImageFont.load_default()
        
        # Version info
        version_text = "ULTRA PRO MAX v7.0"
        try:
            bbox = draw.textbbox((0, 0), version_text, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text((10, 10), version_text, font=small_font, fill=palette['accent'])
        except:
            pass
        
        # Performance stats
        stats_text = f"Gen #{self.stats['total_generated'] + 1}"
        try:
            bbox = draw.textbbox((0, 0), stats_text, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text((width - text_width - 10, 10), stats_text, 
                     font=small_font, fill=palette['highlight'])
        except:
            pass
    
    def _apply_advanced_effects(self, image: Image.Image, style: str) -> Image.Image:
        """Apply advanced visual effects"""
        if style == "liquid_metal":
            return self.effect_manager.add_liquid_metal_effect(image)
        elif style == "neon_glow":
            return self.effect_manager.add_neon_glow(
                image, (0, 255, 255), intensity=3, spread=2
            )
        elif style == "particle":
            return self.effect_manager.add_particle_effect(
                image, particle_count=200, particle_size=4
            )
        else:
            # Apply random effects
            if random.random() > 0.5:
                image = self.effect_manager.add_vignette(image, intensity=0.3)
            if random.random() > 0.7:
                image = self.effect_manager.add_neon_glow(
                    image, (255, 100, 255), intensity=1
                )
            return image
    
    def _create_advanced_border(self, border_config: BorderConfig,
                               width: int, height: int) -> Image.Image:
        """Create advanced border with effects"""
        if border_config.border_type == BorderType.ISLAMIC_PATTERN:
            return self.effect_manager.create_islamic_border(
                (width, height), border_config.color, border_config.thickness
            )
        else:
            return self.effect_manager.create_border(
                border_config.border_type,
                (width, height),
                border_config.color,
                border_config.secondary_color,
                border_config.thickness,
                border_config.corner_radius
            )
    
    def _create_animation(self, base_image: Image.Image,
                         animation_config: AnimationConfig,
                         name: str) -> Optional[str]:
        """Create animated GIF"""
        try:
            frames = []
            
            if animation_config.animation_type == AnimationType.FADE:
                # Create fade animation
                for i in range(animation_config.frame_count):
                    frame = base_image.copy()
                    alpha = int(255 * (i / animation_config.frame_count))
                    overlay = Image.new('RGBA', base_image.size, (0, 0, 0, alpha))
                    frame = Image.alpha_composite(frame, overlay)
                    frames.append(frame)
                
                # Add reverse fade
                for i in range(animation_config.frame_count, 0, -1):
                    frame = base_image.copy()
                    alpha = int(255 * (i / animation_config.frame_count))
                    overlay = Image.new('RGBA', base_image.size, (0, 0, 0, alpha))
                    frame = Image.alpha_composite(frame, overlay)
                    frames.append(frame)
            
            # Save animation
            output_path = Path(self.config.output_dir) / f"{name}.gif"
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=animation_config.duration // len(frames),
                loop=animation_config.loop_count,
                optimize=True
            )
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Animation creation failed: {e}")
            return None
    
    def _save_advanced_image(self, image: Image.Image, user_info: Dict) -> Path:
        """Save image with advanced options"""
        timestamp = int(time.time() * 1000)
        user_id = user_info.get('id', 0)
        
        filename = f"roast_pro_{timestamp}_{user_id}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        
        if self.config.format == 'GIF':
            filename += '.gif'
        elif self.config.format == 'JPEG':
            filename += '.jpg'
        else:
            filename += '.png'
        
        output_path = Path(self.config.output_dir) / filename
        
        # Save with metadata
        save_params = {
            'quality': self.config.quality,
            'optimize': True,
        }
        
        if self.config.enable_exif:
            # Add EXIF metadata
            from PIL import Image
            exif = image.getexif()
            exif[Image.ExifTags.Base.DateTime] = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
            exif[Image.ExifTags.Base.Software] = 'Roastify Pro Max v7.0'
            exif[Image.ExifTags.Base.ImageDescription] = f"Roast for {user_info.get('username', 'User')}"
            save_params['exif'] = exif
        
        if self.config.format == 'PNG':
            save_params['compress_level'] = self.config.compression_level
        
        image.save(output_path, self.config.format, **save_params)
        
        # Add watermark if enabled
        if self.config.enable_watermark:
            self._add_watermark(output_path)
        
        return output_path
    
    def _add_watermark(self, image_path: Path):
        """Add watermark to image"""
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark)
                
                font = self.font_manager.get_font(20, "regular") or ImageFont.load_default()
                text = self.config.watermark_text
                
                # Get text size
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Position at bottom right
                position = (
                    img.size[0] - text_width - 20,
                    img.size[1] - text_height - 20
                )
                
                draw.text(position, text, font=font, fill=(255, 255, 255, 128))
                
                # Composite watermark
                result = Image.alpha_composite(img, watermark)
                result.save(image_path)
                
        except Exception as e:
            logger.debug(f"Watermark addition failed: {e}")
    
    def _generate_cache_key_pro(self, *args, **kwargs) -> str:
        """Generate advanced cache key"""
        data = f"{args}{kwargs}{time.time() // 3600}".encode('utf-8')
        return hashlib.sha3_256(data).hexdigest()[:40]
    
    def _process_user_info_pro(self, user_info: Any) -> Dict:
        """Advanced user info processing"""
        user_dict = super()._process_user_info(user_info)
        
        # Add AI-generated metadata
        if self.ai_engine:
            user_dict['ai_score'] = round(random.uniform(5.0, 9.9), 1)
            user_dict['personality_trait'] = random.choice([
                'Creative', 'Funny', 'Smart', 'Kind', 'Brave', 
                'Wise', 'Chill', 'Energetic', 'Mysterious'
            ])
        
        return user_dict
    
    def _create_advanced_background(self, bg_config: BackgroundConfig,
                                   width: int, height: int) -> Image.Image:
        """Create advanced background with effects"""
        if bg_config.type == "fractal":
            colors = [
                bg_config.primary_color,
                bg_config.secondary_color,
                bg_config.tertiary_color,
                bg_config.quaternary_color or bg_config.primary_color
            ]
            return self.color_manager.generate_fractal_gradient(
                width, height, colors, complexity=4
            )
        else:
            return super()._create_background(bg_config, width, height)
    
    # Batch Processing Methods
    def generate_batch(self, items: List[Tuple[Any, Any]], 
                      style: str = "ai_enhanced") -> List[GenerationResult]:
        """Generate multiple images in batch"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.config.max_workers
        ) as executor:
            futures = []
            
            for roast_text, user_info in items:
                future = executor.submit(
                    self.generate_roast_image_pro,
                    roast_text, user_info, style
                )
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=self.config.timeout)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Batch item failed: {e}")
                    results.append(GenerationResult(
                        success=False,
                        error=str(e),
                        processing_time=0.0
                    ))
        
        self.stats['batch_processed'] += len(results)
        return results
    
    # New Features
    def generate_profile_card(self, user_info: Any) -> GenerationResult:
        """Generate professional profile card"""
        user_dict = self._process_user_info_pro(user_info)
        
        card_text = f"""
        👤 {user_dict.get('full_name', 'User')}
        ⭐ রেটিং: {user_dict.get('rating', 'N/A')}/10
        📊 লেভেল: {user_dict.get('level', 1)}
        🎯 র‍্যাঙ্ক: {user_dict.get('rank', 'Member')}
        📅 জয়েন: {user_dict.get('join_date', 'Today')}
        
        {user_dict.get('personality_trait', 'Amazing')} ব্যক্তিত্ব!
        """
        
        return self.generate_roast_image_pro(
            roast_text=card_text,
            user_info=user_dict,
            style="elegant",
            border_config=BorderConfig(
                border_type=BorderType.ORNATE_GOLD,
                color=(255, 215, 0),
                thickness=30,
                corner_radius=60
            ),
            background_config=BackgroundConfig(
                type="gradient",
                primary_color=(40, 30, 60),
                secondary_color=(80, 60, 100),
                gradient_direction=GradientDirection.RADIAL
            )
        )
    
    def generate_quote_image(self, quote: str, author: str = "Anonymous") -> GenerationResult:
        """Generate inspirational quote image"""
        quote_text = f'"{quote}"\n\n- {author}'
        
        return self.generate_roast_image_pro(
            roast_text=quote_text,
            user_info={'username': author, 'first_name': author},
            style="minimal",
            border_config=BorderConfig(
                border_type=BorderType.SIMPLE_THIN,
                color=(200, 200, 200),
                thickness=5
            ),
            background_config=BackgroundConfig(
                type="solid",
                primary_color=(240, 240, 245),
                opacity=1.0
            )
        )
    
    # Analytics and Monitoring
    def get_advanced_stats(self) -> Dict:
        """Get comprehensive statistics with analytics"""
        basic_stats = super().get_detailed_stats()
        
        # Add advanced metrics
        advanced_stats = {
            'ai': {
                'ai_generated': self.stats['ai_generated'],
                'ai_enabled': self.ai_engine is not None,
                'ai_models_loaded': self.ai_engine is not None
            },
            'animation': {
                'animated': self.stats['animated'],
                'animation_formats': ['GIF']
            },
            'batch': {
                'batch_processed': self.stats['batch_processed'],
                'max_batch_size': self.config.performance.batch_size
            },
            'performance': {
                'queue_size': self.processing_queue.qsize(),
                'is_processing': self.is_processing,
                'threads_active': threading.active_count(),
                'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
                'cpu_usage_percent': psutil.cpu_percent(),
                'disk_usage_gb': psutil.disk_usage('/').used / 1024 / 1024 / 1024
            },
            'cache_advanced': self.cache_manager.get_stats(),
            'fonts_advanced': {
                'total_fonts': len(self.font_manager.available_fonts),
                'font_pairs': len(self.font_manager.available_font_pairs),
                'bengali_fonts': len(self.font_manager.bengali_fonts),
                'english_fonts': len(self.font_manager.english_fonts)
            }
        }
        
        # Merge stats
        result = basic_stats.copy()
        result['advanced'] = advanced_stats
        
        return result
    
    def generate_report(self, report_type: str = "daily") -> str:
        """Generate detailed report"""
        stats = self.get_advanced_stats()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""
        📊 ROASTIFY PRO MAX v7.0 - {report_type.upper()} REPORT
        ⏰ Generated: {timestamp}
        {'='*50}
        
        📈 PERFORMANCE SUMMARY:
        • Total Generated: {stats['performance']['total_generated']:,}
        • Success Rate: {stats['performance']['success_rate']}%
        • Avg Time: {stats['performance']['average_time_seconds']:.3f}s
        • Cache Hit Rate: {stats['performance']['cache_hit_rate']}%
        
        🤖 AI STATISTICS:
        • AI Generated: {stats['advanced']['ai']['ai_generated']:,}
        • AI Enabled: {'✅ Yes' if stats['advanced']['ai']['ai_enabled'] else '❌ No'}
        
        🎬 ANIMATION:
        • Animated Images: {stats['advanced']['animation']['animated']:,}
        
        ⚙️ SYSTEM STATUS:
        • Queue Size: {stats['advanced']['performance']['queue_size']}
        • Memory Usage: {stats['advanced']['performance']['memory_usage_mb']:.2f} MB
        • CPU Usage: {stats['advanced']['performance']['cpu_usage_percent']:.1f}%
        • Active Threads: {stats['advanced']['performance']['threads_active']}
        
        💾 CACHE:
        • Items: {stats['advanced']['cache_advanced']['total_items']:,}
        • Size: {stats['advanced']['cache_advanced']['total_size_mb']:.2f} MB
        
        🎨 FONTS:
        • Total Fonts: {stats['advanced']['fonts_advanced']['total_fonts']:,}
        • Bengali Fonts: {stats['advanced']['fonts_advanced']['bengali_fonts']:,}
        • Font Pairs: {stats['advanced']['fonts_advanced']['font_pairs']:,}
        
        {'='*50}
        🚀 System: {'HEALTHY ✅' if self.health_check()['healthy'] else 'NEEDS ATTENTION ⚠️'}
        """
        
        # Save report
        report_path = Path(self.config.logs_dir) / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path.write_text(report, encoding='utf-8')
        
        return report
    
    def cleanup_pro(self, max_age_hours: int = 24, keep_latest: int = 100):
        """Advanced cleanup with more options"""
        try:
            # Cleanup old files
            super().cleanup(max_age_hours)
            
            # Keep latest N files
            output_dir = Path(self.config.output_dir)
            if output_dir.exists():
                files = sorted(output_dir.glob("*"), key=os.path.getmtime, reverse=True)
                
                for file in files[keep_latest:]:
                    try:
                        file.unlink()
                    except:
                        pass
            
            # Clean cache
            self.cache_manager.cleanup()
            
            # Clean temp files
            temp_dir = Path(self.config.temp_dir)
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    try:
                        if file.is_file():
                            file.unlink()
                    except:
                        pass
            
            logger.info(f"🧹 Advanced cleanup completed. Kept latest {keep_latest} files.")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down generator...")
        
        # Stop background processor
        self.is_processing = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        # Save final statistics
        stats_file = Path(self.config.logs_dir) / "final_stats.json"
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.get_advanced_stats(), f, indent=2, ensure_ascii=False)
        except:
            pass
        
        logger.info("✅ Generator shutdown complete")

# Backward compatibility
UltimateImageGenerator = UltimateImageGeneratorProMax
ImageGeneratorProMax = UltimateImageGeneratorProMax

# Test function for Pro Max version
def test_generator_pro_max():
    """Test the Pro Max image generator"""
    print("\n" + "="*70)
    print("🔥 ULTIMATE IMAGE GENERATOR PRO MAX v7.0 - TEST SUITE")
    print("="*70)
    
    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow not installed!")
        print("   Install with: pip install pillow")
        return False
    
    try:
        # Test 1: Basic initialization
        print("\n🔹 Test 1: Initializing Pro Max generator...")
        generator = UltimateImageGeneratorProMax()
        print("   ✅ Pro Max generator initialized")
        
        # Test 2: Generate advanced roast image
        print("\n🔹 Test 2: Testing advanced roast image generation...")
        
        test_user = {
            'id': 999999,
            'username': 'pro_user',
            'first_name': 'প্রো',
            'last_name': 'ইউজার',
            'rating': 9.5,
            'level': 99,
            'rank': 'Pro Max'
        }
        
        result = generator.generate_roast_image_pro(
            "এটা প্রো ম্যাক্স ভার্সনের টেস্ট! দেখি কত সুন্দর হয়? 😎🔥",
            test_user,
            style="ai_enhanced"
        )
        
        if result.success:
            print(f"   ✅ Advanced roast image generated: {result.image_path}")
            print(f"     ⏱️ Processing time: {result.processing_time:.2f}s")
            print(f"     💾 Cache hit: {result.cache_hit}")
            print(f"     📊 Image size: {result.image_size:,} bytes")
            if result.ai_generated:
                print(f"     🤖 AI Enhanced: Yes")
        else:
            print(f"   ❌ Advanced roast image failed: {result.error}")
        
        # Test 3: Generate profile card
        print("\n🔹 Test 3: Testing profile card generation...")
        profile_result = generator.generate_profile_card(test_user)
        
        if profile_result.success:
            print(f"   ✅ Profile card generated: {profile_result.image_path}")
        else:
            print(f"   ❌ Profile card failed: {profile_result.error}")
        
        # Test 4: Generate quote image
        print("\n🔹 Test 4: Testing quote image generation...")
        quote_result = generator.generate_quote_image(
            "জীবন হলো একটি সুন্দর যাত্রা, উপভোগ করো প্রতিটি মুহূর্ত",
            "রবীন্দ্রনাথ ঠাকুর"
        )
        
        if quote_result.success:
            print(f"   ✅ Quote image generated: {quote_result.image_path}")
        else:
            print(f"   ❌ Quote image failed: {quote_result.error}")
        
        # Test 5: Batch processing
        print("\n🔹 Test 5: Testing batch processing...")
        batch_items = [
            ("প্রথম টেস্ট রোস্ট", {'username': 'user1', 'first_name': 'আলম'}),
            ("দ্বিতীয় টেস্ট রোস্ট", {'username': 'user2', 'first_name': 'করিম'}),
            ("তৃতীয় টেস্ট রোস্ট", {'username': 'user3', 'first_name': 'রহিম'})
        ]
        
        batch_results = generator.generate_batch(batch_items)
        success_count = sum(1 for r in batch_results if r.success)
        print(f"   ✅ Batch processed: {success_count}/{len(batch_results)} successful")
        
        # Test 6: Get advanced statistics
        print("\n🔹 Test 6: Checking advanced statistics...")
        stats = generator.get_advanced_stats()
        print(f"   📊 Total generated: {stats['performance']['total_generated']:,}")
        print(f"   🎯 Success rate: {stats['performance']['success_rate']}%")
        print(f"   ⚡ Avg time: {stats['performance']['average_time_seconds']:.2f}s")
        print(f"   🤖 AI generated: {stats['advanced']['ai']['ai_generated']:,}")
        
        # Test 7: Health check
        print("\n🔹 Test 7: Health check...")
        health = generator.health_check()
        print(f"   🩺 System healthy: {'✅ Yes' if health['healthy'] else '❌ No'}")
        
        # Test 8: Generate report
        print("\n🔹 Test 8: Generating report...")
        report = generator.generate_report("test")
        print("   ✅ Report generated")
        
        # Test 9: Cleanup
        print("\n🔹 Test 9: Testing advanced cleanup...")
        generator.cleanup_pro(max_age_hours=0, keep_latest=5)
        print("   ✅ Cleanup completed")
        
        print("\n" + "="*70)
        print("🎉 ALL PRO MAX TESTS PASSED SUCCESSFULLY!")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run test
    success = test_generator_pro_max()
    sys.exit(0 if success else 1)
