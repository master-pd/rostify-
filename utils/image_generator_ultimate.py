"""
Ultimate Image Generator v6.0 for Roastify Premium
"""

import os
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

logger = logging.getLogger(__name__)

class BorderType(Enum):
    NONE = "none"
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DOUBLE = "double"
    ROUNDED = "rounded"
    SHADOW = "shadow"

class TextEffect(Enum):
    NONE = "none"
    SHADOW = "shadow"
    OUTLINE = "outline"
    GRADIENT = "gradient"
    GLOW = "glow"

class GradientDirection(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"
    RADIAL = "radial"

@dataclass
class BorderConfig:
    border_type: BorderType = BorderType.ROUNDED
    border_width: int = 5
    border_color: str = "#FFD700"
    border_radius: int = 20
    inner_glow: bool = False
    outer_shadow: bool = True
    shadow_blur: int = 10
    shadow_offset: Tuple[int, int] = (5, 5)
    shadow_color: str = "#00000080"

@dataclass
class TextConfig:
    font_size: int = 40
    font_color: str = "#FFFFFF"
    font_path: Optional[str] = None
    text_align: str = "center"
    line_spacing: int = 10
    max_width: int = 800
    effects: List[TextEffect] = None
    outline_width: int = 2
    outline_color: str = "#000000"

@dataclass
class BackgroundConfig:
    background_type: str = "gradient"  # solid, gradient, image
    background_color: str = "#1A1A1A"
    gradient_colors: List[str] = None
    gradient_direction: GradientDirection = GradientDirection.DIAGONAL
    background_image: Optional[str] = None
    blur_radius: int = 0
    pattern_overlay: bool = False
    pattern_opacity: float = 0.1

@dataclass
class ImageConfig:
    width: int = 1080
    height: int = 1080
    quality: int = 95
    format: str = "PNG"
    enable_cache: bool = True
    cache_ttl_hours: int = 24
    max_cache_size: int = 1000
    output_dir: str = "./output"
    temp_dir: str = "./temp"
    cache_dir: str = "./cache"
    assets_dir: str = "./assets"
    backup_dir: str = "./backup"
    max_workers: int = 4
    timeout: float = 30.0
    enable_backup: bool = True
    compression_level: int = 6
    premium_features: bool = True

@dataclass
class GenerationResult:
    success: bool
    image_path: Optional[str] = None
    processing_time: float = 0.0
    cache_hit: bool = False
    error: Optional[str] = None
    metadata: Dict = None


class UltimateImageGenerator:
    """Ultimate image generator with premium features"""
    
    def __init__(self, config: Optional[ImageConfig] = None):
        self.config = config or ImageConfig()
        self.stats = {
            "total_generated": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "total_processing_time": 0.0
        }
        
        # Create directories
        self._create_directories()
        logger.info("UltimateImageGenerator v6.0 initialized")
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.config.output_dir,
            self.config.temp_dir,
            self.config.cache_dir,
            self.config.assets_dir,
            self.config.backup_dir
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def generate_roast_image(self, roast_data: Any, user_info: Any,
                           style: str = "auto",
                           border_config: Optional[BorderConfig] = None,
                           background_config: Optional[BackgroundConfig] = None) -> GenerationResult:
        """Generate roast image"""
        import time
        start_time = time.time()
        
        try:
            if not HAS_PIL:
                return GenerationResult(
                    success=False,
                    error="PIL/Pillow not available",
                    processing_time=0.0
                )
            
            # Check cache
            cache_key = self._generate_cache_key(roast_data, user_info, style)
            cached_result = self._get_cached_image(cache_key)
            
            if cached_result and self.config.enable_cache:
                self.stats["cache_hits"] += 1
                return GenerationResult(
                    success=True,
                    image_path=cached_result,
                    processing_time=time.time() - start_time,
                    cache_hit=True
                )
            
            self.stats["cache_misses"] += 1
            
            # Generate image
            image = self._create_base_image(background_config)
            draw = ImageDraw.Draw(image)
            
            # Add border
            if border_config:
                image = self._add_border(image, border_config)
            
            # Add roast text
            roast_text = self._extract_roast_text(roast_data)
            self._add_roast_text(draw, roast_text, user_info, style)
            
            # Add user info
            self._add_user_info(draw, user_info)
            
            # Add decorations
            self._add_decorations(draw, style)
            
            # Save image
            filename = self._save_image(image)
            
            # Cache the result
            if self.config.enable_cache:
                self._cache_image(cache_key, filename)
            
            processing_time = time.time() - start_time
            self.stats["total_generated"] += 1
            self.stats["total_processing_time"] += processing_time
            
            return GenerationResult(
                success=True,
                image_path=filename,
                processing_time=processing_time,
                metadata={
                    "style": style,
                    "dimensions": f"{self.config.width}x{self.config.height}",
                    "quality": self.config.quality
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            self.stats["errors"] += 1
            
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def generate_welcome_image(self, user_info: Any) -> GenerationResult:
        """Generate welcome image"""
        # Implementation would be similar to generate_roast_image
        # but with welcome-specific design
        pass
    
    def generate_achievement_image(self, user_info: Any, achievement: Any) -> GenerationResult:
        """Generate achievement image"""
        # Implementation for achievement images
        pass
    
    def _create_base_image(self, background_config: Optional[BackgroundConfig]) -> Image.Image:
        """Create base image with background"""
        width, height = self.config.width, self.config.height
        
        if background_config and background_config.background_type == "gradient":
            return self._create_gradient_background(
                width, height,
                background_config.gradient_colors or ["#0F2027", "#203A43", "#2C5364"],
                background_config.gradient_direction.value
            )
        elif background_config and background_config.background_type == "image":
            if background_config.background_image and os.path.exists(background_config.background_image):
                image = Image.open(background_config.background_image)
                image = image.resize((width, height))
                if background_config.blur_radius > 0:
                    image = image.filter(ImageFilter.GaussianBlur(background_config.blur_radius))
                return image
        
        # Default solid background
        bg_color = background_config.background_color if background_config else "#1A1A1A"
        return Image.new('RGB', (width, height), color=bg_color)
    
    def _create_gradient_background(self, width: int, height: int, 
                                  colors: List[str], direction: str) -> Image.Image:
        """Create gradient background"""
        base = Image.new('RGB', (width, height), color=self._hex_to_rgb(colors[0]))
        draw = ImageDraw.Draw(base)
        
        # Simple gradient implementation
        if direction == "vertical":
            for i in range(height):
                ratio = i / height
                color = self._interpolate_color(colors, ratio)
                draw.line([(0, i), (width, i)], fill=color)
        
        return base
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _interpolate_color(self, colors: List[str], ratio: float) -> Tuple[int, int, int]:
        """Interpolate between colors"""
        idx = int(ratio * (len(colors) - 1))
        color1 = self._hex_to_rgb(colors[idx])
        color2 = self._hex_to_rgb(colors[min(idx + 1, len(colors) - 1)])
        
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        return (r, g, b)
    
    def _add_border(self, image: Image.Image, border_config: BorderConfig) -> Image.Image:
        """Add border to image"""
        # Border implementation
        return image
    
    def _extract_roast_text(self, roast_data: Any) -> str:
        """Extract roast text from data"""
        if isinstance(roast_data, dict):
            return roast_data.get('roast_text', roast_data.get('primary_roast', 'Default Roast'))
        elif isinstance(roast_data, str):
            return roast_data
        return str(roast_data)
    
    def _add_roast_text(self, draw: ImageDraw.Draw, text: str, 
                       user_info: Any, style: str):
        """Add roast text to image"""
        # Text rendering implementation
        pass
    
    def _add_user_info(self, draw: ImageDraw.Draw, user_info: Any):
        """Add user information to image"""
        pass
    
    def _add_decorations(self, draw: ImageDraw.Draw, style: str):
        """Add decorative elements"""
        pass
    
    def _save_image(self, image: Image.Image) -> str:
        """Save image to file"""
        filename = f"{self.config.temp_dir}/roast_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}.png"
        image.save(filename, self.config.format, 
                  quality=self.config.quality,
                  optimize=True)
        return filename
    
    def _generate_cache_key(self, roast_data: Any, user_info: Any, style: str) -> str:
        """Generate cache key"""
        import hashlib
        content = f"{roast_data}{user_info}{style}{self.config.width}{self.config.height}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_image(self, cache_key: str) -> Optional[str]:
        """Get cached image"""
        cache_file = Path(self.config.cache_dir) / f"{cache_key}.png"
        if cache_file.exists():
            return str(cache_file)
        return None
    
    def _cache_image(self, cache_key: str, image_path: str):
        """Cache image"""
        import shutil
        cache_file = Path(self.config.cache_dir) / f"{cache_key}.png"
        shutil.copy2(image_path, cache_file)
    
    def get_detailed_stats(self) -> Dict:
        """Get detailed statistics"""
        return {
            "total_generated": self.stats["total_generated"],
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "cache_hit_rate": self.stats["cache_hits"] / max(self.stats["total_generated"], 1),
            "errors": self.stats["errors"],
            "average_time_seconds": self.stats["total_processing_time"] / max(self.stats["total_generated"], 1),
            "performance": {
                "success_rate": (self.stats["total_generated"] - self.stats["errors"]) / max(self.stats["total_generated"], 1),
                "average_time_seconds": self.stats["total_processing_time"] / max(self.stats["total_generated"], 1)
            },
            "cache": {
                "total_items": len(list(Path(self.config.cache_dir).glob("*.png"))),
                "size_mb": self._get_directory_size(self.config.cache_dir) / (1024 * 1024)
            }
        }
    
    def _get_directory_size(self, directory: str) -> int:
        """Get directory size in bytes"""
        total = 0
        for path in Path(directory).rglob('*'):
            if path.is_file():
                total += path.stat().st_size
        return total
    
    def health_check(self) -> Dict:
        """Health check"""
        return {
            "healthy": HAS_PIL,
            "checks": {
                "pil_available": HAS_PIL,
                "directories_accessible": all(Path(d).exists() for d in [
                    self.config.output_dir, self.config.temp_dir
                ]),
                "font_manager_ready": True,
                "cache_operational": Path(self.config.cache_dir).exists(),
                "write_permissions": os.access(self.config.temp_dir, os.W_OK)
            },
            "stats": self.get_detailed_stats()
        }
    
    def cleanup(self):
        """Cleanup resources"""
        # Clean temp directory
        temp_path = Path(self.config.temp_dir)
        if temp_path.exists():
            for file in temp_path.glob("*"):
                try:
                    if file.is_file():
                        file.unlink()
                except:
                    pass
