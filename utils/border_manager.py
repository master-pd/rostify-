#!/usr/bin/env python3
"""
Border Manager for Roastify Bot
Manages random border selection and border image processing
"""

import os
import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageOps, ImageFilter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import BORDERS, PATHS
except ImportError:
    logger.error("Config module not found")
    sys.exit(1)


class BorderManager:
    """Manages border images and their random selection"""
    
    def __init__(self):
        """Initialize border manager"""
        self.config = BORDERS
        self.borders_dir = PATHS["borders"]
        
        # Load available borders
        self.available_borders = self._load_borders()
        
        # Track recent usage
        self.recent_borders = []
        
        logger.info(f"Border Manager initialized with {len(self.available_borders)} borders")
    
    def _load_borders(self) -> List[str]:
        """Load border images from directory"""
        borders = []
        
        # Check for border files in directory
        if os.path.exists(self.borders_dir):
            # Get all image files
            image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
            
            for filename in os.listdir(self.borders_dir):
                if any(filename.lower().endswith(ext) for ext in image_extensions):
                    border_path = os.path.join(self.borders_dir, filename)
                    borders.append(border_path)
        
        # If no borders found, create default ones
        if not borders:
            borders = self._create_default_borders()
        
        return borders
    
    def _create_default_borders(self) -> List[str]:
        """Create default border images"""
        borders = []
        
        # Create borders directory if it doesn't exist
        os.makedirs(self.borders_dir, exist_ok=True)
        
        # Create 10 different border styles
        border_styles = [
            ("rounded_red", (255, 0, 0, 180), "rounded"),
            ("double_blue", (0, 120, 255, 200), "double"),
            ("dotted_green", (0, 200, 0, 150), "dotted"),
            ("neon_purple", (180, 0, 255, 220), "neon"),
            ("golden", (255, 215, 0, 200), "gold"),
            ("silver", (192, 192, 192, 180), "silver"),
            ("gradient_rainbow", None, "gradient"),
            ("ornate_black", (0, 0, 0, 200), "ornate"),
            ("simple_white", (255, 255, 255, 150), "simple"),
            ("shadow_3d", (50, 50, 50, 200), "shadow")
        ]
        
        for i, (name, color, style) in enumerate(border_styles, 1):
            border_path = os.path.join(self.borders_dir, f"border_{i}.png")
            self._create_border_image(border_path, color, style)
            borders.append(border_path)
        
        logger.info(f"Created {len(borders)} default borders")
        return borders
    
    def _create_border_image(self, filepath: str, color: Tuple, style: str):
        """Create a border image with specific style"""
        try:
            # Create transparent image
            img = Image.new('RGBA', (1100, 1100), (0, 0, 0, 0))
            
            if style == "rounded":
                self._draw_rounded_border(img, color)
            elif style == "double":
                self._draw_double_border(img, color)
            elif style == "dotted":
                self._draw_dotted_border(img, color)
            elif style == "neon":
                self._draw_neon_border(img, color)
            elif style == "gold":
                self._draw_golden_border(img)
            elif style == "silver":
                self._draw_silver_border(img)
            elif style == "gradient":
                self._draw_gradient_border(img)
            elif style == "ornate":
                self._draw_ornate_border(img, color)
            elif style == "simple":
                self._draw_simple_border(img, color)
            elif style == "shadow":
                self._draw_shadow_border(img, color)
            
            # Save the border
            img.save(filepath, 'PNG')
            logger.debug(f"Created border: {filepath}")
            
        except Exception as e:
            logger.error(f"Error creating border: {e}")
    
    def _draw_rounded_border(self, img: Image.Image, color: Tuple):
        """Draw rounded rectangle border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Outer rounded rectangle
        draw.rounded_rectangle([50, 50, 1050, 1050], radius=100, 
                              outline=color, width=25)
        
        # Inner rounded rectangle
        draw.rounded_rectangle([100, 100, 1000, 1000], radius=80,
                              outline=color, width=15)
    
    def _draw_double_border(self, img: Image.Image, color: Tuple):
        """Draw double line border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Outer border
        draw.rectangle([30, 30, 1070, 1070], outline=color, width=20)
        
        # Inner border with offset
        draw.rectangle([80, 80, 1020, 1020], outline=color, width=15)
        
        # Middle border
        draw.rectangle([150, 150, 950, 950], outline=color, width=10)
    
    def _draw_dotted_border(self, img: Image.Image, color: Tuple):
        """Draw dotted border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Draw dots around the border
        dot_radius = 12
        spacing = 40
        
        # Top and bottom rows
        for x in range(50, 1051, spacing):
            # Top dots
            draw.ellipse([x-dot_radius, 50-dot_radius, x+dot_radius, 50+dot_radius], 
                        fill=color)
            # Bottom dots
            draw.ellipse([x-dot_radius, 1050-dot_radius, x+dot_radius, 1050+dot_radius], 
                        fill=color)
        
        # Left and right columns
        for y in range(50, 1051, spacing):
            # Left dots
            draw.ellipse([50-dot_radius, y-dot_radius, 50+dot_radius, y+dot_radius], 
                        fill=color)
            # Right dots
            draw.ellipse([1050-dot_radius, y-dot_radius, 1050+dot_radius, y+dot_radius], 
                        fill=color)
    
    def _draw_neon_border(self, img: Image.Image, color: Tuple):
        """Draw neon glow border"""
        from PIL import ImageDraw, ImageFilter
        draw = ImageDraw.Draw(img)
        
        # Draw main border with glow effect
        border_color = color
        glow_color = (min(255, color[0]+100), min(255, color[1]+100), 
                     min(255, color[2]+100), color[3])
        
        # Outer glow (blurred)
        for i in range(3):
            width = 30 - i*5
            offset = i * 3
            draw.rectangle([50+offset, 50+offset, 1050-offset, 1050-offset],
                          outline=glow_color, width=width)
        
        # Main border
        draw.rectangle([60, 60, 1040, 1040], outline=border_color, width=15)
        
        # Add inner glow
        inner_glow = (min(255, color[0]+50), min(255, color[1]+50), 
                     min(255, color[2]+50), color[3])
        draw.rectangle([90, 90, 1010, 1010], outline=inner_glow, width=5)
    
    def _draw_golden_border(self, img: Image.Image):
        """Draw golden border with gradient"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Golden gradient colors
        gold_colors = [
            (255, 215, 0, 200),  # Gold
            (255, 195, 0, 180),  # Dark gold
            (218, 165, 32, 160),  # Golden rod
            (184, 134, 11, 140)   # Dark golden rod
        ]
        
        # Draw layered border
        for i, color in enumerate(gold_colors):
            offset = i * 10
            width = 20 - i*3
            draw.rectangle([50+offset, 50+offset, 1050-offset, 1050-offset],
                          outline=color, width=width)
    
    def _draw_silver_border(self, img: Image.Image):
        """Draw silver metallic border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Silver gradient colors
        silver_colors = [
            (192, 192, 192, 200),  # Silver
            (169, 169, 169, 180),  # Dark gray
            (211, 211, 211, 160),  # Light gray
            (220, 220, 220, 140)   # Gainsboro
        ]
        
        # Draw layered border
        for i, color in enumerate(silver_colors):
            offset = i * 15
            width = 18 - i*2
            draw.rectangle([50+offset, 50+offset, 1050-offset, 1050-offset],
                          outline=color, width=width)
    
    def _draw_gradient_border(self, img: Image.Image):
        """Draw rainbow gradient border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Rainbow colors
        rainbow_colors = [
            (255, 0, 0, 200),      # Red
            (255, 165, 0, 200),    # Orange
            (255, 255, 0, 200),    # Yellow
            (0, 255, 0, 200),      # Green
            (0, 0, 255, 200),      # Blue
            (75, 0, 130, 200),     # Indigo
            (238, 130, 238, 200)   # Violet
        ]
        
        # Calculate segment size
        border_length = 4000  # Perimeter approximation
        segment_length = border_length // len(rainbow_colors)
        
        # Draw each color segment (simplified - full border per color)
        for i, color in enumerate(rainbow_colors):
            offset = i * 10
            draw.rectangle([50+offset, 50+offset, 1050-offset, 1050-offset],
                          outline=color, width=10)
    
    def _draw_ornate_border(self, img: Image.Image, color: Tuple):
        """Draw ornate decorative border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Main border
        draw.rectangle([40, 40, 1060, 1060], outline=color, width=25)
        
        # Corner decorations
        corner_size = 80
        
        # Top-left corner
        draw.arc([40, 40, 40+corner_size*2, 40+corner_size*2], 
                 start=180, end=270, fill=color, width=15)
        
        # Top-right corner
        draw.arc([1060-corner_size*2, 40, 1060, 40+corner_size*2],
                 start=270, end=360, fill=color, width=15)
        
        # Bottom-left corner
        draw.arc([40, 1060-corner_size*2, 40+corner_size*2, 1060],
                 start=90, end=180, fill=color, width=15)
        
        # Bottom-right corner
        draw.arc([1060-corner_size*2, 1060-corner_size*2, 1060, 1060],
                 start=0, end=90, fill=color, width=15)
        
        # Decorative dots at corners
        dot_positions = [
            (40+corner_size, 40+corner_size),
            (1060-corner_size, 40+corner_size),
            (40+corner_size, 1060-corner_size),
            (1060-corner_size, 1060-corner_size)
        ]
        
        for x, y in dot_positions:
            draw.ellipse([x-10, y-10, x+10, y+10], fill=color)
    
    def _draw_simple_border(self, img: Image.Image, color: Tuple):
        """Draw simple clean border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([100, 100, 1000, 1000], outline=color, width=10)
    
    def _draw_shadow_border(self, img: Image.Image, color: Tuple):
        """Draw 3D shadow border"""
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Shadow effect (darker)
        shadow_color = (color[0]//2, color[1]//2, color[2]//2, color[3])
        draw.rectangle([55, 55, 1055, 1055], outline=shadow_color, width=20)
        
        # Main border (raised effect)
        draw.rectangle([50, 50, 1050, 1050], outline=color, width=15)
        
        # Highlight effect (lighter)
        highlight_color = (min(255, color[0]+50), min(255, color[1]+50), 
                         min(255, color[2]+50), color[3])
        draw.rectangle([45, 45, 1045, 1045], outline=highlight_color, width=5)
    
    def get_random_border(self) -> Optional[str]:
        """Get a random border file path"""
        if not self.available_borders:
            logger.warning("No borders available")
            return None
        
        # Apply repetition avoidance
        no_repeat_until = self.config.get("no_repeat_until", 5)
        
        # Filter out recently used borders
        available = [b for b in self.available_borders 
                    if b not in self.recent_borders[-no_repeat_until:]]
        
        # If all borders recently used, use any
        if not available:
            available = self.available_borders
        
        # Select random border
        selected = random.choice(available)
        
        # Update recent borders
        self.recent_borders.append(selected)
        if len(self.recent_borders) > 15:  # Keep last 15
            self.recent_borders.pop(0)
        
        logger.debug(f"Selected border: {os.path.basename(selected)}")
        return selected
    
    def apply_border_to_image(self, image_path: str, border_path: str, 
                             output_path: str) -> bool:
        """Apply border to an image"""
        try:
            # Load images
            image = Image.open(image_path).convert("RGBA")
            border = Image.open(border_path).convert("RGBA")
            
            # Resize border to match image
            border = border.resize(image.size, Image.Resampling.LANCZOS)
            
            # Composite images
            result = Image.new('RGBA', image.size, (0, 0, 0, 0))
            result = Image.alpha_composite(result, image)
            result = Image.alpha_composite(result, border)
            
            # Save result
            result.save(output_path, 'PNG', quality=95)
            
            logger.debug(f"Applied border to image: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error applying border: {e}")
            return False
    
    def create_custom_border(self, width: int, height: int, 
                            border_type: str = "simple",
                            color: Tuple = (255, 255, 255, 200)) -> Optional[Image.Image]:
        """Create a custom border image on the fly"""
        try:
            # Create transparent image
            border = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            
            from PIL import ImageDraw
            draw = ImageDraw.Draw(border)
            
            # Draw based on border type
            if border_type == "simple":
                draw.rectangle([10, 10, width-10, height-10], 
                              outline=color, width=10)
            
            elif border_type == "rounded":
                draw.rounded_rectangle([20, 20, width-20, height-20], 
                                      radius=30, outline=color, width=15)
            
            elif border_type == "double":
                draw.rectangle([15, 15, width-15, height-15], 
                              outline=color, width=8)
                draw.rectangle([30, 30, width-30, height-30], 
                              outline=color, width=5)
            
            elif border_type == "dotted":
                dot_spacing = 30
                dot_radius = 5
                
                # Top and bottom
                for x in range(20, width-20, dot_spacing):
                    draw.ellipse([x-dot_radius, 20-dot_radius, 
                                 x+dot_radius, 20+dot_radius], fill=color)
                    draw.ellipse([x-dot_radius, height-20-dot_radius,
                                 x+dot_radius, height-20+dot_radius], fill=color)
                
                # Left and right
                for y in range(20, height-20, dot_spacing):
                    draw.ellipse([20-dot_radius, y-dot_radius,
                                 20+dot_radius, y+dot_radius], fill=color)
                    draw.ellipse([width-20-dot_radius, y-dot_radius,
                                 width-20+dot_radius, y+dot_radius], fill=color)
            
            return border
            
        except Exception as e:
            logger.error(f"Error creating custom border: {e}")
            return None
    
    def get_border_stats(self) -> Dict[str, Any]:
        """Get border usage statistics"""
        return {
            "total_borders": len(self.available_borders),
            "recently_used": len(self.recent_borders),
            "border_files": [os.path.basename(b) for b in self.available_borders],
            "recent_border_files": [os.path.basename(b) for b in self.recent_borders[-5:]]
        }
    
    def add_border_file(self, filepath: str) -> bool:
        """Add a new border file"""
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"Border file not found: {filepath}")
                return False
            
            # Copy to borders directory
            import shutil
            filename = os.path.basename(filepath)
            dest_path = os.path.join(self.borders_dir, filename)
            
            shutil.copy2(filepath, dest_path)
            
            # Reload borders
            self.available_borders = self._load_borders()
            
            logger.info(f"Added new border: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding border file: {e}")
            return False
    
    def remove_border_file(self, filename: str) -> bool:
        """Remove a border file"""
        try:
            border_path = os.path.join(self.borders_dir, filename)
            
            if not os.path.exists(border_path):
                logger.error(f"Border file not found: {border_path}")
                return False
            
            # Remove file
            os.remove(border_path)
            
            # Remove from available borders if present
            if border_path in self.available_borders:
                self.available_borders.remove(border_path)
            
            # Remove from recent borders if present
            if border_path in self.recent_borders:
                self.recent_borders.remove(border_path)
            
            logger.info(f"Removed border: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing border file: {e}")
            return False
    
    def scan_for_new_borders(self) -> List[str]:
        """Scan for new border files in directory"""
        old_count = len(self.available_borders)
        
        # Reload borders
        self.available_borders = self._load_borders()
        
        new_count = len(self.available_borders)
        
        if new_count > old_count:
            logger.info(f"Found {new_count - old_count} new borders")
        
        return self.available_borders