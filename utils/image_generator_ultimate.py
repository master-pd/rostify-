#!/usr/bin/env python3
"""
🔥 ULTIMATE IMAGE GENERATOR v8.0 - MASTERPIECE EDITION 🔥
Professional, Artistic, Magically Beautiful Image Generator
Author: Roastify Team | Termux Compatible
Version: 8.0.0 | Masterpiece
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
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union, BinaryIO, Callable
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, wraps
import traceback

# Configure artistic logging
class ColorfulFormatter(logging.Formatter):
    """Colorful logging formatter"""
    COLORS = {
        'DEBUG': '\033[96m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[41m',
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['INFO'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ArtisticImageGenerator')
handler = logging.StreamHandler()
handler.setFormatter(ColorfulFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Import PIL with magic
PIL_AVAILABLE = False
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
    from PIL.Image import Resampling
    from PIL.ImageFilter import GaussianBlur, EMBOSS, CONTOUR, DETAIL, SHARPEN
    PIL_AVAILABLE = True
    logger.info("🎨 PIL/Pillow successfully loaded with artistic features")
except ImportError as e:
    logger.error(f"❌ PIL not available: {e}")
    PIL_AVAILABLE = False

# Constants with artistic touch
DEFAULT_WIDTH = 1200  # Increased for more space
DEFAULT_HEIGHT = 1200
DEFAULT_QUALITY = 100  # Maximum quality
SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP']
MAX_CACHE_SIZE = 2000  # More cache for speed
CACHE_TTL_HOURS = 48

# Enums with more styles
class ArtStyle(Enum):
    """Artistic styles for images"""
    RENAISSANCE = auto()
    IMPRESSIONISM = auto()
    CUBISM = auto()
    SURREALISM = auto()
    POP_ART = auto()
    MINIMALISM = auto()
    CYBERPUNK = auto()
    STEAMPUNK = auto()
    FANTASY = auto()
    GLITCH = auto()
    NEON_NOIR = auto()
    VAPORWAVE = auto()
    KAWAI = auto()
    GOTHIC = auto()
    ART_NOUVEAU = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class TextEffect(Enum):
    """Magical text effects"""
    NONE = auto()
    SHADOW_3D = auto()
    NEON_GLOW = auto()
    GOLDEN_EMBOSS = auto()
    GRADIENT_RAINBOW = auto()
    METALLIC_SHEEN = auto()
    GLASS_REFLECTION = auto()
    FIRE_TEXT = auto()
    ICE_TEXT = auto()
    HOLOGRAM = auto()
    STROBE_GLOW = auto()
    RAINBOW_SHINE = auto()
    GALAXY_TEXT = auto()
    WATER_REFLECTION = auto()
    
    @classmethod
    def get_random(cls, count=1):
        effects = list(cls.__members__.values())
        effects.remove(cls.NONE)
        return random.sample(effects, min(count, len(effects)))

class BorderType(Enum):
    """Artistic border types"""
    NONE = auto()
    GOLDEN_FRAME = auto()
    NEON_TUBE = auto()
    VINE_PATTERN = auto()
    GEOMETRIC_ART = auto()
    CELTIC_KNOT = auto()
    MOROCCAN_TILES = auto()
    JAPANESE_WAVE = auto()
    STAINED_GLASS = auto()
    BRUSH_STROKE = auto()
    SPARKLE_FRAME = auto()
    GALAXY_BORDER = auto()
    CRYSTAL_EDGE = auto()
    FIRE_BORDER = auto()
    ICE_CRYSTAL = auto()
    
    @classmethod
    def get_random(cls):
        types = list(cls.__members__.values())
        types.remove(cls.NONE)
        return random.choice(types)

class BackgroundType(Enum):
    """Magical background types"""
    GALAXY_NEBULA = auto()
    AURORA_BOREALIS = auto()
    OCEAN_DEPTH = auto()
    FOREST_MAGIC = auto()
    FIRE_STORM = auto()
    ICE_PALACE = auto()
    CLOUD_HEAVEN = auto()
    SPACE_TRAVEL = auto()
    RAINBOW_PRISM = auto()
    GEOMETRIC_MANDALA = auto()
    LIQUID_METAL = auto()
    CELESTIAL = auto()
    MYSTIC_RUNES = auto()
    DIGITAL_MATRIX = auto()
    PASTEL_DREAM = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

# Data Classes with artistic defaults
@dataclass
class ArtConfig:
    """Artistic configuration for masterpiece creation"""
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    quality: int = DEFAULT_QUALITY
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl_hours: int = CACHE_TTL_HOURS
    max_cache_size: int = MAX_CACHE_SIZE
    output_dir: str = "./masterpieces"
    temp_dir: str = "./temp_art"
    cache_dir: str = "./art_cache"
    assets_dir: str = "./art_assets"
    backup_dir: str = "./art_backups"
    max_workers: int = 8
    timeout: float = 60.0
    enable_backup: bool = True
    compression_level: int = 9
    art_style: ArtStyle = ArtStyle.get_random()
    enable_animations: bool = False
    magic_intensity: float = 1.0
    
    def __post_init__(self):
        """Create artistic directories"""
        directories = [
            self.output_dir, self.temp_dir, self.cache_dir,
            self.assets_dir, self.backup_dir, "./fonts", "./textures"
        ]
        
        for dir_path in directories:
            try:
                path = Path(dir_path)
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"🎨 Artistic directory ready: {dir_path}")
            except Exception as e:
                logger.error(f"❌ Failed to create directory {dir_path}: {e}")
        
        logger.info(f"🖼️ ArtConfig initialized: {self.width}x{self.height}, Style: {self.art_style.name}")

@dataclass
class TextArt:
    """Artistic text configuration"""
    primary_text: str = ""
    secondary_text: str = ""
    emoji: str = ""
    font_size_primary: int = 80
    font_size_secondary: int = 48
    font_size_emoji: int = 120
    text_color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (30, 30, 60)
    effects: List[TextEffect] = field(default_factory=lambda: [TextEffect.NEON_GLOW])
    alignment: str = "center"
    line_spacing: float = 1.3
    max_width: int = 25
    font_style: str = "bold"
    font_family: str = ""
    opacity: float = 1.0
    rotation: float = 0.0
    text_glow_intensity: int = 3
    text_shadow_depth: int = 5
    gradient_colors: List[Tuple[int, int, int]] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate and enhance text art"""
        if not self.gradient_colors:
            self.gradient_colors = [
                (255, 105, 180),  # Hot pink
                (0, 255, 255),    # Cyan
                (255, 215, 0)     # Gold
            ]

@dataclass
class BorderArt:
    """Artistic border configuration"""
    enabled: bool = True
    border_type: BorderType = BorderType.GOLDEN_FRAME
    color: Tuple[int, int, int] = (255, 215, 0)  # Gold
    secondary_color: Tuple[int, int, int] = (255, 105, 180)  # Pink
    tertiary_color: Tuple[int, int, int] = (0, 255, 255)  # Cyan
    thickness: int = 25
    padding: int = 60
    corner_radius: int = 50
    glow_intensity: int = 3
    opacity: float = 1.0
    pattern_density: float = 0.7
    sparkle_intensity: float = 0.3

@dataclass
class BackgroundArt:
    """Artistic background configuration"""
    type: BackgroundType = BackgroundType.GALAXY_NEBULA
    primary_color: Tuple[int, int, int] = (10, 5, 30)  # Deep space
    secondary_color: Tuple[int, int, int] = (100, 20, 150)  # Purple nebula
    tertiary_color: Tuple[int, int, int] = (20, 150, 200)  # Blue nebula
    texture_path: Optional[str] = None
    opacity: float = 1.0
    blur_radius: int = 0
    noise_intensity: float = 0.1
    vignette_intensity: float = 0.4
    star_density: float = 0.3
    nebula_intensity: float = 0.8
    magic_glow: bool = True

@dataclass
class MasterpieceResult:
    """Result of masterpiece creation"""
    success: bool
    image_path: Optional[str] = None
    animation_path: Optional[str] = None
    error: Optional[str] = None
    creation_time: float = 0.0
    cache_hit: bool = False
    image_size: Optional[int] = None
    artistic_score: float = 0.0
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

# Magical Utility Functions
def create_rainbow_gradient(width: int, height: int) -> Image.Image:
    """Create magical rainbow gradient"""
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    for x in range(width):
        # Rainbow colors
        r = int(255 * abs(math.sin(x * 0.01)))
        g = int(255 * abs(math.sin(x * 0.01 + 2)))
        b = int(255 * abs(math.sin(x * 0.01 + 4)))
        
        for y in range(height):
            # Add some vertical variation
            factor = 0.5 + 0.5 * math.sin(y * 0.005)
            draw.point((x, y), fill=(
                int(r * factor),
                int(g * factor),
                int(b * factor)
            ))
    
    return gradient

def add_stars(image: Image.Image, density: float = 0.3) -> Image.Image:
    """Add magical stars to image"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    star_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(star_layer)
    
    num_stars = int(width * height * density / 10000)
    
    for _ in range(num_stars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 4)
        brightness = random.randint(150, 255)
        twinkle = random.randint(50, 150)
        
        # Draw star with glow
        draw.ellipse([x-size, y-size, x+size, y+size], 
                    fill=(brightness, brightness, brightness, twinkle))
        
        # Add twinkle effect
        if random.random() < 0.3:
            draw.ellipse([x-size*2, y-size*2, x+size*2, y+size*2], 
                        fill=(brightness, brightness, brightness, twinkle//3))
    
    return Image.alpha_composite(image, star_layer)

def create_galaxy_background(width: int, height: int) -> Image.Image:
    """Create magical galaxy background"""
    # Base dark space
    background = Image.new('RGB', (width, height), (5, 5, 20))
    draw = ImageDraw.Draw(background)
    
    # Add nebula clouds
    for _ in range(5):
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        radius = random.randint(100, 400)
        
        # Nebula colors
        colors = [
            (100, 20, 150, 30),   # Purple
            (20, 100, 200, 40),   # Blue
            (200, 50, 100, 35),   # Pink
            (50, 200, 150, 25)    # Teal
        ]
        
        for r in range(radius, 0, -radius//10):
            color = random.choice(colors)
            alpha = color[3] * r // radius
            
            draw.ellipse(
                [center_x - r, center_y - r, center_x + r, center_y + r],
                fill=(color[0], color[1], color[2], alpha)
            )
    
    # Convert to RGB for consistency
    background = background.convert('RGB')
    
    # Add stars
    background = add_stars(background.convert('RGBA'), density=0.5)
    
    # Add subtle blur for dreamy effect
    background = background.filter(GaussianBlur(radius=1))
    
    return background.convert('RGB')

# Artistic Managers
class MagicFontManager:
    """Magical font manager with special effects"""
    
    def __init__(self, assets_dir: str = "./art_assets"):
        self.fonts_dir = Path(assets_dir) / "fonts"
        self.fonts_dir.mkdir(parents=True, exist_ok=True)
        
        self.font_cache = {}
        self.available_fonts = []
        self.special_fonts = {}
        
        self._load_magical_fonts()
        logger.info(f"🔮 MagicFontManager loaded {len(self.available_fonts)} fonts")
    
    def _load_magical_fonts(self):
        """Load magical fonts"""
        # Try to load system and custom fonts
        font_locations = [
            self.fonts_dir,
            Path("/system/fonts"),
            Path("/data/data/com.termux/files/usr/share/fonts"),
            Path("/usr/share/fonts/truetype"),
            Path("./fonts"),
        ]
        
        for location in font_locations:
            if location.exists():
                for ext in ['.ttf', '.otf']:
                    for font_file in location.rglob(f"*{ext}"):
                        try:
                            font_path = str(font_file.resolve())
                            if font_path not in self.available_fonts:
                                # Test font
                                ImageFont.truetype(font_path, 12)
                                self.available_fonts.append(font_path)
                                
                                # Categorize by style
                                name = font_file.stem.lower()
                                if any(x in name for x in ['bold', 'heavy', 'black']):
                                    self.special_fonts['bold'] = font_path
                                elif any(x in name for x in ['italic', 'oblique']):
                                    self.special_fonts['italic'] = font_path
                                elif any(x in name for x in ['decorative', 'ornate', 'fancy']):
                                    self.special_fonts['fancy'] = font_path
                        except:
                            continue
        
        # Fallback to default
        if not self.available_fonts:
            logger.warning("Using default fonts - add custom fonts for better results")
    
    def get_magical_font(self, size: int, style: str = "regular", effect: TextEffect = TextEffect.NONE):
        """Get magical font with effects"""
        cache_key = f"{size}_{style}_{effect.name}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        try:
            # Try to get appropriate font
            font_path = None
            
            if style == "bold" and 'bold' in self.special_fonts:
                font_path = self.special_fonts['bold']
            elif style == "italic" and 'italic' in self.special_fonts:
                font_path = self.special_fonts['italic']
            elif style == "fancy" and 'fancy' in self.special_fonts:
                font_path = self.special_fonts['fancy']
            
            if not font_path and self.available_fonts:
                font_path = random.choice(self.available_fonts)
            
            if font_path:
                font = ImageFont.truetype(font_path, size)
            else:
                font = ImageFont.load_default()
                # Enlarge default font for better appearance
                font = ImageFont.truetype("", size) if PIL_AVAILABLE else font
            
            # Apply simulated effects through font selection
            if effect == TextEffect.FIRE_TEXT and 'bold' in self.special_fonts:
                font = ImageFont.truetype(self.special_fonts['bold'], size)
            elif effect == TextEffect.ICE_TEXT and self.available_fonts:
                font = ImageFont.truetype(random.choice(self.available_fonts), size)
            
            self.font_cache[cache_key] = font
            return font
            
        except Exception as e:
            logger.error(f"Font error: {e}")
            return ImageFont.load_default()

class ColorAlchemy:
    """Magical color manipulation"""
    
    def __init__(self):
        self.palettes = self._create_magical_palettes()
        self.gradient_cache = {}
    
    def _create_magical_palettes(self):
        """Create magical color palettes"""
        return {
            "galactic": {
                "name": "Galactic Dream",
                "primary": (10, 5, 30),
                "secondary": (100, 20, 150),
                "accent": (0, 255, 255),
                "text": (255, 255, 255),
                "highlight": (255, 105, 180),
                "border": (255, 215, 0),
                "glow": (0, 200, 255)
            },
            "inferno": {
                "name": "Inferno Flame",
                "primary": (20, 5, 10),
                "secondary": (100, 20, 10),
                "accent": (255, 100, 0),
                "text": (255, 255, 200),
                "highlight": (255, 50, 0),
                "border": (255, 150, 0),
                "glow": (255, 50, 0)
            },
            "arctic": {
                "name": "Arctic Ice",
                "primary": (5, 10, 30),
                "secondary": (20, 50, 100),
                "accent": (150, 230, 255),
                "text": (220, 240, 255),
                "highlight": (100, 200, 255),
                "border": (0, 150, 255),
                "glow": (100, 200, 255)
            },
            "forest": {
                "name": "Enchanted Forest",
                "primary": (5, 20, 10),
                "secondary": (20, 80, 40),
                "accent": (100, 255, 150),
                "text": (220, 255, 220),
                "highlight": (50, 200, 100),
                "border": (100, 255, 150),
                "glow": (50, 255, 100)
            },
            "golden": {
                "name": "Golden Royalty",
                "primary": (30, 20, 5),
                "secondary": (80, 60, 20),
                "accent": (255, 215, 0),
                "text": (255, 240, 200),
                "highlight": (255, 200, 0),
                "border": (255, 215, 0),
                "glow": (255, 200, 50)
            },
            "neon": {
                "name": "Neon Cyberpunk",
                "primary": (0, 5, 15),
                "secondary": (20, 0, 40),
                "accent": (255, 0, 255),
                "text": (0, 255, 255),
                "highlight": (255, 0, 150),
                "border": (0, 255, 200),
                "glow": (255, 0, 255)
            }
        }
    
    def get_magical_palette(self, style: str = None):
        """Get magical color palette"""
        if style and style in self.palettes:
            return self.palettes[style]
        
        # Auto-select based on time
        hour = datetime.now().hour
        if hour < 6:
            return self.palettes["galactic"]
        elif hour < 12:
            return self.palettes["golden"]
        elif hour < 18:
            return self.palettes["forest"]
        else:
            return random.choice(list(self.palettes.values()))
    
    def create_gradient_magic(self, width: int, height: int, palette: Dict) -> Image.Image:
        """Create magical gradient background"""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        # Create diagonal gradient with multiple colors
        for x in range(width):
            for y in range(height):
                ratio = (x + y) / (width + height)
                
                # Interpolate between colors
                if ratio < 0.33:
                    r = int(palette['primary'][0] * (1 - ratio*3) + palette['secondary'][0] * ratio*3)
                    g = int(palette['primary'][1] * (1 - ratio*3) + palette['secondary'][1] * ratio*3)
                    b = int(palette['primary'][2] * (1 - ratio*3) + palette['secondary'][2] * ratio*3)
                elif ratio < 0.66:
                    r = int(palette['secondary'][0] * (1 - (ratio-0.33)*3) + palette['accent'][0] * (ratio-0.33)*3)
                    g = int(palette['secondary'][1] * (1 - (ratio-0.33)*3) + palette['accent'][1] * (ratio-0.33)*3)
                    b = int(palette['secondary'][2] * (1 - (ratio-0.33)*3) + palette['accent'][2] * (ratio-0.33)*3)
                else:
                    r = int(palette['accent'][0] * (1 - (ratio-0.66)*3) + palette['highlight'][0] * (ratio-0.66)*3)
                    g = int(palette['accent'][1] * (1 - (ratio-0.66)*3) + palette['highlight'][1] * (ratio-0.66)*3)
                    b = int(palette['accent'][2] * (1 - (ratio-0.66)*3) + palette['highlight'][2] * (ratio-0.66)*3)
                
                draw.point((x, y), fill=(r, g, b))
        
        return gradient
    
    def rainbow_text_color(self, x: int, y: int, width: int, height: int) -> Tuple[int, int, int]:
        """Generate rainbow color for text"""
        hue = (x + y) / (width + height) * 360
        return self.hsv_to_rgb(hue, 0.8, 1.0)
    
    def hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        h = h % 360
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
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )

class ArtMagic:
    """Magical artistic effects"""
    
    @staticmethod
    def apply_text_magic(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                        position: Tuple[int, int], effect: TextEffect,
                        colors: List[Tuple[int, int, int]] = None):
        """Apply magical effects to text"""
        x, y = position
        
        if effect == TextEffect.NEON_GLOW:
            ArtMagic._neon_glow_text(draw, text, font, (x, y), colors)
        elif effect == TextEffect.GOLDEN_EMBOSS:
            ArtMagic._golden_emboss_text(draw, text, font, (x, y))
        elif effect == TextEffect.GRADIENT_RAINBOW:
            ArtMagic._rainbow_gradient_text(draw, text, font, (x, y))
        elif effect == TextEffect.FIRE_TEXT:
            ArtMagic._fire_text(draw, text, font, (x, y))
        elif effect == TextEffect.ICE_TEXT:
            ArtMagic._ice_text(draw, text, font, (x, y))
        else:
            # Default shadow effect
            draw.text((x+3, y+3), text, font=font, fill=(0, 0, 0, 100))
            draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    @staticmethod
    def _neon_glow_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                       position: Tuple[int, int], colors: List[Tuple[int, int, int]]):
        """Create neon glow text"""
        x, y = position
        
        # Multiple glow layers
        for i in range(5, 0, -1):
            glow_color = (
                min(255, colors[0][0] + i*10),
                min(255, colors[1][1] + i*10),
                min(255, colors[2][2] + i*10),
                50 - i*8
            )
            
            for dx in range(-i, i+1, 2):
                for dy in range(-i, i+1, 2):
                    draw.text((x+dx, y+dy), text, font=font, fill=glow_color)
        
        # Main text
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    @staticmethod
    def _golden_emboss_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                          position: Tuple[int, int]):
        """Create golden embossed text"""
        x, y = position
        
        # Shadow for depth
        draw.text((x+2, y+2), text, font=font, fill=(100, 70, 0))
        
        # Golden gradient
        for i in range(3):
            shade = 200 - i*20
            draw.text((x-i, y-i), text, font=font, fill=(shade, shade//2, 0))
        
        # Highlight
        draw.text((x, y), text, font=font, fill=(255, 215, 0))
    
    @staticmethod
    def _rainbow_gradient_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                              position: Tuple[int, int]):
        """Create rainbow gradient text"""
        x, y = position
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Draw rainbow gradient by drawing each character separately
        for i, char in enumerate(text):
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            
            # Rainbow color based on position
            hue = (i / len(text)) * 360
            color = ColorAlchemy().hsv_to_rgb(hue, 0.8, 1.0)
            
            # Draw character
            char_x = x + sum(draw.textbbox((0, 0), text[j], font=font)[2] - 
                           draw.textbbox((0, 0), text[j], font=font)[0] 
                           for j in range(i))
            
            draw.text((char_x, y), char, font=font, fill=color)
    
    @staticmethod
    def _fire_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                  position: Tuple[int, int]):
        """Create fire effect text"""
        x, y = position
        
        # Fire gradient from yellow to red
        colors = [
            (255, 255, 0),   # Yellow
            (255, 150, 0),   # Orange
            (255, 50, 0),    # Red
            (150, 0, 0)      # Dark red
        ]
        
        # Draw multiple layers for fire effect
        for i, color in enumerate(colors):
            offset = i * 2
            draw.text((x - offset//2, y - offset), text, font=font, fill=color)
        
        # White hot center
        draw.text((x, y), text, font=font, fill=(255, 255, 200))
    
    @staticmethod
    def _ice_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                 position: Tuple[int, int]):
        """Create ice effect text"""
        x, y = position
        
        # Ice gradient
        colors = [
            (200, 230, 255),  # Light blue
            (150, 200, 255),  # Blue
            (100, 170, 255),  # Deep blue
            (50, 100, 200)    # Dark blue
        ]
        
        # Draw icy layers
        for i, color in enumerate(colors):
            offset = i
            for dx in range(-offset, offset+1):
                for dy in range(-offset, offset+1):
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill=(*color, 50))
        
        # Main icy text
        draw.text((x, y), text, font=font, fill=(200, 230, 255))
    
    @staticmethod
    def create_magical_border(image: Image.Image, border_type: BorderType,
                            colors: Tuple[Tuple[int, int, int], ...]) -> Image.Image:
        """Create magical borders"""
        if border_type == BorderType.NONE:
            return image
        
        width, height = image.size
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        border_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border_layer)
        
        if border_type == BorderType.GOLDEN_FRAME:
            # Golden frame with ornate corners
            thickness = 30
            
            # Main frame
            draw.rectangle(
                [thickness, thickness, width-thickness, height-thickness],
                outline=(*colors[0], 255),
                width=thickness
            )
            
            # Inner highlight
            draw.rectangle(
                [thickness*2, thickness*2, width-thickness*2, height-thickness*2],
                outline=(*colors[1], 200),
                width=thickness//3
            )
            
            # Ornate corners
            corner_size = 60
            for corner_x, corner_y in [(0, 0), (width, 0), (0, height), (width, height)]:
                if corner_x == 0 and corner_y == 0:  # Top-left
                    draw.arc([-corner_size, -corner_size, corner_size, corner_size], 
                            0, 90, fill=(*colors[0], 255), width=10)
                elif corner_x == width and corner_y == 0:  # Top-right
                    draw.arc([width-corner_size, -corner_size, width+corner_size, corner_size], 
                            90, 180, fill=(*colors[0], 255), width=10)
                elif corner_x == 0 and corner_y == height:  # Bottom-left
                    draw.arc([-corner_size, height-corner_size, corner_size, height+corner_size], 
                            270, 360, fill=(*colors[0], 255), width=10)
                else:  # Bottom-right
                    draw.arc([width-corner_size, height-corner_size, width+corner_size, height+corner_size], 
                            180, 270, fill=(*colors[0], 255), width=10)
        
        elif border_type == BorderType.NEON_TUBE:
            # Neon tube border with glow
            thickness = 20
            
            # Multiple glow layers
            for i in range(3):
                glow_thickness = thickness + i * 10
                glow_alpha = 150 - i * 50
                
                draw.rounded_rectangle(
                    [glow_thickness, glow_thickness, 
                     width-glow_thickness, height-glow_thickness],
                    radius=40,
                    outline=(*colors[0], glow_alpha),
                    width=5
                )
            
            # Main neon tube
            draw.rounded_rectangle(
                [thickness, thickness, width-thickness, height-thickness],
                radius=40,
                outline=(*colors[0], 255),
                width=thickness//2
            )
        
        elif border_type == BorderType.SPARKLE_FRAME:
            # Sparkling frame
            thickness = 25
            
            # Frame
            draw.rectangle(
                [thickness, thickness, width-thickness, height-thickness],
                outline=(*colors[0], 255),
                width=thickness
            )
            
            # Add sparkles
            for _ in range(50):
                side = random.choice(['top', 'bottom', 'left', 'right'])
                
                if side == 'top':
                    x = random.randint(thickness*2, width-thickness*2)
                    y = thickness
                elif side == 'bottom':
                    x = random.randint(thickness*2, width-thickness*2)
                    y = height - thickness
                elif side == 'left':
                    x = thickness
                    y = random.randint(thickness*2, height-thickness*2)
                else:
                    x = width - thickness
                    y = random.randint(thickness*2, height-thickness*2)
                
                size = random.randint(2, 5)
                sparkle_color = random.choice([colors[0], colors[1], (255, 255, 255)])
                
                draw.ellipse(
                    [x-size, y-size, x+size, y+size],
                    fill=(*sparkle_color, 200)
                )
        
        # Composite with original image
        return Image.alpha_composite(image, border_layer)

# Main Magical Generator
class MagicalImageGenerator:
    """✨ MAGICAL IMAGE GENERATOR v8.0 - MASTERPIECE EDITION ✨"""
    
    def __init__(self, config: Optional[ArtConfig] = None):
        if not PIL_AVAILABLE:
            logger.critical("❌ PIL/Pillow not available!")
            raise ImportError("Install PIL/Pillow: pip install pillow")
        
        self.config = config or ArtConfig()
        self.font_magic = MagicFontManager(self.config.assets_dir)
        self.color_alchemy = ColorAlchemy()
        self.art_magic = ArtMagic()
        
        # Statistics with artistic flair
        self.stats = {
            'masterpieces_created': 0,
            'magic_score': 0.0,
            'creation_time': 0.0,
            'cache_magic': 0,
            'failed_spells': 0,
            'styles_used': {}
        }
        
        logger.info("✨ Magical Image Generator v8.0 Initialized!")
        logger.info(f"   🎨 Art Style: {self.config.art_style.name}")
        logger.info(f"   📏 Canvas: {self.config.width}x{self.config.height}")
        logger.info(f"   🌈 Magic Intensity: {self.config.magic_intensity}")
    
    def create_masterpiece(self, text: str, user_info: Any,
                          art_style: Optional[ArtStyle] = None,
                          border_art: Optional[BorderArt] = None,
                          background_art: Optional[BackgroundArt] = None) -> MasterpieceResult:
        """
        Create a magical masterpiece!
        
        Args:
            text: The text to display
            user_info: User information for personalization
            art_style: Artistic style
            border_art: Border configuration
            background_art: Background configuration
            
        Returns:
            MasterpieceResult with magical details
        """
        start_time = time.time()
        
        try:
            # Prepare magical ingredients
            art_style = art_style or self.config.art_style
            border_art = border_art or BorderArt()
            background_art = background_art or BackgroundArt()
            
            # Process user info
            user_dict = self._process_user_magic(user_info)
            
            # Update style usage
            self.stats['styles_used'][art_style.name] = \
                self.stats['styles_used'].get(art_style.name, 0) + 1
            
            # Create magical canvas
            width, height = self.config.width, self.config.height
            
            # 1. Create magical background
            logger.info(f"🎨 Creating {background_art.type.name} background...")
            background = self._create_magical_background(
                width, height, background_art, art_style
            )
            
            # 2. Prepare text art
            text_art = TextArt(
                primary_text=text,
                secondary_text=f"By: {user_dict.get('name', 'Anonymous')}",
                emoji=random.choice(['✨', '🌟', '🎨', '🔥', '❄️', '💫', '🌠', '🎭']),
                effects=TextEffect.get_random(random.randint(1, 2))
            )
            
            # 3. Render magical text
            logger.info(f"🔮 Applying {text_art.effects[0].name} to text...")
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            self._render_magical_text(draw, text_art, width, height, user_dict)
            
            # 4. Apply magical border
            if border_art.enabled and border_art.border_type != BorderType.NONE:
                logger.info(f"🖼️ Adding {border_art.border_type.name} border...")
                colors = (border_art.color, border_art.secondary_color, border_art.tertiary_color)
                image = self.art_magic.create_magical_border(
                    image, border_art.border_type, colors
                )
            
            # 5. Apply final magical effects
            image = self._apply_final_magic(image, art_style)
            
            # 6. Save masterpiece
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            masterpiece_name = f"masterpiece_{timestamp}_{hash(text) % 10000:04d}.png"
            output_path = Path(self.config.output_dir) / masterpiece_name
            
            # Ensure highest quality
            save_kwargs = {
                'quality': self.config.quality,
                'optimize': True,
                'compress_level': self.config.compression_level
            }
            
            if self.config.format == 'PNG':
                image.save(output_path, 'PNG', **save_kwargs)
            else:
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                image.save(output_path, self.config.format, **save_kwargs)
            
            # 7. Calculate magical score
            creation_time = time.time() - start_time
            magic_score = self._calculate_magic_score(
                creation_time, 
                len(text), 
                len(text_art.effects)
            )
            
            # Update statistics
            self.stats['masterpieces_created'] += 1
            self.stats['magic_score'] += magic_score
            self.stats['creation_time'] += creation_time
            
            # Create magical result
            result = MasterpieceResult(
                success=True,
                image_path=str(output_path),
                creation_time=round(creation_time, 3),
                cache_hit=False,
                image_size=os.path.getsize(output_path),
                artistic_score=round(magic_score, 2),
                metadata={
                    'masterpiece_id': masterpiece_name,
                    'art_style': art_style.name,
                    'border_type': border_art.border_type.name,
                    'background_type': background_art.type.name,
                    'text_effects': [e.name for e in text_art.effects],
                    'user': user_dict.get('name', 'Anonymous'),
                    'magic_level': self._get_magic_level(magic_score),
                    'creation_date': datetime.now().isoformat()
                }
            )
            
            logger.info(f"✅ MASTERPIECE CREATED: {masterpiece_name}")
            logger.info(f"   ⭐ Magic Score: {magic_score:.2f}")
            logger.info(f"   ⏱️ Creation Time: {creation_time:.2f}s")
            logger.info(f"   🎨 Style: {art_style.name}")
            
            return result
            
        except Exception as e:
            creation_time = time.time() - start_time
            self.stats['failed_spells'] += 1
            
            logger.error(f"❌ Masterpiece creation failed: {e}")
            logger.error(traceback.format_exc())
            
            return MasterpieceResult(
                success=False,
                error=str(e),
                creation_time=round(creation_time, 3),
                artistic_score=0.0,
                metadata={'error_type': type(e).__name__}
            )
    
    def _create_magical_background(self, width: int, height: int, 
                                 background_art: BackgroundArt, 
                                 art_style: ArtStyle) -> Image.Image:
        """Create magical background based on type"""
        bg_type = background_art.type
        
        if bg_type == BackgroundType.GALAXY_NEBULA:
            background = create_galaxy_background(width, height)
        elif bg_type == BackgroundType.AURORA_BOREALIS:
            # Create aurora effect
            background = Image.new('RGB', (width, height), (5, 10, 30))
            draw = ImageDraw.Draw(background)
            
            # Aurora waves
            for y in range(0, height, 20):
                wave_height = random.randint(30, 100)
                aurora_color = random.choice([
                    (0, 255, 150, 50),  # Green
                    (150, 0, 255, 60),  # Purple
                    (0, 150, 255, 55)   # Blue
                ])
                
                for x in range(width):
                    wave = wave_height * math.sin(x * 0.02 + y * 0.01)
                    draw.line(
                        [(x, y + wave), (x, y + wave + 5)],
                        fill=aurora_color,
                        width=3
                    )
        else:
            # Default gradient background
            palette = self.color_alchemy.get_magical_palette()
            background = self.color_alchemy.create_gradient_magic(width, height, palette)
        
        # Apply artistic filters based on style
        if art_style == ArtStyle.IMPRESSIONISM:
            background = background.filter(GaussianBlur(radius=2))
        elif art_style == ArtStyle.CYBERPUNK:
            # Increase contrast and saturation
            enhancer = ImageEnhance.Contrast(background)
            background = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Color(background)
            background = enhancer.enhance(1.8)
        elif art_style == ArtStyle.GLITCH:
            # Apply glitch effect
            for _ in range(3):
                offset = random.randint(-10, 10)
                glitch_layer = background.copy()
                glitch_layer = ImageChops.offset(glitch_layer, offset, 0)
                background = Image.blend(background, glitch_layer, 0.3)
        
        return background
    
    def _render_magical_text(self, draw: ImageDraw.Draw, text_art: TextArt,
                           width: int, height: int, user_info: Dict):
        """Render text with magical effects"""
        # Get magical font
        font = self.font_magic.get_magical_font(
            text_art.font_size_primary,
            text_art.font_style,
            text_art.effects[0] if text_art.effects else TextEffect.NONE
        )
        
        # Wrap text for beauty
        lines = textwrap.wrap(text_art.primary_text, width=text_art.max_width)
        
        # Calculate text position (centered)
        line_height = int(text_art.font_size_primary * text_art.line_spacing)
        total_text_height = len(lines) * line_height
        
        # Start position (slightly above center for better composition)
        start_y = (height - total_text_height) // 3
        
        # Draw each line with magic
        palette = self.color_alchemy.get_magical_palette()
        
        for i, line in enumerate(lines):
            # Get text width
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            
            # Center position
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            # Apply magical effect
            colors = [
                palette['accent'],
                palette['highlight'],
                palette['glow']
            ]
            
            self.art_magic.apply_text_magic(
                draw, line, font, (x, y), 
                text_art.effects[0] if text_art.effects else TextEffect.NEON_GLOW,
                colors
            )
        
        # Add signature/emoji
        if text_art.emoji:
            emoji_font = self.font_magic.get_magical_font(
                text_art.font_size_emoji, "regular", TextEffect.NONE
            )
            bbox = draw.textbbox((0, 0), text_art.emoji, font=emoji_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + len(lines) * line_height + 50
            draw.text((x, y), text_art.emoji, font=emoji_font, fill=palette['highlight'])
        
        # Add user signature
        signature = f"~ {user_info.get('name', 'Anonymous')}"
        small_font = self.font_magic.get_magical_font(24, "italic", TextEffect.NONE)
        bbox = draw.textbbox((0, 0), signature, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = width - text_width - 50
        y = height - 80
        draw.text((x, y), signature, font=small_font, fill=palette['text'])
        
        # Add magical watermark
        watermark = "✨ Magically Created by Roastify ✨"
        watermark_font = self.font_magic.get_magical_font(20, "regular", TextEffect.NONE)
        bbox = draw.textbbox((0, 0), watermark, font=watermark_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 40
        draw.text((x, y), watermark, font=watermark_font, fill=(255, 255, 255, 150))
    
    def _apply_final_magic(self, image: Image.Image, art_style: ArtStyle) -> Image.Image:
        """Apply final magical touches"""
        # Apply vignette
        if random.random() > 0.2:
            image = self._apply_vignette(image, intensity=0.3)
        
        # Apply glow based on style
        if art_style in [ArtStyle.CYBERPUNK, ArtStyle.NEON_NOIR, ArtStyle.VAPORWAVE]:
            image = self._apply_glow_effect(image, intensity=0.2)
        
        # Add subtle noise for texture
        if random.random() > 0.5:
            image = self._add_texture_noise(image, intensity=0.05)
        
        return image
    
    def _apply_vignette(self, image: Image.Image, intensity: float = 0.3) -> Image.Image:
        """Apply vignette effect"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        width, height = image.size
        vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vignette)
        
        center_x, center_y = width // 2, height // 2
        max_radius = int(math.sqrt(width**2 + height**2) / 2)
        
        for i in range(20):
            radius = int(max_radius * (i / 20))
            alpha = int(255 * intensity * (1 - (i / 20)**2))
            
            if radius > 0 and alpha > 0:
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    fill=(0, 0, 0, alpha),
                    outline=None
                )
        
        return Image.alpha_composite(image, vignette)
    
    def _apply_glow_effect(self, image: Image.Image, intensity: float = 0.2) -> Image.Image:
        """Apply glow effect"""
        glow = image.filter(GaussianBlur(radius=5))
        return Image.blend(image, glow, intensity)
    
    def _add_texture_noise(self, image: Image.Image, intensity: float = 0.05) -> Image.Image:
        """Add subtle texture noise"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        width, height = image.size
        noise = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(noise)
        
        num_dots = int(width * height * intensity)
        
        for _ in range(num_dots):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            alpha = random.randint(5, 20)
            size = random.randint(1, 2)
            brightness = random.randint(200, 255)
            
            draw.ellipse(
                [x, y, x + size, y + size],
                fill=(brightness, brightness, brightness, alpha)
            )
        
        return Image.alpha_composite(image, noise)
    
    def _process_user_magic(self, user_info: Any) -> Dict:
        """Process user information with magical touch"""
        default_user = {
            'id': random.randint(1000, 9999),
            'name': 'Mysterious Traveler',
            'title': random.choice(['Wizard', 'Sorcerer', 'Enchanter', 'Mage', 'Artisan']),
            'magic_level': random.randint(1, 100),
            'favorite_color': random.choice(['Azure', 'Crimson', 'Emerald', 'Amethyst', 'Gold']),
            'joined': datetime.now().strftime('%Y-%m-%d')
        }
        
        if isinstance(user_info, dict):
            default_user.update(user_info)
        
        return default_user
    
    def _calculate_magic_score(self, time_taken: float, text_length: int, 
                             effects_count: int) -> float:
        """Calculate magical score for the masterpiece"""
        # Base score
        score = 100.0
        
        # Time bonus (faster = better, but not too fast)
        if time_taken < 0.5:
            score += 20
        elif time_taken < 1.0:
            score += 10
        elif time_taken > 5.0:
            score -= 10
        
        # Text length bonus
        if text_length > 50:
            score += text_length / 10
        
        # Effects bonus
        score += effects_count * 15
        
        # Random magic factor
        score += random.uniform(-10, 20)
        
        # Ensure reasonable range
        return max(50, min(score, 200))
    
    def _get_magic_level(self, score: float) -> str:
        """Get magical level based on score"""
        if score >= 180:
            return "✨ LEGENDARY ✨"
        elif score >= 150:
            return "🌟🌟🌟 MASTERPIECE 🌟🌟🌟"
        elif score >= 120:
            return "🌟🌟 EXCELLENT 🌟🌟"
        elif score >= 90:
            return "⭐ GOOD ⭐"
        elif score >= 70:
            return "🔼 DECENT 🔼"
        else:
            return "📝 PRACTICE 📝"
    
    def get_magical_stats(self) -> Dict:
        """Get magical statistics"""
        avg_score = 0
        avg_time = 0
        
        if self.stats['masterpieces_created'] > 0:
            avg_score = self.stats['magic_score'] / self.stats['masterpieces_created']
            avg_time = self.stats['creation_time'] / self.stats['masterpieces_created']
        
        return {
            'magical_performance': {
                'masterpieces_created': self.stats['masterpieces_created'],
                'average_magic_score': round(avg_score, 2),
                'average_creation_time': round(avg_time, 3),
                'failed_spells': self.stats['failed_spells'],
                'success_rate': round(
                    (self.stats['masterpieces_created'] / 
                     max(self.stats['masterpieces_created'] + self.stats['failed_spells'], 1)) * 100, 
                    1
                )
            },
            'artistic_insights': {
                'total_styles_used': len(self.stats['styles_used']),
                'most_popular_style': max(
                    self.stats['styles_used'].items(), 
                    key=lambda x: x[1], 
                    default=('NONE', 0)
                )[0],
                'style_distribution': self.stats['styles_used']
            },
            'generator_info': {
                'version': '8.0.0',
                'art_style': self.config.art_style.name,
                'magic_intensity': self.config.magic_intensity,
                'canvas_size': f"{self.config.width}x{self.config.height}",
                'max_workers': self.config.max_workers
            }
        }
    
    def create_demo_masterpiece(self):
        """Create a demo masterpiece to show magical powers"""
        demo_texts = [
            "✨ Magic is Real! ✨",
            "🎨 Create Your Masterpiece 🎨",
            "🌟 Dream Big, Create Bigger 🌟",
            "🔥 Passion Fuels Creation 🔥",
            "💫 Where Art Meets Magic 💫"
        ]
        
        demo_user = {
            'name': 'Artistic Soul',
            'title': 'Master Creator',
            'magic_level': 99,
            'favorite_color': 'Rainbow'
        }
        
        result = self.create_masterpiece(
            text=random.choice(demo_texts),
            user_info=demo_user,
            art_style=ArtStyle.get_random(),
            border_art=BorderArt(border_type=BorderType.get_random()),
            background_art=BackgroundArt(type=BackgroundType.get_random())
        )
        
        return result

# For backward compatibility
UltimateImageGenerator = MagicalImageGenerator
GenerationResult = MasterpieceResult
ImageConfig = ArtConfig
TextConfig = TextArt
BorderConfig = BorderArt
BackgroundConfig = BackgroundArt

# Magical test function
def test_magical_generator():
    """Test the magical generator"""
    print("\n" + "="*70)
    print("✨ MAGICAL IMAGE GENERATOR v8.0 - DEMONSTRATION ✨")
    print("="*70)
    
    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow not installed!")
        print("   Install with: pip install pillow")
        return False
    
    try:
        # Create magical generator
        print("\n🔮 Initializing Magical Generator...")
        generator = MagicalImageGenerator()
        print("   ✅ Generator ready with magical powers!")
        
        # Create demo masterpiece
        print("\n🎨 Creating Demo Masterpiece...")
        result = generator.create_demo_masterpiece()
        
        if result.success:
            print(f"   ✅ Masterpiece created: {result.image_path}")
            print(f"   ⭐ Artistic Score: {result.artistic_score}")
            print(f"   ⏱️ Creation Time: {result.creation_time}s")
            print(f"   🎭 Style: {result.metadata['art_style']}")
            print(f"   🖼️ Border: {result.metadata['border_type']}")
            print(f"   🌈 Background: {result.metadata['background_type']}")
            print(f"   ✨ Magic Level: {result.metadata['magic_level']}")
        else:
            print(f"   ❌ Failed: {result.error}")
        
        # Show statistics
        print("\n📊 Magical Statistics:")
        stats = generator.get_magical_stats()
        print(f"   Masterpieces Created: {stats['magical_performance']['masterpieces_created']}")
        print(f"   Average Magic Score: {stats['magical_performance']['average_magic_score']}")
        print(f"   Success Rate: {stats['magical_performance']['success_rate']}%")
        print(f"   Styles Used: {stats['artistic_insights']['total_styles_used']}")
        
        print("\n" + "="*70)
        print("🎉 MAGICAL TEST COMPLETED SUCCESSFULLY! 🎉")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ MAGICAL TEST FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run magical test
    print("Starting Magical Image Generator v8.0...")
    success = test_magical_generator()
    
    if success:
        print("\n✨ Generator is ready to create MASTERPIECES! ✨")
        print("\nUsage example:")
        print("""
        # Create magical generator
        generator = MagicalImageGenerator()
        
        # Create a masterpiece
        result = generator.create_masterpiece(
            text="Your magical text here",
            user_info={"name": "Your Name"},
            art_style=ArtStyle.CYBERPUNK,
            border_art=BorderArt(border_type=BorderType.NEON_TUBE),
            background_art=BackgroundArt(type=BackgroundType.GALAXY_NEBULA)
        )
        
        if result.success:
            print(f"🎨 Masterpiece saved to: {result.image_path}")
            print(f"⭐ Artistic Score: {result.artistic_score}")
        else:
            print(f"❌ Failed: {result.error}")
        """)
    else:
        print("\n⚠️ Generator needs some magical tuning!")
    
    sys.exit(0 if success else 1)
