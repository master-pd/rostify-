# utils/image_generator.py - COMPLETE FIXED VERSION
import os
import logging
import random
import math
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np

logger = logging.getLogger(__name__)

class ProfessionalImageGenerator:
    """High Quality 3D Image Generator with Font Support"""
    
    def __init__(self):
        self.fonts = self._load_fonts()
        self.default_font = self._get_default_font()
        self.border_styles = self._load_border_styles()
        self.effect_presets = self._create_effect_presets()
        
        logger.info(f"ProfessionalImageGenerator initialized with {len(self.fonts)} fonts")
    
    def _load_fonts(self) -> List[ImageFont.FreeTypeFont]:
        """Load all available font files from assets/fonts/"""
        fonts = []
        font_dir = "assets/fonts"
        
        if not os.path.exists(font_dir):
            os.makedirs(font_dir, exist_ok=True)
            logger.warning("Font directory created. Please add .ttf files named 1.ttf, 2.ttf, etc.")
            return fonts
        
        # Load font files in order (1.ttf, 2.ttf, 3.ttf, etc.)
        for i in range(1, 51):  # Check up to 50 fonts
            font_path = os.path.join(font_dir, f"{i}.ttf")
            if os.path.exists(font_path):
                try:
                    # Try different sizes to find working one
                    for size in [32, 36, 40, 48]:
                        try:
                            font = ImageFont.truetype(font_path, size)
                            fonts.append(font)
                            logger.info(f"Loaded font: {i}.ttf (size: {size})")
                            break
                        except:
                            continue
                except Exception as e:
                    logger.warning(f"Failed to load font {i}.ttf: {e}")
        
        # If no fonts found, create a default font
        if not fonts:
            logger.warning("No font files found. Using system default.")
            fonts = [self._create_system_font()]
        
        return fonts
    
    def _get_default_font(self) -> ImageFont.FreeTypeFont:
        """Get a reliable default font"""
        if self.fonts:
            return random.choice(self.fonts)
        
        # Create system font
        return self._create_system_font()
    
    def _create_system_font(self) -> ImageFont.FreeTypeFont:
        """Create a system font that works everywhere"""
        try:
            # Try to load a system font
            system_fonts = [
                "arial.ttf",
                "DejaVuSans.ttf",
                "/system/fonts/DroidSansFallback.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ]
            
            for font_path in system_fonts:
                try:
                    if os.path.exists(font_path):
                        return ImageFont.truetype(font_path, 36)
                except:
                    continue
            
            # Ultimate fallback
            return ImageFont.load_default()
            
        except Exception as e:
            logger.error(f"Error creating system font: {e}")
            return ImageFont.load_default()
    
    def _load_border_styles(self) -> List[Dict]:
        """Define border styles"""
        return [
            {"type": "neon", "color": (0, 255, 255), "width": 10, "glow": True},
            {"type": "gold", "color": (255, 215, 0), "width": 8, "glow": False},
            {"type": "gradient", "color1": (255, 0, 255), "color2": (0, 255, 255), "width": 12},
            {"type": "dotted", "color": (255, 255, 255), "width": 6, "pattern": "dotted"},
            {"type": "double", "color": (0, 255, 0), "width": 5, "lines": 2},
        ]
    
    def _create_effect_presets(self) -> Dict:
        """Create visual effect presets"""
        return {
            "neon": {
                "shadow": True,
                "glow": True,
                "blur": 3,
                "color": (0, 255, 255)
            },
            "gold": {
                "gradient": True,
                "shine": True,
                "color1": (255, 215, 0),
                "color2": (255, 255, 150)
            },
            "fire": {
                "gradient": True,
                "glow": True,
                "color1": (255, 100, 0),
                "color2": (255, 255, 0)
            },
            "ice": {
                "gradient": True,
                "sparkle": True,
                "color1": (0, 200, 255),
                "color2": (200, 255, 255)
            },
            "matrix": {
                "glitch": True,
                "scanlines": True,
                "color": (0, 255, 0)
            }
        }
    
    def _get_font(self, size: int = 36) -> ImageFont.FreeTypeFont:
        """Get a font with specified size"""
        try:
            if self.fonts:
                # Return random font with adjusted size
                font = random.choice(self.fonts)
                # Try to resize the font
                try:
                    # Get font path from existing font
                    if hasattr(font, 'path'):
                        return ImageFont.truetype(font.path, size)
                except:
                    pass
            
            # Fallback to default font with size
            return self.default_font
            
        except Exception as e:
            logger.error(f"Error getting font: {e}")
            return self.default_font
    
    def _render_text_with_effects(self, draw: ImageDraw.Draw, text: str, 
                                 font: ImageFont.FreeTypeFont, position: Tuple[int, int],
                                 effect_type: str = "neon") -> None:
        """Render text with professional effects"""
        x, y = position
        effect = self.effect_presets.get(effect_type, self.effect_presets["neon"])
        
        # Split text into lines if needed
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_y = y + (i * (font.size + 20))
            
            if effect_type == "neon":
                self._draw_neon_text(draw, line, font, (x, line_y), effect)
            elif effect_type == "gold":
                self._draw_gold_text(draw, line, font, (x, line_y), effect)
            elif effect_type == "fire":
                self._draw_fire_text(draw, line, font, (x, line_y), effect)
            elif effect_type == "ice":
                self._draw_ice_text(draw, line, font, (x, line_y), effect)
            else:
                self._draw_basic_text(draw, line, font, (x, line_y), (255, 255, 255))
    
    def _draw_neon_text(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                       position: Tuple[int, int], effect: Dict) -> None:
        """Draw text with neon effect"""
        x, y = position
        color = effect.get("color", (0, 255, 255))
        
        # Draw multiple layers for glow effect
        for offset in range(5, 0, -1):
            glow_color = (*color, 50 // offset)
            for dx, dy in [(offset, 0), (-offset, 0), (0, offset), (0, -offset),
                          (offset, offset), (-offset, offset), (offset, -offset), (-offset, -offset)]:
                draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
        
        # Draw inner highlight
        highlight_color = (255, 255, 255)
        draw.text((x-1, y-1), text, font=font, fill=highlight_color)
    
    def _draw_gold_text(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                       position: Tuple[int, int], effect: Dict) -> None:
        """Draw text with gold effect"""
        x, y = position
        
        # Draw shadow
        shadow_color = (100, 70, 0, 150)
        for offset in range(1, 4):
            draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
        
        # Draw gradient text
        colors = [(255, 215, 0), (255, 255, 150), (255, 215, 0)]
        for i, color in enumerate(colors):
            offset = i - 1
            draw.text((x + offset, y + offset), text, font=font, fill=color)
    
    def _draw_fire_text(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                       position: Tuple[int, int], effect: Dict) -> None:
        """Draw text with fire effect"""
        x, y = position
        
        # Draw fire gradient
        colors = [
            (255, 255, 0),   # Yellow
            (255, 200, 0),   # Orange-yellow
            (255, 100, 0),   # Orange
            (255, 50, 0),    # Red-orange
            (200, 0, 0)      # Dark red
        ]
        
        for i, color in enumerate(colors):
            offset = i * 2
            draw.text((x, y + offset), text, font=font, fill=color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    def _draw_ice_text(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                      position: Tuple[int, int], effect: Dict) -> None:
        """Draw text with ice effect"""
        x, y = position
        
        # Draw ice gradient
        colors = [
            (255, 255, 255),  # White
            (200, 255, 255),  # Light blue
            (100, 255, 255),  # Cyan
            (0, 200, 255),    # Blue
            (0, 100, 200)     # Dark blue
        ]
        
        for i, color in enumerate(colors):
            offset = i
            draw.text((x + offset, y + offset), text, font=font, fill=color)
    
    def _draw_basic_text(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                        position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """Draw basic text with shadow"""
        x, y = position
        
        # Draw shadow
        shadow_color = (0, 0, 0, 150)
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
    
    def _create_background(self, width: int, height: int, bg_type: str = "gradient") -> Image.Image:
        """Create professional background"""
        if bg_type == "gradient":
            return self._create_gradient_background(width, height)
        elif bg_type == "abstract":
            return self._create_abstract_background(width, height)
        elif bg_type == "space":
            return self._create_space_background(width, height)
        else:
            return self._create_solid_background(width, height)
    
    def _create_gradient_background(self, width: int, height: int) -> Image.Image:
        """Create gradient background"""
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Create gradient
        for y in range(height):
            # Vertical gradient
            r = int(20 + (y / height) * 100)
            g = int(30 + (y / height) * 120)
            b = int(40 + (y / height) * 140)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add subtle noise
        self._add_noise(image, intensity=5)
        
        return image
    
    def _create_abstract_background(self, width: int, height: int) -> Image.Image:
        """Create abstract background"""
        image = Image.new('RGB', (width, height), (20, 20, 40))
        draw = ImageDraw.Draw(image)
        
        # Draw abstract shapes
        for _ in range(20):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            size = random.randint(50, 200)
            color = (
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(30, 100)
            )
            draw.ellipse([x1, y1, x1 + size, y1 + size], fill=color, outline=None)
        
        # Apply blur
        image = image.filter(ImageFilter.GaussianBlur(radius=10))
        
        return image
    
    def _create_space_background(self, width: int, height: int) -> Image.Image:
        """Create space-like background"""
        image = Image.new('RGB', (width, height), (10, 10, 30))
        draw = ImageDraw.Draw(image)
        
        # Draw stars
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            draw.ellipse([x, y, x + size, y + size], fill=(brightness, brightness, brightness))
        
        # Draw nebula
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(100, 300)
            color = (
                random.randint(100, 200),
                random.randint(50, 150),
                random.randint(150, 250),
                random.randint(30, 80)
            )
            draw.ellipse([x, y, x + size, y + size], fill=color)
        
        image = image.filter(ImageFilter.GaussianBlur(radius=3))
        
        return image
    
    def _create_solid_background(self, width: int, height: int) -> Image.Image:
        """Create solid color background"""
        colors = [
            (25, 25, 112),   # Midnight Blue
            (139, 0, 139),   # Dark Magenta
            (0, 100, 0),     # Dark Green
            (128, 0, 0),     # Maroon
            (47, 79, 79),    # Dark Slate Gray
            (72, 61, 139),   # Dark Slate Blue
            (85, 107, 47),   # Dark Olive Green
        ]
        
        color = random.choice(colors)
        return Image.new('RGB', (width, height), color)
    
    def _add_noise(self, image: Image.Image, intensity: int = 10) -> None:
        """Add subtle noise to image"""
        width, height = image.size
        pixels = image.load()
        
        for x in range(width):
            for y in range(height):
                if random.random() < 0.1:  # 10% pixels
                    r, g, b = pixels[x, y]
                    noise = random.randint(-intensity, intensity)
                    pixels[x, y] = (
                        max(0, min(255, r + noise)),
                        max(0, min(255, g + noise)),
                        max(0, min(255, b + noise))
                    )
    
    def _add_border_effect(self, image: Image.Image, border_style: Dict) -> Image.Image:
        """Add professional border to image"""
        width, height = image.size
        
        if border_style["type"] == "neon":
            return self._add_neon_border(image, border_style)
        elif border_style["type"] == "gradient":
            return self._add_gradient_border(image, border_style)
        else:
            return self._add_basic_border(image, border_style)
    
    def _add_neon_border(self, image: Image.Image, style: Dict) -> Image.Image:
        """Add neon glowing border"""
        border = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        color = style.get("color", (0, 255, 255))
        width = style.get("width", 10)
        
        # Draw glow effect
        for i in range(width, 0, -1):
            glow_color = (*color, 100 // i)
            draw.rectangle(
                [i, i, image.width - i, image.height - i],
                outline=glow_color,
                width=2
            )
        
        # Draw main border
        draw.rectangle(
            [0, 0, image.width - 1, image.height - 1],
            outline=color,
            width=width
        )
        
        # Composite with original image
        result = Image.alpha_composite(image.convert('RGBA'), border)
        return result.convert('RGB')
    
    def _add_gradient_border(self, image: Image.Image, style: Dict) -> Image.Image:
        """Add gradient border"""
        border = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        color1 = style.get("color1", (255, 0, 255))
        color2 = style.get("color2", (0, 255, 255))
        width = style.get("width", 12)
        
        # Draw gradient border
        for i in range(width):
            ratio = i / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            draw.rectangle(
                [i, i, image.width - i - 1, image.height - i - 1],
                outline=(r, g, b),
                width=1
            )
        
        result = Image.alpha_composite(image.convert('RGBA'), border)
        return result.convert('RGB')
    
    def _add_basic_border(self, image: Image.Image, style: Dict) -> Image.Image:
        """Add basic border"""
        border = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(border)
        
        color = style.get("color", (255, 255, 255))
        width = style.get("width", 8)
        
        draw.rectangle(
            [0, 0, image.width - 1, image.height - 1],
            outline=color,
            width=width
        )
        
        result = Image.alpha_composite(image.convert('RGBA'), border)
        return result.convert('RGB')
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            # Estimate width
            test_width = len(test_line) * font.size // 2
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text[:50] + "..."]
    
    async def generate_roast_image(self, roast_data: Dict, user: Any, target_user: Any = None) -> Optional[str]:
        """Generate professional roast image"""
        try:
            # Create temp directory
            os.makedirs("temp", exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_num = random.randint(1000, 9999)
            filename = f"temp/roast_{timestamp}_{random_num}.png"
            
            # Extract roast text
            primary_text = roast_data.get("primary_roast", "রোস্ট টাইম! 🔥")
            secondary_text = roast_data.get("secondary_roast", "")
            
            # Prepare full text
            full_text = primary_text
            if secondary_text:
                full_text += f"\n\n{secondary_text}"
            
            # Add user info
            user_name = user.first_name if hasattr(user, 'first_name') else "User"
            if target_user:
                target_name = target_user.first_name if hasattr(target_user, 'first_name') else "Target"
                full_text += f"\n\n🎯 Target: {target_name}"
            
            full_text += f"\n\n- {user_name}"
            
            # Image dimensions
            width, height = 1080, 1080
            
            # Create background
            bg_type = random.choice(["gradient", "abstract", "space", "solid"])
            image = self._create_background(width, height, bg_type)
            draw = ImageDraw.Draw(image)
            
            # Choose random effect
            effect_type = random.choice(list(self.effect_presets.keys()))
            
            # Get font
            font = self._get_font(36)
            
            # Wrap text
            lines = self._wrap_text(full_text, font, width - 200)
            
            # Calculate text position
            total_height = len(lines) * (font.size + 20)
            start_y = (height - total_height) // 2
            
            # Draw each line
            for i, line in enumerate(lines):
                # Estimate line width
                line_width = len(line) * font.size // 2
                x = (width - line_width) // 2
                y = start_y + (i * (font.size + 20))
                
                # Render text with effects
                self._render_text_with_effects(draw, line, font, (x, y), effect_type)
            
            # Add border
            border_style = random.choice(self.border_styles)
            image = self._add_border_effect(image, border_style)
            
            # Apply final effects
            image = self._apply_final_effects(image, effect_type)
            
            # Save image
            image.save(filename, 'PNG', quality=95, optimize=True)
            logger.info(f"Professional image saved: {filename}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating professional image: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _apply_final_effects(self, image: Image.Image, effect_type: str) -> Image.Image:
        """Apply final image effects"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance color
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        # Add slight sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def create_test_image(self) -> str:
        """Create a test image to verify functionality"""
        try:
            os.makedirs("temp", exist_ok=True)
            filename = "temp/test_image.png"
            
            width, height = 800, 600
            image = self._create_background(width, height, "gradient")
            draw = ImageDraw.Draw(image)
            
            # Test Bangla text
            test_text = "পরীক্ষা - Test\nবাংলা ফন্ট কাজ করছে! ✅\nEnglish font working! 🎉"
            
            font = self._get_font(32)
            lines = test_text.split('\n')
            
            for i, line in enumerate(lines):
                x = 50
                y = 100 + (i * 50)
                self._draw_basic_text(draw, line, font, (x, y), (255, 255, 255))
            
            # Add info
            info_text = f"Fonts loaded: {len(self.fonts)}\nGenerator: Professional v1.0"
            font_small = self._get_font(24)
            draw.text((50, 400), info_text, font=font_small, fill=(200, 200, 200))
            
            # Save
            image.save(filename, 'PNG')
            logger.info(f"Test image created: {filename}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Error creating test image: {e}")
            return ""


# Simple wrapper for backward compatibility
class ImageGenerator(ProfessionalImageGenerator):
    """Wrapper for backward compatibility"""
    pass


def setup_fonts():
    """Setup font files for the bot"""
    font_dir = "assets/fonts"
    os.makedirs(font_dir, exist_ok=True)
    
    # Create instructions file
    instructions = """# Roastify Bot Fonts Directory

## Required Fonts:
Please add Bangla font files in this directory with names:
1.ttf, 2.ttf, 3.ttf, etc.

## Recommended Bangla Fonts:
1. SolaimanLipi.ttf - Rename to 1.ttf
2. Kalpurush.ttf - Rename to 2.ttf
3. NotoSansBengali.ttf - Rename to 3.ttf

## Download Links:
• https://www.omicronlab.com/bangla-fonts.html
• https://fonts.google.com/noto/specimen/Noto+Sans+Bengali

## How to add fonts:
1. Download .ttf font files
2. Rename them to 1.ttf, 2.ttf, etc.
3. Place in this directory
4. Restart the bot

The bot will automatically detect and use these fonts.
"""
    
    with open(os.path.join(font_dir, "README.txt"), "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Font directory setup complete!")
    print("📁 Please add Bangla .ttf files to assets/fonts/")
    print("📝 Instructions are in assets/fonts/README.txt")


if __name__ == "__main__":
    # Test the image generator
    generator = ProfessionalImageGenerator()
    test_file = generator.create_test_image()
    if test_file:
        print(f"✅ Test image created: {test_file}")
    else:
        print("❌ Failed to create test image")
