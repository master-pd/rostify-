#!/usr/bin/env python3
"""
Festival Mode for Roastify Bot
Special themes and features for festivals
"""

import json
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
from PIL import Image, ImageDraw, ImageFont

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import EXTRA_FEATURES, PATHS
    from utils.helpers import Helpers
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class FestivalMode:
    """Manages festival-themed features"""
    
    def __init__(self):
        """Initialize festival mode"""
        self.config = EXTRA_FEATURES.get("festival_event_mode", {})
        
        # Load festival data
        self.festivals = self._load_festivals()
        
        # Current active festival
        self.active_festival = None
        self.festival_end_time = None
        
        # Festival-specific templates and settings
        self.festival_templates = {}
        self.festival_colors = {}
        
        logger.info("Festival Mode initialized")
    
    def _load_festivals(self) -> Dict[str, Dict]:
        """Load festival definitions"""
        festivals = {
            "pohela_boishakh": {
                "name": "পহেলা বৈশাখ",
                "english_name": "Bengali New Year",
                "date": (4, 14),  # April 14
                "duration_days": 3,
                "colors": [(255, 0, 0), (255, 255, 0), (0, 128, 0)],  # Red, Yellow, Green
                "emoji": "🎉",
                "greeting": "শুভ নববর্ষ!",
                "templates": ["festival_boishakh_1", "festival_boishakh_2"],
                "special_roasts": True,
                "special_backgrounds": True
            },
            "eid": {
                "name": "ঈদ উল ফিতর",
                "english_name": "Eid al-Fitr",
                "date": None,  # Islamic calendar - calculated
                "duration_days": 3,
                "colors": [(0, 150, 0), (255, 255, 255), (0, 100, 0)],  # Green, White
                "emoji": "🌙",
                "greeting": "ঈদ মোবারক!",
                "templates": ["festival_eid_1", "festival_eid_2"],
                "special_roasts": True,
                "special_backgrounds": True
            },
            "durga_puja": {
                "name": "দুর্গা পূজা",
                "english_name": "Durga Puja",
                "date": (10, 1),  # October (variable)
                "duration_days": 5,
                "colors": [(255, 0, 0), (255, 165, 0), (139, 0, 139)],  # Red, Orange, Purple
                "emoji": "🪔",
                "greeting": "শুভ দুর্গা পূজা!",
                "templates": ["festival_durga_1", "festival_durga_2"],
                "special_roasts": True,
                "special_backgrounds": True
            },
            "christmas": {
                "name": "ক্রিসমাস",
                "english_name": "Christmas",
                "date": (12, 25),
                "duration_days": 7,
                "colors": [(255, 0, 0), (0, 128, 0), (255, 255, 255)],  # Red, Green, White
                "emoji": "🎄",
                "greeting": "শুভ বড়দিন!",
                "templates": ["festival_christmas_1", "festival_christmas_2"],
                "special_roasts": True,
                "special_backgrounds": True
            },
            "halloween": {
                "name": "হ্যালোউইন",
                "english_name": "Halloween",
                "date": (10, 31),
                "duration_days": 2,
                "colors": [(255, 165, 0), (0, 0, 0), (128, 0, 128)],  # Orange, Black, Purple
                "emoji": "🎃",
                "greeting": "হ্যালোউইনের শুভেচ্ছা!",
                "templates": ["festival_halloween_1", "festival_halloween_2"],
                "special_roasts": True,
                "special_backgrounds": True
            },
            "new_year": {
                "name": "নতুন বছর",
                "english_name": "New Year",
                "date": (12, 31),
                "duration_days": 2,
                "colors": [(255, 215, 0), (255, 255, 255), (0, 0, 0)],  # Gold, White, Black
                "emoji": "🎆",
                "greeting": "নতুন বছরের শুভেচ্ছা!",
                "templates": ["festival_newyear_1", "festival_newyear_2"],
                "special_roasts": True,
                "special_backgrounds": True
            }
        }
        
        # Load from file if exists
        festivals_file = os.path.join(PATHS["templates"], "festivals.json")
        if os.path.exists(festivals_file):
            try:
                with open(festivals_file, 'r', encoding='utf-8') as f:
                    file_festivals = json.load(f)
                    festivals.update(file_festivals)
            except Exception as e:
                logger.error(f"Error loading festivals: {e}")
        
        return festivals
    
    def check_festival(self) -> Optional[Dict]:
        """Check if any festival is currently active"""
        today = datetime.now()
        current_date = (today.month, today.day)
        
        for festival_id, festival_data in self.festivals.items():
            festival_date = festival_data.get("date")
            
            if festival_date:
                # Check if today matches festival date
                if current_date == festival_date:
                    self.active_festival = festival_id
                    duration = festival_data.get("duration_days", 1)
                    self.festival_end_time = today + timedelta(days=duration)
                    
                    logger.info(f"Festival detected: {festival_data['name']}")
                    return festival_data
            
            # For Islamic festivals, we need special calculation
            # This is simplified - in production use hijri-converter
        
        # Clear if festival period ended
        if self.active_festival and self.festival_end_time:
            if today > self.festival_end_time:
                logger.info(f"Festival ended: {self.active_festival}")
                self.active_festival = None
                self.festival_end_time = None
        
        return None
    
    def is_festival_active(self) -> bool:
        """Check if festival mode is active"""
        return self.active_festival is not None
    
    def get_active_festival(self) -> Optional[Dict]:
        """Get active festival data"""
        if not self.active_festival:
            return None
        
        return self.festivals.get(self.active_festival)
    
    def get_festival_greeting(self) -> str:
        """Get festival greeting message"""
        festival = self.get_active_festival()
        
        if festival:
            return f"{festival['emoji']} {festival['greeting']} {festival['emoji']}"
        
        return ""
    
    def get_festival_colors(self) -> List[Tuple[int, int, int]]:
        """Get festival colors"""
        festival = self.get_active_festival()
        
        if festival:
            return festival.get("colors", [(255, 255, 255)])
        
        # Default colors
        return [(255, 255, 255), (200, 200, 200), (150, 150, 150)]
    
    def get_random_festival_color(self) -> Tuple[int, int, int]:
        """Get random color from festival palette"""
        colors = self.get_festival_colors()
        return random.choice(colors)
    
    def get_festival_template(self) -> Optional[str]:
        """Get festival-specific template"""
        festival = self.get_active_festival()
        
        if festival:
            templates = festival.get("templates", [])
            if templates:
                return random.choice(templates)
        
        return None
    
    def get_festival_background(self) -> Optional[str]:
        """Get festival background image path"""
        if not self.active_festival:
            return None
        
        backgrounds_dir = os.path.join(PATHS["backgrounds"], "festivals")
        background_file = os.path.join(backgrounds_dir, f"{self.active_festival}.png")
        
        if os.path.exists(background_file):
            return background_file
        
        # Create default festival background
        return self._create_festival_background()
    
    def _create_festival_background(self) -> Optional[str]:
        """Create festival background image"""
        try:
            festival = self.get_active_festival()
            if not festival:
                return None
            
            # Create background
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (30, 30, 30))
            draw = ImageDraw.Draw(image)
            
            # Get festival colors
            colors = festival.get("colors", [(255, 255, 255)])
            
            # Draw festival pattern
            pattern_size = 100
            for y in range(0, height, pattern_size):
                for x in range(0, width, pattern_size):
                    color = random.choice(colors)
                    
                    # Draw pattern based on festival
                    if self.active_festival == "pohela_boishakh":
                        # Alpana pattern
                        draw.ellipse([x+10, y+10, x+90, y+90], 
                                    outline=color, width=5)
                    elif self.active_festival == "eid":
                        # Crescent pattern
                        draw.arc([x+20, y+20, x+80, y+80], 
                                start=30, end=330, fill=color, width=8)
                    elif self.active_festival == "durga_puja":
                        # Lotus pattern
                        for i in range(8):
                            angle = i * 45
                            rad = angle * 3.14159 / 180
                            x1 = x + 50 + int(30 * math.cos(rad))
                            y1 = y + 50 + int(30 * math.sin(rad))
                            x2 = x + 50 + int(15 * math.cos(rad + 0.5))
                            y2 = y + 50 + int(15 * math.sin(rad + 0.5))
                            draw.line([(x+50, y+50), (x1, y1)], fill=color, width=3)
                    elif self.active_festival == "christmas":
                        # Star pattern
                        points = []
                        for i in range(5):
                            angle = 90 + i * 72
                            rad = angle * 3.14159 / 180
                            px = x + 50 + int(40 * math.cos(rad))
                            py = y + 50 + int(40 * math.sin(rad))
                            points.append((px, py))
                        draw.polygon(points, outline=color, width=4)
            
            # Add festival name
            try:
                font = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 60)
                festival_name = festival["name"]
                bbox = draw.textbbox((0, 0), festival_name, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                draw.text((text_x, height - 100), festival_name, 
                         font=font, fill=colors[0])
            except:
                pass
            
            # Save background
            os.makedirs(os.path.join(PATHS["backgrounds"], "festivals"), exist_ok=True)
            background_file = os.path.join(PATHS["backgrounds"], "festivals", 
                                          f"{self.active_festival}.png")
            
            image.save(background_file, 'PNG', quality=95)
            
            return background_file
            
        except Exception as e:
            logger.error(f"Error creating festival background: {e}")
            return None
    
    def get_festival_roast(self, original_roast: str) -> str:
        """Add festival flavor to roast"""
        if not self.active_festival:
            return original_roast
        
        festival = self.get_active_festival()
        festival_name = festival["name"]
        emoji = festival["emoji"]
        
        festival_prefixes = [
            f"{festival_name} উপলক্ষে বিশেষ রোস্ট! {emoji}",
            f"{festival_name} এর শুভেচ্ছা সহ! {emoji}",
            f"{festival_name} স্পেশাল! {emoji}",
            f"{emoji} {festival_name} রোস্ট! {emoji}"
        ]
        
        festival_suffixes = [
            f"\n\n{festival['greeting']} {emoji}",
            f"\n\n{festival_name} এর শুভেচ্ছা রইল!",
            f"\n\n{emoji} উৎসবের আনন্দে মাতো! {emoji}"
        ]
        
        prefix = random.choice(festival_prefixes)
        suffix = random.choice(festival_suffixes)
        
        return f"{prefix}\n\n{original_roast}{suffix}"
    
    def apply_festival_effects(self, image: Image.Image) -> Image.Image:
        """Apply festival effects to image"""
        if not self.active_festival:
            return image
        
        festival = self.get_active_festival()
        
        # Convert to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Create overlay with festival effects
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Add festival emoji corners
        emoji = festival["emoji"]
        colors = festival.get("colors", [(255, 255, 255)])
        
        try:
            # Try to load a font that might have the emoji
            font = ImageFont.truetype("seguiemj.ttf", 60)  # Windows emoji font
        except:
            font = ImageFont.load_default()
        
        # Draw emojis at corners
        positions = [
            (50, 50),  # Top-left
            (image.width - 100, 50),  # Top-right
            (50, image.height - 100),  # Bottom-left
            (image.width - 100, image.height - 100)  # Bottom-right
        ]
        
        for x, y in positions:
            draw.text((x, y), emoji, font=font, fill=(*colors[0], 100))
        
        # Add festive border
        border_color = (*colors[0], 150)
        draw.rectangle([20, 20, image.width-20, image.height-20], 
                      outline=border_color, width=15)
        
        # Composite images
        result = Image.alpha_composite(image, overlay)
        
        return result
    
    def create_festival_special_image(self, text: str, user_name: str) -> Optional[str]:
        """Create special festival image"""
        try:
            festival = self.get_active_festival()
            if not festival:
                return None
            
            # Create image
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (20, 20, 40))
            draw = ImageDraw.Draw(image)
            
            # Load font
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 70)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 45)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 35)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Get festival colors
            colors = festival.get("colors", [(255, 255, 255)])
            
            # Draw festival title
            title = f"{festival['emoji']} {festival['name']} {festival['emoji']}"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 80), title, font=font_large, fill=colors[0])
            
            # Draw greeting
            greeting = festival['greeting']
            greeting_bbox = draw.textbbox((0, 0), greeting, font=font_medium)
            greeting_width = greeting_bbox[2] - greeting_bbox[0]
            greeting_x = (width - greeting_width) // 2
            draw.text((greeting_x, 180), greeting, font=font_medium, fill=colors[1])
            
            # Draw text box
            text_box_y = 280
            text_box_height = 400
            text_box_color = (*colors[0], 30)
            draw.rectangle([100, text_box_y, width-100, text_box_y+text_box_height],
                          fill=text_box_color, outline=colors[1], width=5)
            
            # Draw user text
            wrapped_text = Helpers.truncate_text(text, 100)
            text_lines = self._wrap_text(draw, wrapped_text, font_medium, width-250)
            
            text_y = text_box_y + 50
            for line in text_lines:
                line_bbox = draw.textbbox((0, 0), line, font=font_medium)
                line_width = line_bbox[2] - line_bbox[0]
                line_x = (width - line_width) // 2
                draw.text((line_x, text_y), line, font=font_medium, fill=(255, 255, 255))
                text_y += 60
            
            # Draw user name
            user_text = f"শুভেচ্ছা: {user_name}"
            user_bbox = draw.textbbox((0, 0), user_text, font=font_small)
            user_width = user_bbox[2] - user_bbox[0]
            user_x = (width - user_width) // 2
            draw.text((user_x, text_box_y + text_box_height + 50), 
                     user_text, font=font_small, fill=colors[2])
            
            # Draw festival pattern
            self._draw_festival_pattern(draw, festival, width, height)
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"festival_{self.active_festival}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error creating festival image: {e}")
            return None
    
    def _wrap_text(self, draw: ImageDraw, text: str, font: ImageFont, 
                  max_width: int) -> List[str]:
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _draw_festival_pattern(self, draw: ImageDraw, festival: Dict, 
                              width: int, height: int):
        """Draw festival-specific pattern"""
        import math
        
        if self.active_festival == "pohela_boishakh":
            # Draw Alpana patterns
            colors = festival.get("colors", [(255, 255, 255)])
            for i in range(20):
                x = random.randint(100, width-100)
                y = random.randint(100, height-100)
                color = random.choice(colors)
                radius = random.randint(10, 30)
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                            outline=color, width=3)
        
        elif self.active_festival == "eid":
            # Draw crescents
            colors = festival.get("colors", [(255, 255, 255)])
            for i in range(15):
                x = random.randint(100, width-100)
                y = random.randint(100, height-100)
                color = random.choice(colors)
                size = random.randint(20, 50)
                draw.arc([x, y, x+size, y+size], 
                        start=30, end=330, fill=color, width=5)
        
        elif self.active_festival == "christmas":
            # Draw snowflakes
            for i in range(30):
                x = random.randint(100, width-100)
                y = random.randint(100, height-100)
                draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255))
    
    async def announce_festival(self, chat_id: int, context: Any):
        """Announce festival start"""
        try:
            festival = self.get_active_festival()
            if not festival:
                return
            
            # Create announcement message
            message = f"""
🎊 <b>ফেস্টিভাল মোড একটিভ!</b> 🎊

{festival['emoji']} <b>{festival['name']}</b> {festival['emoji']}

{festival['greeting']} সবাইকে!

✨ <b>বিশেষ ফিচারসমূহ:</b>
• ফেস্টিভাল থিমড রোস্ট
• বিশেষ ব্যাকগ্রাউন্ড
• ফেস্টিভাল কালার স্কিম
• স্পেশাল গ্রিটিংস

উৎসবের আনন্দে রোস্টের মজা দ্বিগুণ! 😊
            """
            
            # Send announcement
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML"
            )
            
            logger.info(f"Announced festival {festival['name']} in chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error announcing festival: {e}")
    
    def get_festival_stats(self) -> Dict[str, Any]:
        """Get festival mode statistics"""
        return {
            "active_festival": self.active_festival,
            "festival_end_time": self.festival_end_time,
            "total_festivals": len(self.festivals),
            "festival_list": list(self.festivals.keys())
        }
    
    def add_custom_festival(self, festival_id: str, festival_data: Dict) -> bool:
        """Add custom festival"""
        try:
            # Validate required fields
            required_fields = ["name", "colors", "emoji", "greeting"]
            for field in required_fields:
                if field not in festival_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add to festivals
            self.festivals[festival_id] = festival_data
            
            # Save to file
            festivals_file = os.path.join(PATHS["templates"], "festivals.json")
            Helpers.save_json(festivals_file, self.festivals)
            
            logger.info(f"Added custom festival: {festival_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding custom festival: {e}")
            return False