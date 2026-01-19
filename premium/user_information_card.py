"""
Premium User Information Card System v15.0
==========================================
Advanced, Image-Style User Information Card with Premium Features
No Pilot Integration | Standalone Implementation
"""

import os
import json
import random
import uuid
import hashlib
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# Image processing
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    import numpy as np
    HAS_IMAGE_LIBS = True
except ImportError:
    HAS_IMAGE_LIBS = False

# Data visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import cm
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Logging
import logging
logger = logging.getLogger(__name__)


class CardTheme(Enum):
    """Premium card themes"""
    DIAMOND = "diamond"
    NEO = "neo"
    CYBER = "cyber"
    GLASS = "glass"
    Holographic = "holographic"
    GOLD = "gold"
    SILVER = "silver"
    PLATINUM = "platinum"
    ROYAL = "royal"
    GALAXY = "galaxy"


@dataclass
class UserData:
    """User data structure"""
    id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    join_date: datetime
    total_roasts: int = 0
    upvotes: int = 0
    downvotes: int = 0
    rank: int = 0
    level: int = 1
    xp: int = 0
    badges: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    premium: bool = True
    theme: str = "diamond"
    analytics: Dict = field(default_factory=dict)


@dataclass
class CardConfig:
    """Card configuration"""
    width: int = 1200
    height: int = 800
    corner_radius: int = 40
    padding: int = 50
    shadow_blur: int = 20
    shadow_offset: Tuple[int, int] = (10, 10)
    shadow_color: str = "#00000040"
    border_width: int = 4
    border_color: str = "#FFD700"
    bg_opacity: int = 230


class PremiumBadge:
    """Premium badge system"""
    
    BADGES = {
        "veteran": {"name": "🎖️ Veteran", "color": "#FFD700", "desc": "100+ roasts"},
        "elite": {"name": "👑 Elite", "color": "#C0C0C0", "desc": "Top 10 ranking"},
        "creative": {"name": "🎨 Creative", "color": "#FF6B6B", "desc": "50+ custom roasts"},
        "social": {"name": "🤝 Social", "color": "#00C851", "desc": "500+ votes received"},
        "fast": {"name": "⚡ Speedster", "color": "#33B5E5", "desc": "Fastest response"},
        "funny": {"name": "😂 Comedian", "color": "#FF8800", "desc": "Most funny roasts"},
        "clever": {"name": "🧠 Genius", "color": "#AA66CC", "desc": "Most clever roasts"},
        "helpful": {"name": "🌟 Helper", "color": "#FFBB33", "desc": "Helped other users"},
        "legend": {"name": "🏆 Legend", "color": "#FF4444", "desc": "All badges unlocked"},
        "premium": {"name": "💎 Premium", "color": "#00D2FF", "desc": "Premium member"},
        "active": {"name": "🔥 Active", "color": "#FF5252", "desc": "Daily user"},
        "popular": {"name": "⭐ Popular", "color": "#FFD740", "desc": "High upvote ratio"}
    }
    
    @classmethod
    def get_badges_for_user(cls, user_data: UserData) -> List[Dict]:
        """Get badges user has earned"""
        badges = []
        
        # Always add premium badge
        badges.append(cls.BADGES["premium"])
        
        # Check conditions
        if user_data.total_roasts >= 100:
            badges.append(cls.BADGES["veteran"])
        
        if user_data.rank <= 10 and user_data.rank > 0:
            badges.append(cls.BADGES["elite"])
        
        if user_data.upvotes >= 500:
            badges.append(cls.BADGES["social"])
        
        vote_ratio = user_data.upvotes / max(user_data.upvotes + user_data.downvotes, 1)
        if vote_ratio >= 0.8:
            badges.append(cls.BADGES["popular"])
        
        if len(user_data.badges) >= 3:
            badges.append(cls.BADGES["legend"])
        
        return badges


class ThemeManager:
    """Theme manager for cards"""
    
    THEMES = {
        "diamond": {
            "name": "💎 Diamond",
            "primary": "#FFD700",
            "secondary": "#FFFFFF",
            "accent": "#B9F2FF",
            "danger": "#FF6B6B",
            "success": "#00D26A",
            "bg_gradient": ["#0F2027", "#203A43", "#2C5364"],
            "text_color": "#FFFFFF",
            "glass_effect": True,
            "glow": True
        },
        "neo": {
            "name": "🌌 Neo Cyber",
            "primary": "#00FFFF",
            "secondary": "#FF00FF",
            "accent": "#00FF00",
            "danger": "#FF5555",
            "success": "#55FF55",
            "bg_gradient": ["#000428", "#004e92", "#000428"],
            "text_color": "#FFFFFF",
            "glass_effect": True,
            "glow": True,
            "neon": True
        },
        "gold": {
            "name": "🏆 Gold Elite",
            "primary": "#FFD700",
            "secondary": "#FFA500",
            "accent": "#FF8C00",
            "danger": "#FF3333",
            "success": "#33CC33",
            "bg_gradient": ["#1A1A1A", "#333333", "#1A1A1A"],
            "text_color": "#FFD700",
            "glass_effect": False,
            "metallic": True
        },
        "silver": {
            "name": "⚡ Silver Pro",
            "primary": "#C0C0C0",
            "secondary": "#E8E8E8",
            "accent": "#A0A0A0",
            "danger": "#FF6666",
            "success": "#66FF66",
            "bg_gradient": ["#2B2B2B", "#4A4A4A", "#2B2B2B"],
            "text_color": "#FFFFFF",
            "glass_effect": True,
            "chrome": True
        },
        "platinum": {
            "name": "🔮 Platinum VIP",
            "primary": "#E5E4E2",
            "secondary": "#C0C0C0",
            "accent": "#A0A0A0",
            "danger": "#FF7777",
            "success": "#77FF77",
            "bg_gradient": ["#16222A", "#3A6073", "#16222A"],
            "text_color": "#E5E4E2",
            "glass_effect": True,
            "crystal": True
        },
        "royal": {
            "name": "👑 Royal",
            "primary": "#9370DB",
            "secondary": "#8A2BE2",
            "accent": "#4B0082",
            "danger": "#FF4500",
            "success": "#32CD32",
            "bg_gradient": ["#23074d", "#cc5333", "#23074d"],
            "text_color": "#FFFFFF",
            "glass_effect": True,
            "royal": True
        },
        "galaxy": {
            "name": "🌠 Galaxy",
            "primary": "#9D50BB",
            "secondary": "#6E48AA",
            "accent": "#4776E6",
            "danger": "#FF416C",
            "success": "#36D1DC",
            "bg_gradient": ["#0B0B3B", "#1F1F7A", "#0B0B3B"],
            "text_color": "#FFFFFF",
            "glass_effect": True,
            "stars": True
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name: str) -> Dict:
        """Get theme configuration"""
        return cls.THEMES.get(theme_name, cls.THEMES["diamond"])
    
    @classmethod
    def get_random_theme(cls) -> Dict:
        """Get random theme"""
        return random.choice(list(cls.THEMES.values()))


class GraphicsEngine:
    """Advanced graphics engine for card generation"""
    
    def __init__(self):
        self.config = CardConfig()
        self.font_cache = {}
        logger.info("GraphicsEngine initialized")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def hex_to_rgba(self, hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
        """Convert hex color to RGBA"""
        rgb = self.hex_to_rgb(hex_color)
        return (*rgb, alpha)
    
    def create_gradient(self, width: int, height: int, colors: List[str], 
                       direction: str = "diagonal") -> Image.Image:
        """Create gradient background"""
        if not HAS_IMAGE_LIBS:
            return Image.new('RGB', (width, height), color=(30, 30, 30))
        
        # Create base image
        base = Image.new('RGB', (width, height), color=self.hex_to_rgb(colors[0]))
        draw = ImageDraw.Draw(base)
        
        # Simple gradient implementation
        if direction == "vertical":
            for i in range(height):
                ratio = i / height
                color_idx = int(ratio * (len(colors) - 1))
                color1 = self.hex_to_rgb(colors[color_idx])
                color2 = self.hex_to_rgb(colors[min(color_idx + 1, len(colors) - 1)])
                
                # Interpolate
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        elif direction == "horizontal":
            for i in range(width):
                ratio = i / width
                color_idx = int(ratio * (len(colors) - 1))
                color1 = self.hex_to_rgb(colors[color_idx])
                color2 = self.hex_to_rgb(colors[min(color_idx + 1, len(colors) - 1)])
                
                # Interpolate
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                draw.line([(i, 0), (i, height)], fill=(r, g, b))
        
        else:  # diagonal
            for i in range(width):
                for j in range(height):
                    ratio = (i + j) / (width + height)
                    color_idx = int(ratio * (len(colors) - 1))
                    color1 = self.hex_to_rgb(colors[color_idx])
                    color2 = self.hex_to_rgb(colors[min(color_idx + 1, len(colors) - 1)])
                    
                    # Interpolate
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    
                    draw.point((i, j), fill=(r, g, b))
        
        return base
    
    def apply_glass_effect(self, image: Image.Image, blur_radius: int = 10) -> Image.Image:
        """Apply glass morphism effect"""
        if not HAS_IMAGE_LIBS:
            return image
        
        # Create blur layer
        blur_layer = image.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Create glass overlay
        glass = Image.new('RGBA', image.size, (255, 255, 255, 30))
        
        # Composite
        result = Image.alpha_composite(blur_layer.convert('RGBA'), glass)
        return result.convert('RGB')
    
    def apply_neon_glow(self, image: Image.Image, color: Tuple[int, int, int]) -> Image.Image:
        """Apply neon glow effect"""
        if not HAS_IMAGE_LIBS:
            return image
        
        # Convert to array
        arr = np.array(image)
        
        # Create glow effect
        glow = np.zeros_like(arr)
        glow[:, :] = color
        
        # Blend
        result = np.clip(arr * 0.7 + glow * 0.3, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    def draw_rounded_rectangle(self, draw: ImageDraw.Draw, bbox: Tuple[int, int, int, int], 
                             radius: int, fill: Optional[Tuple] = None, 
                             outline: Optional[Tuple] = None, width: int = 1) -> None:
        """Draw rounded rectangle"""
        x1, y1, x2, y2 = bbox
        
        # Draw rounded corners
        draw.ellipse([x1, y1, x1 + radius*2, y1 + radius*2], fill=fill, outline=outline, width=width)
        draw.ellipse([x2 - radius*2, y1, x2, y1 + radius*2], fill=fill, outline=outline, width=width)
        draw.ellipse([x1, y2 - radius*2, x1 + radius*2, y2], fill=fill, outline=outline, width=width)
        draw.ellipse([x2 - radius*2, y2 - radius*2, x2, y2], fill=fill, outline=outline, width=width)
        
        # Draw rectangles
        draw.rectangle([x1 + radius, y1, x2 - radius, y1 + radius*2], 
                      fill=fill, outline=outline, width=width)
        draw.rectangle([x1, y1 + radius, x1 + radius*2, y2 - radius], 
                      fill=fill, outline=outline, width=width)
        draw.rectangle([x2 - radius*2, y1 + radius, x2, y2 - radius], 
                      fill=fill, outline=outline, width=width)
        draw.rectangle([x1 + radius, y2 - radius*2, x2 - radius, y2], 
                      fill=fill, outline=outline, width=width)
        
        # Draw center rectangle
        draw.rectangle([x1 + radius, y1 + radius, x2 - radius, y2 - radius], 
                      fill=fill, outline=outline, width=width)
    
    def add_text_with_outline(self, draw: ImageDraw.Draw, position: Tuple[int, int], 
                            text: str, font: ImageFont.FreeTypeFont, 
                            fill: Tuple[int, int, int], 
                            outline_fill: Tuple[int, int, int] = (0, 0, 0),
                            outline_width: int = 2) -> None:
        """Draw text with outline"""
        x, y = position
        
        # Draw outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_fill)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=fill)
    
    def create_badge(self, badge_data: Dict, size: int = 80) -> Image.Image:
        """Create badge image"""
        if not HAS_IMAGE_LIBS:
            return Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Get badge color
        color = self.hex_to_rgba(badge_data["color"], 200)
        
        # Draw badge shape (hexagon for premium)
        points = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            x = size//2 + (size//2 - 10) * math.cos(angle)
            y = size//2 + (size//2 - 10) * math.sin(angle)
            points.append((x, y))
        
        draw.polygon(points, fill=color, outline=(255, 255, 255, 255), width=3)
        
        # Add badge emoji/text
        badge_text = badge_data["name"][0]  # First character/emoji
        try:
            font = ImageFont.truetype("assets/fonts/arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), badge_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text(
            ((size - text_width) // 2, (size - text_height) // 2),
            badge_text,
            font=font,
            fill=(255, 255, 255, 255)
        )
        
        # Add shine effect
        shine = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        shine_draw = ImageDraw.Draw(shine)
        shine_draw.polygon(points[:3], fill=(255, 255, 255, 50))
        
        img = Image.alpha_composite(img, shine)
        
        return img
    
    def create_progress_bar(self, width: int, height: int, progress: float, 
                          theme: Dict) -> Image.Image:
        """Create progress bar"""
        bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bar)
        
        # Draw background
        bg_color = self.hex_to_rgba(theme["secondary"], 100)
        self.draw_rounded_rectangle(draw, (0, 0, width, height), height//2, 
                                   fill=bg_color, outline=None)
        
        # Draw progress
        progress_width = int(width * progress)
        if progress_width > 0:
            progress_color = self.hex_to_rgba(theme["success"], 200)
            self.draw_rounded_rectangle(draw, (0, 0, progress_width, height), height//2, 
                                       fill=progress_color, outline=None)
        
        # Draw border
        border_color = self.hex_to_rgba(theme["primary"], 150)
        self.draw_rounded_rectangle(draw, (0, 0, width, height), height//2, 
                                   fill=None, outline=border_color, width=2)
        
        return bar
    
    def create_stat_card(self, label: str, value: Any, icon: str, 
                        theme: Dict, width: int = 200, height: int = 80) -> Image.Image:
        """Create stat card component"""
        card = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)
        
        # Draw card background with glass effect
        bg_color = self.hex_to_rgba(theme["secondary"], 50)
        border_color = self.hex_to_rgba(theme["primary"], 100)
        
        self.draw_rounded_rectangle(draw, (0, 0, width, height), 15, 
                                   fill=bg_color, outline=border_color, width=2)
        
        # Add icon
        icon_color = self.hex_to_rgba(theme["primary"], 255)
        try:
            font = ImageFont.truetype("assets/fonts/arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((15, 15), icon, font=font, fill=icon_color)
        
        # Add value
        value_color = self.hex_to_rgba(theme["text_color"], 255)
        try:
            value_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 28)
        except:
            value_font = ImageFont.load_default()
        
        draw.text((50, 10), str(value), font=value_font, fill=value_color)
        
        # Add label
        label_color = self.hex_to_rgba(theme["text_color"], 180)
        try:
            label_font = ImageFont.truetype("assets/fonts/arial.ttf", 14)
        except:
            label_font = ImageFont.load_default()
        
        draw.text((50, 45), label, font=label_font, fill=label_color)
        
        return card


class UserInformationCard:
    """Main class for generating user information cards"""
    
    def __init__(self):
        self.graphics = GraphicsEngine()
        self.config = CardConfig()
        logger.info("UserInformationCard Premium v15.0 initialized")
    
    async def generate_user_card(self, user_data: Any, theme_name: str = "diamond") -> Dict:
        """Generate user information card"""
        try:
            # Convert Telegram user to our UserData format
            user = self._prepare_user_data(user_data)
            
            # Get theme
            theme = ThemeManager.get_theme(theme_name)
            
            # Generate card
            card_path = await self._generate_card_image(user, theme)
            
            if card_path:
                return {
                    "success": True,
                    "image_path": card_path,
                    "user_id": user.id,
                    "theme": theme_name,
                    "generated_at": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate card"
                }
                
        except Exception as e:
            logger.error(f"Error generating user card: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _prepare_user_data(self, telegram_user: Any) -> UserData:
        """Prepare user data from Telegram user object"""
        # This would typically come from database
        # For now, create mock data
        
        join_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        return UserData(
            id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            join_date=join_date,
            total_roasts=random.randint(10, 500),
            upvotes=random.randint(50, 5000),
            downvotes=random.randint(0, 500),
            rank=random.randint(1, 100),
            level=random.randint(1, 50),
            xp=random.randint(0, 10000),
            badges=["veteran", "premium", "social"] if random.random() > 0.5 else ["premium"],
            achievements=["First Roast", "100 Roasts", "Top 10"],
            premium=True,
            theme="diamond",
            analytics={
                "activity_level": random.choice(["hyper_active", "active", "moderate"]),
                "roast_style": random.choice(["funny", "clever", "savage"]),
                "engagement_score": random.randint(50, 100)
            }
        )
    
    async def _generate_card_image(self, user: UserData, theme: Dict) -> Optional[str]:
        """Generate the actual card image"""
        if not HAS_IMAGE_LIBS:
            logger.error("PIL/Pillow not available")
            return None
        
        try:
            # Create directories
            os.makedirs("temp/cards", exist_ok=True)
            
            # Create base image with gradient
            width, height = self.config.width, self.config.height
            base = self.graphics.create_gradient(width, height, theme["bg_gradient"])
            
            # Apply effects based on theme
            if theme.get("glass_effect"):
                base = self.graphics.apply_glass_effect(base)
            
            if theme.get("neon"):
                base = self.graphics.apply_neon_glow(base, self.graphics.hex_to_rgb(theme["primary"]))
            
            # Create main drawing context
            draw = ImageDraw.Draw(base)
            
            # Create main card container
            card_margin = 40
            card_rect = (
                card_margin, card_margin,
                width - card_margin, height - card_margin
            )
            
            # Draw card background with glass effect
            card_bg = Image.new('RGBA', (width - 2*card_margin, height - 2*card_margin), 
                              self.graphics.hex_to_rgba(theme["secondary"], 30))
            
            if theme.get("glass_effect"):
                card_bg = self.graphics.apply_glass_effect(card_bg, 15)
            
            # Paste onto base
            base.paste(card_bg, (card_margin, card_margin), card_bg)
            
            # Draw card border
            border_color = self.graphics.hex_to_rgba(theme["primary"], 150)
            self.graphics.draw_rounded_rectangle(
                draw, card_rect, self.config.corner_radius,
                fill=None, outline=border_color, width=self.config.border_width
            )
            
            # Draw header section
            await self._draw_header(draw, user, theme, width, height)
            
            # Draw stats section
            await self._draw_stats(draw, user, theme, width, height)
            
            # Draw badges section
            await self._draw_badges(draw, user, theme, width, height)
            
            # Draw analytics section
            await self._draw_analytics(draw, user, theme, width, height)
            
            # Draw footer
            await self._draw_footer(draw, user, theme, width, height)
            
            # Apply final effects
            if theme.get("glow"):
                base = base.filter(ImageFilter.GaussianBlur(1))
            
            # Save image
            filename = f"temp/cards/card_{user.id}_{uuid.uuid4().hex[:8]}.png"
            base.save(filename, 'PNG', quality=95, optimize=True)
            
            logger.info(f"User card generated: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error in card generation: {e}")
            return None
    
    async def _draw_header(self, draw: ImageDraw.Draw, user: UserData, 
                          theme: Dict, width: int, height: int):
        """Draw header section"""
        padding = self.config.padding
        
        # User name
        name = f"{user.first_name} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else f"ID: {user.id}"
        
        # Theme name
        theme_name = theme["name"]
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 48)
            subtitle_font = ImageFont.truetype("assets/fonts/arial.ttf", 24)
            theme_font = ImageFont.truetype("assets/fonts/arial.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            theme_font = ImageFont.load_default()
        
        # Draw user name with outline
        name_color = self.graphics.hex_to_rgb(theme["text_color"])
        outline_color = self.graphics.hex_to_rgb(theme["primary"])
        
        self.graphics.add_text_with_outline(
            draw, (padding + 150, padding + 30),
            name, title_font, name_color, outline_color, 3
        )
        
        # Draw username
        username_color = self.graphics.hex_to_rgb(theme["accent"])
        draw.text((padding + 150, padding + 90), username, 
                 font=subtitle_font, fill=username_color)
        
        # Draw theme badge
        theme_bg = self.graphics.hex_to_rgb(theme["primary"])
        theme_text_color = (0, 0, 0) if theme["primary"] in ["#FFD700", "#FFFFFF"] else (255, 255, 255)
        
        theme_width = 200
        theme_height = 40
        theme_rect = (width - padding - theme_width, padding, 
                     width - padding, padding + theme_height)
        
        self.graphics.draw_rounded_rectangle(
            draw, theme_rect, 20,
            fill=theme_bg, outline=None
        )
        
        draw.text(
            (width - padding - theme_width + 10, padding + 10),
            theme_name, theme_font, fill=theme_text_color
        )
        
        # Draw premium badge
        if user.premium:
            premium_text = "💎 PREMIUM"
            premium_color = self.graphics.hex_to_rgb("#00D2FF")
            
            try:
                premium_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 28)
            except:
                premium_font = ImageFont.load_default()
            
            premium_width = 180
            premium_rect = (padding, padding, padding + premium_width, padding + 50)
            
            premium_bg = self.graphics.hex_to_rgb("#00D2FF")
            self.graphics.draw_rounded_rectangle(
                draw, premium_rect, 25,
                fill=premium_bg, outline=None
            )
            
            draw.text((padding + 10, padding + 10), premium_text, 
                     font=premium_font, fill=(0, 0, 0))
    
    async def _draw_stats(self, draw: ImageDraw.Draw, user: UserData, 
                         theme: Dict, width: int, height: int):
        """Draw statistics section"""
        padding = self.config.padding
        start_y = 180
        
        # Create stats grid
        stats = [
            {"label": "Total Roasts", "value": user.total_roasts, "icon": "🔥"},
            {"label": "Upvotes", "value": user.upvotes, "icon": "👍"},
            {"label": "Rank", "value": f"#{user.rank}", "icon": "🏆"},
            {"label": "Level", "value": user.level, "icon": "⭐"},
            {"label": "XP", "value": user.xp, "icon": "⚡"},
            {"label": "Join Date", "value": user.join_date.strftime("%d/%m/%Y"), "icon": "📅"}
        ]
        
        # Draw stats in 2x3 grid
        card_width = 220
        card_height = 90
        spacing = 20
        
        for i, stat in enumerate(stats):
            row = i // 3
            col = i % 3
            
            x = padding + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            # Create stat card
            stat_card = self.graphics.create_stat_card(
                stat["label"], stat["value"], stat["icon"], theme, card_width, card_height
            )
            
            # Convert draw to image for pasting
            main_image = draw._image
            main_image.paste(stat_card, (x, y), stat_card)
    
    async def _draw_badges(self, draw: ImageDraw.Draw, user: UserData, 
                          theme: Dict, width: int, height: int):
        """Draw badges section"""
        padding = self.config.padding
        start_y = 400
        
        # Get badges for user
        badge_data = PremiumBadge.get_badges_for_user(user)
        
        # Section title
        try:
            section_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 28)
            badge_font = ImageFont.truetype("assets/fonts/arial.ttf", 14)
        except:
            section_font = ImageFont.load_default()
            badge_font = ImageFont.load_default()
        
        section_color = self.graphics.hex_to_rgb(theme["primary"])
        draw.text((padding, start_y - 40), "🎖️ PREMIUM BADGES", 
                 font=section_font, fill=section_color)
        
        # Draw badges
        badge_size = 70
        badge_spacing = 90
        badges_per_row = 5
        
        for i, badge in enumerate(badge_data[:10]):  # Max 10 badges
            row = i // badges_per_row
            col = i % badges_per_row
            
            x = padding + col * badge_spacing
            y = start_y + row * badge_spacing
            
            # Create badge
            badge_img = self.graphics.create_badge(badge, badge_size)
            
            # Paste badge
            main_image = draw._image
            main_image.paste(badge_img, (x, y), badge_img)
            
            # Draw badge name
            badge_name = badge["name"]
            name_width = draw.textbbox((0, 0), badge_name, font=badge_font)[2]
            
            draw.text(
                (x + (badge_size - name_width) // 2, y + badge_size + 5),
                badge_name, badge_font, fill=self.graphics.hex_to_rgb(theme["text_color"])
            )
    
    async def _draw_analytics(self, draw: ImageDraw.Draw, user: UserData, 
                             theme: Dict, width: int, height: int):
        """Draw analytics section"""
        padding = self.config.padding
        start_y = 550
        
        # Section title
        try:
            section_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 28)
            label_font = ImageFont.truetype("assets/fonts/arial.ttf", 18)
            value_font = ImageFont.truetype("assets/fonts/arialbd.ttf", 22)
        except:
            section_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            value_font = ImageFont.load_default()
        
        section_color = self.graphics.hex_to_rgb(theme["primary"])
        draw.text((padding, start_y - 40), "📈 USER ANALYTICS", 
                 font=section_font, fill=section_color)
        
        # Analytics data
        analytics = user.analytics
        
        # Activity Level
        activity_level = analytics.get("activity_level", "moderate").replace("_", " ").title()
        activity_color = self.graphics.hex_to_rgb(theme["success"])
        
        draw.text((padding, start_y), "Activity Level:", 
                 font=label_font, fill=self.graphics.hex_to_rgb(theme["text_color"]))
        draw.text((padding + 150, start_y), activity_level, 
                 font=value_font, fill=activity_color)
        
        # Roast Style
        roast_style = analytics.get("roast_style", "balanced").replace("_", " ").title()
        style_color = self.graphics.hex_to_rgb(theme["accent"])
        
        draw.text((padding, start_y + 35), "Roast Style:", 
                 font=label_font, fill=self.graphics.hex_to_rgb(theme["text_color"]))
        draw.text((padding + 150, start_y + 35), roast_style, 
                 font=value_font, fill=style_color)
        
        # Engagement Score
        engagement = analytics.get("engagement_score", 0)
        engagement_color = self.graphics.hex_to_rgb(theme["danger"] if engagement < 50 
                                                   else theme["success"] if engagement >= 80 
                                                   else theme["accent"])
        
        draw.text((padding, start_y + 70), "Engagement Score:", 
                 font=label_font, fill=self.graphics.hex_to_rgb(theme["text_color"]))
        draw.text((padding + 200, start_y + 70), f"{engagement}/100", 
                 font=value_font, fill=engagement_color)
        
        # Progress bar for engagement
        bar_width = 300
        bar_height = 20
        bar_x = width - padding - bar_width
        bar_y = start_y + 70
        
        progress_bar = self.graphics.create_progress_bar(
            bar_width, bar_height, engagement/100, theme
        )
        
        main_image = draw._image
        main_image.paste(progress_bar, (bar_x, bar_y), progress_bar)
        
        # Draw percentage on progress bar
        percentage = f"{engagement}%"
        percentage_width = draw.textbbox((0, 0), percentage, font=label_font)[2]
        
        percentage_color = (0, 0, 0) if engagement >= 50 else (255, 255, 255)
        draw.text(
            (bar_x + (bar_width - percentage_width) // 2, bar_y),
            percentage, label_font, fill=percentage_color
        )
    
    async def _draw_footer(self, draw: ImageDraw.Draw, user: UserData, 
                          theme: Dict, width: int, height: int):
        """Draw footer section"""
        padding = self.config.padding
        
        # Footer text
        footer_text = "Roastify Premium v15.0 • User Information Card"
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            footer_font = ImageFont.truetype("assets/fonts/arial.ttf", 16)
        except:
            footer_font = ImageFont.load_default()
        
        footer_color = self.graphics.hex_to_rgb(theme["text_color"])
        footer_color = (*footer_color[:3], 150)  # Add transparency
        
        # Draw footer
        footer_y = height - padding - 20
        draw.text((padding, footer_y), footer_text, 
                 font=footer_font, fill=footer_color)
        
        # Draw generation time
        time_width = draw.textbbox((0, 0), generated_at, font=footer_font)[2]
        draw.text((width - padding - time_width, footer_y), generated_at, 
                 font=footer_font, fill=footer_color)
    
    async def generate_multiple_cards(self, users: List[Any], 
                                    theme: str = "diamond") -> List[Dict]:
        """Generate cards for multiple users"""
        results = []
        
        for user in users:
            result = await self.generate_user_card(user, theme)
            results.append(result)
        
        return results
    
    async def generate_theme_preview(self) -> Optional[str]:
        """Generate theme preview card"""
        try:
            # Create mock user for preview
            class MockUser:
                def __init__(self):
                    self.id = 123456789
                    self.username = "premium_user"
                    self.first_name = "Premium"
                    self.last_name = "User"
            
            mock_user = MockUser()
            
            # Generate card with random theme
            themes = list(ThemeManager.THEMES.keys())
            random_theme = random.choice(themes)
            
            result = await self.generate_user_card(mock_user, random_theme)
            return result.get("image_path") if result.get("success") else None
            
        except Exception as e:
            logger.error(f"Error generating theme preview: {e}")
            return None
    
    def get_available_themes(self) -> List[Dict]:
        """Get list of available themes"""
        themes = []
        
        for key, theme in ThemeManager.THEMES.items():
            themes.append({
                "id": key,
                "name": theme["name"],
                "primary_color": theme["primary"],
                "preview_url": f"#theme_{key}"  # Would be actual URL in production
            })
        
        return themes
    
    def cleanup_old_cards(self, max_age_hours: int = 24):
        """Cleanup old card files"""
        try:
            cards_dir = Path("temp/cards")
            if cards_dir.exists():
                cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
                
                for file in cards_dir.glob("*.png"):
                    if file.stat().st_mtime < cutoff_time:
                        try:
                            file.unlink()
                            logger.debug(f"Cleaned up old card: {file}")
                        except:
                            pass
        except Exception as e:
            logger.error(f"Error cleaning up old cards: {e}")


# Utility functions
def create_sample_user() -> UserData:
    """Create sample user for testing"""
    return UserData(
        id=123456789,
        username="premium_user",
        first_name="John",
        last_name="Doe",
        join_date=datetime.now() - timedelta(days=100),
        total_roasts=250,
        upvotes=1250,
        downvotes=50,
        rank=15,
        level=42,
        xp=8500,
        badges=["veteran", "premium", "social", "elite"],
        achievements=["First Roast", "100 Roasts", "Top 10", "Master Roaster"],
        premium=True,
        theme="diamond",
        analytics={
            "activity_level": "very_active",
            "roast_style": "clever_witty",
            "engagement_score": 87
        }
    )


async def demo():
    """Demo function to test card generation"""
    print("User Information Card System v15.0 - Demo")
    print("=" * 50)
    
    if not HAS_IMAGE_LIBS:
        print("❌ PIL/Pillow not installed. Install: pip install pillow numpy")
        return
    
    card_system = UserInformationCard()
    
    # Create sample user
    user = create_sample_user()
    
    print(f"Generating card for: {user.first_name} {user.last_name}")
    print(f"Theme: Diamond Premium")
    
    # Generate card
    result = await card_system.generate_user_card(user, "diamond")
    
    if result["success"]:
        print(f"✅ Card generated successfully!")
        print(f"📁 Path: {result['image_path']}")
        print(f"👤 User ID: {result['user_id']}")
        print(f"🎨 Theme: {result['theme']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # Show available themes
    themes = card_system.get_available_themes()
    print(f"\n🎨 Available Themes ({len(themes)}):")
    for theme in themes:
        print(f"  • {theme['name']} ({theme['id']})")


if __name__ == "__main__":
    # Run demo if executed directly
    import asyncio
    asyncio.run(demo())
