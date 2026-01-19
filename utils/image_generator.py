#!/usr/bin/env python3
"""
ROASTIFY ULTIMATE IMAGE GENERATOR
Professional Production-Grade Image Generation System
Version: 4.0.0 | Termux Compatible | Fully Fixed
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
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union, BinaryIO
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache

# Configure Unicode support
if sys.version_info < (3, 7):
    reload(sys)
    sys.setdefaultencoding('utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_generator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import PIL with comprehensive fallback
PIL_AVAILABLE = False
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
    from PIL.Image import Resampling
    PIL_AVAILABLE = True
    logger.info("✓ PIL/Pillow successfully loaded")
except ImportError as e:
    logger.error(f"✗ PIL not available: {e}. Install with: pip install pillow")


class ImageStyle(Enum):
    """Available image styles"""
    DARK = "dark"
    LIGHT = "light"
    NEON = "neon"
    VINTAGE = "vintage"
    CYBERPUNK = "cyberpunk"
    MINIMAL = "minimal"
    GRUNGE = "grunge"
    RETRO = "retro"
    GLOW = "glow"


class TextEffect(Enum):
    """Text effect types"""
    SHADOW = "shadow"
    GLOW = "glow"
    OUTLINE = "outline"
    GRADIENT = "gradient"
    EMBOSS = "emboss"
    NEON = "neon"
    STROKE = "stroke"
    REFLECTION = "reflection"


class BorderType(Enum):
    """Border styles"""
    SIMPLE = "simple"
    DOUBLE = "double"
    ROUNDED = "rounded"
    DOTTED = "dotted"
    DASHED = "dashed"
    ORNATE = "ornate"
    NEON = "neon"
    NONE = "none"


@dataclass
class ImageConfig:
    """Image generation configuration"""
    width: int = 1080
    height: int = 1080
    quality: int = 95
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl_hours: int = 24
    max_cache_size: int = 100
    output_dir: str = "./output"
    temp_dir: str = "./temp"
    cache_dir: str = "./cache"
    assets_dir: str = "./assets"
    
    def __post_init__(self):
        """Create directories"""
        for dir_path in [self.output_dir, self.temp_dir, self.cache_dir, self.assets_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


@dataclass
class TextConfig:
    """Text configuration"""
    primary_text: str
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
    max_width: int = 30
    font_style: str = "bold"


@dataclass
class BorderConfig:
    """Border configuration"""
    enabled: bool = True
    border_type: BorderType = BorderType.ROUNDED
    color: Tuple[int, int, int] = (255, 105, 180)
    thickness: int = 20
    padding: int = 50
    corner_radius: int = 40
    glow_intensity: int = 0


@dataclass
class BackgroundConfig:
    """Background configuration"""
    type: str = "gradient"  # solid, gradient, pattern, image
    primary_color: Tuple[int, int, int] = (20, 20, 40)
    secondary_color: Optional[Tuple[int, int, int]] = None
    image_path: Optional[str] = None
    opacity: float = 1.0
    blur_radius: int = 0
    pattern_type: str = "none"  # grid, dots, lines, noise, geometric
    pattern_color: Optional[Tuple[int, int, int]] = None
    pattern_intensity: float = 0.3


class FontManager:
    """Professional font manager with caching and fallbacks"""
    
    def __init__(self, assets_dir: str = "./assets"):
        self.assets_dir = Path(assets_dir)
        self.fonts_dir = self.assets_dir / "fonts"
        self.fonts_dir.mkdir(parents=True, exist_ok=True)
        
        self.font_cache = {}
        self.available_fonts = []
        self.font_families = {}
        
        self._load_fonts()
        logger.info(f"Font Manager initialized with {len(self.available_fonts)} fonts")
    
    def _load_fonts(self):
        """Load all available fonts"""
        if not PIL_AVAILABLE:
            return
        
        # Common font locations (Termux + system)
        font_locations = [
            self.fonts_dir,
            Path("/system/fonts"),
            Path("/data/data/com.termux/files/usr/share/fonts"),
            Path("/usr/share/fonts"),
            Path("."),
        ]
        
        font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']
        
        for location in font_locations:
            if location.exists():
                # Check specific font files
                for ext in font_extensions:
                    for font_file in location.glob(f"*{ext}"):
                        try:
                            font_path = str(font_file.resolve())
                            font_name = font_file.stem
                            
                            # Test load the font
                            test_font = ImageFont.truetype(font_path, 12)
                            self.available_fonts.append(font_path)
                            
                            # Categorize by family
                            family = self._extract_font_family(font_name)
                            if family not in self.font_families:
                                self.font_families[family] = []
                            self.font_families[family].append(font_path)
                            
                            logger.debug(f"Loaded font: {font_name}")
                        except Exception as e:
                            logger.debug(f"Failed to load font {font_file}: {e}")
        
        # Add default fallback
        if not self.available_fonts:
            logger.warning("No custom fonts found, using PIL default")
    
    def _extract_font_family(self, font_name: str) -> str:
        """Extract font family from filename"""
        font_name = font_name.lower()
        
        # Remove common suffixes
        suffixes = ['-regular', '-bold', '-italic', '-light', '-medium', 
                   '-black', '-thin', 'bold', 'italic', 'regular']
        
        for suffix in suffixes:
            if font_name.endswith(suffix):
                font_name = font_name[:-len(suffix)]
        
        # Clean up
        font_name = font_name.replace('_', ' ').replace('-', ' ').strip()
        
        return font_name.title() if font_name else "Default"
    
    @lru_cache(maxsize=50)
    def get_font(self, size: int, style: str = "regular", family: str = None) -> Any:
        """Get font with caching"""
        if not PIL_AVAILABLE:
            return None
        
        cache_key = f"{size}_{style}_{family}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        try:
            font_path = None
            
            # Try to find font by family and style
            if family and family in self.font_families:
                family_fonts = self.font_families[family]
                # Try to match style
                for font in family_fonts:
                    font_lower = font.lower()
                    if style == "bold" and "bold" in font_lower:
                        font_path = font
                        break
                    elif style == "italic" and "italic" in font_lower:
                        font_path = font
                        break
                    elif style == "regular" and ("regular" in font_lower or 
                                               "bold" not in font_lower and 
                                               "italic" not in font_lower):
                        font_path = font
                        break
                
                # Fallback to first font in family
                if not font_path and family_fonts:
                    font_path = family_fonts[0]
            
            # Fallback to random available font
            if not font_path and self.available_fonts:
                font_path = random.choice(self.available_fonts)
            
            # Load font
            if font_path:
                font = ImageFont.truetype(font_path, size)
            else:
                font = ImageFont.load_default()
            
            self.font_cache[cache_key] = font
            return font
            
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            return ImageFont.load_default()
    
    def get_random_font(self, size: int) -> Any:
        """Get random font"""
        if not self.available_fonts:
            return self.get_font(size)
        
        try:
            font_path = random.choice(self.available_fonts)
            return ImageFont.truetype(font_path, size)
        except:
            return self.get_font(size)


class ColorManager:
    """Professional color management and theming"""
    
    def __init__(self):
        self.palettes = self._load_palettes()
        self.current_theme = None
    
    def _load_palettes(self) -> Dict[str, Dict]:
        """Load color palettes"""
        return {
            "midnight": {
                "background": (10, 15, 30),
                "text": (240, 240, 255),
                "accent": (0, 200, 255),
                "secondary": (100, 100, 150),
                "shadow": (20, 20, 40),
                "highlight": (255, 100, 150)
            },
            "sunset": {
                "background": (255, 200, 150),
                "text": (60, 30, 20),
                "accent": (255, 80, 80),
                "secondary": (255, 150, 50),
                "shadow": (200, 150, 100),
                "highlight": (255, 220, 100)
            },
            "forest": {
                "background": (20, 40, 30),
                "text": (220, 240, 220),
                "accent": (80, 200, 120),
                "secondary": (40, 100, 80),
                "shadow": (10, 30, 20),
                "highlight": (150, 220, 180)
            },
            "cyberpunk": {
                "background": (0, 0, 20),
                "text": (0, 255, 255),
                "accent": (255, 0, 255),
                "secondary": (255, 255, 0),
                "shadow": (0, 50, 50),
                "highlight": (255, 100, 0)
            },
            "golden": {
                "background": (30, 25, 20),
                "text": (255, 215, 0),
                "accent": (200, 160, 0),
                "secondary": (150, 120, 50),
                "shadow": (50, 40, 20),
                "highlight": (255, 240, 150)
            }
        }
    
    def get_palette(self, palette_name: str = None) -> Dict:
        """Get color palette"""
        if not palette_name:
            # Auto-select based on time
            hour = datetime.now().hour
            if 6 <= hour < 12:
                palette_name = "sunset"
            elif 12 <= hour < 18:
                palette_name = "golden"
            elif 18 <= hour < 22:
                palette_name = "cyberpunk"
            else:
                palette_name = "midnight"
        
        return self.palettes.get(palette_name, self.palettes["midnight"])
    
    def generate_gradient(self, width: int, height: int, 
                         color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int],
                         direction: str = "diagonal") -> Image.Image:
        """Generate gradient image"""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        if direction == "horizontal":
            for x in range(width):
                ratio = x / width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
        elif direction == "vertical":
            for y in range(height):
                ratio = y / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        else:  # diagonal
            for x in range(width):
                for y in range(height):
                    ratio = (x + y) / (width + height)
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    draw.point((x, y), fill=(r, g, b))
        
        return gradient
    
    def interpolate_color(self, color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         ratio: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)


class EffectManager:
    """Advanced visual effects manager"""
    
    @staticmethod
    def add_text_shadow(draw: ImageDraw, text: str, font: ImageFont,
                       position: Tuple[int, int], text_color: Tuple[int, int, int],
                       shadow_color: Tuple[int, int, int] = None,
                       offset: int = 4, blur_radius: int = 2) -> None:
        """Add professional shadow effect to text"""
        x, y = position
        
        if shadow_color is None:
            shadow_color = (text_color[0]//4, text_color[1]//4, text_color[2]//4)
        
        # Multiple shadow layers for depth
        for i in range(blur_radius, 0, -1):
            alpha = 100 // (i + 1)
            shadow_pos = (x + offset * i // blur_radius, 
                         y + offset * i // blur_radius)
            draw.text(shadow_pos, text, font=font, fill=shadow_color)
        
        # Main text
        draw.text(position, text, font=font, fill=text_color)
        
        # Subtle highlight
        highlight_color = (
            min(255, text_color[0] + 30),
            min(255, text_color[1] + 30),
            min(255, text_color[2] + 30)
        )
        draw.text((x-1, y-1), text, font=font, fill=highlight_color)
    
    @staticmethod
    def add_text_glow(image: Image.Image, glow_color: Tuple[int, int, int] = None,
                     intensity: int = 3) -> Image.Image:
        """Add glow effect around text"""
        if glow_color is None:
            glow_color = (0, 200, 255)
        
        # Create glow layer
        glow = image.copy()
        
        # Apply multiple blur passes for smooth glow
        for i in range(intensity):
            glow = glow.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Colorize glow
        color_layer = Image.new('RGBA', image.size, (*glow_color, 100))
        glow = Image.alpha_composite(glow, color_layer)
        
        # Composite with original
        result = Image.alpha_composite(glow, image)
        return result
    
    @staticmethod
    def add_vignette(image: Image.Image, intensity: float = 0.6) -> Image.Image:
        """Add vignette effect"""
        width, height = image.size
        vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vignette)
        
        center_x, center_y = width // 2, height // 2
        max_radius = int(math.sqrt(width**2 + height**2) / 2)
        
        for i in range(0, max_radius, max_radius // 20):
            radius = i
            alpha = int(255 * intensity * (1 - (i / max_radius)**2))
            
            if radius > 0:
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    fill=(0, 0, 0, alpha),
                    outline=None
                )
        
        return Image.alpha_composite(image.convert('RGBA'), vignette)
    
    @staticmethod
    def add_noise(image: Image.Image, intensity: float = 0.1) -> Image.Image:
        """Add film grain/noise effect"""
        import numpy as np
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        arr = np.array(image)
        noise = np.random.randint(0, int(255 * intensity), arr.shape[:2])
        
        # Apply noise to RGB channels
        for i in range(3):
            arr[:, :, i] = np.clip(arr[:, :, i] + noise, 0, 255)
        
        return Image.fromarray(arr)
    
    @staticmethod
    def add_light_leak(image: Image.Image, color: Tuple[int, int, int] = (255, 100, 100),
                      intensity: float = 0.3) -> Image.Image:
        """Add light leak effect"""
        width, height = image.size
        leak = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(leak)
        
        # Create light leak gradient
        for i in range(width // 2, width):
            alpha = int(255 * intensity * (1 - (i - width // 2) / (width // 2)))
            if alpha > 0:
                draw.line([(i, 0), (i, height)], 
                         fill=(*color, alpha), 
                         width=3)
        
        return Image.alpha_composite(image.convert('RGBA'), leak)
    
    @staticmethod
    def create_border(border_type: BorderType, size: Tuple[int, int],
                     color: Tuple[int, int, int] = (255, 255, 255),
                     thickness: int = 20, corner_radius: int = 40) -> Image.Image:
        """Create professional borders"""
        width, height = size
        border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        if border_type == BorderType.NONE:
            return border
        
        color_rgba = (*color, 255)
        
        if border_type == BorderType.SIMPLE:
            draw.rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                outline=color_rgba,
                width=thickness
            )
        
        elif border_type == BorderType.DOUBLE:
            # Outer border
            draw.rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                outline=color_rgba,
                width=thickness // 2
            )
            # Inner border
            inner_thickness = thickness * 2
            draw.rectangle(
                [inner_thickness, inner_thickness,
                 width - inner_thickness, height - inner_thickness],
                outline=color_rgba,
                width=thickness // 3
            )
        
        elif border_type == BorderType.ROUNDED:
            # Draw rounded rectangle
            draw.rounded_rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                radius=corner_radius,
                outline=color_rgba,
                width=thickness
            )
        
        elif border_type == BorderType.DOTTED:
            dot_spacing = 40
            dot_size = thickness // 2
            
            # Draw dots around border
            for x in range(dot_spacing, width - dot_spacing, dot_spacing):
                # Top
                draw.ellipse(
                    [x - dot_size, thickness - dot_size,
                     x + dot_size, thickness + dot_size],
                    fill=color_rgba
                )
                # Bottom
                draw.ellipse(
                    [x - dot_size, height - thickness - dot_size,
                     x + dot_size, height - thickness + dot_size],
                    fill=color_rgba
                )
            
            for y in range(dot_spacing, height - dot_spacing, dot_spacing):
                # Left
                draw.ellipse(
                    [thickness - dot_size, y - dot_size,
                     thickness + dot_size, y + dot_size],
                    fill=color_rgba
                )
                # Right
                draw.ellipse(
                    [width - thickness - dot_size, y - dot_size,
                     width - thickness + dot_size, y + dot_size],
                    fill=color_rgba
                )
        
        elif border_type == BorderType.NEON:
            # Neon glow border
            for i in range(3):
                glow_thickness = thickness + i * 5
                glow_color = (*color, 150 - i * 50)
                
                draw.rounded_rectangle(
                    [glow_thickness, glow_thickness,
                     width - glow_thickness, height - glow_thickness],
                    radius=corner_radius,
                    outline=glow_color,
                    width=3
                )
        
        return border
    
    @staticmethod
    def add_reflection(image: Image.Image, reflection_height: int = 100) -> Image.Image:
        """Add reflection effect"""
        width, height = image.size
        
        # Create reflection
        reflection = image.transpose(Image.FLIP_TOP_BOTTOM)
        reflection = reflection.crop((0, 0, width, reflection_height))
        
        # Create gradient mask
        mask = Image.new('L', (width, reflection_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        for y in range(reflection_height):
            alpha = int(255 * (1 - (y / reflection_height) ** 2))
            mask_draw.line([(0, y), (width, y)], fill=alpha)
        
        reflection.putalpha(mask)
        
        # Create new image with reflection
        result = Image.new('RGBA', (width, height + reflection_height))
        result.paste(image, (0, 0))
        result.paste(reflection, (0, height), reflection)
        
        return result


class CacheManager:
    """Professional cache management system"""
    
    def __init__(self, cache_dir: str = "./cache", ttl_hours: int = 24, max_size: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.max_size = max_size
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
        
        # Clean old cache on init
        self.cleanup()
    
    def _load_metadata(self) -> Dict:
        """Load cache metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save cache metadata"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata: {e}")
    
    def generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from parameters"""
        data = f"{args}{kwargs}".encode('utf-8')
        return hashlib.sha256(data).hexdigest()[:32]
    
    def get(self, key: str) -> Optional[bytes]:
        """Get cached item"""
        cache_file = self.cache_dir / f"{key}.png"
        
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
                return f.read()
        except Exception as e:
            logger.error(f"Error reading cache file {key}: {e}")
            return None
    
    def set(self, key: str, data: bytes):
        """Cache item"""
        if len(self.metadata) >= self.max_size:
            self._evict_oldest()
        
        cache_file = self.cache_dir / f"{key}.png"
        
        try:
            with open(cache_file, 'wb') as f:
                f.write(data)
            
            # Update metadata
            self.metadata[key] = {
                'created': datetime.now().isoformat(),
                'size': len(data),
                'hits': 0
            }
            self._save_metadata()
        except Exception as e:
            logger.error(f"Error writing cache file {key}: {e}")
    
    def delete(self, key: str):
        """Delete cached item"""
        cache_file = self.cache_dir / f"{key}.png"
        
        try:
            if cache_file.exists():
                cache_file.unlink()
            
            if key in self.metadata:
                del self.metadata[key]
                self._save_metadata()
        except Exception as e:
            logger.error(f"Error deleting cache file {key}: {e}")
    
    def _evict_oldest(self):
        """Evict oldest cache entries"""
        if not self.metadata:
            return
        
        # Find oldest entries
        sorted_entries = sorted(
            self.metadata.items(),
            key=lambda x: datetime.fromisoformat(x[1]['created'])
        )
        
        # Remove oldest 10%
        to_remove = max(1, len(sorted_entries) // 10)
        
        for key, _ in sorted_entries[:to_remove]:
            self.delete(key)
    
    def cleanup(self):
        """Clean up expired cache entries"""
        cutoff = datetime.now() - self.ttl
        
        for key, data in list(self.metadata.items()):
            created = datetime.fromisoformat(data['created'])
            if created < cutoff:
                self.delete(key)
        
        logger.info(f"Cache cleanup completed. {len(self.metadata)} items remaining.")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_size = sum(data['size'] for data in self.metadata.values())
        
        return {
            'total_items': len(self.metadata),
            'total_size_mb': total_size / (1024 * 1024),
            'max_size': self.max_size,
            'ttl_hours': self.ttl.total_seconds() / 3600
        }


class UltimateImageGenerator:
    """
    ULTIMATE IMAGE GENERATOR
    Professional-grade image generation system
    """
    
    def __init__(self, config: Optional[ImageConfig] = None):
        if not PIL_AVAILABLE:
            logger.error("PIL/Pillow not available. Image generation disabled.")
            raise ImportError("Install PIL/Pillow: pip install pillow")
        
        self.config = config or ImageConfig()
        self.font_manager = FontManager(self.config.assets_dir)
        self.color_manager = ColorManager()
        self.effect_manager = EffectManager()
        self.cache_manager = CacheManager(
            cache_dir=self.config.cache_dir,
            ttl_hours=self.config.cache_ttl_hours,
            max_size=self.config.max_cache_size
        )
        
        # Statistics
        self.stats = {
            'total_generated': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'total_time': 0.0
        }
        
        logger.info("✓ Ultimate Image Generator initialized")
    
    def _safe_text_extract(self, text_input: Any) -> str:
        """
        Safely extract text from various input types
        Handles: str, dict, list, etc.
        """
        if isinstance(text_input, str):
            return text_input
        
        elif isinstance(text_input, dict):
            # Common keys that might contain text
            text_keys = ['text', 'message', 'roast', 'content', 
                        'caption', 'title', 'description', 'quote']
            
            for key in text_keys:
                if key in text_input and isinstance(text_input[key], str):
                    return text_input[key]
            
            # Try to find any string value
            for key, value in text_input.items():
                if isinstance(value, str) and len(value) > 10:
                    return value
            
            # Convert dict to string
            return json.dumps(text_input, ensure_ascii=False)
        
        elif isinstance(text_input, (list, tuple)):
            # Join list items
            return ' '.join(str(item) for item in text_input)
        
        else:
            # Convert to string
            return str(text_input)
    
    def _wrap_text_smart(self, text: str, max_width: int = 30) -> List[str]:
        """
        Smart text wrapping with Unicode support
        """
        # Clean text
        text = text.strip()
        
        # If text is very short, return as is
        if len(text) <= max_width:
            return [text]
        
        try:
            # Try standard textwrap first
            return textwrap.wrap(text, width=max_width)
        except (UnicodeEncodeError, AttributeError):
            # Fallback to manual wrapping for Unicode text
            words = text.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word)
                
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
        """Create professional background"""
        palette = self.color_manager.get_palette()
        
        if bg_config.type == "gradient":
            color1 = bg_config.primary_color or palette['background']
            color2 = bg_config.secondary_color or palette['secondary']
            
            background = self.color_manager.generate_gradient(
                width, height, color1, color2, "diagonal"
            )
        
        elif bg_config.type == "solid":
            background = Image.new('RGB', (width, height), 
                                 bg_config.primary_color or palette['background'])
        
        else:  # pattern or image
            background = Image.new('RGB', (width, height), palette['background'])
        
        # Apply pattern if specified
        if bg_config.pattern_type != "none":
            background = self._apply_pattern(background, bg_config)
        
        # Apply blur if specified
        if bg_config.blur_radius > 0:
            background = background.filter(
                ImageFilter.GaussianBlur(bg_config.blur_radius)
            )
        
        return background
    
    def _apply_pattern(self, image: Image.Image, bg_config: BackgroundConfig) -> Image.Image:
        """Apply pattern to background"""
        width, height = image.size
        pattern = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pattern)
        
        pattern_color = bg_config.pattern_color or (255, 255, 255)
        intensity = int(255 * bg_config.pattern_intensity)
        
        if bg_config.pattern_type == "grid":
            spacing = 50
            for x in range(0, width, spacing):
                draw.line([(x, 0), (x, height)], 
                         fill=(*pattern_color, intensity//2), 
                         width=1)
            for y in range(0, height, spacing):
                draw.line([(0, y), (width, y)], 
                         fill=(*pattern_color, intensity//2), 
                         width=1)
        
        elif bg_config.pattern_type == "dots":
            spacing = 40
            for x in range(spacing, width - spacing, spacing):
                for y in range(spacing, height - spacing, spacing):
                    draw.ellipse([x-2, y-2, x+2, y+2], 
                               fill=(*pattern_color, intensity))
        
        elif bg_config.pattern_type == "noise":
            for _ in range(width * height // 100):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                draw.point((x, y), fill=(*pattern_color, random.randint(0, intensity)))
        
        return Image.alpha_composite(image.convert('RGBA'), pattern)
    
    def _render_text(self, draw: ImageDraw, text_config: TextConfig, 
                    width: int, height: int) -> Tuple[int, int]:
        """Render text with effects"""
        palette = self.color_manager.get_palette()
        
        # Get fonts
        primary_font = self.font_manager.get_font(
            text_config.font_size_primary, 
            text_config.font_style
        )
        secondary_font = self.font_manager.get_font(
            text_config.font_size_secondary,
            "regular"
        )
        
        # Wrap primary text
        primary_lines = self._wrap_text_smart(
            text_config.primary_text, 
            text_config.max_width
        )
        
        # Calculate total height
        line_height_primary = int(text_config.font_size_primary * text_config.line_spacing)
        line_height_secondary = int(text_config.font_size_secondary * text_config.line_spacing)
        
        total_height = (
            len(primary_lines) * line_height_primary +
            (len(primary_lines) - 1) * 10  # spacing between lines
        )
        
        if text_config.secondary_text:
            secondary_lines = self._wrap_text_smart(
                text_config.secondary_text,
                text_config.max_width
            )
            total_height += len(secondary_lines) * line_height_secondary + 40
        
        if text_config.emoji:
            total_height += text_config.font_size_emoji + 20
        
        # Start Y position (centered)
        current_y = (height - total_height) // 3
        
        # Draw primary text
        text_color = text_config.text_color or palette['text']
        shadow_color = text_config.shadow_color or palette['shadow']
        
        for line in primary_lines:
            # Get text bbox
            bbox = draw.textbbox((0, 0), line, font=primary_font)
            text_width = bbox[2] - bbox[0]
            
            # Center horizontally
            x_position = (width - text_width) // 2
            
            # Apply effects
            if TextEffect.SHADOW in text_config.effects:
                self.effect_manager.add_text_shadow(
                    draw, line, primary_font,
                    (x_position, current_y),
                    text_color, shadow_color
                )
            else:
                draw.text((x_position, current_y), line, 
                         font=primary_font, fill=text_color)
            
            current_y += line_height_primary
        
        # Draw secondary text if exists
        if text_config.secondary_text:
            current_y += 30
            
            secondary_lines = self._wrap_text_smart(
                text_config.secondary_text,
                text_config.max_width
            )
            
            for line in secondary_lines:
                bbox = draw.textbbox((0, 0), line, font=secondary_font)
                text_width = bbox[2] - bbox[0]
                x_position = (width - text_width) // 2
                
                draw.text((x_position, current_y), line,
                         font=secondary_font, fill=palette['secondary'])
                
                current_y += line_height_secondary
        
        # Draw emoji if exists
        if text_config.emoji:
            current_y += 40
            emoji_font = self.font_manager.get_font(text_config.font_size_emoji)
            
            bbox = draw.textbbox((0, 0), text_config.emoji, font=emoji_font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) // 2
            
            draw.text((x_position, current_y), text_config.emoji,
                     font=emoji_font, fill=text_color)
            
            current_y += text_config.font_size_emoji
        
        return current_y
    
    def _add_metadata(self, draw: ImageDraw, user_info: Dict, 
                     width: int, current_y: int):
        """Add metadata to image"""
        palette = self.color_manager.get_palette()
        small_font = self.font_manager.get_font(24, "regular")
        
        # User info
        username = user_info.get('username', 'User')
        user_text = f"@{username}"
        
        if 'first_name' in user_info:
            user_text = f"{user_info['first_name']} ({user_text})"
        
        if 'rating' in user_info:
            user_text += f" ⭐ {user_info['rating']}/10"
        
        bbox = draw.textbbox((0, 0), user_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, current_y + 30),
                 user_text, font=small_font, fill=palette['accent'])
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d • %H:%M:%S")
        bbox = draw.textbbox((0, 0), timestamp, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, current_y + 70),
                 timestamp, font=small_font, fill=palette['secondary'])
        
        # Bot signature
        signature = "🔥 Roastify Pro • roastify-bot.com"
        bbox = draw.textbbox((0, 0), signature, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, current_y + 110),
                 signature, font=small_font, fill=palette['highlight'])
    
    def generate_roast_image(self, roast_text: Any, user_info: Dict,
                            style: str = "auto", border_config: BorderConfig = None,
                            background_config: BackgroundConfig = None) -> str:
        """
        Generate professional roast image
        
        Args:
            roast_text: Text to display (string or dict with text)
            user_info: User information dict
            style: Color palette style
            border_config: Border configuration
            background_config: Background configuration
            
        Returns:
            Path to generated image
        """
        start_time = datetime.now()
        
        try:
            # 1. Extract and validate text
            actual_text = self._safe_text_extract(roast_text)
            
            if not actual_text or len(actual_text.strip()) < 3:
                logger.warning("Text too short, using default")
                actual_text = "আপনি খুবই স্মার্ট! 😄"
            
            # 2. Create text config
            text_config = TextConfig(
                primary_text=actual_text,
                secondary_text=user_info.get('subtext', ''),
                emoji=random.choice(['🔥', '😈', '⚡', '💥', '🎯']),
                text_color=(255, 255, 255),
                effects=[TextEffect.SHADOW, TextEffect.GLOW],
                max_width=28
            )
            
            # 3. Generate cache key
            cache_key = self.cache_manager.generate_key(
                actual_text[:100], style, 
                border_config.border_type.value if border_config else "default"
            )
            
            # 4. Check cache
            if self.config.enable_cache:
                cached_data = self.cache_manager.get(cache_key)
                if cached_data:
                    self.stats['cache_hits'] += 1
                    output_path = Path(self.config.output_dir) / f"roast_{cache_key[:8]}.png"
                    output_path.write_bytes(cached_data)
                    logger.info(f"Cache hit: {cache_key[:8]}")
                    return str(output_path)
            
            self.stats['cache_misses'] += 1
            
            # 5. Setup configurations
            border_config = border_config or BorderConfig(
                border_type=random.choice([BorderType.ROUNDED, BorderType.NEON, BorderType.DOUBLE]),
                color=self.color_manager.get_palette(style)['accent'],
                thickness=random.randint(15, 25)
            )
            
            bg_config = background_config or BackgroundConfig(
                type=random.choice(["gradient", "solid", "pattern"]),
                primary_color=self.color_manager.get_palette(style)['background']
            )
            
            # 6. Create image
            width, height = self.config.width, self.config.height
            
            # Background
            background = self._create_background(bg_config, width, height)
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # Text
            text_bottom = self._render_text(draw, text_config, width, height)
            
            # Metadata
            self._add_metadata(draw, user_info, width, text_bottom)
            
            # Effects
            if random.random() > 0.5:
                image = self.effect_manager.add_vignette(image, intensity=0.3)
            
            if random.random() > 0.7:
                image = self.effect_manager.add_light_leak(image)
            
            # Border
            if border_config.enabled and border_config.border_type != BorderType.NONE:
                border = self.effect_manager.create_border(
                    border_config.border_type,
                    (width, height),
                    border_config.color,
                    border_config.thickness,
                    border_config.corner_radius
                )
                image = Image.alpha_composite(image, border)
            
            # Final glow effect
            if TextEffect.GLOW in text_config.effects:
                image = self.effect_manager.add_text_glow(image)
            
            # 7. Save image
            output_path = Path(self.config.output_dir) / f"roast_{int(datetime.now().timestamp())}.png"
            
            # Convert to RGB for better compatibility
            if image.mode == 'RGBA':
                rgb_background = Image.new('RGB', image.size, 
                                         self.color_manager.get_palette(style)['background'])
                rgb_background.paste(image, mask=image.split()[3])
                image = rgb_background
            
            # Save with high quality
            image.save(output_path, self.config.format, 
                      quality=self.config.quality,
                      optimize=True)
            
            # 8. Cache the image
            if self.config.enable_cache:
                with open(output_path, 'rb') as f:
                    image_data = f.read()
                self.cache_manager.set(cache_key, image_data)
            
            # 9. Update statistics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.stats['total_generated'] += 1
            self.stats['total_time'] += duration
            
            logger.info(f"✓ Image generated: {output_path} ({duration:.2f}s)")
            
            return str(output_path)
            
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"✗ Error generating image: {e}", exc_info=True)
            
            # Create error image
            return self._create_error_image(f"Error: {str(e)[:50]}")
    
    def generate_welcome_image(self, user_info: Dict, chat_info: Dict = None) -> str:
        """Generate welcome image for new users"""
        try:
            # Create festive text
            welcome_texts = [
                "স্বাগতম! রোস্টের জগতে আপনাকে হৃদয়ের অভিনন্দন! 🎉",
                "আসসালামু আলাইকুম! রোস্টিফাই পরিবারে আপনাকে স্বাগতম! 👋",
                "হ্যালো! প্রস্তুত থাকুন মজাদার রোস্টের জন্য! 😄",
                "ওহো! একজন নতুন রোস্টার এসেছেন! 🔥",
                "Welcome to Roastify! Get ready for some fun! 🎊"
            ]
            
            text_config = TextConfig(
                primary_text=random.choice(welcome_texts),
                secondary_text=f"@{user_info.get('username', 'User')}",
                emoji="🎉",
                font_size_primary=64,
                font_size_secondary=48,
                text_color=(255, 255, 255),
                effects=[TextEffect.SHADOW, TextEffect.GLOW]
            )
            
            # Special welcome background
            bg_config = BackgroundConfig(
                type="gradient",
                primary_color=(30, 10, 50),  # Purple
                secondary_color=(70, 30, 90)
            )
            
            # Special border for welcome
            border_config = BorderConfig(
                border_type=BorderType.NEON,
                color=(255, 215, 0),  # Gold
                thickness=25,
                glow_intensity=2
            )
            
            return self.generate_roast_image(
                roast_text=text_config.primary_text,
                user_info=user_info,
                style="cyberpunk",
                border_config=border_config,
                background_config=bg_config
            )
            
        except Exception as e:
            logger.error(f"Error generating welcome image: {e}")
            return self._create_error_image("Welcome")
    
    def generate_achievement_image(self, user_info: Dict, achievement: Dict) -> str:
        """Generate achievement/unlock image"""
        try:
            text_config = TextConfig(
                primary_text=achievement.get('title', 'ACHIEVEMENT UNLOCKED!'),
                secondary_text=achievement.get('description', ''),
                emoji=achievement.get('emoji', '🏆'),
                font_size_primary=60,
                font_size_secondary=36,
                text_color=(255, 215, 0),  # Gold
                effects=[TextEffect.SHADOW, TextEffect.GLOW, TextEffect.REFLECTION]
            )
            
            bg_config = BackgroundConfig(
                type="gradient",
                primary_color=(40, 20, 60),  # Dark purple
                secondary_color=(80, 40, 100)
            )
            
            border_config = BorderConfig(
                border_type=BorderType.ORNATE,
                color=(255, 215, 0),  # Gold
                thickness=30,
                corner_radius=60
            )
            
            return self.generate_roast_image(
                roast_text=text_config.primary_text,
                user_info=user_info,
                style="golden",
                border_config=border_config,
                background_config=bg_config
            )
            
        except Exception as e:
            logger.error(f"Error generating achievement image: {e}")
            return self._create_error_image("Achievement")
    
    def _create_error_image(self, error_type: str = "Error") -> str:
        """Create error image when generation fails"""
        try:
            width, height = 800, 400
            image = Image.new('RGB', (width, height), (40, 40, 60))
            draw = ImageDraw.Draw(image)
            
            font = self.font_manager.get_font(48, "bold")
            small_font = self.font_manager.get_font(24, "regular")
            
            # Error title
            error_text = f"{error_type} Occurred"
            bbox = draw.textbbox((0, 0), error_text, font=font)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) // 2, 100),
                     error_text, font=font, fill=(255, 100, 100))
            
            # Message
            message = "Please try again or contact support"
            bbox = draw.textbbox((0, 0), message, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) // 2, 200),
                     message, font=small_font, fill=(200, 200, 255))
            
            # Save
            error_path = Path(self.config.temp_dir) / f"error_{int(datetime.now().timestamp())}.png"
            image.save(error_path, 'PNG')
            
            return str(error_path)
            
        except Exception as e:
            # Last resort
            error_file = Path(self.config.temp_dir) / "error_fallback.txt"
            error_file.write_text(f"Image generation failed: {error_type}")
            return str(error_file)
    
    def get_stats(self) -> Dict:
        """Get generator statistics"""
        avg_time = 0
        if self.stats['total_generated'] > 0:
            avg_time = self.stats['total_time'] / self.stats['total_generated']
        
        cache_stats = self.cache_manager.get_stats()
        
        return {
            'performance': {
                'total_generated': self.stats['total_generated'],
                'cache_hits': self.stats['cache_hits'],
                'cache_misses': self.stats['cache_misses'],
                'cache_hit_rate': (
                    self.stats['cache_hits'] / max(self.stats['cache_hits'] + self.stats['cache_misses'], 1) * 100
                ),
                'errors': self.stats['errors'],
                'average_time_seconds': round(avg_time, 2)
            },
            'cache': cache_stats,
            'fonts': {
                'available': len(self.font_manager.available_fonts),
                'families': len(self.font_manager.font_families)
            },
            'system': {
                'pil_available': PIL_AVAILABLE,
                'config': {
                    'width': self.config.width,
                    'height': self.config.height,
                    'quality': self.config.quality
                }
            }
        }
    
    def cleanup(self, max_age_hours: int = 24):
        """Clean up old files"""
        try:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            
            for dir_path in [self.config.temp_dir, self.config.output_dir]:
                dir_obj = Path(dir_path)
                if dir_obj.exists():
                    for file in dir_obj.glob("*"):
                        if file.is_file():
                            mtime = datetime.fromtimestamp(file.stat().st_mtime)
                            if mtime < cutoff:
                                file.unlink()
                                logger.debug(f"Cleaned up: {file}")
            
            # Clean cache
            self.cache_manager.cleanup()
            
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Backward compatibility alias
ImageGenerator = UltimateImageGenerator


def test_generator():
    """Test the image generator"""
    print("\n" + "="*60)
    print("ULTIMATE IMAGE GENERATOR - TEST SUITE")
    print("="*60)
    
    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow not installed!")
        print("   Install with: pip install pillow")
        return False
    
    try:
        # Initialize generator
        print("🚀 Initializing generator...")
        generator = UltimateImageGenerator()
        
        # Test data
        test_user = {
            'username': 'test_user',
            'first_name': 'Test User',
            'rating': 8.5,
            'subtext': 'This is a test roast!'
        }
        
        # Test 1: Roast image
        print("\n🔹 Test 1: Generating roast image...")
        roast_text = "এটা একটা টেস্ট রোস্ট! দেখি ইমেজ জেনারেট করতে পারে কিনা।"
        roast_path = generator.generate_roast_image(roast_text, test_user)
        print(f"   ✓ Roast image: {roast_path}")
        
        # Test 2: Welcome image
        print("\n🔹 Test 2: Generating welcome image...")
        welcome_path = generator.generate_welcome_image(test_user)
        print(f"   ✓ Welcome image: {welcome_path}")
        
        # Test 3: Achievement image
        print("\n🔹 Test 3: Generating achievement image...")
        achievement = {
            'title': 'Expert Roaster',
            'description': 'Completed 100+ roasts',
            'emoji': '🏆'
        }
        achievement_path = generator.generate_achievement_image(test_user, achievement)
        print(f"   ✓ Achievement image: {achievement_path}")
        
        # Show statistics
        print("\n📊 GENERATOR STATISTICS:")
        print("-"*40)
        
        stats = generator.get_stats()
        for category, data in stats.items():
            print(f"\n{category.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {data}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run test suite
    success = test_generator()
    sys.exit(0 if success else 1)
