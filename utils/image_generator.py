#!/usr/bin/env python3
"""
Roastify Advanced Image Generator - Termux Compatible
Complete fixed version with all features
"""

import os
import sys
import random
import logging
import textwrap
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import PIL with fallback
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
    from PIL.Image import Resampling
    PIL_AVAILABLE = True
    logger.info("PIL/Pillow loaded successfully")
except ImportError as e:
    PIL_AVAILABLE = False
    logger.warning(f"PIL not available: {e}. Image generation disabled.")


class ImageConfig:
    """Configuration for image generation"""
    
    def __init__(self):
        self.width = 1080
        self.height = 1080
        self.quality = 90
        self.format = "PNG"
        self.enable_cache = True
        self.cache_dir = "./cache"
        self.output_dir = "./output"
        self.temp_dir = "./temp"
        
        # Create directories
        for dir_path in [self.cache_dir, self.output_dir, self.temp_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Color schemes
        self.color_schemes = {
            'dark': {
                'background': (20, 20, 40),
                'text': (255, 255, 255),
                'accent': (255, 105, 180),
                'border': (0, 255, 255),
                'shadow': (50, 50, 50)
            },
            'light': {
                'background': (255, 255, 255),
                'text': (30, 30, 30),
                'accent': (70, 130, 180),
                'border': (100, 100, 100),
                'shadow': (200, 200, 200)
            },
            'neon': {
                'background': (0, 0, 20),
                'text': (0, 255, 255),
                'accent': (255, 0, 255),
                'border': (255, 255, 0),
                'shadow': (0, 100, 100)
            },
            'vintage': {
                'background': (249, 245, 235),
                'text': (101, 67, 33),
                'accent': (188, 143, 143),
                'border': (139, 69, 19),
                'shadow': (160, 120, 90)
            }
        }


class FontManager:
    """Manage fonts with fallback system"""
    
    def __init__(self):
        self.fonts = {}
        self.default_font = None
        self._load_fonts()
    
    def _load_fonts(self):
        """Load available fonts"""
        if not PIL_AVAILABLE:
            return
        
        font_paths = []
        
        # Check common font locations
        possible_paths = [
            # Termux system fonts
            "/system/fonts",
            "/data/data/com.termux/files/usr/share/fonts",
            # Project fonts
            "./fonts",
            "./assets/fonts",
            # Current directory
            "."
        ]
        
        # Common font files to look for
        font_files = [
            "Roboto-Regular.ttf",
            "Roboto-Bold.ttf",
            "DroidSans.ttf",
            "DejaVuSans.ttf",
            "DejaVuSans-Bold.ttf",
            "arial.ttf",
            "Arial.ttf",
            "NotoSans-Regular.ttf",
            "NotoSansBengali-Regular.ttf"
        ]
        
        # Search for fonts
        for base_path in possible_paths:
            if os.path.exists(base_path):
                # Look for specific font files
                for font_file in font_files:
                    font_path = os.path.join(base_path, font_file)
                    if os.path.exists(font_path):
                        font_paths.append(font_path)
                
                # Also look for any .ttf files
                if os.path.isdir(base_path):
                    for file in os.listdir(base_path):
                        if file.lower().endswith(('.ttf', '.otf')):
                            font_paths.append(os.path.join(base_path, file))
        
        # Load fonts
        for font_path in font_paths:
            try:
                font_name = os.path.basename(font_path)
                # Test load with small size
                font = ImageFont.truetype(font_path, 10)
                self.fonts[font_name] = font_path
                logger.debug(f"Loaded font: {font_name}")
            except Exception as e:
                logger.debug(f"Could not load font {font_path}: {e}")
        
        # Set default font
        if self.fonts:
            self.default_font = list(self.fonts.values())[0]
        else:
            self.default_font = None
        
        logger.info(f"Loaded {len(self.fonts)} fonts")
    
    def get_font(self, size: int = 40, style: str = "regular") -> Optional[Any]:
        """Get font with specified size"""
        if not PIL_AVAILABLE:
            return None
        
        try:
            if self.default_font:
                return ImageFont.truetype(self.default_font, size)
            else:
                return ImageFont.load_default()
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            return ImageFont.load_default()
    
    def get_random_font(self, size: int = 40) -> Optional[Any]:
        """Get random font"""
        if not PIL_AVAILABLE or not self.fonts:
            return self.get_font(size)
        
        try:
            font_path = random.choice(list(self.fonts.values()))
            return ImageFont.truetype(font_path, size)
        except:
            return self.get_font(size)


class EffectManager:
    """Manage visual effects"""
    
    @staticmethod
    def add_shadow(draw: ImageDraw, text: str, font: ImageFont,
                   position: Tuple[int, int], color: Tuple[int, int, int],
                   shadow_color: Optional[Tuple[int, int, int]] = None,
                   offset: int = 3) -> None:
        """Add shadow to text"""
        x, y = position
        if shadow_color is None:
            shadow_color = (color[0]//3, color[1]//3, color[2]//3)
        
        draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
        draw.text(position, text, font=font, fill=color)
    
    @staticmethod
    def add_glow_effect(image: Image.Image, intensity: int = 2) -> Image.Image:
        """Add glow effect to image"""
        try:
            # Create blurred copy
            glow = image.copy()
            glow = glow.filter(ImageFilter.GaussianBlur(radius=intensity))
            
            # Composite with original
            result = Image.new('RGBA', image.size, (0, 0, 0, 0))
            result = Image.alpha_composite(result, glow)
            result = Image.alpha_composite(result, image)
            return result
        except Exception as e:
            logger.error(f"Error applying glow effect: {e}")
            return image
    
    @staticmethod
    def add_vignette(image: Image.Image, intensity: float = 0.7) -> Image.Image:
        """Add vignette effect"""
        try:
            width, height = image.size
            vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(vignette)
            
            # Draw radial gradient
            center_x, center_y = width // 2, height // 2
            max_radius = int((width**2 + height**2)**0.5 / 2)
            
            for i in range(0, max_radius, 50):
                radius = i
                alpha = int(255 * intensity * (i / max_radius))
                
                if radius > 0:
                    draw.ellipse(
                        [center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        fill=(0, 0, 0, alpha),
                        outline=None
                    )
            
            return Image.alpha_composite(image.convert('RGBA'), vignette)
        except Exception as e:
            logger.error(f"Error applying vignette: {e}")
            return image
    
    @staticmethod
    def create_gradient(width: int, height: int,
                       start_color: Tuple[int, int, int],
                       end_color: Tuple[int, int, int]) -> Image.Image:
        """Create gradient background"""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        # Vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return gradient


class BorderManager:
    """Manage border creation"""
    
    @staticmethod
    def create_border(width: int, height: int,
                     border_type: str = "simple",
                     color: Tuple[int, int, int] = (255, 255, 255),
                     thickness: int = 20) -> Image.Image:
        """Create border image"""
        border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        if border_type == "simple":
            # Simple rectangle border
            draw.rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                outline=color + (255,),
                width=thickness
            )
            
        elif border_type == "double":
            # Double border
            draw.rectangle(
                [thickness, thickness, width - thickness, height - thickness],
                outline=color + (255,),
                width=thickness // 2
            )
            draw.rectangle(
                [thickness * 2, thickness * 2,
                 width - thickness * 2, height - thickness * 2],
                outline=color + (200,),
                width=thickness // 3
            )
            
        elif border_type == "rounded":
            # Rounded corners
            radius = 40
            # Top line
            draw.line([radius, thickness, width - radius, thickness],
                     fill=color + (255,), width=thickness)
            # Bottom line
            draw.line([radius, height - thickness, width - radius, height - thickness],
                     fill=color + (255,), width=thickness)
            # Left line
            draw.line([thickness, radius, thickness, height - radius],
                     fill=color + (255,), width=thickness)
            # Right line
            draw.line([width - thickness, radius, width - thickness, height - radius],
                     fill=color + (255,), width=thickness)
            
            # Corners
            draw.arc([thickness, thickness, radius * 2, radius * 2],
                    180, 270, fill=color + (255,), width=thickness)
            draw.arc([width - radius * 2, thickness, width - thickness, radius * 2],
                    270, 360, fill=color + (255,), width=thickness)
            draw.arc([thickness, height - radius * 2, radius * 2, height - thickness],
                    90, 180, fill=color + (255,), width=thickness)
            draw.arc([width - radius * 2, height - radius * 2,
                     width - thickness, height - thickness],
                    0, 90, fill=color + (255,), width=thickness)
            
        elif border_type == "dotted":
            # Dotted border
            dot_spacing = 30
            dot_size = thickness // 2
            
            # Top
            for x in range(dot_spacing, width - dot_spacing, dot_spacing):
                draw.ellipse([x, thickness, x + dot_size, thickness + dot_size],
                            fill=color + (255,))
            
            # Bottom
            for x in range(dot_spacing, width - dot_spacing, dot_spacing):
                draw.ellipse([x, height - thickness - dot_size,
                             x + dot_size, height - thickness],
                            fill=color + (255,))
            
            # Left
            for y in range(dot_spacing, height - dot_spacing, dot_spacing):
                draw.ellipse([thickness, y, thickness + dot_size, y + dot_size],
                            fill=color + (255,))
            
            # Right
            for y in range(dot_spacing, height - dot_spacing, dot_spacing):
                draw.ellipse([width - thickness - dot_size, y,
                             width - thickness, y + dot_size],
                            fill=color + (255,))
        
        return border
    
    @staticmethod
    def get_random_border_type() -> str:
        """Get random border type"""
        border_types = ["simple", "double", "rounded", "dotted"]
        return random.choice(border_types)


class AdvancedImageGenerator:
    """Advanced Image Generator with all features"""
    
    def __init__(self, config: Optional[ImageConfig] = None):
        self.config = config or ImageConfig()
        self.font_manager = FontManager()
        self.effect_manager = EffectManager()
        self.border_manager = BorderManager()
        
        # Performance tracking
        self.stats = {
            'images_generated': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0
        }
        
        logger.info("Advanced Image Generator initialized")
    
    def _get_color_scheme(self, scheme_name: str = None) -> Dict[str, Tuple[int, int, int]]:
        """Get color scheme"""
        if scheme_name and scheme_name in self.config.color_schemes:
            return self.config.color_schemes[scheme_name]
        
        # Auto-select based on time
        current_hour = datetime.now().hour
        if 6 <= current_hour < 18:
            return self.config.color_schemes['light']
        else:
            return self.config.color_schemes['dark']
    
    def _wrap_text(self, text: str, max_width: int = 30) -> List[str]:
        """Wrap text to fit within max width"""
        return textwrap.wrap(text, width=max_width)
    
    def _calculate_text_position(self, lines: List[str], font: ImageFont,
                                total_height: int) -> Tuple[int, int]:
        """Calculate text position for centering"""
        # This is a simplified version - actual implementation would
        # calculate based on exact text dimensions
        return (self.config.width // 2, (self.config.height - total_height) // 2)
    
    def _save_to_cache(self, image_data: bytes, key: str) -> str:
        """Save image to cache and return filepath"""
        cache_dir = Path(self.config.cache_dir)
        cache_file = cache_dir / f"{key}.png"
        
        try:
            with open(cache_file, 'wb') as f:
                f.write(image_data)
            return str(cache_file)
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
            return ""
    
    def _get_from_cache(self, key: str) -> Optional[bytes]:
        """Get image from cache"""
        cache_file = Path(self.config.cache_dir) / f"{key}.png"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading from cache: {e}")
        
        return None
    
    def generate_roast_image(self, roast_text: str, user_info: Dict[str, Any],
                            style: str = "auto", with_border: bool = True) -> str:
        """
        Generate roast image
        
        Args:
            roast_text: The roast text to display
            user_info: Dictionary with user information
            style: Color scheme style
            with_border: Whether to add border
            
        Returns:
            Path to generated image file
        """
        start_time = datetime.now()
        
        if not PIL_AVAILABLE:
            logger.error("PIL not available. Cannot generate image.")
            self.stats['failed'] += 1
            return self._create_error_image("PIL/Pillow not installed")
        
        try:
            # Generate cache key
            cache_key = hashlib.md5(
                f"{roast_text}_{style}_{with_border}".encode()
            ).hexdigest()[:12]
            
            # Check cache
            if self.config.enable_cache:
                cached = self._get_from_cache(cache_key)
                if cached:
                    output_path = Path(self.config.output_dir) / f"roast_{cache_key}.png"
                    with open(output_path, 'wb') as f:
                        f.write(cached)
                    logger.info(f"Cache hit for image {cache_key}")
                    self.stats['successful'] += 1
                    return str(output_path)
            
            # Get color scheme
            colors = self._get_color_scheme(style)
            
            # Create background
            if random.choice([True, False]):
                # Solid background
                background = Image.new('RGB', (self.config.width, self.config.height),
                                     colors['background'])
            else:
                # Gradient background
                start_color = colors['background']
                end_color = tuple(max(0, c - 30) for c in start_color)
                background = self.effect_manager.create_gradient(
                    self.config.width, self.config.height,
                    start_color, end_color
                )
            
            # Convert to RGBA for effects
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # Get fonts
            font_large = self.font_manager.get_random_font(self.config.width // 18)
            font_medium = self.font_manager.get_font(self.config.width // 27)
            font_small = self.font_manager.get_font(self.config.width // 36)
            
            # Wrap roast text
            lines = self._wrap_text(roast_text, max_width=25)
            
            # Calculate positions
            line_height_large = self.config.height // 15
            total_text_height = len(lines) * line_height_large
            current_y = (self.config.height - total_text_height) // 3
            
            # Draw roast text with effects
            for line in lines:
                # Get text dimensions
                bbox = draw.textbbox((0, 0), line, font=font_large)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Center horizontally
                x_position = (self.config.width - text_width) // 2
                
                # Add shadow effect
                self.effect_manager.add_shadow(
                    draw, line, font_large,
                    (x_position, current_y),
                    colors['text'],
                    colors['shadow']
                )
                
                current_y += line_height_large
            
            # Add user information
            user_text = f"@{user_info.get('username', 'user')}"
            if 'rating' in user_info:
                user_text += f" | Rating: {user_info['rating']}/10"
            
            bbox = draw.textbbox((0, 0), user_text, font=font_small)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2,
                 self.config.height - 150),
                user_text,
                font=font_small,
                fill=colors['accent']
            )
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bbox = draw.textbbox((0, 0), timestamp, font=font_small)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2,
                 self.config.height - 100),
                timestamp,
                font=font_small,
                fill=colors['timestamp']
            )
            
            # Add bot signature
            signature = "Roastify Pro 🔥"
            bbox = draw.textbbox((0, 0), signature, font=font_small)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2,
                 self.config.height - 50),
                signature,
                font=font_small,
                fill=colors['accent']
            )
            
            # Apply effects
            if random.choice([True, False]):
                image = self.effect_manager.add_glow_effect(image, intensity=1)
            
            if random.choice([True, False]):
                image = self.effect_manager.add_vignette(image, intensity=0.3)
            
            # Add border
            if with_border:
                border_type = self.border_manager.get_random_border_type()
                border = self.border_manager.create_border(
                    self.config.width, self.config.height,
                    border_type, colors['border'],
                    thickness=15
                )
                image = Image.alpha_composite(image, border)
            
            # Convert back to RGB for saving
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, colors['background'])
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            
            # Save image
            output_path = Path(self.config.output_dir) / f"roast_{int(datetime.now().timestamp())}.png"
            
            # Convert to bytes for cache
            img_byte_arr = self._image_to_bytes(image)
            
            # Save to file
            with open(output_path, 'wb') as f:
                f.write(img_byte_arr)
            
            # Cache the image
            if self.config.enable_cache:
                self._save_to_cache(img_byte_arr, cache_key)
            
            # Update stats
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.stats['images_generated'] += 1
            self.stats['successful'] += 1
            self.stats['total_time'] += duration
            
            logger.info(f"Image generated: {output_path} (took {duration:.2f}s)")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating roast image: {e}", exc_info=True)
            self.stats['failed'] += 1
            return self._create_error_image(str(e))
    
    def generate_welcome_image(self, user_info: Dict[str, Any],
                              welcome_message: str = "Welcome to Roastify!") -> str:
        """Generate welcome image for new users"""
        if not PIL_AVAILABLE:
            return self._create_error_image("Image generation disabled")
        
        try:
            colors = self.config.color_schemes['neon']
            
            # Create festive background
            background = self.effect_manager.create_gradient(
                self.config.width, self.config.height,
                (30, 10, 50),  # Dark purple
                (70, 30, 90)   # Lighter purple
            )
            
            image = background.convert('RGBA')
            draw = ImageDraw.Draw(image)
            
            # Get fonts
            font_title = self.font_manager.get_random_font(self.config.width // 10)
            font_welcome = self.font_manager.get_font(self.config.width // 20)
            font_user = self.font_manager.get_font(self.config.width // 25)
            font_info = self.font_manager.get_font(self.config.width // 30)
            
            # Draw title
            title = "🎉 WELCOME 🎉"
            bbox = draw.textbbox((0, 0), title, font=font_title)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 100),
                title,
                font=font_title,
                fill=(255, 215, 0)  # Gold color
            )
            
            # Draw welcome message
            bbox = draw.textbbox((0, 0), welcome_message, font=font_welcome)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 250),
                welcome_message,
                font=font_welcome,
                fill=colors['text']
            )
            
            # Draw user info
            user_line = f"@{user_info.get('username', 'New User')}"
            if 'first_name' in user_info:
                user_line = f"{user_info['first_name']} ({user_line})"
            
            bbox = draw.textbbox((0, 0), user_line, font=font_user)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 350),
                user_line,
                font=font_user,
                fill=colors['accent']
            )
            
            # Draw member count if available
            if 'member_count' in user_info:
                member_text = f"Member #{user_info['member_count']}"
                bbox = draw.textbbox((0, 0), member_text, font=font_info)
                text_width = bbox[2] - bbox[0]
                draw.text(
                    ((self.config.width - text_width) // 2, 450),
                    member_text,
                    font=font_info,
                    fill=(150, 255, 150)  # Light green
                )
            
            # Draw instructions
            instructions = [
                "Use /roast to get roasted 🔥",
                "Use /rate to rate others ⭐",
                "Use /help for more commands ℹ️"
            ]
            
            current_y = 550
            for instruction in instructions:
                bbox = draw.textbbox((0, 0), instruction, font=font_info)
                text_width = bbox[2] - bbox[0]
                draw.text(
                    ((self.config.width - text_width) // 2, current_y),
                    instruction,
                    font=font_info,
                    fill=(200, 200, 255)  # Light blue
                )
                current_y += 60
            
            # Add decorative border
            border = self.border_manager.create_border(
                self.config.width, self.config.height,
                "rounded", (255, 215, 0),  # Gold border
                thickness=25
            )
            image = Image.alpha_composite(image, border)
            
            # Add celebration emojis
            emojis = ["🎊", "🎈", "🥳", "👏", "✨"]
            for i in range(8):
                emoji = random.choice(emojis)
                font_emoji = self.font_manager.get_font(80)
                bbox = draw.textbbox((0, 0), emoji, font=font_emoji)
                text_width = bbox[2] - bbox[0]
                
                x = random.randint(100, self.config.width - 100 - text_width)
                y = random.randint(500, self.config.height - 150)
                
                draw.text((x, y), emoji, font=font_emoji, fill=(255, 255, 255, 180))
            
            # Convert and save
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, colors['background'])
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            
            output_path = Path(self.config.output_dir) / f"welcome_{int(datetime.now().timestamp())}.png"
            image.save(output_path, 'PNG', quality=self.config.quality)
            
            logger.info(f"Welcome image generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating welcome image: {e}")
            return self._create_error_image("Welcome image error")
    
    def generate_achievement_image(self, user_info: Dict[str, Any],
                                  achievement: Dict[str, Any]) -> str:
        """Generate achievement/unlock image"""
        if not PIL_AVAILABLE:
            return self._create_error_image("Image generation disabled")
        
        try:
            colors = self.config.color_schemes['vintage']
            
            # Create background
            background = Image.new('RGB', (self.config.width, self.config.height),
                                 colors['background'])
            
            # Add texture
            texture = Image.new('RGBA', (self.config.width, self.config.height),
                              (0, 0, 0, 0))
            draw_texture = ImageDraw.Draw(texture)
            
            for _ in range(500):
                x = random.randint(0, self.config.width)
                y = random.randint(0, self.config.height)
                size = random.randint(1, 3)
                alpha = random.randint(10, 30)
                draw_texture.ellipse([x, y, x + size, y + size],
                                    fill=(101, 67, 33, alpha))
            
            background = Image.alpha_composite(background.convert('RGBA'), texture)
            
            image = background
            draw = ImageDraw.Draw(image)
            
            # Get fonts
            font_title = self.font_manager.get_random_font(self.config.width // 12)
            font_achievement = self.font_manager.get_font(self.config.width // 18)
            font_user = self.font_manager.get_font(self.config.width // 25)
            font_desc = self.font_manager.get_font(self.config.width // 30)
            
            # Draw achievement icon/emoji
            achievement_icon = achievement.get('icon', '🏆')
            font_icon = self.font_manager.get_font(120)
            bbox = draw.textbbox((0, 0), achievement_icon, font=font_icon)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 150),
                achievement_icon,
                font=font_icon,
                fill=(255, 215, 0)  # Gold
            )
            
            # Draw achievement title
            title = achievement.get('title', 'ACHIEVEMENT UNLOCKED!')
            bbox = draw.textbbox((0, 0), title, font=font_title)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 300),
                title,
                font=font_title,
                fill=colors['accent']
            )
            
            # Draw achievement name
            achievement_name = achievement.get('name', 'Unknown Achievement')
            bbox = draw.textbbox((0, 0), achievement_name, font=font_achievement)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, 400),
                achievement_name,
                font=font_achievement,
                fill=colors['text']
            )
            
            # Draw achievement description
            description = achievement.get('description', '')
            if description:
                wrapped_desc = self._wrap_text(description, 40)
                current_y = 480
                for line in wrapped_desc:
                    bbox = draw.textbbox((0, 0), line, font=font_desc)
                    text_width = bbox[2] - bbox[0]
                    draw.text(
                        ((self.config.width - text_width) // 2, current_y),
                        line,
                        font=font_desc,
                        fill=(150, 150, 150)
                    )
                    current_y += 40
            
            # Draw user info
            user_text = f"Awarded to: @{user_info.get('username', 'user')}"
            bbox = draw.textbbox((0, 0), user_text, font=font_user)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, self.config.height - 150),
                user_text,
                font=font_user,
                fill=colors['accent']
            )
            
            # Draw date
            date_text = datetime.now().strftime("%B %d, %Y")
            bbox = draw.textbbox((0, 0), date_text, font=font_desc)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((self.config.width - text_width) // 2, self.config.height - 100),
                date_text,
                font=font_desc,
                fill=(100, 100, 100)
            )
            
            # Add decorative border
            border = self.border_manager.create_border(
                self.config.width, self.config.height,
                "double", colors['border'],
                thickness=20
            )
            image = Image.alpha_composite(image, border)
            
            # Add shine effect
            shine = Image.new('RGBA', (self.config.width, self.config.height),
                            (0, 0, 0, 0))
            draw_shine = ImageDraw.Draw(shine)
            
            # Draw light rays
            for angle in range(0, 360, 45):
                rad = angle * 3.14159 / 180
                length = 400
                end_x = self.config.width // 2 + int(length * 0.7 * math.cos(rad))
                end_y = self.config.height // 2 + int(length * 0.7 * math.sin(rad))
                
                draw_shine.line(
                    [self.config.width // 2, self.config.height // 2,
                     end_x, end_y],
                    fill=(255, 255, 255, 30),
                    width=10
                )
            
            image = Image.alpha_composite(image, shine)
            
            # Convert and save
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, colors['background'])
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            
            output_path = Path(self.config.output_dir) / f"achievement_{int(datetime.now().timestamp())}.png"
            image.save(output_path, 'PNG', quality=self.config.quality)
            
            logger.info(f"Achievement image generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating achievement image: {e}")
            return self._create_error_image("Achievement image error")
    
    def _create_error_image(self, error_message: str) -> str:
        """Create error image when generation fails"""
        try:
            # Create simple error image
            width, height = 800, 400
            image = Image.new('RGB', (width, height), (255, 200, 200))
            draw = ImageDraw.Draw(image)
            
            # Try to get font
            try:
                font = self.font_manager.get_font(40)
            except:
                font = ImageFont.load_default()
            
            # Draw error text
            error_title = "Image Generation Error"
            draw.text((width//4, height//3), error_title, font=font, fill=(255, 0, 0))
            
            # Draw message (truncate if too long)
            if len(error_message) > 50:
                error_message = error_message[:47] + "..."
            draw.text((width//4, height//2), error_message, font=font, fill=(100, 0, 0))
            
            # Save to temp directory
            temp_path = Path(self.config.temp_dir) / f"error_{int(datetime.now().timestamp())}.png"
            image.save(temp_path, 'PNG')
            
            return str(temp_path)
        except Exception as e:
            # Last resort: create simple text file
            error_file = Path(self.config.temp_dir) / "error.txt"
            with open(error_file, 'w') as f:
                f.write(f"Image generation failed: {error_message}")
            return str(error_file)
    
    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes"""
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=self.config.format,
                  quality=self.config.quality)
        return img_byte_arr.getvalue()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get generator statistics"""
        avg_time = 0
        if self.stats['successful'] > 0:
            avg_time = self.stats['total_time'] / self.stats['successful']
        
        return {
            'total_generated': self.stats['images_generated'],
            'successful': self.stats['successful'],
            'failed': self.stats['failed'],
            'success_rate': (
                (self.stats['successful'] / self.stats['images_generated'] * 100)
                if self.stats['images_generated'] > 0 else 0
            ),
            'average_time': f"{avg_time:.2f}s",
            'pil_available': PIL_AVAILABLE,
            'fonts_loaded': len(self.font_manager.fonts)
        }
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old generated files"""
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            
            for dir_path in [self.config.temp_dir, self.config.cache_dir]:
                if os.path.exists(dir_path):
                    for file in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file)
                        if os.path.isfile(file_path):
                            if os.path.getmtime(file_path) < cutoff_time:
                                os.remove(file_path)
                                logger.debug(f"Removed old file: {file_path}")
            
            logger.info("Cleaned up old files")
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")


# For backward compatibility
ImageGenerator = AdvancedImageGenerator


# Quick test function
def test_generator():
    """Test the image generator"""
    print("Testing Image Generator...")
    
    if not PIL_AVAILABLE:
        print("ERROR: PIL/Pillow not installed!")
        print("Install with: pip install pillow")
        return False
    
    generator = AdvancedImageGenerator()
    
    # Test data
    test_roast = "This is a test roast to check if the image generator is working properly!"
    test_user = {
        'username': 'test_user',
        'first_name': 'Test',
        'rating': 7.5,
        'member_count': 42
    }
    
    try:
        # Generate roast image
        print("Generating roast image...")
        roast_path = generator.generate_roast_image(test_roast, test_user)
        print(f"✓ Roast image: {roast_path}")
        
        # Generate welcome image
        print("Generating welcome image...")
        welcome_path = generator.generate_welcome_image(test_user)
        print(f"✓ Welcome image: {welcome_path}")
        
        # Show stats
        stats = generator.get_stats()
        print("\nGenerator Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run test if file is executed directly
    success = test_generator()
    sys.exit(0 if success else 1)
