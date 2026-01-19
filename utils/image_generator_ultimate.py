"""
🔥 ULTRA PREMIUM IMAGE GENERATOR v12.0 - RANA EDITION
🎨 8K Ready | AI-Powered | Complete Professional Suite
✨ Features: HD Backgrounds | Dynamic Profiles | Premium Effects
🚀 Performance Optimized for Mass Production
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
import requests
import io
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, wraps
import traceback
from concurrent.futures import ThreadPoolExecutor

# PIL Imports with fallback
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageColor
    from PIL.Image import Resampling
    from PIL.ImageFilter import GaussianBlur, UnsharpMask, MedianFilter, Kernel
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("❌ PIL not installed! Install: pip install pillow")

# Configure advanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('UltraPremiumRana')

# ==================== CONSTANTS ====================
RESOLUTION_PRESETS = {
    '8K_ULTRA': {'width': 7680, 'height': 4320, 'quality': 100},
    '4K_PRO': {'width': 3840, 'height': 2160, 'quality': 98},
    '2K_PREMIUM': {'width': 2560, 'height': 1440, 'quality': 95},
    'FULL_HD': {'width': 1920, 'height': 1080, 'quality': 90},
    'SOCIAL_OPTIMAL': {'width': 1200, 'height': 1200, 'quality': 92}
}

# Premium Color Palettes
PREMIUM_PALETTES = {
    'RANA_GOLD': {
        'name': 'Rana Gold',
        'primary': (212, 175, 55),   # Gold
        'secondary': (184, 134, 11), # Dark Gold
        'accent': (255, 215, 0),     # Golden Yellow
        'text': (255, 250, 240),     # Floral White
        'background': (30, 30, 40),  # Dark Navy
        'highlight': (255, 140, 0),  # Orange
        'success': (0, 200, 100),    # Emerald
        'warning': (255, 200, 0),    # Amber
        'error': (255, 50, 50)       # Red
    },
    'CYBER_PURPLE': {
        'name': 'Cyber Purple',
        'primary': (138, 43, 226),   # Blue Violet
        'secondary': (75, 0, 130),   # Indigo
        'accent': (0, 255, 255),     # Cyan
        'text': (255, 255, 255),
        'background': (10, 10, 20),
        'highlight': (255, 0, 255),  # Magenta
        'success': (0, 255, 200),
        'warning': (255, 255, 0),
        'error': (255, 0, 100)
    },
    'BENGALI_FIESTA': {
        'name': 'Bengali Fiesta',
        'primary': (220, 20, 60),    Crimson
        'secondary': (255, 140, 0),  Dark Orange
        'accent': (255, 215, 0),     Gold
        'text': (255, 250, 240),
        'background': (30, 30, 50),
        'highlight': (50, 205, 50),  Lime Green
        'success': (0, 200, 0),
        'warning': (255, 165, 0),
        'error': (178, 34, 34)
    },
    'OCEAN_DEPTH': {
        'name': 'Ocean Depth',
        'primary': (0, 105, 148),    Deep Sea Blue
        'secondary': (0, 168, 204),  Ocean Blue
        'accent': (0, 207, 255),     Bright Cyan
        'text': (240, 248, 255),     Alice Blue
        'background': (0, 30, 60),   Midnight Blue
        'highlight': (64, 224, 208), Turquoise
        'success': (0, 255, 150),    Spring Green
        'warning': (255, 215, 0),    Gold
        'error': (255, 50, 50)
    }
}

# ==================== ENUMS ====================
class UltraStyle(Enum):
    """Ultra Premium Styles"""
    GLASS_MORPHISM_3D = auto()
    NEON_CYBERPUNK = auto()
    GOLDEN_LUXURY = auto()
    DARK_FUTURISTIC = auto()
    GRADIENT_DREAM = auto()
    BENGALI_ROYAL = auto()
    ISLAMIC_GOLD = auto()
    ABSTRACT_ART = auto()
    NATURE_VIBRANT = auto()
    CITY_NIGHTS = auto()
    SPACE_GALAXY = auto()
    WATERCOLOR = auto()
    OIL_PAINTING = auto()
    SKETCH_ARTISTIC = auto()
    PARTICLE_EFFECT = auto()
    HOLOGRAM = auto()
    METALLIC = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class BackgroundSource(Enum):
    """Background Source Types"""
    HD_GRADIENT_MESH = auto()
    AI_GENERATED_ART = auto()
    PATTERN_GEOMETRIC = auto()
    TEXTURE_PREMIUM = auto()
    CULTURAL_ART = auto()
    PHOTO_REALISTIC = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

class ProfileDesign(Enum):
    """Premium Profile Designs"""
    GOLDEN_FRAME_3D = auto()
    NEON_GLOW_CIRCLE = auto()
    DIAMOND_CUT = auto()
    VIP_BADGE = auto()
    PREMIUM_STAR = auto()
    FLOWER_MANDALA = auto()
    GEOMETRIC_ART = auto()
    SPARKLE_AURA = auto()
    HOLOGRAM_EFFECT = auto()
    METAL_PLATE = auto()
    GLASS_MORPH = auto()
    ANIMATED_BORDER = auto()
    
    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

# ==================== DATACLASSES ====================
@dataclass
class UltraConfig:
    """Ultra Premium Configuration"""
    # Resolution
    resolution_preset: str = "4K_PRO"
    custom_width: int = 0
    custom_height: int = 0
    quality: int = 98
    format: str = "PNG"
    
    # Features
    enable_hd_backgrounds: bool = True
    enable_dynamic_profiles: bool = True
    enable_premium_effects: bool = True
    enable_ai_enhancement: bool = True
    enable_cultural_elements: bool = True
    enable_animation: bool = False
    
    # Performance
    max_workers: int = 4
    cache_enabled: bool = True
    cache_size: int = 1000
    compression_level: int = 1
    
    # Paths
    output_dir: str = "./output/rana_premium"
    assets_dir: str = "./assets/rana_premium"
    backgrounds_dir: str = "./assets/backgrounds_hd"
    profiles_dir: str = "./assets/profiles_premium"
    fonts_dir: str = "./assets/fonts_premium"
    cache_dir: str = "./cache/rana"
    
    # Advanced
    enable_watermark: bool = True
    watermark_text: str = "Roastify Ultra Premium"
    max_file_size_mb: int = 20
    
    def __post_init__(self):
        """Initialize configuration"""
        # Set resolution
        if self.resolution_preset in RESOLUTION_PRESETS:
            preset = RESOLUTION_PRESETS[self.resolution_preset]
            if self.custom_width <= 0:
                self.custom_width = preset['width']
            if self.custom_height <= 0:
                self.custom_height = preset['height']
            self.quality = preset['quality']
        else:
            self.custom_width = max(1080, min(self.custom_width, 7680))
            self.custom_height = max(1080, min(self.custom_height, 7680))
        
        # Create directories
        directories = [
            self.output_dir, self.assets_dir, self.backgrounds_dir,
            self.profiles_dir, self.fonts_dir, self.cache_dir
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ UltraConfig initialized: {self.custom_width}x{self.custom_height}")

@dataclass
class UserProfile:
    """Premium User Profile"""
    id: int
    username: str
    first_name: str = ""
    last_name: str = ""
    display_name: str = ""
    rating: float = 0.0
    level: int = 1
    rank: str = "Member"
    join_date: str = ""
    badges: List[str] = field(default_factory=list)
    is_premium: bool = False
    is_vip: bool = False
    is_admin: bool = False
    is_creator: bool = False
    profile_color: Tuple[int, int, int] = None
    signature_color: Tuple[int, int, int] = None
    
    def __post_init__(self):
        """Initialize profile with premium features"""
        if not self.display_name:
            if self.first_name and self.last_name:
                self.display_name = f"{self.first_name} {self.last_name}"
            elif self.first_name:
                self.display_name = self.first_name
            else:
                self.display_name = self.username
        
        if not self.join_date:
            self.join_date = datetime.now().strftime("%d %b %Y")
        
        # Generate unique colors
        if self.profile_color is None:
            self.profile_color = self._generate_color_from_id(self.id)
        
        if self.signature_color is None:
            self.signature_color = self._adjust_color(self.profile_color, 40)
        
        # Special recognition for specific usernames
        special_usernames = ['rana', 'রানা', 'admin', 'creator', 'founder']
        username_lower = self.username.lower()
        
        if any(special in username_lower for special in special_usernames):
            self.is_premium = True
            if 'rana' in username_lower or 'রানা' in username_lower:
                self.is_vip = True
                self.rank = "Premium VIP"
                self.profile_color = (255, 215, 0)  # Gold
                self.signature_color = (255, 140, 0)  # Dark Orange
    
    def _generate_color_from_id(self, user_id: int) -> Tuple[int, int, int]:
        """Generate unique color from user ID"""
        # Use golden ratio for pleasing colors
        golden_ratio_conjugate = 0.618033988749895
        
        hue = (user_id * golden_ratio_conjugate) % 1.0
        
        # Convert HSV to RGB
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def _adjust_color(self, color: Tuple[int, int, int], 
                     adjustment: int) -> Tuple[int, int, int]:
        """Adjust color brightness"""
        r, g, b = color
        return (
            min(255, max(0, r + adjustment)),
            min(255, max(0, g + adjustment)),
            min(255, max(0, b + adjustment))
        )
    
    def get_badge_text(self) -> str:
        """Get badge display text"""
        if self.is_vip:
            return "⭐ VIP ⭐"
        elif self.is_premium:
            return "✨ Premium ✨"
        elif self.is_admin:
            return "🛡️ Admin 🛡️"
        elif self.is_creator:
            return "🎨 Creator 🎨"
        return ""

# ==================== PREMIUM BACKGROUND GENERATOR ====================
class PremiumBackgroundGenerator:
    """Generates Ultra HD Premium Backgrounds"""
    
    def __init__(self, config: UltraConfig):
        self.config = config
        self.cache = {}
        self.max_cache_size = 100
        
    def generate(self, width: int, height: int, 
                 style: UltraStyle) -> Image.Image:
        """Generate premium background"""
        cache_key = f"{width}x{height}_{style.name}"
        
        if cache_key in self.cache:
            return self.cache[cache_key].copy()
        
        try:
            # Select background type based on style
            if style in [UltraStyle.GLASS_MORPHISM_3D, UltraStyle.GOLDEN_LUXURY]:
                background = self._generate_glass_morphism(width, height)
            elif style in [UltraStyle.NEON_CYBERPUNK, UltraStyle.DARK_FUTURISTIC]:
                background = self._generate_cyberpunk(width, height)
            elif style == UltraStyle.BENGALI_ROYAL:
                background = self._generate_bengali_royal(width, height)
            elif style == UltraStyle.ISLAMIC_GOLD:
                background = self._generate_islamic_gold(width, height)
            elif style == UltraStyle.SPACE_GALAXY:
                background = self._generate_space_galaxy(width, height)
            elif style == UltraStyle.GRADIENT_DREAM:
                background = self._generate_gradient_dream(width, height)
            else:
                background = self._generate_abstract_art(width, height)
            
            # Apply style-specific enhancements
            background = self._apply_style_effects(background, style)
            
            # Cache result
            if len(self.cache) >= self.max_cache_size:
                # Remove oldest item
                self.cache.pop(next(iter(self.cache)))
            
            self.cache[cache_key] = background.copy()
            return background
            
        except Exception as e:
            logger.error(f"Background generation failed: {e}")
            return self._generate_fallback_background(width, height)
    
    def _generate_glass_morphism(self, width: int, height: int) -> Image.Image:
        """Generate glass morphism background"""
        # Create base gradient
        base = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(base)
        
        # Create multiple gradient layers
        colors = [
            (30, 30, 50, 150),   # Dark Blue
            (50, 50, 80, 100),   # Medium Blue
            (80, 80, 120, 80),   # Light Blue
            (120, 120, 180, 60)  # Very Light Blue
        ]
        
        # Draw gradient circles
        for i in range(8):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(width // 4, width // 2)
            color = random.choice(colors)
            
            for r in range(radius, 0, -20):
                alpha = int(color[3] * (r / radius))
                draw.ellipse([x - r, y - r, x + r, y + r],
                           fill=(color[0], color[1], color[2], alpha))
        
        # Add blur for glass effect
        base = base.filter(GaussianBlur(radius=50))
        
        return base
    
    def _generate_cyberpunk(self, width: int, height: int) -> Image.Image:
        """Generate cyberpunk background"""
        base = Image.new('RGB', (width, height), (10, 10, 30))
        draw = ImageDraw.Draw(base)
        
        # Grid lines
        grid_spacing = width // 20
        grid_color = (0, 255, 255, 30)
        
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=grid_color[:3], width=1)
        
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=grid_color[:3], width=1)
        
        # Neon elements
        neon_colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
        
        for _ in range(20):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            color = random.choice(neon_colors)
            
            # Draw neon line with glow
            for i in range(3):
                glow_width = 3 - i
                glow_color = (*color, 100 - i * 30)
                draw.line([(x1, y1), (x2, y2)], 
                         fill=glow_color[:3], 
                         width=glow_width)
        
        # Add scan lines
        for y in range(0, height, 4):
            draw.line([(0, y), (width, y)], 
                     fill=(0, 0, 0, 20)[:3], 
                     width=1)
        
        return base
    
    def _generate_bengali_royal(self, width: int, height: int) -> Image.Image:
        """Generate Bengali royal background"""
        # Rich colors: Red, Orange, Gold
        colors = [
            (139, 0, 0),    # Dark Red
            (178, 34, 34),  # Firebrick
            (255, 140, 0),  # Dark Orange
            (255, 165, 0),  # Orange
            (255, 215, 0)   # Gold
        ]
        
        # Create gradient background
        base = self._create_gradient(width, height, colors)
        
        # Add traditional patterns
        draw = ImageDraw.Draw(base.convert('RGBA'))
        
        # Alpana-style patterns
        pattern_size = width // 15
        for x in range(0, width, pattern_size):
            for y in range(0, height, pattern_size):
                if random.random() > 0.7:
                    # Draw floral pattern
                    center_x = x + pattern_size // 2
                    center_y = y + pattern_size // 2
                    
                    # Petals
                    for angle in range(0, 360, 45):
                        rad = math.radians(angle)
                        x1 = center_x + math.cos(rad) * (pattern_size // 4)
                        y1 = center_y + math.sin(rad) * (pattern_size // 4)
                        x2 = center_x + math.cos(rad) * (pattern_size // 3)
                        y2 = center_y + math.sin(rad) * (pattern_size // 3)
                        
                        draw.line([(x1, y1), (x2, y2)], 
                                 fill=(255, 255, 255, 100), 
                                 width=2)
        
        return base
    
    def _generate_islamic_gold(self, width: int, height: int) -> Image.Image:
        """Generate Islamic geometric gold background"""
        base = Image.new('RGB', (width, height), (0, 40, 30))  # Dark Green
        draw = ImageDraw.Draw(base.convert('RGBA'))
        
        # Gold geometric patterns
        gold_color = (218, 165, 32, 200)  # Golden
        pattern_size = width // 12
        
        for x in range(0, width, pattern_size):
            for y in range(0, height, pattern_size):
                # Draw 8-point star
                center_x = x + pattern_size // 2
                center_y = y + pattern_size // 2
                
                points = []
                for i in range(16):
                    angle = math.pi * i / 8
                    radius = pattern_size // 3 if i % 2 == 0 else pattern_size // 6
                    points.append((
                        center_x + radius * math.cos(angle),
                        center_y + radius * math.sin(angle)
                    ))
                
                if len(points) >= 3:
                    draw.polygon(points, fill=gold_color[:3] + (150,), 
                                outline=gold_color[:3] + (200,))
        
        return base
    
    def _generate_space_galaxy(self, width: int, height: int) -> Image.Image:
        """Generate space galaxy background"""
        base = Image.new('RGB', (width, height), (0, 0, 20))  # Deep Space
        draw = ImageDraw.Draw(base.convert('RGBA'))
        
        # Stars
        for _ in range(500):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            draw.ellipse([x - size, y - size, x + size, y + size],
                        fill=(brightness, brightness, brightness, 200))
        
        # Nebula
        nebula_colors = [(138, 43, 226), (75, 0, 130), (0, 191, 255)]
        
        for _ in range(5):
            center_x = random.randint(width // 4, width * 3 // 4)
            center_y = random.randint(height // 4, height * 3 // 4)
            radius = random.randint(width // 6, width // 3)
            color = random.choice(nebula_colors)
            
            for r in range(radius, 0, -10):
                alpha = int(100 * (r / radius))
                draw.ellipse([center_x - r, center_y - r, 
                             center_x + r, center_y + r],
                            fill=(*color, alpha))
        
        return base
    
    def _generate_gradient_dream(self, width: int, height: int) -> Image.Image:
        """Generate dreamy gradient background"""
        colors = [
            (255, 182, 193),  # Light Pink
            (221, 160, 221),  # Plum
            (176, 224, 230),  # Powder Blue
            (152, 251, 152)   # Pale Green
        ]
        
        base = self._create_gradient(width, height, colors)
        
        # Add soft blur
        base = base.filter(GaussianBlur(radius=20))
        
        # Add soft particles
        draw = ImageDraw.Draw(base.convert('RGBA'))
        
        for _ in range(200):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 6)
            color = random.choice([(255, 255, 255, 50), 
                                   (255, 240, 245, 30),
                                   (230, 230, 250, 40)])
            draw.ellipse([x - size, y - size, x + size, y + size],
                        fill=color)
        
        return base
    
    def _generate_abstract_art(self, width: int, height: int) -> Image.Image:
        """Generate abstract art background"""
        base = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(base)
        
        # Abstract shapes
        for _ in range(15):
            # Random shape
            shape_type = random.choice(['circle', 'rectangle', 'triangle'])
            
            if shape_type == 'circle':
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(50, width // 4)
                color = (random.randint(50, 200), 
                        random.randint(50, 200), 
                        random.randint(50, 200))
                draw.ellipse([x - radius, y - radius, 
                             x + radius, y + radius], 
                            fill=color)
            
            elif shape_type == 'rectangle':
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = random.randint(x1, width)
                y2 = random.randint(y1, height)
                color = (random.randint(50, 200), 
                        random.randint(50, 200), 
                        random.randint(50, 200))
                draw.rectangle([x1, y1, x2, y2], fill=color)
        
        # Apply artistic filters
        base = base.filter(GaussianBlur(radius=10))
        
        return base
    
    def _create_gradient(self, width: int, height: int, 
                        colors: List[Tuple[int, int, int]]) -> Image.Image:
        """Create smooth gradient"""
        base = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(base)
        
        # Diagonal gradient
        for x in range(width):
            for y in range(height):
                ratio = (x + y) / (width + height)
                
                # Map ratio to color stops
                color_index = ratio * (len(colors) - 1)
                index1 = int(color_index)
                index2 = min(index1 + 1, len(colors) - 1)
                
                local_ratio = color_index - index1
                
                # Interpolate between colors
                r = int(colors[index1][0] * (1 - local_ratio) + 
                       colors[index2][0] * local_ratio)
                g = int(colors[index1][1] * (1 - local_ratio) + 
                       colors[index2][1] * local_ratio)
                b = int(colors[index1][2] * (1 - local_ratio) + 
                       colors[index2][2] * local_ratio)
                
                draw.point((x, y), fill=(r, g, b))
        
        return base
    
    def _apply_style_effects(self, image: Image.Image, 
                            style: UltraStyle) -> Image.Image:
        """Apply style-specific effects"""
        if style == UltraStyle.GLASS_MORPHISM_3D:
            # Add more blur and brightness
            image = image.filter(GaussianBlur(radius=30))
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)
            
        elif style == UltraStyle.NEON_CYBERPUNK:
            # Boost colors and contrast
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.5)
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            
        elif style in [UltraStyle.GOLDEN_LUXURY, UltraStyle.BENGALI_ROYAL]:
            # Add warmth and saturation
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.4)
            
            # Add golden tint
            if image.mode == 'RGB':
                golden = image.copy()
                enhancer = ImageEnhance.Color(golden)
                golden = enhancer.enhance(0.7)  # Desaturate
                image = Image.blend(image, golden, 0.3)
        
        # Always apply slight sharpening
        if hasattr(ImageFilter, 'UnsharpMask'):
            image = image.filter(UnsharpMask(radius=2, percent=150, threshold=3))
        
        return image
    
    def _generate_fallback_background(self, width: int, height: int) -> Image.Image:
        """Generate fallback background"""
        colors = [(40, 40, 60), (70, 70, 100), (100, 100, 150)]
        return self._create_gradient(width, height, colors)

# ==================== PREMIUM PROFILE GENERATOR ====================
class PremiumProfileGenerator:
    """Generates Ultra Premium Profile Pictures"""
    
    def __init__(self, config: UltraConfig):
        self.config = config
        self.profile_cache = {}
        self.max_cache_size = 500
    
    def generate(self, user_profile: UserProfile, 
                 size: int = 400,
                 design: ProfileDesign = None) -> Image.Image:
        """Generate premium profile picture"""
        cache_key = f"{user_profile.id}_{size}_{design.name if design else 'default'}"
        
        if cache_key in self.profile_cache:
            return self.profile_cache[cache_key].copy()
        
        try:
            design = design or ProfileDesign.get_random()
            
            # Create base profile
            if design == ProfileDesign.GOLDEN_FRAME_3D:
                profile = self._create_golden_frame(user_profile, size)
            elif design == ProfileDesign.NEON_GLOW_CIRCLE:
                profile = self._create_neon_glow(user_profile, size)
            elif design == ProfileDesign.DIAMOND_CUT:
                profile = self._create_diamond_cut(user_profile, size)
            elif design == ProfileDesign.VIP_BADGE:
                profile = self._create_vip_badge(user_profile, size)
            elif design == ProfileDesign.PREMIUM_STAR:
                profile = self._create_premium_star(user_profile, size)
            elif design == ProfileDesign.FLOWER_MANDALA:
                profile = self._create_flower_mandala(user_profile, size)
            elif design == ProfileDesign.GEOMETRIC_ART:
                profile = self._create_geometric_art(user_profile, size)
            elif design == ProfileDesign.SPARKLE_AURA:
                profile = self._create_sparkle_aura(user_profile, size)
            elif design == ProfileDesign.HOLOGRAM_EFFECT:
                profile = self._create_hologram(user_profile, size)
            elif design == ProfileDesign.METAL_PLATE:
                profile = self._create_metal_plate(user_profile, size)
            elif design == ProfileDesign.GLASS_MORPH:
                profile = self._create_glass_morph(user_profile, size)
            else:
                profile = self._create_animated_border(user_profile, size)
            
            # Cache result
            if len(self.profile_cache) >= self.max_cache_size:
                self.profile_cache.pop(next(iter(self.profile_cache)))
            
            self.profile_cache[cache_key] = profile.copy()
            return profile
            
        except Exception as e:
            logger.error(f"Profile generation failed: {e}")
            return self._create_fallback_profile(user_profile, size)
    
    def _create_golden_frame(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create golden frame profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Base gradient circle
        center = size // 2
        base_radius = size // 2 - 20
        
        # Multi-layer gradient
        colors = [
            (255, 215, 0),   # Gold
            (255, 140, 0),   # Dark Orange
            (218, 165, 32),  # Golden Rod
            (184, 134, 11)   # Dark Golden Rod
        ]
        
        for i, color in enumerate(colors):
            radius = base_radius - (i * 15)
            if radius > 0:
                alpha = 255 - (i * 40)
                draw.ellipse([center - radius, center - radius,
                             center + radius, center + radius],
                            fill=(*color, alpha))
        
        # Add user initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Text with shadow
        draw.text((position[0] + 3, position[1] + 3), initial,
                 font=font, fill=(0, 0, 0, 150))
        draw.text(position, initial, font=font, fill=(255, 255, 255, 255))
        
        # Golden frame
        frame_thickness = 15
        for i in range(3):
            offset = 5 + i * 5
            thickness = frame_thickness - i * 3
            alpha = 200 - i * 50
            
            draw.ellipse([offset, offset, size - offset, size - offset],
                        outline=(255, 215, 0, alpha), width=thickness)
        
        return profile
    
    def _create_neon_glow(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create neon glow profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        base_radius = size // 2 - 30
        
        # Neon colors
        neon_colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
        color = neon_colors[hash(user_profile.username) % len(neon_colors)]
        
        # Glow effect
        for i in range(5):
            radius = base_radius + i * 10
            alpha = 100 - i * 20
            draw.ellipse([center - radius, center - radius,
                         center + radius, center + radius],
                        outline=(*color, alpha), width=5)
        
        # Base circle
        draw.ellipse([center - base_radius, center - base_radius,
                     center + base_radius, center + base_radius],
                    fill=(*color, 200))
        
        # User initial with glow
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 2
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Neon text glow
        for i in range(3):
            offset = i + 1
            draw.text((position[0] + offset, position[1] + offset), initial,
                     font=font, fill=(*color, 100))
        
        draw.text(position, initial, font=font, fill=(255, 255, 255, 255))
        
        return profile
    
    def _create_vip_badge(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create VIP badge profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # VIP Crown background
        center = size // 2
        crown_radius = size // 2 - 20
        
        # Crown base (gold)
        draw.ellipse([center - crown_radius, center - crown_radius,
                     center + crown_radius, center + crown_radius],
                    fill=(255, 215, 0, 200))
        
        # Crown points
        points = []
        for i in range(5):
            angle = math.pi * 2 * i / 5 - math.pi / 2
            x = center + crown_radius * 0.7 * math.cos(angle)
            y = center + crown_radius * 0.7 * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            draw.polygon(points, fill=(255, 255, 0, 150), 
                        outline=(255, 140, 0, 200))
        
        # VIP Text
        try:
            font_size = size // 4
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        vip_text = "VIP"
        bbox = draw.textbbox((0, 0), vip_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, vip_text, font=font, fill=(255, 0, 0, 255))
        
        # User initial at bottom
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            initial_font_size = size // 6
            initial_font = ImageFont.truetype("arial.ttf", initial_font_size)
        except:
            initial_font = ImageFont.load_default()
        
        initial_bbox = draw.textbbox((0, 0), initial, font=initial_font)
        initial_width = initial_bbox[2] - initial_bbox[0]
        initial_position = ((size - initial_width) // 2, size * 3 // 4)
        
        draw.text(initial_position, initial, font=initial_font, 
                 fill=(255, 255, 255, 255))
        
        return profile
    
    def _create_premium_star(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create premium star profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        star_radius = size // 2 - 30
        
        # Create star
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            radius = star_radius if i % 2 == 0 else star_radius // 2
            points.append((
                center + radius * math.cos(angle - math.pi/2),
                center + radius * math.sin(angle - math.pi/2)
            ))
        
        if len(points) >= 3:
            draw.polygon(points, fill=(138, 43, 226, 200),  # Blue Violet
                        outline=(75, 0, 130, 255))  # Indigo
        
        # User initial in center
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 4
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, initial, font=font, fill=(255, 255, 255, 255))
        
        # Sparkle effects
        for _ in range(20):
            x = random.randint(0, size)
            y = random.randint(0, size)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2],
                        fill=(255, 255, 255, 100))
        
        return profile
    
    def _create_flower_mandala(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create flower mandala profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        max_radius = size // 2 - 20
        
        # Flower petals
        petal_colors = [(255, 105, 180), (255, 20, 147), (255, 182, 193)]
        
        for petal in range(8):
            for layer in range(3):
                radius = max_radius - layer * 20
                if radius <= 0:
                    continue
                
                # Create petal shape
                points = []
                for i in range(5):
                    angle = math.pi * 2 * (petal + i/10) / 8
                    petal_radius = radius * (0.3 + 0.7 * abs(math.sin(i * math.pi / 4)))
                    points.append((
                        center + petal_radius * math.cos(angle),
                        center + petal_radius * math.sin(angle)
                    ))
                
                if len(points) >= 3:
                    color = petal_colors[layer % len(petal_colors)]
                    alpha = 200 - layer * 50
                    draw.polygon(points, fill=(*color, alpha))
        
        # Center circle
        draw.ellipse([center - 40, center - 40, center + 40, center + 40],
                    fill=(255, 255, 255, 200))
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 6
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, initial, font=font, fill=(0, 0, 0, 255))
        
        return profile
    
    def _create_geometric_art(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create geometric art profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Hexagon pattern
        center = size // 2
        hex_radius = size // 3
        
        # Draw hexagon
        points = []
        for i in range(6):
            angle = math.pi * i / 3
            points.append((
                center + hex_radius * math.cos(angle),
                center + hex_radius * math.sin(angle)
            ))
        
        if len(points) >= 3:
            draw.polygon(points, fill=(70, 130, 180, 200),  # Steel Blue
                        outline=(30, 144, 255, 255))  # Dodger Blue
        
        # Inner shapes
        for i in range(3):
            inner_radius = hex_radius - 40 - i * 30
            if inner_radius <= 0:
                continue
            
            # Triangle
            tri_points = []
            for j in range(3):
                angle = math.pi * 2 * j / 3 + math.pi/6
                tri_points.append((
                    center + inner_radius * math.cos(angle),
                    center + inner_radius * math.sin(angle)
                ))
            
            if len(tri_points) >= 3:
                color = (255, 140 + i * 30, 0, 150 - i * 30)
                draw.polygon(tri_points, fill=color)
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 5
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, initial, font=font, fill=(255, 255, 255, 255))
        
        return profile
    
    def _create_sparkle_aura(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create sparkle aura profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        base_radius = size // 2 - 40
        
        # Aura effect
        aura_colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
        
        for i in range(5):
            radius = base_radius + i * 15
            color = aura_colors[i % len(aura_colors)]
            alpha = 80 - i * 15
            
            # Draw aura rings
            for j in range(8):
                angle = math.pi * 2 * j / 8
                x = center + radius * math.cos(angle)
                y = center + radius * math.sin(angle)
                
                draw.ellipse([x - 10, y - 10, x + 10, y + 10],
                            fill=(*color, alpha))
        
        # Center circle
        draw.ellipse([center - base_radius, center - base_radius,
                     center + base_radius, center + base_radius],
                    fill=(255, 255, 255, 150))
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Text glow
        for i in range(3):
            offset = i + 1
            draw.text((position[0] + offset, position[1] + offset), initial,
                     font=font, fill=(255, 255, 255, 50))
        
        draw.text(position, initial, font=font, fill=(0, 0, 0, 255))
        
        # Sparkles
        for _ in range(50):
            angle = random.random() * 2 * math.pi
            distance = random.randint(base_radius + 20, base_radius + 60)
            x = center + distance * math.cos(angle)
            y = center + distance * math.sin(angle)
            
            sparkle_size = random.randint(2, 4)
            draw.ellipse([x - sparkle_size, y - sparkle_size,
                         x + sparkle_size, y + sparkle_size],
                        fill=(255, 255, 255, random.randint(100, 200)))
        
        return profile
    
    def _create_hologram(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create hologram effect profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        base_radius = size // 2 - 30
        
        # Holographic colors
        hologram_colors = [
            (0, 255, 255, 100),   # Cyan
            (255, 0, 255, 100),   # Magenta
            (255, 255, 0, 100),   # Yellow
            (0, 255, 0, 100)      # Green
        ]
        
        # Create holographic rings
        for i in range(6):
            radius = base_radius - i * 15
            if radius <= 0:
                continue
            
            color = hologram_colors[i % len(hologram_colors)]
            
            # Draw segmented ring
            for segment in range(8):
                start_angle = math.pi * 2 * segment / 8
                end_angle = math.pi * 2 * (segment + 0.7) / 8
                
                # Draw arc
                points = []
                steps = 20
                for step in range(steps + 1):
                    angle = start_angle + (end_angle - start_angle) * step / steps
                    points.append((
                        center + radius * math.cos(angle),
                        center + radius * math.sin(angle)
                    ))
                
                # Draw thickness
                inner_points = []
                for point in reversed(points):
                    inner_radius = radius * 0.8
                    angle = math.atan2(point[1] - center, point[0] - center)
                    inner_points.append((
                        center + inner_radius * math.cos(angle),
                        center + inner_radius * math.sin(angle)
                    ))
                
                all_points = points + inner_points
                if len(all_points) >= 3:
                    draw.polygon(all_points, fill=color)
        
        # Center with user initial
        draw.ellipse([center - 50, center - 50, center + 50, center + 50],
                    fill=(255, 255, 255, 150))
        
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 5
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Holographic text
        for i in range(3):
            offset = i * 2
            color = hologram_colors[i % len(hologram_colors)]
            draw.text((position[0] + offset, position[1] + offset), initial,
                     font=font, fill=color)
        
        return profile
    
    def _create_metal_plate(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create metal plate profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        # Metal texture
        center = size // 2
        plate_radius = size // 2 - 20
        
        # Metal gradient
        metal_colors = [
            (192, 192, 192),  # Silver
            (169, 169, 169),  # Dark Gray
            (128, 128, 128),  # Gray
            (105, 105, 105)   # Dim Gray
        ]
        
        for i, color in enumerate(metal_colors):
            radius = plate_radius - i * 10
            if radius <= 0:
                continue
            
            draw.ellipse([center - radius, center - radius,
                         center + radius, center + radius],
                        fill=(*color, 200))
        
        # Bolts/screws
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x = center + (plate_radius - 15) * math.cos(rad)
            y = center + (plate_radius - 15) * math.sin(rad)
            
            # Screw head
            draw.ellipse([x - 8, y - 8, x + 8, y + 8],
                        fill=(0, 0, 0, 150))
            draw.line([x - 4, y, x + 4, y], fill=(255, 255, 255, 200), width=2)
            draw.line([x, y - 4, x, y + 4], fill=(255, 255, 255, 200), width=2)
        
        # User initial engraved
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Engraved effect (shadow offset)
        draw.text((position[0] + 3, position[1] + 3), initial,
                 font=font, fill=(0, 0, 0, 100))
        draw.text(position, initial, font=font, fill=(255, 255, 255, 200))
        
        return profile
    
    def _create_glass_morph(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create glass morphism profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        glass_radius = size // 2 - 30
        
        # Glass effect with gradient
        for i in range(5):
            radius = glass_radius - i * 10
            if radius <= 0:
                continue
            
            # Glass color (semi-transparent blue)
            color = (135, 206, 235, 100 - i * 15)  # Sky Blue
            
            # Draw glass circle
            draw.ellipse([center - radius, center - radius,
                         center + radius, center + radius],
                        fill=color)
        
        # Glass reflection
        reflection_height = size // 3
        for y in range(reflection_height):
            alpha = int(100 * (1 - y / reflection_height))
            draw.ellipse([center - glass_radius, y,
                         center + glass_radius, y + 10],
                        fill=(255, 255, 255, alpha))
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Text with glass effect
        draw.text((position[0] + 2, position[1] + 2), initial,
                 font=font, fill=(255, 255, 255, 100))
        draw.text(position, initial, font=font, fill=(255, 255, 255, 200))
        
        # Glass border
        draw.ellipse([10, 10, size - 10, size - 10],
                    outline=(255, 255, 255, 100), width=5)
        
        return profile
    
    def _create_animated_border(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create animated border profile (static preview)"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        base_radius = size // 2 - 25
        
        # Colorful border segments
        segment_colors = [
            (255, 0, 0),    # Red
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (238, 130, 238) # Violet
        ]
        
        # Draw color segments
        num_segments = len(segment_colors)
        for i, color in enumerate(segment_colors):
            start_angle = math.pi * 2 * i / num_segments
            end_angle = math.pi * 2 * (i + 0.9) / num_segments
            
            # Draw segment
            points = []
            steps = 20
            for step in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * step / steps
                points.append((
                    center + base_radius * math.cos(angle),
                    center + base_radius * math.sin(angle)
                ))
            
            # Inner points
            inner_points = []
            for point in reversed(points):
                inner_radius = base_radius * 0.7
                angle = math.atan2(point[1] - center, point[0] - center)
                inner_points.append((
                    center + inner_radius * math.cos(angle),
                    center + inner_radius * math.sin(angle)
                ))
            
            all_points = points + inner_points
            if len(all_points) >= 3:
                draw.polygon(all_points, fill=(*color, 150))
        
        # Center circle
        draw.ellipse([center - 60, center - 60, center + 60, center + 60],
                    fill=(255, 255, 255, 200))
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 4
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, initial, font=font, fill=(0, 0, 0, 255))
        
        return profile
    
    def _create_fallback_profile(self, user_profile: UserProfile, size: int) -> Image.Image:
        """Create fallback profile"""
        profile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(profile)
        
        center = size // 2
        radius = size // 2 - 10
        
        # Simple circle
        draw.ellipse([center - radius, center - radius,
                     center + radius, center + radius],
                    fill=(*user_profile.profile_color, 200))
        
        # User initial
        initial = user_profile.display_name[0].upper() if user_profile.display_name else 'U'
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, initial, font=font, fill=(255, 255, 255, 255))
        
        return profile

# ==================== ULTRA TEXT RENDERER ====================
class UltraTextRenderer:
    """Renders Premium Text with Effects"""
    
    def __init__(self):
        self.font_cache = {}
    
    def render_text(self, image: Image.Image, text: str, 
                   user_profile: UserProfile,
                   style: UltraStyle) -> Image.Image:
        """Render premium text on image"""
        if not text:
            return image
        
        # Create text layer
        text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Get appropriate font
        font_size = self._calculate_font_size(image.width, len(text))
        font = self._get_font(font_size, style)
        
        # Wrap text
        max_chars_per_line = self._get_max_chars(image.width, font_size)
        lines = self._wrap_text(text, max_chars_per_line)
        
        # Calculate text position
        total_height = len(lines) * font_size * 1.5
        start_y = (image.height - total_height) // 3
        
        # Text color based on style
        text_color = self._get_text_color(style)
        shadow_color = self._get_shadow_color(text_color)
        
        # Render each line
        for i, line in enumerate(lines):
            y_pos = start_y + i * font_size * 1.5
            
            # Center text
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x_pos = (image.width - line_width) // 2
            
            # Apply text effects
            self._apply_text_effects(draw, line, font, (x_pos, y_pos), 
                                   text_color, shadow_color, style)
        
        # Add user badge if available
        badge_text = user_profile.get_badge_text()
        if badge_text:
            self._render_badge(draw, badge_text, image.size, font_size // 2)
        
        # Composite text layer
        result = Image.alpha_composite(image.convert('RGBA'), text_layer)
        
        # Apply global text effects
        result = self._apply_global_effects(result, style)
        
        return result
    
    def _calculate_font_size(self, image_width: int, text_length: int) -> int:
        """Calculate optimal font size"""
        base_size = max(40, image_width // 20)
        
        # Adjust based on text length
        if text_length > 100:
            return max(30, base_size - 10)
        elif text_length > 50:
            return max(35, base_size - 5)
        else:
            return base_size
    
    def _get_font(self, size: int, style: UltraStyle):
        """Get appropriate font"""
        cache_key = f"{size}_{style.name}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        try:
            # Try different fonts based on style
            if style in [UltraStyle.BENGALI_ROYAL, UltraStyle.ISLAMIC_GOLD]:
                # Try Bengali/Arabic fonts
                font_paths = [
                    "arial.ttf",
                    "times.ttf",
                    "/system/fonts/DroidSans.ttf"
                ]
            elif style in [UltraStyle.NEON_CYBERPUNK, UltraStyle.DARK_FUTURISTIC]:
                # Modern fonts
                font_paths = ["arial.ttf", "verdana.ttf"]
            else:
                # Elegant fonts
                font_paths = ["times.ttf", "georgia.ttf", "arial.ttf"]
            
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, size)
                    self.font_cache[cache_key] = font
                    return font
                except:
                    continue
            
            # Fallback to default
            font = ImageFont.load_default()
            self.font_cache[cache_key] = font
            return font
            
        except Exception as e:
            logger.warning(f"Font loading failed: {e}")
            return ImageFont.load_default()
    
    def _get_max_chars(self, image_width: int, font_size: int) -> int:
        """Calculate maximum characters per line"""
        # Approximate character width
        char_width = font_size * 0.6
        return max(20, int(image_width / char_width))
    
    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Wrap text into lines"""
        if len(text) <= max_chars:
            return [text]
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length <= max_chars:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _get_text_color(self, style: UltraStyle) -> Tuple[int, int, int, int]:
        """Get text color based on style"""
        if style == UltraStyle.GOLDEN_LUXURY:
            return (255, 215, 0, 255)  # Gold
        elif style == UltraStyle.NEON_CYBERPUNK:
            return (0, 255, 255, 255)  # Cyan
        elif style == UltraStyle.BENGALI_ROYAL:
            return (255, 255, 255, 255)  # White
        elif style == UltraStyle.ISLAMIC_GOLD:
            return (218, 165, 32, 255)  # Golden Rod
        elif style == UltraStyle.SPACE_GALAXY:
            return (255, 255, 255, 255)  # White
        else:
            return (255, 255, 255, 255)  # Default white
    
    def _get_shadow_color(self, text_color: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """Get shadow color from text color"""
        r, g, b, a = text_color
        return (max(0, r - 50), max(0, g - 50), max(0, b - 50), a)
    
    def _apply_text_effects(self, draw: ImageDraw.Draw, text: str, font,
                           position: Tuple[int, int], 
                           text_color: Tuple[int, int, int, int],
                           shadow_color: Tuple[int, int, int, int],
                           style: UltraStyle):
        """Apply text effects"""
        x, y = position
        
        # Shadow effect
        if style != UltraStyle.GLASS_MORPHISM_3D:
            # Draw shadow
            shadow_offset = 3
            draw.text((x + shadow_offset, y + shadow_offset), 
                     text, font=font, fill=shadow_color)
        
        # Glow effect for neon styles
        if style == UltraStyle.NEON_CYBERPUNK:
            for i in range(3):
                offset = i + 1
                glow_color = (*text_color[:3], 100 - i * 30)
                draw.text((x + offset, y + offset), 
                         text, font=font, fill=glow_color)
        
        # Main text
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Outline for certain styles
        if style in [UltraStyle.GOLDEN_LUXURY, UltraStyle.BENGALI_ROYAL]:
            outline_color = (0, 0, 0, 150)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), 
                                 text, font=font, fill=outline_color)
    
    def _render_badge(self, draw: ImageDraw.Draw, badge_text: str,
                     image_size: Tuple[int, int], font_size: int):
        """Render user badge"""
        width, height = image_size
        
        # Get font for badge
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate badge position (top center)
        bbox = draw.textbbox((0, 0), badge_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x_pos = (width - text_width) // 2
        y_pos = height // 8  # Top area
        
        # Badge background
        padding = 10
        draw.rounded_rectangle([
            x_pos - padding, y_pos - padding,
            x_pos + text_width + padding, y_pos + text_height + padding
        ], radius=15, fill=(0, 0, 0, 150))
        
        # Badge text
        draw.text((x_pos, y_pos), badge_text, font=font, 
                 fill=(255, 215, 0, 255))  # Gold text
    
    def _apply_global_effects(self, image: Image.Image, 
                            style: UltraStyle) -> Image.Image:
        """Apply global text effects"""
        if style == UltraStyle.NEON_CYBERPUNK:
            # Add glow to text areas
            alpha = image.split()[3]
            
            # Create glow layer
            glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow)
            
            # Find text areas from alpha channel
            text_mask = alpha.point(lambda x: 255 if x > 50 else 0)
            
            # Apply glow color
            glow_color = (0, 255, 255, 50)  # Cyan glow
            glow.paste(glow_color, (0, 0), text_mask)
            
            # Blur glow
            glow = glow.filter(GaussianBlur(radius=5))
            
            # Composite
            image = Image.alpha_composite(glow, image)
        
        return image

# ==================== MAIN GENERATOR ====================
class UltraPremiumGenerator:
    """Main Ultra Premium Image Generator"""
    
    def __init__(self, config: Optional[UltraConfig] = None):
        if not PIL_AVAILABLE:
            raise ImportError("PIL/Pillow is required. Install: pip install pillow")
        
        self.config = config or UltraConfig()
        
        # Initialize managers
        self.background_gen = PremiumBackgroundGenerator(self.config)
        self.profile_gen = PremiumProfileGenerator(self.config)
        self.text_renderer = UltraTextRenderer()
        
        # Statistics
        self.stats = {
            'total_generated': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0
        }
        
        logger.info("🚀 Ultra Premium Generator v12.0 Initialized")
        logger.info(f"   • Resolution: {self.config.custom_width}x{self.config.custom_height}")
        logger.info(f"   • Quality: {self.config.quality}%")
        logger.info(f"   • Features: HD Backgrounds: {self.config.enable_hd_backgrounds}")
        logger.info(f"   • Features: Premium Profiles: {self.config.enable_dynamic_profiles}")
    
    def generate_roast_image(self, roast_text: str, user_info: Dict,
                            mentioned_user: Optional[Dict] = None,
                            style: UltraStyle = None) -> Dict:
        """Generate ultra premium roast image"""
        start_time = time.time()
        
        try:
            # Process user info
            main_user = self._create_user_profile(user_info)
            mentioned_profile = None
            if mentioned_user:
                mentioned_profile = self._create_user_profile(mentioned_user)
            
            # Select style
            style = style or UltraStyle.get_random()
            
            # Generate background
            background = self.background_gen.generate(
                self.config.custom_width, 
                self.config.custom_height, 
                style
            )
            
            # Add profile pictures
            if self.config.enable_dynamic_profiles:
                background = self._add_profile_pictures(
                    background, main_user, mentioned_profile, style
                )
            
            # Add text
            if roast_text:
                background = self.text_renderer.render_text(
                    background, roast_text, main_user, style
                )
            
            # Add watermark
            if self.config.enable_watermark:
                background = self._add_watermark(background)
            
            # Save image
            output_path = self._save_image(background, main_user)
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['total_generated'] += 1
            self.stats['successful'] += 1
            self.stats['total_time'] += processing_time
            
            logger.info(f"✅ Ultra Premium Image Generated: {output_path}")
            logger.info(f"   • Processing Time: {processing_time:.2f}s")
            logger.info(f"   • Style: {style.name}")
            logger.info(f"   • User: {main_user.display_name}")
            
            return {
                'success': True,
                'image_path': str(output_path),
                'processing_time': processing_time,
                'style': style.name,
                'user': main_user.display_name,
                'resolution': f"{self.config.custom_width}x{self.config.custom_height}"
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.stats['total_generated'] += 1
            self.stats['failed'] += 1
            self.stats['total_time'] += processing_time
            
            logger.error(f"❌ Image generation failed: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'processing_time': processing_time
            }
    
    def _create_user_profile(self, user_info: Dict) -> UserProfile:
        """Create UserProfile from dict"""
        return UserProfile(
            id=user_info.get('id', random.randint(1000, 9999)),
            username=user_info.get('username', 'User'),
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            rating=user_info.get('rating', random.uniform(5.0, 9.9)),
            level=user_info.get('level', random.randint(1, 100)),
            rank=user_info.get('rank', 'Member'),
            is_premium=user_info.get('is_premium', False),
            is_vip=user_info.get('is_vip', False),
            is_admin=user_info.get('is_admin', False),
            badges=user_info.get('badges', [])
        )
    
    def _add_profile_pictures(self, image: Image.Image, 
                             main_user: UserProfile,
                             mentioned_user: Optional[UserProfile],
                             style: UltraStyle) -> Image.Image:
        """Add profile pictures to image"""
        width, height = image.size
        
        # Main user profile (top right)
        main_profile_size = min(width, height) // 6
        main_profile = self.profile_gen.generate(
            main_user, main_profile_size, ProfileDesign.get_random()
        )
        
        # Position main profile
        main_x = width - main_profile_size - 50
        main_y = 50
        
        # Create mask for circular profile
        mask = Image.new('L', (main_profile_size, main_profile_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, main_profile_size, main_profile_size], fill=255)
        
        # Paste main profile
        image.paste(main_profile, (main_x, main_y), mask)
        
        # Mentioned user profile (top left)
        if mentioned_user:
            mentioned_size = main_profile_size - 20
            mentioned_profile = self.profile_gen.generate(
                mentioned_user, mentioned_size, ProfileDesign.get_random()
            )
            
            mentioned_x = 50
            mentioned_y = 50
            
            # Create mask for mentioned profile
            mentioned_mask = Image.new('L', (mentioned_size, mentioned_size), 0)
            mentioned_mask_draw = ImageDraw.Draw(mentioned_mask)
            mentioned_mask_draw.ellipse([0, 0, mentioned_size, mentioned_size], fill=255)
            
            # Paste mentioned profile
            image.paste(mentioned_profile, (mentioned_x, mentioned_y), mentioned_mask)
            
            # Draw connection line if both profiles exist
            draw = ImageDraw.Draw(image.convert('RGBA'))
            draw.line([(mentioned_x + mentioned_size // 2, mentioned_y + mentioned_size // 2),
                      (main_x + main_profile_size // 2, main_y + main_profile_size // 2)],
                     fill=(255, 255, 255, 100), width=3)
        
        return image
    
    def _add_watermark(self, image: Image.Image) -> Image.Image:
        """Add watermark to image"""
        draw = ImageDraw.Draw(image.convert('RGBA'))
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        watermark = f"{self.config.watermark_text} • {datetime.now().strftime('%Y-%m-%d')}"
        
        bbox = draw.textbbox((0, 0), watermark, font=font)
        text_width = bbox[2] - bbox[0]
        
        position = (image.width - text_width - 20, image.height - 40)
        
        # Semi-transparent background for watermark
        padding = 5
        draw.rectangle([
            position[0] - padding, position[1] - padding,
            position[0] + text_width + padding, position[1] + (bbox[3] - bbox[1]) + padding
        ], fill=(0, 0, 0, 100))
        
        # Watermark text
        draw.text(position, watermark, font=font, fill=(255, 255, 255, 150))
        
        return image
    
    def _save_image(self, image: Image.Image, user: UserProfile) -> Path:
        """Save image to file"""
        timestamp = int(time.time())
        filename = f"ultra_premium_{timestamp}_{user.id}_{user.username}.png"
        output_path = Path(self.config.output_dir) / filename
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with high quality settings
        save_params = {
            'quality': self.config.quality,
            'optimize': True,
            'compress_level': self.config.compression_level
        }
        
        # Convert to RGB if saving as JPEG
        if self.config.format == 'JPEG' and image.mode == 'RGBA':
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            image = rgb_image
        
        image.save(output_path, self.config.format, **save_params)
        
        return output_path
    
    def get_stats(self) -> Dict:
        """Get generator statistics"""
        avg_time = 0
        if self.stats['total_generated'] > 0:
            avg_time = self.stats['total_time'] / self.stats['total_generated']
        
        success_rate = 0
        if self.stats['total_generated'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_generated']) * 100
        
        return {
            'total_generated': self.stats['total_generated'],
            'successful': self.stats['successful'],
            'failed': self.stats['failed'],
            'success_rate': f"{success_rate:.1f}%",
            'average_time': f"{avg_time:.2f}s",
            'total_time': f"{self.stats['total_time']:.2f}s",
            'resolution': f"{self.config.custom_width}x{self.config.custom_height}"
        }
    
    def cleanup(self):
        """Cleanup old files"""
        try:
            output_dir = Path(self.config.output_dir)
            if output_dir.exists():
                # Keep only last 100 images
                images = list(output_dir.glob("*.png"))
                images.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for old_image in images[100:]:
                    old_image.unlink()
                
                logger.info(f"Cleanup: Kept {min(len(images), 100)} images")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

# ==================== EXAMPLE USAGE ====================
def example_usage():
    """Example usage of Ultra Premium Generator"""
    print("\n" + "="*60)
    print("🔥 ULTRA PREMIUM GENERATOR v12.0 - EXAMPLE")
    print("="*60)
    
    if not PIL_AVAILABLE:
        print("❌ PIL not available. Install: pip install pillow")
        return
    
    try:
        # Create configuration
        config = UltraConfig(
            resolution_preset="4K_PRO",
            enable_hd_backgrounds=True,
            enable_dynamic_profiles=True,
            enable_premium_effects=True,
            output_dir="./output/examples"
        )
        
        # Initialize generator
        generator = UltraPremiumGenerator(config)
        
        # Create test users
        test_user = {
            'id': 1001,
            'username': 'রানা',
            'first_name': 'রানা',
            'rating': 9.5,
            'level': 95,
            'is_vip': True,
            'is_premium': True
        }
        
        mentioned_user = {
            'id': 1002,
            'username': 'VIP_User',
            'first_name': 'ভিআইপি',
            'rating': 8.8,
            'level': 80,
            'is_premium': True
        }
        
        # Generate image
        roast_text = "🎯 এই রোস্টে আল্ট্রা প্রিমিয়াম কোয়ালিটি! " \
                    "এখন প্রতিটি ইমেজ হবে মাস্টারপিসের মতো সুন্দর! ✨"
        
        print("\n🔹 Generating Ultra Premium Image...")
        
        result = generator.generate_roast_image(
            roast_text=roast_text,
            user_info=test_user,
            mentioned_user=mentioned_user,
            style=UltraStyle.GOLDEN_LUXURY
        )
        
        if result['success']:
            print(f"\n✅ Image Generated Successfully!")
            print(f"   📁 Path: {result['image_path']}")
            print(f"   ⏱️ Time: {result['processing_time']:.2f}s")
            print(f"   🎨 Style: {result['style']}")
            print(f"   👤 User: {result['user']}")
            print(f"   📏 Resolution: {result['resolution']}")
            
            # Show statistics
            stats = generator.get_stats()
            print(f"\n📊 Statistics:")
            print(f"   • Total Generated: {stats['total_generated']}")
            print(f"   • Success Rate: {stats['success_rate']}")
            print(f"   • Average Time: {stats['average_time']}")
        else:
            print(f"\n❌ Generation Failed: {result['error']}")
        
        print("\n" + "="*60)
        print("🎉 Example Completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    example_usage()
