#!/usr/bin/env python3
"""
3D Image Generator for Roastify Bot
Generates stylish images with text, borders, and effects
"""

import os
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import textwrap
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import IMAGE_GENERATION, BORDERS, FONTS, PATHS, TIME_BASED_BEHAVIOR
except ImportError:
    logger.error("Config module not found")
    sys.exit(1)


class ImageGenerator:
    """Generate 3D styled roast images"""
    
    def __init__(self):
        """Initialize image generator"""
        self.config = IMAGE_GENERATION
        self.border_config = BORDERS
        self.font_config = FONTS
        
        # Load available assets
        self.available_fonts = self._load_fonts()
        self.available_borders = self._load_borders()
        self.templates = self._load_templates()
        
        # Track recent usage for randomization
        self.recent_fonts = []
        self.recent_borders = []
        self.recent_templates = []
        
        logger.info("Image Generator initialized")
    
    def _load_fonts(self) -> List[str]:
        """Load available font files"""
        fonts = []
        fonts_dir = PATHS["fonts"]
        
        # Check font files from config
        for font_file in self.font_config.get("font_files", []):
            font_path = os.path.join(fonts_dir, font_file)
            if os.path.exists(font_path):
                fonts.append(font_path)
            else:
                logger.warning(f"Font file not found: {font_path}")
        
        # Also check for any .ttf or .otf files in fonts directory
        if not fonts:
            for ext in [".ttf", ".otf", ".TTF", ".OTF"]:
                fonts.extend([
                    os.path.join(fonts_dir, f) for f in os.listdir(fonts_dir)
                    if f.endswith(ext)
                ])
        
        # Add default system fonts as fallback
        default_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arial.ttf"
        ]
        
        for font in default_fonts:
            if os.path.exists(font) and font not in fonts:
                fonts.append(font)
        
        if not fonts:
            logger.warning("No font files found, using default")
            fonts = []  # PIL will use default font
        
        logger.info(f"Loaded {len(fonts)} fonts")
        return fonts
    
    def _load_borders(self) -> List[str]:
        """Load available border images"""
        borders = []
        borders_dir = PATHS["borders"]
        
        # Check border files from config
        for border_file in self.border_config.get("border_files", []):
            border_path = os.path.join(borders_dir, border_file)
            if os.path.exists(border_path):
                borders.append(border_path)
            else:
                logger.warning(f"Border file not found: {border_path}")
        
        # Also check for any image files in borders directory
        if not borders:
            for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
                borders.extend([
                    os.path.join(borders_dir, f) for f in os.listdir(borders_dir)
                    if f.endswith(ext)
                ])
        
        # Create default borders if none found
        if not borders:
            borders = self._create_default_borders()
        
        logger.info(f"Loaded {len(borders)} borders")
        return borders
    
    def _create_default_borders(self) -> List[str]:
        """Create default border images"""
        borders = []
        borders_dir = PATHS["borders"]
        os.makedirs(borders_dir, exist_ok=True)
        
        # Create 5 default borders
        border_styles = [
            ("simple_round", (255, 0, 0, 100)),  # Red border
            ("double_line", (0, 255, 0, 100)),   # Green border
            ("dotted", (0, 0, 255, 100)),        # Blue border
            ("thick_thin", (255, 255, 0, 100)),  # Yellow border
            ("ornate", (255, 0, 255, 100))       # Magenta border
        ]
        
        for i, (style, color) in enumerate(border_styles, 1):
            border_path = os.path.join(borders_dir, f"default_border_{i}.png")
            
            # Create a simple border image
            img = Image.new('RGBA', (1100, 1100), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            if style == "simple_round":
                # Simple rounded border
                draw.rectangle([50, 50, 1050, 1050], outline=color, width=20)
                draw.rectangle([70, 70, 1030, 1030], outline=color, width=10)
            elif style == "double_line":
                # Double line border
                draw.rectangle([40, 40, 1060, 1060], outline=color, width=15)
                draw.rectangle([80, 80, 1020, 1020], outline=color, width=10)
            elif style == "dotted":
                # Dotted border
                for x in range(50, 1051, 30):
                    draw.ellipse([x, 50, x+10, 60], fill=color)
                    draw.ellipse([x, 1040, x+10, 1050], fill=color)
                for y in range(50, 1051, 30):
                    draw.ellipse([50, y, 60, y+10], fill=color)
                    draw.ellipse([1040, y, 1050, y+10], fill=color)
            elif style == "thick_thin":
                # Thick and thin border
                draw.rectangle([30, 30, 1070, 1070], outline=color, width=25)
                draw.rectangle([90, 90, 1010, 1010], outline=color, width=5)
            elif style == "ornate":
                # Ornate corner border
                # Corners
                draw.rectangle([50, 50, 200, 100], fill=color)
                draw.rectangle([50, 50, 100, 200], fill=color)
                draw.rectangle([950, 50, 1050, 200], fill=color)
                draw.rectangle([900, 50, 1050, 100], fill=color)
                draw.rectangle([50, 950, 200, 1050], fill=color)
                draw.rectangle([50, 900, 100, 1050], fill=color)
                draw.rectangle([900, 950, 1050, 1050], fill=color)
                draw.rectangle([950, 900, 1050, 1050], fill=color)
            
            img.save(border_path, 'PNG')
            borders.append(border_path)
        
        return borders
    
    def _load_templates(self) -> Dict:
        """Load template configurations"""
        templates_file = os.path.join(PATHS["templates"], "templates.json")
        
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading templates: {e}")
        
        # Return default template structure
        return {
            "cartoon_roast": [
                {
                    "name": "default_cartoon",
                    "style": "funny",
                    "background_color": (255, 255, 200),
                    "text_color": (0, 0, 0),
                    "border_color": (255, 100, 100),
                    "shadow": True,
                    "effects": ["rounded_corners", "drop_shadow"]
                }
            ],
            "neon_savage": [
                {
                    "name": "default_neon",
                    "style": "savage",
                    "background_color": (0, 0, 20),
                    "text_color": (0, 255, 255),
                    "border_color": (255, 0, 255),
                    "shadow": True,
                    "effects": ["glow", "gradient"]
                }
            ]
        }
    
    def _get_random_font(self) -> Optional[str]:
        """Get a random font, avoiding recent repeats"""
        if not self.available_fonts:
            return None
        
        # Filter out recently used fonts
        available = [f for f in self.available_fonts 
                    if f not in self.recent_fonts[-self.font_config.get("no_repeat_until", 3):]]
        
        # If all fonts recently used, use any
        if not available:
            available = self.available_fonts
        
        # Select random font
        selected = random.choice(available)
        
        # Update recent fonts list
        self.recent_fonts.append(selected)
        if len(self.recent_fonts) > 10:  # Keep last 10
            self.recent_fonts.pop(0)
        
        return selected
    
    def _get_random_border(self) -> Optional[str]:
        """Get a random border, avoiding recent repeats"""
        if not self.available_borders:
            return None
        
        # Filter out recently used borders
        available = [b for b in self.available_borders 
                    if b not in self.recent_borders[-self.border_config.get("no_repeat_until", 5):]]
        
        # If all borders recently used, use any
        if not available:
            available = self.available_borders
        
        # Select random border
        selected = random.choice(available)
        
        # Update recent borders list
        self.recent_borders.append(selected)
        if len(self.recent_borders) > 15:  # Keep last 15
            self.recent_borders.pop(0)
        
        return selected
    
    def _get_random_template(self, category: str = None) -> Dict:
        """Get a random template"""
        if category and category in self.templates:
            templates = self.templates[category]
        else:
            # Flatten all templates
            templates = []
            for cat in self.templates.values():
                if isinstance(cat, list):
                    templates.extend(cat)
        
        if not templates:
            # Return default template
            return {
                "name": "default",
                "style": "normal",
                "background_color": (255, 255, 255),
                "text_color": (0, 0, 0),
                "border_color": (100, 100, 100),
                "shadow": False,
                "effects": []
            }
        
        # Avoid recent templates
        available = [t for t in templates 
                    if t.get("name") not in self.recent_templates[-5:]]
        
        if not available:
            available = templates
        
        selected = random.choice(available)
        
        # Update recent templates
        self.recent_templates.append(selected.get("name", "unknown"))
        if len(self.recent_templates) > 10:
            self.recent_templates.pop(0)
        
        return selected
    
    def _get_time_based_theme(self) -> Dict:
        """Get theme based on current time"""
        current_hour = datetime.now().hour
        
        if TIME_BASED_BEHAVIOR["day_mode"]["time_range"][0] <= current_hour <= \
           TIME_BASED_BEHAVIOR["day_mode"]["time_range"][2]:
            theme = TIME_BASED_BEHAVIOR["day_mode"]["theme"]
            return {
                "mode": "day",
                "theme": theme,
                "brightness": 1.0,
                "contrast": 1.0,
                "colors": {
                    "primary": (255, 255, 255),  # White background
                    "secondary": (240, 240, 240),
                    "text": (30, 30, 30),  # Dark text
                    "accent": (70, 130, 180)  # Steel blue
                }
            }
        else:
            theme = TIME_BASED_BEHAVIOR["night_mode"]["theme"]
            return {
                "mode": "night",
                "theme": theme,
                "brightness": 0.7,
                "contrast": 1.2,
                "colors": {
                    "primary": (20, 20, 40),  # Dark blue background
                    "secondary": (40, 40, 60),
                    "text": (220, 220, 255),  # Light blue text
                    "accent": (255, 105, 180)  # Hot pink
                }
            }
    
    def _create_3d_text_effect(self, draw: ImageDraw, text: str, font: ImageFont, 
                              position: Tuple[int, int], color: Tuple[int, int, int], 
                              depth: int = 3) -> None:
        """Create 3D text effect with shadows"""
        x, y = position
        
        # Draw shadow layers for 3D effect
        shadow_color = (color[0]//4, color[1]//4, color[2]//4)
        for i in range(depth, 0, -1):
            shadow_pos = (x + i, y + i)
            draw.text(shadow_pos, text, font=font, fill=shadow_color)
        
        # Draw main text
        draw.text(position, text, font=font, fill=color)
        
        # Add highlight effect
        highlight_color = (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50))
        highlight_pos = (x - 1, y - 1)
        draw.text(highlight_pos, text, font=font, fill=highlight_color)
    
    def _add_glow_effect(self, image: Image.Image, color: Tuple[int, int, int], 
                        intensity: int = 2) -> Image.Image:
        """Add glow effect to image"""
        # Create glow layer
        glow = image.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=intensity))
        
        # Adjust glow color
        enhancer = ImageEnhance.Color(glow)
        glow = enhancer.enhance(1.5)
        
        # Composite with original
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result = Image.alpha_composite(result, glow)
        result = Image.alpha_composite(result, image)
        
        return result
    
    def _add_cinematic_lighting(self, image: Image.Image, 
                               theme: Dict) -> Image.Image:
        """Add cinematic lighting effects"""
        width, height = image.size
        
        # Create gradient overlay
        gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        if theme["mode"] == "day":
            # Sunlight effect from top-left
            for i in range(height):
                alpha = int(30 * (1 - i/height))
                draw.rectangle([0, i, width, i+1], 
                              fill=(255, 255, 200, alpha))
        else:
            # Moonlight effect
            for i in range(width):
                alpha = int(40 * (1 - i/width))
                draw.rectangle([i, 0, i+1, height], 
                              fill=(150, 150, 255, alpha))
        
        # Apply gradient
        result = Image.alpha_composite(image, gradient)
        return result
    
    async def generate_roast_image(self, roast_data: Dict, user: Any, 
                                  target_user: Any = None) -> str:
        """Generate roast image with all effects"""
        try:
            # Get dimensions from config
            width, height = self.config["image_resolution"]
            
            # Get time-based theme
            theme = self._get_time_based_theme()
            
            # Get random template
            template = self._get_random_template(roast_data.get("template_category"))
            
            # Create base image with theme colors
            base_color = template.get("background_color", theme["colors"]["primary"])
            image = Image.new('RGB', (width, height), base_color)
            draw = ImageDraw.Draw(image)
            
            # Add background effects if specified
            if template.get("effects"):
                image = self._apply_background_effects(image, template["effects"], theme)
            
            # Get random font
            font_path = self._get_random_font()
            try:
                if font_path:
                    font_large = ImageFont.truetype(font_path, 60)
                    font_medium = ImageFont.truetype(font_path, 40)
                    font_small = ImageFont.truetype(font_path, 30)
                else:
                    # Use default fonts
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Prepare text
            primary_text = roast_data.get("primary_roast", "রোস্ট")
            secondary_text = roast_data.get("secondary_roast", "")
            emoji_text = roast_data.get("emoji_layer", "😈")
            
            # Wrap text to fit image
            wrapper = textwrap.TextWrapper(width=30)
            primary_lines = wrapper.wrap(primary_text)
            secondary_lines = wrapper.wrap(secondary_text) if secondary_text else []
            
            # Calculate positions
            current_y = 100
            text_color = template.get("text_color", theme["colors"]["text"])
            
            # Draw primary text with 3D effect
            for line in primary_lines:
                text_width = draw.textlength(line, font=font_large)
                x_position = (width - text_width) // 2
                
                self._create_3d_text_effect(
                    draw, line, font_large, (x_position, current_y), text_color, depth=3
                )
                current_y += 80
            
            # Draw secondary text
            if secondary_lines:
                current_y += 40
                for line in secondary_lines:
                    text_width = draw.textlength(line, font=font_medium)
                    x_position = (width - text_width) // 2
                    draw.text((x_position, current_y), line, font=font_medium, fill=text_color)
                    current_y += 50
            
            # Draw emoji
            if emoji_text:
                text_width = draw.textlength(emoji_text, font=font_large)
                x_position = (width - text_width) // 2
                draw.text((x_position, current_y + 20), emoji_text, font=font_large, 
                         fill=text_color)
            
            # Add user info if available
            user_info_y = height - 150
            user_text = f"@{user.username}" if user.username else user.first_name
            if target_user:
                target_text = f"@{target_user.username}" if target_user.username else target_user.first_name
                user_text = f"{user_text} → {target_text}"
            
            user_font = ImageFont.truetype(font_path, 25) if font_path else ImageFont.load_default()
            user_width = draw.textlength(user_text, font=user_font)
            draw.text(((width - user_width) // 2, user_info_y), user_text, 
                     font=user_font, fill=(150, 150, 150))
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            time_width = draw.textlength(timestamp, font=user_font)
            draw.text(((width - time_width) // 2, user_info_y + 40), timestamp,
                     font=user_font, fill=(100, 100, 100))
            
            # Add bot signature
            bot_signature = "Roastify 😈"
            sig_width = draw.textlength(bot_signature, font=user_font)
            draw.text(((width - sig_width) // 2, user_info_y + 80), bot_signature,
                     font=user_font, fill=theme["colors"]["accent"])
            
            # Apply visual effects from config
            if self.config["visual_elements"]["glow_effect"]:
                image = self._add_glow_effect(Image.fromarray(np.array(image)), 
                                             template.get("border_color", theme["colors"]["accent"]))
            
            if self.config["visual_elements"]["cinematic_lighting"]:
                image = self._add_cinematic_lighting(image, theme)
            
            if self.config["visual_elements"]["background_blur"]:
                # Convert to array for blur
                import numpy as np
                img_array = np.array(image)
                # Simple blur effect
                from PIL import ImageFilter
                image = image.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Add border
            border_path = self._get_random_border()
            if border_path and os.path.exists(border_path):
                try:
                    border = Image.open(border_path).convert("RGBA")
                    border = border.resize((width, height), Image.Resampling.LANCZOS)
                    image = Image.alpha_composite(image.convert("RGBA"), border)
                except Exception as e:
                    logger.warning(f"Could not apply border: {e}")
            
            # Convert back to RGB for saving
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            
            # Save image
            temp_dir = PATHS["temp"]
            os.makedirs(temp_dir, exist_ok=True)
            filename = f"roast_{user.id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(temp_dir, filename)
            
            image.save(filepath, 'PNG', quality=95)
            logger.info(f"Image generated: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            # Return a default image path or raise
            raise
    
    def _apply_background_effects(self, image: Image.Image, effects: List[str], 
                                 theme: Dict) -> Image.Image:
        """Apply background effects to image"""
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        for effect in effects:
            if effect == "gradient":
                # Apply vertical gradient
                for y in range(height):
                    factor = y / height
                    r = int(theme["colors"]["primary"][0] * (1 - factor) + 
                           theme["colors"]["secondary"][0] * factor)
                    g = int(theme["colors"]["primary"][1] * (1 - factor) + 
                           theme["colors"]["secondary"][1] * factor)
                    b = int(theme["colors"]["primary"][2] * (1 - factor) + 
                           theme["colors"]["secondary"][2] * factor)
                    draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            elif effect == "grid":
                # Add grid lines
                grid_color = (100, 100, 100, 50)
                for x in range(0, width, 50):
                    draw.line([(x, 0), (x, height)], fill=grid_color)
                for y in range(0, height, 50):
                    draw.line([(0, y), (width, y)], fill=grid_color)
            
            elif effect == "noise":
                # Add subtle noise
                import random
                for _ in range(1000):
                    x = random.randint(0, width-1)
                    y = random.randint(0, height-1)
                    draw.point((x, y), fill=(255, 255, 255, random.randint(0, 30)))
        
        return image
    
    async def generate_diagram_image(self, data: Dict) -> str:
        """Generate a diagram image based on data"""
        try:
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Get random font
            font_path = self._get_random_font()
            try:
                font = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Draw diagram title
            title = data.get("title", "Diagram")
            text_width = draw.textlength(title, font=font)
            draw.text(((width - text_width) // 2, 50), title, font=font, fill=(0, 0, 0))
            
            # Draw simple bar chart or diagram based on data
            if "values" in data:
                values = data["values"]
                max_value = max(values) if values else 1
                bar_width = width // (len(values) + 2)
                
                for i, value in enumerate(values):
                    x = (i + 1) * bar_width
                    bar_height = (value / max_value) * (height - 300)
                    y = height - 150 - bar_height
                    
                    # Draw bar
                    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                    draw.rectangle([x, y, x + bar_width - 20, height - 150], fill=color)
                    
                    # Draw value label
                    label = str(value)
                    label_width = draw.textlength(label, font=font)
                    draw.text((x + (bar_width - label_width) // 2, height - 100), 
                             label, font=font, fill=(0, 0, 0))
            
            # Add border
            border_path = self._get_random_border()
            if border_path and os.path.exists(border_path):
                try:
                    border = Image.open(border_path).convert("RGBA")
                    border = border.resize((width, height), Image.Resampling.LANCZOS)
                    image = Image.alpha_composite(image.convert("RGBA"), border)
                except Exception as e:
                    logger.warning(f"Could not apply border to diagram: {e}")
            
            # Save diagram
            temp_dir = PATHS["temp"]
            filename = f"diagram_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(temp_dir, filename)
            
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            
            image.save(filepath, 'PNG', quality=95)
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating diagram: {e}")
            # Create a simple error diagram
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (255, 200, 200))
            draw = ImageDraw.Draw(image)
            
            error_text = "Diagram Error"
            font = ImageFont.load_default()
            text_width = draw.textlength(error_text, font=font)
            draw.text(((width - text_width) // 2, height // 2), error_text, 
                     font=font, fill=(255, 0, 0))
            
            temp_dir = PATHS["temp"]
            filepath = os.path.join(temp_dir, f"error_diagram_{int(datetime.now().timestamp())}.png")
            image.save(filepath, 'PNG')
            return filepath