#!/usr/bin/env python3
"""
Advanced 3D Image Generator for Roastify Bot
Professional-grade image generation with caching, async operations, and advanced effects
"""

import os
import sys
import random
import asyncio
import logging
import hashlib
import functools
from typing import Dict, List, Any, Optional, Tuple, Union, BinaryIO
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import json
import pickle
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from PIL.Image import Resampling
import textwrap
from cachetools import TTLCache, cached
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
import aiofiles

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
console = Console()

# Import config with fallbacks
try:
    from config import IMAGE_GENERATION, BORDERS, FONTS, PATHS, TIME_BASED_BEHAVIOR
except ImportError:
    logger.error("Config module not found. Using defaults.")
    
    # Default configuration
    IMAGE_GENERATION = {
        "image_resolution": (1080, 1080),
        "visual_elements": {
            "glow_effect": True,
            "cinematic_lighting": True,
            "background_blur": False,
            "reflection_effect": True
        },
        "quality": 95,
        "format": "PNG",
        "max_file_size_mb": 5
    }
    
    BORDERS = {
        "border_files": ["*.png", "*.jpg"],
        "no_repeat_until": 5,
        "auto_generate": True,
        "styles": ["neon", "vintage", "modern", "cyberpunk"]
    }
    
    FONTS = {
        "font_files": ["*.ttf", "*.otf"],
        "no_repeat_until": 3,
        "fallback_fonts": [
            "arial.ttf",
            "roboto.ttf",
            "montserrat.ttf"
        ],
        "font_styles": ["regular", "bold", "italic", "bold_italic"]
    }
    
    PATHS = {
        "fonts": "./assets/fonts",
        "borders": "./assets/borders",
        "temp": "./temp",
        "templates": "./templates",
        "cache": "./cache",
        "output": "./output"
    }
    
    TIME_BASED_BEHAVIOR = {
        "day_mode": {
            "time_range": [6, 18],
            "theme": "light",
            "brightness": 1.0
        },
        "night_mode": {
            "time_range": [18, 6],
            "theme": "dark",
            "brightness": 0.8
        }
    }


class ImageStyle(Enum):
    """Enum for image styles"""
    CARTOON = "cartoon"
    NEON = "neon"
    VINTAGE = "vintage"
    CYBERPUNK = "cyberpunk"
    MINIMAL = "minimal"
    GRUNGE = "grunge"


class TextEffect(Enum):
    """Enum for text effects"""
    GLOW = "glow"
    SHADOW_3D = "shadow_3d"
    GRADIENT = "gradient"
    OUTLINE = "outline"
    EMBOSS = "emboss"
    NEON = "neon"


@dataclass
class GenerationConfig:
    """Configuration for image generation"""
    width: int = 1080
    height: int = 1080
    style: ImageStyle = ImageStyle.NEON
    quality: int = 95
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    use_async: bool = True
    max_workers: int = 4


@dataclass
class TextConfig:
    """Configuration for text rendering"""
    primary_text: str
    secondary_text: str = ""
    emoji: str = ""
    font_size_primary: int = 60
    font_size_secondary: int = 40
    font_size_emoji: int = 80
    text_color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (0, 0, 0)
    effects: List[TextEffect] = field(default_factory=lambda: [TextEffect.GLOW])
    alignment: str = "center"
    line_spacing: int = 1
    max_width: int = 30


@dataclass
class BorderConfig:
    """Configuration for borders"""
    enabled: bool = True
    style: str = "random"
    color: Optional[Tuple[int, int, int]] = None
    thickness: int = 20
    padding: int = 50
    corner_radius: int = 20


@dataclass
class BackgroundConfig:
    """Configuration for backgrounds"""
    type: str = "gradient"  # solid, gradient, image, pattern
    primary_color: Tuple[int, int, int] = (0, 0, 0)
    secondary_color: Optional[Tuple[int, int, int]] = None
    image_path: Optional[str] = None
    opacity: float = 1.0
    blur_radius: int = 0
    pattern: str = "none"  # grid, dots, lines, noise


class AsyncImageProcessor:
    """Handle async image operations"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()
    
    async def process_image_async(self, func, *args, **kwargs):
        """Run image processing in thread pool"""
        return await self.loop.run_in_executor(
            self.executor,
            functools.partial(func, *args, **kwargs)
        )
    
    @asynccontextmanager
    async def async_open_image(self, path: str):
        """Async context manager for opening images"""
        async with aiofiles.open(path, 'rb') as f:
            content = await f.read()
        image = Image.open(io.BytesIO(content))
        try:
            yield image
        finally:
            image.close()
    
    def close(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=False)


class CacheManager:
    """Manage caching for generated images"""
    
    def __init__(self, cache_dir: str = "./cache", max_size: int = 100, ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache = TTLCache(maxsize=max_size, ttl=ttl)
        self.metadata_file = self.cache_dir / "metadata.pkl"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load cache metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
            except:
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save cache metadata"""
        try:
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            logger.error(f"Error saving cache metadata: {e}")
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        data = f"{args}{kwargs}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[bytes]:
        """Get cached image"""
        # Check memory cache first
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{key}.png"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    data = f.read()
                self.memory_cache[key] = data
                return data
            except Exception as e:
                logger.error(f"Error reading cache file: {e}")
        
        return None
    
    def set(self, key: str, data: bytes):
        """Cache image data"""
        # Store in memory cache
        self.memory_cache[key] = data
        
        # Store in disk cache
        cache_file = self.cache_dir / f"{key}.png"
        try:
            with open(cache_file, 'wb') as f:
                f.write(data)
            
            # Update metadata
            self.metadata[key] = {
                'timestamp': datetime.now().isoformat(),
                'size': len(data)
            }
            self._save_metadata()
        except Exception as e:
            logger.error(f"Error writing cache file: {e}")
    
    def clear_old_cache(self, max_age_hours: int = 24):
        """Clear old cache entries"""
        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)
        
        for cache_file in self.cache_dir.glob("*.png"):
            if cache_file.stat().st_mtime < cutoff:
                try:
                    cache_file.unlink()
                    key = cache_file.stem
                    if key in self.metadata:
                        del self.metadata[key]
                except Exception as e:
                    logger.error(f"Error deleting cache file {cache_file}: {e}")
        
        self._save_metadata()


class AdvancedImageGenerator:
    """Advanced 3D image generator with professional features"""
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        """Initialize advanced image generator"""
        self.config = config or GenerationConfig()
        self.async_processor = AsyncImageProcessor(
            max_workers=self.config.max_workers
        )
        self.cache_manager = CacheManager(
            cache_dir=PATHS["cache"],
            ttl=self.config.cache_ttl
        )
        
        # Initialize components
        self.font_manager = FontManager()
        self.border_manager = BorderManager()
        self.effect_manager = EffectManager()
        self.template_manager = TemplateManager()
        
        # Performance tracking
        self.performance_stats = {
            'total_generated': 0,
            'avg_generation_time': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Load assets asynchronously
        self._load_assets_async()
        
        logger.info(f"Advanced Image Generator initialized with config: {self.config}")
    
    async def _load_assets_async(self):
        """Load assets asynchronously"""
        tasks = [
            self.font_manager.load_fonts_async(),
            self.border_manager.load_borders_async(),
            self.template_manager.load_templates_async()
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading assets...", total=len(tasks))
            
            for coro in asyncio.as_completed(tasks):
                await coro
                progress.advance(task)
    
    def _create_performance_decorator(self, func):
        """Decorator to track performance"""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            
            duration = (end_time - start_time).total_seconds()
            self.performance_stats['total_generated'] += 1
            self.performance_stats['avg_generation_time'] = (
                (self.performance_stats['avg_generation_time'] * 
                 (self.performance_stats['total_generated'] - 1) + duration) /
                self.performance_stats['total_generated']
            )
            
            logger.debug(f"{func.__name__} executed in {duration:.2f}s")
            return result
        
        return wrapper
    
    @cached(cache=TTLCache(maxsize=100, ttl=300))
    def _get_theme_config(self, hour: Optional[int] = None) -> Dict:
        """Get theme configuration based on time (cached)"""
        if hour is None:
            hour = datetime.now().hour
        
        if TIME_BASED_BEHAVIOR["day_mode"]["time_range"][0] <= hour <= \
           TIME_BASED_BEHAVIOR["day_mode"]["time_range"][1]:
            theme = "day"
        else:
            theme = "night"
        
        themes = {
            "day": {
                "mode": "day",
                "brightness": 1.0,
                "contrast": 1.0,
                "saturation": 1.1,
                "colors": {
                    "primary": (255, 255, 255),
                    "secondary": (245, 245, 245),
                    "text": (30, 30, 30),
                    "accent": (70, 130, 180),
                    "shadow": (200, 200, 200)
                }
            },
            "night": {
                "mode": "night",
                "brightness": 0.8,
                "contrast": 1.2,
                "saturation": 0.9,
                "colors": {
                    "primary": (20, 20, 40),
                    "secondary": (40, 40, 60),
                    "text": (220, 220, 255),
                    "accent": (255, 105, 180),
                    "shadow": (50, 50, 80)
                }
            }
        }
        
        return themes.get(theme, themes["day"])
    
    async def _create_advanced_text_effect(
        self,
        draw: ImageDraw,
        text: str,
        font: ImageFont,
        position: Tuple[int, int],
        config: TextConfig
    ) -> Image.Image:
        """Create advanced text effects with multiple techniques"""
        x, y = position
        
        # Create a temporary image for text effects
        temp_image = Image.new('RGBA', (font.size * len(text), font.size * 2), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_image)
        
        # Draw base text
        temp_draw.text((0, 0), text, font=font, fill=config.text_color)
        
        # Apply effects
        for effect in config.effects:
            if effect == TextEffect.GLOW:
                temp_image = await self.effect_manager.apply_glow_effect(
                    temp_image, intensity=3
                )
            elif effect == TextEffect.SHADOW_3D:
                temp_image = await self.effect_manager.apply_3d_shadow(
                    temp_image, depth=5
                )
            elif effect == TextEffect.GRADIENT:
                temp_image = await self.effect_manager.apply_gradient_text(
                    temp_image,
                    start_color=config.text_color,
                    end_color=config.shadow_color
                )
            elif effect == TextEffect.OUTLINE:
                temp_image = await self.effect_manager.apply_outline(
                    temp_image,
                    outline_color=config.shadow_color,
                    thickness=2
                )
            elif effect == TextEffect.EMBOSS:
                temp_image = await self.effect_manager.apply_emboss_effect(temp_image)
            elif effect == TextEffect.NEON:
                temp_image = await self.effect_manager.apply_neon_effect(
                    temp_image,
                    glow_color=config.text_color
                )
        
        # Composite back to main image
        bbox = temp_image.getbbox()
        if bbox:
            temp_image = temp_image.crop(bbox)
            draw.bitmap(position, temp_image, fill=None)
        
        return temp_image
    
    async def _generate_background(
        self,
        width: int,
        height: int,
        config: BackgroundConfig
    ) -> Image.Image:
        """Generate advanced background"""
        if config.type == "gradient":
            background = await self.effect_manager.create_gradient(
                width, height,
                config.primary_color,
                config.secondary_color or config.primary_color,
                direction="diagonal"
            )
        elif config.type == "image" and config.image_path:
            async with self.async_processor.async_open_image(config.image_path) as img:
                background = img.resize((width, height), Resampling.LANCZOS)
                if config.opacity < 1.0:
                    background = await self.effect_manager.adjust_opacity(
                        background, config.opacity
                    )
        else:
            background = Image.new('RGB', (width, height), config.primary_color)
        
        # Apply patterns
        if config.pattern != "none":
            pattern = await self.effect_manager.create_pattern(
                width, height,
                pattern_type=config.pattern,
                color=config.secondary_color or config.primary_color
            )
            background = Image.alpha_composite(
                background.convert('RGBA'),
                pattern
            )
        
        # Apply blur if specified
        if config.blur_radius > 0:
            background = await self.async_processor.process_image_async(
                background.filter,
                ImageFilter.GaussianBlur(config.blur_radius)
            )
        
        return background
    
    @_create_performance_decorator
    async def generate_image(
        self,
        text_config: TextConfig,
        border_config: Optional[BorderConfig] = None,
        background_config: Optional[BackgroundConfig] = None,
        metadata: Optional[Dict] = None
    ) -> Union[bytes, str]:
        """
        Generate image with advanced features
        
        Args:
            text_config: Text configuration
            border_config: Border configuration
            background_config: Background configuration
            metadata: Additional metadata
            
        Returns:
            Image bytes or file path
        """
        # Generate cache key
        cache_key = self.cache_manager._generate_key(
            text_config, border_config, background_config, metadata
        )
        
        # Check cache
        if self.config.enable_cache:
            cached_data = self.cache_manager.get(cache_key)
            if cached_data:
                self.performance_stats['cache_hits'] += 1
                logger.debug("Cache hit for image generation")
                return cached_data
        
        self.performance_stats['cache_misses'] += 1
        
        try:
            # Get current theme
            theme = self._get_theme_config()
            
            # Create background
            bg_config = background_config or BackgroundConfig(
                type="gradient",
                primary_color=theme["colors"]["primary"],
                secondary_color=theme["colors"]["secondary"]
            )
            
            background = await self._generate_background(
                self.config.width, self.config.height, bg_config
            )
            
            # Create main image
            image = background.copy()
            draw = ImageDraw.Draw(image)
            
            # Get fonts
            primary_font = await self.font_manager.get_font(
                size=text_config.font_size_primary,
                style="bold"
            )
            secondary_font = await self.font_manager.get_font(
                size=text_config.font_size_secondary
            )
            emoji_font = await self.font_manager.get_font(
                size=text_config.font_size_emoji
            )
            
            # Wrap text
            wrapper = textwrap.TextWrapper(width=text_config.max_width)
            primary_lines = wrapper.wrap(text_config.primary_text)
            secondary_lines = wrapper.wrap(text_config.secondary_text) if text_config.secondary_text else []
            
            # Calculate positions
            total_height = (
                len(primary_lines) * text_config.font_size_primary +
                len(secondary_lines) * text_config.font_size_secondary +
                text_config.font_size_emoji +
                (len(primary_lines) + len(secondary_lines)) * text_config.line_spacing * 10
            )
            
            current_y = (self.config.height - total_height) // 2
            
            # Draw primary text with effects
            for line in primary_lines:
                bbox = draw.textbbox((0, 0), line, font=primary_font)
                text_width = bbox[2] - bbox[0]
                x_position = (self.config.width - text_width) // 2
                
                await self._create_advanced_text_effect(
                    draw, line, primary_font,
                    (x_position, current_y), text_config
                )
                
                current_y += text_config.font_size_primary + text_config.line_spacing * 10
            
            # Draw secondary text
            if secondary_lines:
                current_y += 20
                for line in secondary_lines:
                    bbox = draw.textbbox((0, 0), line, font=secondary_font)
                    text_width = bbox[2] - bbox[0]
                    x_position = (self.config.width - text_width) // 2
                    
                    draw.text(
                        (x_position, current_y),
                        line,
                        font=secondary_font,
                        fill=text_config.text_color
                    )
                    
                    current_y += text_config.font_size_secondary + text_config.line_spacing * 5
            
            # Draw emoji
            if text_config.emoji:
                bbox = draw.textbbox((0, 0), text_config.emoji, font=emoji_font)
                text_width = bbox[2] - bbox[0]
                x_position = (self.config.width - text_width) // 2
                
                draw.text(
                    (x_position, current_y + 20),
                    text_config.emoji,
                    font=emoji_font,
                    fill=text_config.text_color
                )
            
            # Apply post-processing effects
            image = await self.effect_manager.apply_cinematic_lighting(
                image, theme["mode"]
            )
            
            if IMAGE_GENERATION["visual_elements"]["reflection_effect"]:
                image = await self.effect_manager.apply_reflection_effect(image)
            
            # Add border
            if border_config and border_config.enabled:
                border = await self.border_manager.get_border(
                    style=border_config.style,
                    color=border_config.color or theme["colors"]["accent"],
                    size=(self.config.width, self.config.height)
                )
                if border:
                    image = Image.alpha_composite(image.convert('RGBA'), border)
            
            # Add metadata watermark if provided
            if metadata:
                image = await self._add_metadata_watermark(image, metadata)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(
                img_byte_arr,
                format=self.config.format,
                quality=self.config.quality,
                optimize=True
            )
            
            result = img_byte_arr.getvalue()
            
            # Cache the result
            if self.config.enable_cache:
                self.cache_manager.set(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            raise ImageGenerationError(f"Failed to generate image: {str(e)}")
    
    async def generate_image_batch(
        self,
        text_configs: List[TextConfig],
        output_dir: Optional[str] = None,
        concurrent: bool = True
    ) -> List[str]:
        """Generate multiple images in batch"""
        output_dir = output_dir or PATHS["output"]
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        file_paths = []
        
        if concurrent:
            # Generate images concurrently
            tasks = [
                self.generate_image(text_config)
                for text_config in text_configs
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error generating image {i}: {result}")
                    continue
                
                filename = f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = Path(output_dir) / filename
                
                with open(filepath, 'wb') as f:
                    f.write(result)
                
                file_paths.append(str(filepath))
        else:
            # Generate images sequentially
            for i, text_config in enumerate(text_configs):
                try:
                    result = await self.generate_image(text_config)
                    
                    filename = f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = Path(output_dir) / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(result)
                    
                    file_paths.append(str(filepath))
                except Exception as e:
                    logger.error(f"Error generating image {i}: {e}")
        
        return file_paths
    
    async def _add_metadata_watermark(self, image: Image.Image, metadata: Dict) -> Image.Image:
        """Add metadata as watermark"""
        draw = ImageDraw.Draw(image.convert('RGBA'))
        
        # Create watermark text
        watermark_text = []
        for key, value in metadata.items():
            if key not in ['user_id', 'timestamp']:
                watermark_text.append(f"{key}: {value}")
        
        if watermark_text:
            watermark = "\n".join(watermark_text)
            font = await self.font_manager.get_font(size=12)
            
            # Add semi-transparent background for watermark
            watermark_bg = Image.new('RGBA', image.size, (0, 0, 0, 0))
            watermark_draw = ImageDraw.Draw(watermark_bg)
            
            bbox = watermark_draw.textbbox((0, 0), watermark, font=font)
            padding = 10
            
            watermark_draw.rectangle(
                [
                    bbox[0] - padding, bbox[1] - padding,
                    bbox[2] + padding, bbox[3] + padding
                ],
                fill=(0, 0, 0, 100)
            )
            
            watermark_draw.text(
                (padding, image.height - bbox[3] - padding * 2),
                watermark,
                font=font,
                fill=(255, 255, 255, 150)
            )
            
            image = Image.alpha_composite(image, watermark_bg)
        
        return image
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        return {
            **self.performance_stats,
            'cache_hit_rate': (
                self.performance_stats['cache_hits'] /
                max(self.performance_stats['cache_hits'] + self.performance_stats['cache_misses'], 1)
            ) * 100
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.async_processor.close()
        self.cache_manager.clear_old_cache()


class FontManager:
    """Manage font loading and caching"""
    
    def __init__(self):
        self.fonts_cache = {}
        self.available_fonts = []
        self.font_variants = {}
    
    async def load_fonts_async(self):
        """Load fonts asynchronously"""
        fonts_dir = Path(PATHS["fonts"])
        
        if fonts_dir.exists():
            font_files = []
            for pattern in FONTS["font_files"]:
                font_files.extend(fonts_dir.glob(pattern))
            
            for font_file in font_files:
                try:
                    font = ImageFont.truetype(str(font_file), 12)
                    self.available_fonts.append(str(font_file))
                    
                    # Extract font family and styles
                    self._analyze_font_variants(font_file)
                except Exception as e:
                    logger.warning(f"Could not load font {font_file}: {e}")
        
        logger.info(f"Loaded {len(self.available_fonts)} fonts")
    
    def _analyze_font_variants(self, font_path: Path):
        """Analyze font variants and styles"""
        # This is a simplified implementation
        # In production, you might want to use fontTools or similar
        font_name = font_path.stem.lower()
        
        if "bold" in font_name and "italic" in font_name:
            style = "bold_italic"
        elif "bold" in font_name:
            style = "bold"
        elif "italic" in font_name:
            style = "italic"
        else:
            style = "regular"
        
        family = font_name.replace("bold", "").replace("italic", "").replace("_", "").strip()
        
        if family not in self.font_variants:
            self.font_variants[family] = {}
        
        self.font_variants[family][style] = str(font_path)
    
    async def get_font(self, size: int = 12, style: str = "regular") -> ImageFont.FreeTypeFont:
        """Get font with caching"""
        cache_key = f"{size}_{style}"
        
        if cache_key in self.fonts_cache:
            return self.fonts_cache[cache_key]
        
        # Try to find appropriate font
        font_path = None
        
        # Look for specific style
        for family in self.font_variants:
            if style in self.font_variants[family]:
                font_path = self.font_variants[family][style]
                break
        
        # Fallback to any available font
        if not font_path and self.available_fonts:
            font_path = random.choice(self.available_fonts)
        
        # Load font
        try:
            if font_path:
                font = ImageFont.truetype(font_path, size)
            else:
                font = ImageFont.load_default()
            
            self.fonts_cache[cache_key] = font
            return font
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            return ImageFont.load_default()


class BorderManager:
    """Manage border generation and caching"""
    
    def __init__(self):
        self.borders_cache = {}
        self.available_borders = []
    
    async def load_borders_async(self):
        """Load borders asynchronously"""
        borders_dir = Path(PATHS["borders"])
        
        if borders_dir.exists():
            border_files = []
            for pattern in BORDERS["border_files"]:
                border_files.extend(borders_dir.glob(pattern))
            
            self.available_borders = [str(f) for f in border_files]
        
        # Generate default borders if none found
        if not self.available_borders and BORDERS.get("auto_generate", True):
            await self._generate_default_borders_async()
        
        logger.info(f"Loaded {len(self.available_borders)} borders")
    
    async def _generate_default_borders_async(self):
        """Generate default borders asynchronously"""
        borders_dir = Path(PATHS["borders"])
        borders_dir.mkdir(parents=True, exist_ok=True)
        
        border_styles = BORDERS.get("styles", ["neon", "vintage", "modern"])
        
        for style in border_styles:
            border_path = borders_dir / f"default_{style}_border.png"
            
            # Generate different styles
            if style == "neon":
                border = await self._create_neon_border(1080, 1080)
            elif style == "vintage":
                border = await self._create_vintage_border(1080, 1080)
            elif style == "modern":
                border = await self._create_modern_border(1080, 1080)
            else:
                border = await self._create_simple_border(1080, 1080)
            
            border.save(border_path, 'PNG')
            self.available_borders.append(str(border_path))
    
    async def _create_neon_border(self, width: int, height: int) -> Image.Image:
        """Create neon border"""
        border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        # Draw neon glow effect
        for i in range(3):
            thickness = 20 - i * 5
            color = (0, 255, 255, 150 - i * 50)
            draw.rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                outline=color,
                width=5
            )
        
        return border
    
    async def get_border(
        self,
        style: str = "random",
        color: Optional[Tuple[int, int, int]] = None,
        size: Tuple[int, int] = (1080, 1080)
    ) -> Optional[Image.Image]:
        """Get border image"""
        cache_key = f"{style}_{color}_{size}"
        
        if cache_key in self.borders_cache:
            return self.borders_cache[cache_key]
        
        if not self.available_borders:
            return None
        
        # Select border based on style
        if style == "random":
            border_path = random.choice(self.available_borders)
        else:
            # Find border matching style
            matching = [b for b in self.available_borders if style in b.lower()]
            border_path = matching[0] if matching else random.choice(self.available_borders)
        
        try:
            async with aiofiles.open(border_path, 'rb') as f:
                content = await f.read()
            
            border = Image.open(io.BytesIO(content)).convert('RGBA')
            border = border.resize(size, Resampling.LANCZOS)
            
            # Recolor if color specified
            if color:
                border = await self._recolor_border(border, color)
            
            self.borders_cache[cache_key] = border
            return border
        except Exception as e:
            logger.error(f"Error loading border {border_path}: {e}")
            return None
    
    async def _recolor_border(self, border: Image.Image, color: Tuple[int, int, int]) -> Image.Image:
        """Recolor border image"""
        # Convert border to numpy array for efficient processing
        arr = np.array(border)
        
        # Create mask of non-transparent pixels
        mask = arr[:, :, 3] > 0
        
        # Recolor
        arr[mask, 0] = color[0]
        arr[mask, 1] = color[1]
        arr[mask, 2] = color[2]
        
        return Image.fromarray(arr)


class EffectManager:
    """Manage visual effects"""
    
    def __init__(self):
        self.effect_cache = {}
    
    async def apply_glow_effect(
        self,
        image: Image.Image,
        intensity: int = 2,
        color: Optional[Tuple[int, int, int]] = None
    ) -> Image.Image:
        """Apply glow effect"""
        cache_key = f"glow_{intensity}_{color}_{image.size}"
        
        if cache_key in self.effect_cache:
            return self.effect_cache[cache_key]
        
        # Create glow layer
        glow = image.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=intensity))
        
        # Adjust color if specified
        if color:
            color_layer = Image.new('RGBA', image.size, (*color, 100))
            glow = Image.alpha_composite(glow, color_layer)
        
        # Composite with original
        result = Image.alpha_composite(glow, image)
        
        self.effect_cache[cache_key] = result
        return result
    
    async def apply_3d_shadow(
        self,
        image: Image.Image,
        depth: int = 3,
        angle: float = 45
    ) -> Image.Image:
        """Apply 3D shadow effect"""
        angle_rad = np.radians(angle)
        dx = int(np.cos(angle_rad) * depth)
        dy = int(np.sin(angle_rad) * depth)
        
        # Create shadow layers
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        for i in range(depth, 0, -1):
            offset_x = dx * i // depth
            offset_y = dy * i // depth
            
            shadow_layer = image.copy()
            # Make shadow darker
            shadow_layer = self._adjust_brightness(shadow_layer, 0.3)
            shadow.paste(shadow_layer, (offset_x, offset_y), shadow_layer)
        
        # Composite shadow with original
        result = Image.alpha_composite(shadow, image)
        return result
    
    async def create_gradient(
        self,
        width: int,
        height: int,
        start_color: Tuple[int, int, int],
        end_color: Tuple[int, int, int],
        direction: str = "horizontal"
    ) -> Image.Image:
        """Create gradient background"""
        cache_key = f"gradient_{width}_{height}_{start_color}_{end_color}_{direction}"
        
        if cache_key in self.effect_cache:
            return self.effect_cache[cache_key]
        
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        if direction == "horizontal":
            for x in range(width):
                ratio = x / width
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        elif direction == "vertical":
            for y in range(height):
                ratio = y / height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:  # diagonal
            for x in range(width):
                for y in range(height):
                    ratio = (x + y) / (width + height)
                    r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                    g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                    b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                    draw.point((x, y), fill=(r, g, b))
        
        self.effect_cache[cache_key] = gradient
        return gradient
    
    async def apply_cinematic_lighting(
        self,
        image: Image.Image,
        mode: str = "day"
    ) -> Image.Image:
        """Apply cinematic lighting effects"""
        width, height = image.size
        
        # Create lighting overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        if mode == "day":
            # Sunlight from top-left
            center_x, center_y = width // 4, height // 4
            max_radius = max(width, height)
            
            for i in range(0, max_radius, 10):
                radius = i
                alpha = int(30 * (1 - i / max_radius))
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    fill=(255, 255, 200, alpha),
                    outline=None
                )
        else:
            # Moonlight from top-right
            center_x, center_y = width * 3 // 4, height // 4
            max_radius = max(width, height) // 2
            
            for i in range(0, max_radius, 10):
                radius = i
                alpha = int(40 * (1 - i / max_radius))
                draw.ellipse(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    fill=(150, 150, 255, alpha),
                    outline=None
                )
        
        # Apply vignette effect
        vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        vignette_draw = ImageDraw.Draw(vignette)
        
        for i in range(0, max(width, height) // 2, 10):
            radius = i
            alpha = int(50 * (i / (max(width, height) // 2)))
            
            # Create circular vignette
            bbox = [
                width // 2 - radius, height // 2 - radius,
                width // 2 + radius, height // 2 + radius
            ]
            
            if bbox[0] > 0 and bbox[1] > 0:
                vignette_draw.ellipse(
                    bbox,
                    fill=(0, 0, 0, alpha),
                    outline=None
                )
        
        # Composite all effects
        result = Image.alpha_composite(image.convert('RGBA'), overlay)
        result = Image.alpha_composite(result, vignette)
        
        return result.convert('RGB')
    
    async def apply_reflection_effect(self, image: Image.Image) -> Image.Image:
        """Apply reflection effect to image"""
        width, height = image.size
        
        # Create reflection
        reflection = image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Create gradient mask
        mask = Image.new('L', (width, height // 2), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        for y in range(height // 2):
            alpha = int(255 * (1 - y / (height // 2)))
            mask_draw.line([(0, y), (width, y)], fill=alpha)
        
        # Apply mask to reflection
        reflection.putalpha(mask)
        
        # Create new image with reflection
        result = Image.new('RGBA', (width, height + height // 2))
        result.paste(image, (0, 0))
        result.paste(reflection, (0, height), reflection)
        
        return result
    
    def _adjust_brightness(self, image: Image.Image, factor: float) -> Image.Image:
        """Adjust image brightness"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)


class TemplateManager:
    """Manage image templates"""
    
    def __init__(self):
        self.templates = {}
        self.template_cache = {}
    
    async def load_templates_async(self):
        """Load templates asynchronously"""
        templates_dir = Path(PATHS["templates"])
        
        if templates_dir.exists():
            # Load JSON templates
            json_files = templates_dir.glob("*.json")
            
            for json_file in json_files:
                try:
                    async with aiofiles.open(json_file, 'r', encoding='utf-8') as f:
                        content = await f.read()
                    templates = json.loads(content)
                    self.templates[json_file.stem] = templates
                except Exception as e:
                    logger.error(f"Error loading template {json_file}: {e}")
        
        logger.info(f"Loaded {len(self.templates)} template sets")


class ImageGenerationError(Exception):
    """Custom exception for image generation errors"""
    pass


# Factory function for convenience
async def create_image_generator(
    config: Optional[GenerationConfig] = None
) -> AdvancedImageGenerator:
    """Factory function to create image generator"""
    generator = AdvancedImageGenerator(config)
    # Wait for assets to load
    await asyncio.sleep(0.1)  # Small delay for async loading
    return generator


# Example usage
async def example_usage():
    """Example usage of the advanced image generator"""
    # Create generator
    generator = await create_image_generator(
        GenerationConfig(
            width=1200,
            height=1200,
            style=ImageStyle.NEON,
            quality=98,
            enable_cache=True
        )
    )
    
    try:
        # Create text configuration
        text_config = TextConfig(
            primary_text="Advanced Roast Generator",
            secondary_text="Professional grade image generation",
            emoji="🔥",
            font_size_primary=72,
            font_size_secondary=36,
            text_color=(255, 255, 255),
            effects=[TextEffect.GLOW, TextEffect.SHADOW_3D]
        )
        
        # Create border configuration
        border_config = BorderConfig(
            enabled=True,
            style="neon",
            color=(0, 255, 255),
            thickness=15
        )
        
        # Generate image
        image_data = await generator.generate_image(
            text_config=text_config,
            border_config=border_config
        )
        
        # Save to file
        output_path = Path(PATHS["output"]) / "example_roast.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        console.print(f"[green]✓ Image generated: {output_path}[/green]")
        
        # Show performance stats
        stats = generator.get_performance_stats()
        console.print(f"[blue]Performance Stats:[/blue]")
        console.print(f"  Cache hit rate: {stats['cache_hit_rate']:.1f}%")
        console.print(f"  Avg generation time: {stats['avg_generation_time']:.2f}s")
        
    finally:
        # Cleanup
        await generator.cleanup()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
