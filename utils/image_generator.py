# utils/image_generator.py
import os
import logging
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generate 3D styled roast images with Bangla support"""
    
    def __init__(self):
        self.fonts = self._load_fonts()
        self.borders = self._load_borders()
        self.default_font = None
        self._setup_default_font()
        
        logger.info(f"Image Generator initialized with {len(self.fonts)} fonts and {len(self.borders)} borders")
    
    def _load_fonts(self) -> List[str]:
        """Load available font files with UTF-8 encoding support"""
        font_files = []
        font_dir = "assets/fonts"
        
        if os.path.exists(font_dir):
            try:
                # List all font files
                for file in os.listdir(font_dir):
                    if file.lower().endswith(('.ttf', '.otf')):
                        font_path = os.path.join(font_dir, file)
                        # Fix encoding for file path
                        font_path = os.path.normpath(font_path)
                        font_files.append(font_path)
                
                logger.info(f"Found {len(font_files)} font files")
            except Exception as e:
                logger.error(f"Error reading font directory: {e}")
        
        # If no fonts found, create a default font list
        if not font_files:
            logger.warning("No font files found, will use system defaults")
            # Add system font paths
            system_fonts = [
                "/system/fonts/NotoSansBengali-Regular.ttf",
                "/system/fonts/DroidSansFallback.ttf",
                "arial.ttf",
                "DejaVuSans.ttf"
            ]
            
            for font_path in system_fonts:
                if os.path.exists(font_path):
                    font_files.append(font_path)
        
        return font_files
    
    def _setup_default_font(self):
        """Setup a default font that supports Unicode"""
        try:
            # Try to load a Unicode-compatible font
            font_paths_to_try = [
                "assets/fonts/NotoSansBengali-Regular.ttf",
                "assets/fonts/SolaimanLipi.ttf",
                "assets/fonts/Kalpurush.ttf",
                "/system/fonts/DroidSansFallback.ttf",
                "arialuni.ttf",  # Windows Unicode font
                "DejaVuSans.ttf"  # Linux Unicode font
            ]
            
            for font_path in font_paths_to_try:
                if os.path.exists(font_path):
                    try:
                        self.default_font = ImageFont.truetype(font_path, 40)
                        logger.info(f"Using default font: {font_path}")
                        return
                    except:
                        continue
            
            # Ultimate fallback - create a simple font
            self.default_font = ImageFont.load_default()
            logger.info("Using system default font")
            
        except Exception as e:
            logger.error(f"Error setting up default font: {e}")
            self.default_font = ImageFont.load_default()
    
    def _load_borders(self) -> List[str]:
        """Load border image files"""
        border_files = []
        border_dir = "assets/borders"
        
        if os.path.exists(border_dir):
            try:
                for file in os.listdir(border_dir):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        border_path = os.path.join(border_dir, file)
                        border_files.append(border_path)
            except Exception as e:
                logger.error(f"Error loading borders: {e}")
        
        # If no borders found, we'll create dynamic ones
        if not border_files:
            logger.info("No border files found, will generate dynamic borders")
        
        return border_files
    
    def _get_random_font(self, size: int = 40) -> ImageFont.FreeTypeFont:
        """Get a random font that supports Unicode"""
        try:
            if self.fonts:
                font_path = random.choice(self.fonts)
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception as e:
                    logger.warning(f"Failed to load font {font_path}: {e}")
            
            # Fallback to default font
            if self.default_font:
                # Try to resize default font
                try:
                    return ImageFont.truetype(self.default_font.path, size)
                except:
                    return ImageFont.load_default().font_variant(size=size)
            
            return ImageFont.load_default().font_variant(size=size)
            
        except Exception as e:
            logger.error(f"Error getting font: {e}")
            return ImageFont.load_default().font_variant(size=size)
    
    def _create_text_image(self, text: str, font_size: int = 40, width: int = 800, height: int = 400) -> Image.Image:
        """Create a text-only image with proper Unicode handling"""
        try:
            # Create image with transparent background
            image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Get font
            font = self._get_random_font(font_size)
            
            # Prepare text for drawing
            # Ensure text is properly encoded
            if isinstance(text, str):
                # Text is already Unicode
                text_to_draw = text
            else:
                # Try to decode
                try:
                    text_to_draw = text.decode('utf-8')
                except:
                    text_to_draw = str(text)
            
            # Split text into lines
            lines = self._wrap_text(text_to_draw, draw, font, width - 100)
            
            # Calculate total text height
            line_height = font_size + 10
            total_text_height = len(lines) * line_height
            start_y = (height - total_text_height) // 2
            
            # Draw each line
            for i, line in enumerate(lines):
                # Calculate text width
                try:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                except:
                    text_width = len(line) * font_size // 2
                
                x = (width - text_width) // 2
                y = start_y + (i * line_height)
                
                # Draw text with shadow for 3D effect
                shadow_offset = 2
                shadow_color = (0, 0, 0, 150)  # Semi-transparent black
                text_color = (255, 255, 255, 255)  # White
                
                # Draw shadow
                draw.text((x + shadow_offset, y + shadow_offset), 
                         line, font=font, fill=shadow_color)
                
                # Draw main text
                draw.text((x, y), line, font=font, fill=text_color)
            
            return image
            
        except Exception as e:
            logger.error(f"Error creating text image: {e}")
            # Create a simple error image
            error_image = Image.new('RGB', (width, height), (255, 0, 0))
            draw = ImageDraw.Draw(error_image)
            draw.text((50, 50), f"Error: {str(e)[:50]}", fill=(255, 255, 255))
            return error_image
    
    def _wrap_text(self, text: str, draw: ImageDraw.Draw, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                test_width = bbox[2] - bbox[0]
            except:
                # Estimate width
                test_width = len(test_line) * 20
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # If still too long, split long words
        if not lines:
            lines = [text[:50] + "..."]
        
        return lines
    
    def _add_3d_effects(self, image: Image.Image) -> Image.Image:
        """Add 3D effects to image"""
        try:
            # Create a copy to work on
            result = image.copy()
            
            # Add drop shadow
            shadow = Image.new('RGBA', result.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            
            # Create shadow offset
            shadow_offset = 5
            
            # Get image bounds
            bounds = result.getbbox()
            if bounds:
                # Draw shadow
                shadow_draw.rectangle(
                    [bounds[0] + shadow_offset, bounds[1] + shadow_offset,
                     bounds[2] + shadow_offset, bounds[3] + shadow_offset],
                    fill=(0, 0, 0, 100)
                )
                
                # Composite shadow with original
                result = Image.alpha_composite(shadow, result)
            
            # Add glow effect
            glow = result.filter(ImageFilter.GaussianBlur(radius=2))
            result = Image.blend(glow, result, 0.7)
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding 3D effects: {e}")
            return image
    
    def _add_border(self, image: Image.Image) -> Image.Image:
        """Add border to image"""
        try:
            if self.borders:
                # Load random border
                border_path = random.choice(self.borders)
                border = Image.open(border_path).convert('RGBA')
                
                # Resize border to match image
                border = border.resize(image.size, Image.Resampling.LANCZOS)
                
                # Composite with image
                result = Image.alpha_composite(image, border)
                return result
            else:
                # Create dynamic border
                bordered = Image.new('RGBA', image.size, (0, 0, 0, 0))
                bordered.paste(image, (0, 0))
                
                draw = ImageDraw.Draw(bordered)
                border_width = 10
                border_color = (random.randint(50, 255), 
                              random.randint(50, 255), 
                              random.randint(50, 255),
                              255)
                
                # Draw border
                draw.rectangle(
                    [border_width, border_width,
                     image.width - border_width, image.height - border_width],
                    outline=border_color,
                    width=border_width
                )
                
                return bordered
                
        except Exception as e:
            logger.error(f"Error adding border: {e}")
            return image
    
    async def generate_roast_image(self, roast_data: Dict, user: Any, target_user: Any = None) -> Optional[str]:
        """Generate a roast image"""
        try:
            # Create temp directory
            os.makedirs("temp", exist_ok=True)
            
            # Generate filename with safe encoding
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_num = random.randint(1000, 9999)
            filename = f"temp/roast_{timestamp}_{random_num}.png"
            
            # Extract text from roast data
            primary_text = roast_data.get("primary_roast", "রোস্ট টাইম! 🔥")
            secondary_text = roast_data.get("secondary_roast", "")
            
            # Combine texts
            full_text = primary_text
            if secondary_text:
                full_text += f"\n\n{secondary_text}"
            
            # Add user info
            user_name = user.first_name if hasattr(user, 'first_name') else "User"
            if target_user:
                target_name = target_user.first_name if hasattr(target_user, 'first_name') else "Target"
                full_text += f"\n\n🎯 Target: {target_name}"
            
            full_text += f"\n\n- {user_name}"
            
            # Create base image
            width, height = 1080, 1080
            base_image = self._create_text_image(full_text, font_size=36, width=width, height=height)
            
            # Add 3D effects
            image_with_effects = self._add_3d_effects(base_image)
            
            # Add border
            final_image = self._add_border(image_with_effects)
            
            # Convert to RGB if needed
            if final_image.mode == 'RGBA':
                background = Image.new('RGB', final_image.size, (20, 20, 20))
                background.paste(final_image, mask=final_image.split()[3])
                final_image = background
            
            # Save image
            final_image.save(filename, 'PNG', quality=95)
            logger.info(f"Image saved: {filename}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating roast image: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def create_simple_image(self, text: str) -> Optional[str]:
        """Create a simple image for testing"""
        try:
            os.makedirs("temp", exist_ok=True)
            filename = f"temp/test_{datetime.now().strftime('%H%M%S')}.png"
            
            width, height = 800, 600
            image = Image.new('RGB', (width, height), (30, 30, 30))
            draw = ImageDraw.Draw(image)
            
            # Try to use a font that supports Unicode
            try:
                font = self._get_random_font(32)
            except:
                font = ImageFont.load_default()
            
            # Draw text
            lines = text.split('\n')
            y = 50
            for line in lines:
                draw.text((50, y), line, font=font, fill=(255, 255, 255))
                y += 40
            
            image.save(filename, 'PNG')
            logger.info(f"Simple image created: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error creating simple image: {e}")
            return None
