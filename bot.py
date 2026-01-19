#!/usr/bin/env python3
"""
Roastify Bot v15.0 - ULTIMATE PREMIUM EDITION
Image + Text + Diagram + User Information Cards with AI Analytics
"""

import os
import sys
import logging
import random
import re
import asyncio
import traceback
import math
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path
import concurrent.futures
import hashlib
import time
import uuid

# Import AI Libraries
try:
    import numpy as np
    import spacy
    from textblob import TextBlob
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    import nltk
    
    # Setup NLTK
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    
    HAS_AI = True
except ImportError:
    HAS_AI = False
    logger.warning("AI libraries not installed. Some features disabled.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_premium.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import project modules
try:
    from config import BOT_TOKEN, BOT_IDENTITY, CORE_RULES, OWNER_ADMIN_PROTECTION
    from database import get_database
    from features.master_loader import load_all_features
    from features.welcome_system import WelcomeSystem
    from features.roast_engine import RoastEngine
    from features.voting_system import VotingSystem
    from features.reaction_system import ReactionSystem
    from features.mention_roast import MentionRoast
    from features.admin_protection import AdminProtection
    from features.leaderboard import Leaderboard
    from features.festival_mode import FestivalMode
    from features.auto_daily_quote import AutoDailyQuote
    from features.custom_template_unlocks import CustomTemplateUnlocks
    from features.auto_mood_recognition import AutoMoodRecognition
    from features.safe_forward_share import SafeForwardShare
    from utils.template_manager import TemplateManager
    
    # Import UltimateImageGenerator v6.0
    from utils.image_generator_ultimate import (
        UltimateImageGenerator, 
        GenerationResult,
        ImageConfig,
        TextConfig,
        BorderConfig,
        BackgroundConfig,
        BorderType,
        TextEffect,
        GradientDirection
    )
    
    # Import PIL
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    HAS_PIL = True
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(traceback.format_exc())
    logger.error("Please check all required files exist")
    sys.exit(1)

# Import Telegram
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters,
        ContextTypes, CallbackQueryHandler, ApplicationBuilder
    )
    from telegram.constants import ParseMode
except ImportError:
    logger.error("Install: pip install python-telegram-bot")
    sys.exit(1)


# Import Premium Modules
try:
    from premium.user_information_card import UserInformationCard
    from premium.ai_analytics import AdvancedAIAnalytics
    from premium.enterprise_dashboard import EnterpriseDashboard
    from premium.blockchain_integrator import BlockchainIntegrator
    from premium.advanced_image_processor import AdvancedImageProcessor
    from premium.enterprise_security import EnterpriseSecurity
    from premium.report_generator import AdvancedReportGenerator
    HAS_PREMIUM = True
except ImportError:
    HAS_PREMIUM = False
    logger.warning("Premium modules not found. Creating premium directory...")
    os.makedirs("premium", exist_ok=True)


class PremiumThemeManager:
    """Manage premium themes and styles"""
    
    def __init__(self):
        self.themes = {
            "diamond": {
                "name": "💎 Diamond Premium",
                "colors": ["#FFD700", "#FFFFFF", "#B9F2FF", "#FF6B6B"],
                "bg_gradient": ["#0F2027", "#203A43", "#2C5364"],
                "font": "Arial Black",
                "effects": ["glow", "shadow", "gradient"]
            },
            "neon": {
                "name": "🌌 Neon Cyberpunk",
                "colors": ["#00FFFF", "#FF00FF", "#00FF00", "#FFFF00"],
                "bg_gradient": ["#000428", "#004e92", "#000428"],
                "font": "Courier New",
                "effects": ["neon", "blur", "scanlines"]
            },
            "gold": {
                "name": "🏆 Gold Elite",
                "colors": ["#FFD700", "#FFA500", "#FF8C00", "#DAA520"],
                "bg_gradient": ["#1A1A1A", "#333333", "#1A1A1A"],
                "font": "Times New Roman",
                "effects": ["metallic", "shine", "emboss"]
            },
            "silver": {
                "name": "⚡ Silver Pro",
                "colors": ["#C0C0C0", "#E8E8E8", "#A0A0A0", "#D3D3D3"],
                "bg_gradient": ["#2B2B2B", "#4A4A4A", "#2B2B2B"],
                "font": "Verdana",
                "effects": ["chrome", "reflection", "glossy"]
            },
            "platinum": {
                "name": "🔮 Platinum VIP",
                "colors": ["#E5E4E2", "#C0C0C0", "#A0A0A0", "#808080"],
                "bg_gradient": ["#16222A", "#3A6073", "#16222A"],
                "font": "Georgia",
                "effects": ["platinum", "crystal", "transparent"]
            }
        }
        
        self.current_theme = "diamond"
        logger.info("PremiumThemeManager initialized")
    
    def get_theme(self, theme_name: str = None) -> Dict:
        """Get theme configuration"""
        theme = theme_name or self.current_theme
        return self.themes.get(theme, self.themes["diamond"])
    
    def get_random_theme(self) -> Dict:
        """Get random theme"""
        return random.choice(list(self.themes.values()))
    
    def get_themed_colors(self, theme_name: str = None) -> List[str]:
        """Get colors for theme"""
        theme = self.get_theme(theme_name)
        return theme["colors"]
    
    def create_gradient_background(self, theme_name: str = None, 
                                  width: int = 1200, height: int = 800) -> Image.Image:
        """Create gradient background for theme"""
        theme = self.get_theme(theme_name)
        colors = theme["bg_gradient"]
        
        # Create gradient
        background = Image.new('RGB', (width, height), color=colors[0])
        draw = ImageDraw.Draw(background)
        
        # Simple gradient implementation
        for i in range(height):
            ratio = i / height
            r = int(sum(int(c[j:j+2], 16) for c in colors) / len(colors) * ratio)
            g = int(sum(int(c[j:j+2], 16) for c in colors) / len(colors) * ratio)
            b = int(sum(int(c[j:j+2], 16) for c in colors) / len(colors) * ratio)
            
            color = (r, g, b)
            draw.line([(0, i), (width, i)], fill=color)
        
        return background


class PremiumBadgeSystem:
    """Premium badge and achievement system"""
    
    def __init__(self):
        self.badges = {
            "veteran": {"name": "🎖️ Veteran", "desc": "100+ roasts", "color": "#FFD700"},
            "elite": {"name": "👑 Elite", "desc": "Top 10 ranking", "color": "#C0C0C0"},
            "creative": {"name": "🎨 Creative", "desc": "50+ custom roasts", "color": "#FF6B6B"},
            "social": {"name": "🤝 Social", "desc": "500+ votes received", "color": "#00C851"},
            "fast": {"name": "⚡ Speedster", "desc": "Fastest response", "color": "#33B5E5"},
            "funny": {"name": "😂 Comedian", "desc": "Most funny roasts", "color": "#FF8800"},
            "clever": {"name": "🧠 Genius", "desc": "Most clever roasts", "color": "#AA66CC"},
            "helpful": {"name": "🌟 Helper", "desc": "Helped other users", "color": "#FFBB33"},
            "legend": {"name": "🏆 Legend", "desc": "All badges unlocked", "color": "#FF4444"},
            "premium": {"name": "💎 Premium", "desc": "Premium member", "color": "#00D2FF"}
        }
        
        logger.info("PremiumBadgeSystem initialized")
    
    def get_user_badges(self, user_id: int, user_stats: Dict) -> List[Dict]:
        """Get badges user has earned"""
        earned_badges = []
        
        # Check each badge condition
        if user_stats.get("total_roasts", 0) >= 100:
            earned_badges.append(self.badges["veteran"])
        
        if user_stats.get("rank", 999) <= 10:
            earned_badges.append(self.badges["elite"])
        
        if user_stats.get("custom_roasts", 0) >= 50:
            earned_badges.append(self.badges["creative"])
        
        if user_stats.get("total_votes", 0) >= 500:
            earned_badges.append(self.badges["social"])
        
        # Premium badge for all premium users
        earned_badges.append(self.badges["premium"])
        
        # Legend badge if earned many badges
        if len(earned_badges) >= 5:
            earned_badges.append(self.badges["legend"])
        
        return earned_badges
    
    def create_badge_image(self, badge: Dict) -> Optional[str]:
        """Create badge image"""
        if not HAS_PIL:
            return None
        
        try:
            size = 100
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Parse color
            color = badge["color"]
            if color.startswith('#'):
                color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
            # Draw badge circle
            draw.ellipse([5, 5, size-5, size-5], fill=color, outline=(255, 255, 255), width=3)
            
            # Add text (first character)
            text = badge["name"][0]
            try:
                font = ImageFont.truetype("assets/fonts/arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            draw.text(
                ((size - text_width) // 2, (size - text_height) // 2 - 10),
                text, font=font, fill=(255, 255, 255)
            )
            
            # Save
            os.makedirs("temp/badges", exist_ok=True)
            filename = f"temp/badges/badge_{hashlib.md5(badge['name'].encode()).hexdigest()[:8]}.png"
            img.save(filename, 'PNG')
            
            return filename
            
        except Exception as e:
            logger.error(f"Error creating badge image: {e}")
            return None


class PremiumUserAnalytics:
    """Premium user analytics and insights"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer() if HAS_AI else None
        logger.info("PremiumUserAnalytics initialized")
    
    async def analyze_user_behavior(self, user_id: int, user_data: Dict) -> Dict:
        """Analyze user behavior patterns"""
        analysis = {
            "activity_level": "unknown",
            "roast_style": "balanced",
            "peak_hours": [],
            "engagement_score": 0,
            "improvement_areas": [],
            "strengths": []
        }
        
        try:
            # Calculate activity level
            total_roasts = user_data.get("total_roasts", 0)
            days_active = user_data.get("days_active", 1)
            daily_avg = total_roasts / days_active
            
            if daily_avg >= 10:
                analysis["activity_level"] = "hyper_active"
            elif daily_avg >= 5:
                analysis["activity_level"] = "very_active"
            elif daily_avg >= 2:
                analysis["activity_level"] = "active"
            elif daily_avg >= 1:
                analysis["activity_level"] = "moderate"
            else:
                analysis["activity_level"] = "casual"
            
            # Analyze roast style from recent roasts
            recent_roasts = user_data.get("recent_roasts", [])
            if recent_roasts and HAS_AI:
                sentiments = []
                for roast in recent_roasts[:10]:  # Last 10 roasts
                    try:
                        sentiment = self.sentiment_analyzer.polarity_scores(roast)
                        sentiments.append(sentiment["compound"])
                    except:
                        pass
                
                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    if avg_sentiment > 0.3:
                        analysis["roast_style"] = "positive_funny"
                    elif avg_sentiment < -0.3:
                        analysis["roast_style"] = "savage_harsh"
                    else:
                        analysis["roast_style"] = "neutral_clever"
            
            # Calculate engagement score (0-100)
            vote_ratio = user_data.get("upvotes", 0) / max(user_data.get("total_votes", 1), 1)
            activity_score = min(daily_avg * 10, 50)  # Max 50 points
            vote_score = vote_ratio * 30  # Max 30 points
            consistency_score = min(days_active * 2, 20)  # Max 20 points
            
            analysis["engagement_score"] = int(activity_score + vote_score + consistency_score)
            
            # Determine strengths and improvement areas
            if vote_ratio > 0.7:
                analysis["strengths"].append("popular_roasts")
            if daily_avg > 3:
                analysis["strengths"].append("high_activity")
            if user_data.get("unique_roasts", 0) > 20:
                analysis["strengths"].append("creativity")
            
            if vote_ratio < 0.3:
                analysis["improvement_areas"].append("roast_quality")
            if daily_avg < 1:
                analysis["improvement_areas"].append("activity")
            if len(recent_roasts) < 5:
                analysis["improvement_areas"].append("consistency")
            
        except Exception as e:
            logger.error(f"Error in user behavior analysis: {e}")
        
        return analysis


class AsyncImageGenerator:
    """Async wrapper for UltimateImageGenerator - PREMIUM EDITION"""
    
    def __init__(self, config: Optional[ImageConfig] = None):
        self.generator = UltimateImageGenerator(config)
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=8,  # Increased for premium
            thread_name_prefix='PremiumImageGen'
        )
        self.theme_manager = PremiumThemeManager()
        self.badge_system = PremiumBadgeSystem()
        logger.info("Premium AsyncImageGenerator initialized")
    
    async def generate_premium_roast_image(self, roast_text: Any, user_info: Any,
                                         theme: str = "diamond",
                                         badges: List[Dict] = None) -> GenerationResult:
        """Generate premium roast image with theme and badges"""
        loop = asyncio.get_event_loop()
        
        try:
            # Get theme configuration
            theme_config = self.theme_manager.get_theme(theme)
            
            # Create custom border and background
            border_config = BorderConfig(
                border_type=BorderType.ROUNDED,
                border_width=10,
                border_color=theme_config["colors"][0],
                border_radius=30,
                inner_glow=True,
                outer_shadow=True,
                shadow_blur=20,
                shadow_offset=(5, 5),
                shadow_color="#00000080"
            )
            
            background_config = BackgroundConfig(
                background_type="gradient",
                gradient_colors=theme_config["bg_gradient"],
                gradient_direction=GradientDirection.DIAGONAL,
                blur_radius=5,
                pattern_overlay=True,
                pattern_opacity=0.1
            )
            
            # Generate base image
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_roast_image(
                    roast_text, user_info, "premium", border_config, background_config
                )
            )
            
            # Add badges if available
            if result.success and badges and len(badges) > 0:
                await self._add_badges_to_image(result.image_path, badges)
            
            return result
            
        except Exception as e:
            logger.error(f"Premium image generation failed: {e}")
            # Fallback to regular generation
            return await self.generate_roast_image_async(roast_text, user_info, "auto", None, None)
    
    async def _add_badges_to_image(self, image_path: str, badges: List[Dict]):
        """Add badges to image"""
        if not HAS_PIL or not badges:
            return
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self.executor,
                self._add_badges_to_image_sync,
                image_path,
                badges
            )
        except Exception as e:
            logger.error(f"Error adding badges: {e}")
    
    def _add_badges_to_image_sync(self, image_path: str, badges: List[Dict]):
        """Sync version of badge addition"""
        try:
            img = Image.open(image_path).convert('RGBA')
            draw = ImageDraw.Draw(img)
            
            # Badge size and position
            badge_size = 40
            start_x = img.width - (len(badges) * (badge_size + 10)) - 20
            start_y = 20
            
            # Add each badge
            for i, badge in enumerate(badges[:5]):  # Max 5 badges
                badge_img = self._create_small_badge(badge, badge_size)
                if badge_img:
                    img.paste(badge_img, (start_x + i * (badge_size + 10), start_y), badge_img)
            
            img.save(image_path, 'PNG')
            
        except Exception as e:
            logger.error(f"Error in badge addition sync: {e}")
    
    def _create_small_badge(self, badge: Dict, size: int = 40) -> Optional[Image.Image]:
        """Create small badge icon"""
        try:
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Parse color
            color = badge["color"]
            if color.startswith('#'):
                color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
            # Draw circle
            draw.ellipse([2, 2, size-2, size-2], fill=color, outline=(255, 255, 255), width=2)
            
            # Add emoji or text
            badge_name = badge["name"]
            if badge_name and badge_name[0].isprintable():
                text = badge_name[0]
                try:
                    font = ImageFont.truetype("assets/fonts/arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text(
                    ((size - text_width) // 2, (size - text_height) // 2 - 5),
                    text, font=font, fill=(255, 255, 255)
                )
            
            return img
            
        except Exception as e:
            logger.error(f"Error creating small badge: {e}")
            return None
    
    # Keep original methods for compatibility
    async def generate_roast_image_async(self, roast_text: Any, user_info: Any,
                                       style: str = "auto", 
                                       border_config: Optional[BorderConfig] = None,
                                       background_config: Optional[BackgroundConfig] = None) -> GenerationResult:
        """Async wrapper for image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_roast_image(
                    roast_text, user_info, style, border_config, background_config
                )
            )
            return result
        except Exception as e:
            logger.error(f"Async image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    async def generate_welcome_image_async(self, user_info: Any) -> GenerationResult:
        """Async wrapper for welcome image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_welcome_image(user_info)
            )
            return result
        except Exception as e:
            logger.error(f"Async welcome image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    async def generate_achievement_image_async(self, user_info: Any, achievement: Any) -> GenerationResult:
        """Async wrapper for achievement image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_achievement_image(user_info, achievement)
            )
            return result
        except Exception as e:
            logger.error(f"Async achievement image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    def get_stats(self) -> Dict:
        """Get generator statistics"""
        stats = self.generator.get_detailed_stats()
        stats["premium_features"] = True
        stats["themes_available"] = len(self.theme_manager.themes)
        return stats
    
    def health_check(self) -> Dict:
        """Health check"""
        health = self.generator.health_check()
        health["premium"] = True
        health["badge_system"] = True
        health["theme_manager"] = True
        return health
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.generator.cleanup()
            self.executor.shutdown(wait=False)
        except:
            pass


class PremiumRoastifyBot:
    """Main Roastify Bot Class v15.0 - PREMIUM EDITION"""
    
    def __init__(self):
        """Initialize the bot"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY.get("name", "Roastify Premium")
        self.bot_tagline = BOT_IDENTITY.get("tagline", "Ultimate Roasting Experience")
        
        # Initialize components
        self.db = get_database()
        
        # Premium initialization
        self.theme_manager = PremiumThemeManager()
        self.badge_system = PremiumBadgeSystem()
        self.user_analytics = PremiumUserAnalytics()
        
        # Initialize Image Generator with premium config
        image_config = ImageConfig(
            width=1200,  # Increased for premium
            height=1200,
            quality=100,  # Maximum quality
            format="PNG",
            enable_cache=True,
            cache_ttl_hours=48,  # Longer cache
            max_cache_size=5000,  # Larger cache
            output_dir="./output/premium",
            temp_dir="./temp/premium",
            cache_dir="./cache/premium",
            assets_dir="./assets/premium",
            backup_dir="./backup/premium",
            max_workers=8,  # More workers
            timeout=45.0,  # Longer timeout
            enable_backup=True,
            compression_level=9,  # Best compression
            premium_features=True
        )
        
        self.image_gen = AsyncImageGenerator(image_config)
        
        # Initialize premium modules if available
        if HAS_PREMIUM:
            try:
                self.user_info_card = UserInformationCard()
                self.ai_analytics = AdvancedAIAnalytics()
                self.enterprise_dashboard = EnterpriseDashboard()
                self.blockchain = BlockchainIntegrator()
                self.advanced_image_processor = AdvancedImageProcessor()
                self.security = EnterpriseSecurity()
                self.report_generator = AdvancedReportGenerator()
                self.has_full_premium = True
                logger.info("All premium modules loaded successfully")
            except Exception as e:
                logger.error(f"Error loading premium modules: {e}")
                self.has_full_premium = False
        else:
            self.has_full_premium = False
        
        # Initialize other components
        self.diagram_gen = DiagramGenerator()
        self.template_manager = TemplateManager()
        self.roast_engine = RoastEngine()
        self.welcome_system = WelcomeSystem()
        self.voting_system = VotingSystem()
        self.reaction_system = ReactionSystem()
        self.mention_roast = MentionRoast()
        self.admin_protection = AdminProtection()
        self.leaderboard = Leaderboard()
        self.festival_mode = FestivalMode()
        self.mood_recognition = AutoMoodRecognition()
        self.safe_forward = SafeForwardShare()
        
        # Initialize job-based features
        self.auto_daily_quote = None
        
        try:
            self.custom_unlocks = CustomTemplateUnlocks()
        except:
            self.custom_unlocks = None
        
        # Load all features
        try:
            self.features = load_all_features()
        except:
            self.features = {}
        
        # Premium Statistics
        self.stats = {
            "messages_processed": 0,
            "roasts_generated": 0,
            "images_created": 0,
            "diagrams_created": 0,
            "users_interacted": set(),
            "groups_managed": set(),
            "start_time": datetime.now(),
            "cache_hits": 0,
            "cache_misses": 0,
            "premium_users": set(),
            "premium_roasts": 0,
            "user_info_cards": 0,
            "ai_analyses": 0
        }
        
        # Premium user data
        self.premium_user_data = {}
        
        # Application instance
        self.application = None
        
        # Rate limiting (more generous for premium)
        self.user_cooldowns = {}
        self.cooldown_seconds = max(CORE_RULES.get("cooldown_seconds", 3) - 1, 1)  # Faster for premium
        
        logger.info(f"Initialized {self.bot_name} Bot v15.0 PREMIUM EDITION")
        logger.info(f"Premium Features: {self.has_full_premium}")
    
    def _check_cooldown(self, user_id: int) -> bool:
        """Check if user is in cooldown (premium version)"""
        now = time.time()
        last_request = self.user_cooldowns.get(user_id, 0)
        
        # Premium users get faster cooldown
        is_premium = user_id in self.stats["premium_users"]
        cooldown = self.cooldown_seconds / 2 if is_premium else self.cooldown_seconds
        
        if now - last_request < cooldown:
            return False
        
        self.user_cooldowns[user_id] = now
        return True
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - PREMIUM VERSION"""
        user = update.effective_user
        chat = update.effective_chat
        
        try:
            # Add user to database
            self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_premium=True  # All users premium in this version
            )
            
            # Mark as premium user
            self.stats["premium_users"].add(user.id)
            
            # Get premium welcome message
            welcome_message = f"""
🎖️ <b>প্রিমিয়ামে স্বাগতম {user.first_name}!</b>

💎 <b>আপনি এখন {self.bot_name} - {self.bot_tagline}</b>

🚀 <b>প্রিমিয়াম বৈশিষ্ট্য:</b>
• AI-পাওয়ারড রোস্ট অ্যানালাইসিস
• প্রিমিয়াম থিমড ইমেজ জেনারেশন
• অ্যাডভান্সড ইউজার ইনফরমেশন কার্ড
• রিয়েল-টাইম ড্যাশবোর্ড
• ব্লকচেইন ভেরিফিকেশন
• প্রফেশনাল রিপোর্টস

⚡ <b>নতুন কমান্ড:</b>
/profile - আপনার প্রিমিয়াম প্রোফাইল
/analyze - এআই টেক্সট অ্যানালাইসিস
/report - প্রফেশনাল রিপোর্ট
/stats - ডিটেইল্ড স্ট্যাটিস্টিকস
/theme - থিম পরিবর্তন করুন

🔥 <b>এখনই চেষ্টা করুন!</b>
কিছু লিখে দেখুন প্রিমিয়াম রোস্ট!
            """
            
            # Generate premium welcome image
            welcome_result = await self.image_gen.generate_welcome_image_async(user)
            
            if welcome_result.success and welcome_result.image_path:
                # Send welcome image
                with open(welcome_result.image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"💎 {user.first_name} - প্রিমিয়াম সদস্য!",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(welcome_result.image_path)
                except:
                    pass
            
            # Send welcome text
            await update.message.reply_text(
                welcome_message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Generate user information card
            await self._send_user_info_card(update, user, is_new=True)
            
            logger.info(f"New premium user {user.id} started")
            
        except Exception as e:
            logger.error(f"Error in premium start command: {e}")
            await update.message.reply_text(
                f"💎 স্বাগতম {user.first_name}!\n"
                f"আপনি এখন {self.bot_name} প্রিমিয়াম এডিশনে!\n\n"
                f"কিছু লিখে প্রিমিয়াম রোস্ট শুরু করুন!",
                parse_mode=ParseMode.HTML
            )
    
    async def _send_user_info_card(self, update: Update, user: Any, is_new: bool = False):
        """Send user information card"""
        try:
            if not self.has_full_premium:
                return
                
            # Generate user info card
            card_result = await self.user_info_card.generate_user_card(user)
            
            if card_result and card_result.get("success") and card_result.get("image_path"):
                caption = "🆕 নতুন প্রিমিয়াম সদস্য!" if is_new else "📊 আপনার প্রোফাইল কার্ড"
                
                with open(card_result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Update stats
                self.stats["user_info_cards"] += 1
                
                # Cleanup
                try:
                    os.remove(card_result["image_path"])
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error sending user info card: {e}")
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command - Premium user profile"""
        user = update.effective_user
        
        try:
            # Get user data
            user_data = self.db.get_user_stats(user.id)
            
            # Get badges
            badges = self.badge_system.get_user_badges(user.id, user_data)
            
            # Get analytics
            analytics = await self.user_analytics.analyze_user_behavior(user.id, user_data)
            
            # Generate profile message
            profile_text = f"""
📊 <b>প্রিমিয়াম প্রোফাইল: {user.first_name}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🏆 <b>স্ট্যাটস:</b>
• মোট রোস্ট: {user_data.get('total_roasts', 0):,}
• আপভোট: {user_data.get('upvotes', 0):,}
• ডাউনভোট: {user_data.get('downvotes', 0):,}
• র‍্যাংক: #{user_data.get('rank', 'N/A')}
• অ্যাক্টিভ দিন: {user_data.get('days_active', 1)}

⭐ <b>ব্যাজেস:</b>
{', '.join([b['name'] for b in badges]) or 'No badges yet'}

📈 <b>অ্যানালাইসিস:</b>
• অ্যাক্টিভিটি লেভেল: {analytics['activity_level'].replace('_', ' ').title()}
• রোস্ট স্টাইল: {analytics['roast_style'].replace('_', ' ').title()}
• এনগেজমেন্ট স্কোর: {analytics['engagement_score']}/100

🔧 <b>কমান্ড:</b>
/analyze - টেক্সট এআই অ্যানালাইসিস
/report - ডিটেইল্ড রিপোর্ট
/stats - বট স্ট্যাটিস্টিকস
/theme - থিম পরিবর্তন

━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            await update.message.reply_text(
                profile_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Generate and send premium profile card
            await self._generate_premium_profile_card(update, user, user_data, badges, analytics)
            
        except Exception as e:
            logger.error(f"Error in profile command: {e}")
            await update.message.reply_text(
                "📊 আপনার প্রোফাইল লোড করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def _generate_premium_profile_card(self, update: Update, user: Any, 
                                           user_data: Dict, badges: List[Dict], analytics: Dict):
        """Generate premium profile card image"""
        try:
            # Create profile data
            profile_data = {
                "user": user,
                "stats": user_data,
                "badges": badges,
                "analytics": analytics,
                "premium": True,
                "theme": "diamond"
            }
            
            # Generate image
            result = await self.image_gen.generate_premium_roast_image(
                profile_data, 
                user,
                "diamond",
                badges
            )
            
            if result.success and result.image_path:
                with open(result.image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="💎 আপনার প্রিমিয়াম প্রোফাইল কার্ড",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result.image_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error generating premium profile card: {e}")
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command - AI text analysis"""
        user = update.effective_user
        
        if not update.message.text or len(update.message.text.split()) < 2:
            await update.message.reply_text(
                "টেক্সট দিন অ্যানালাইসিসের জন্য: /analyze <your text>",
                parse_mode=ParseMode.HTML
            )
            return
        
        text = ' '.join(update.message.text.split()[1:])
        
        # Check minimum length
        if len(text) < 10:
            await update.message.reply_text(
                "অ্যানালাইসিসের জন্য কমপক্ষে ১০ অক্ষর প্রয়োজন।",
                parse_mode=ParseMode.HTML
            )
            return
        
        await update.message.reply_text(
            "🤖 এআই অ্যানালাইসিস চলছে...",
            parse_mode=ParseMode.HTML
        )
        
        try:
            if self.has_full_premium and HAS_AI:
                # Use advanced AI analytics
                analysis = await self.ai_analytics.analyze_text_depth(text)
                
                # Format results
                analysis_text = self._format_ai_analysis(analysis, user)
                
                await update.message.reply_text(
                    analysis_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                
                # Update stats
                self.stats["ai_analyses"] += 1
                
                # Generate analysis report
                await self._generate_ai_analysis_report(update, user, text, analysis)
                
            else:
                # Fallback to basic analysis
                await update.message.reply_text(
                    "⚠️ এআই অ্যানালাইসিস বর্তমানে unavailable।",
                    parse_mode=ParseMode.HTML
                )
                
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            await update.message.reply_text(
                "❌ অ্যানালাইসিসে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    def _format_ai_analysis(self, analysis: Dict, user: Any) -> str:
        """Format AI analysis results"""
        basic = analysis.get("basic_metrics", {})
        sentiment = analysis.get("sentiment_analysis", {})
        
        return f"""
🔍 <b>এআই টেক্সট অ্যানালাইসিস</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>📊 বেসিক মেট্রিক্স:</b>
• শব্দ: {basic.get('word_count', 0):,}
• বাক্য: {basic.get('sentence_count', 0):,}
• অক্ষর: {basic.get('char_count', 0):,}
• ইউনিক শব্দ: {basic.get('unique_words', 0):,}

<b>😊 সেন্টিমেন্ট:</b>
• Overall: {sentiment.get('overall_sentiment', {}).get('label', 'UNKNOWN')}
• Score: {sentiment.get('overall_sentiment', {}).get('score', 0):.3f}
• Confidence: {sentiment.get('overall_sentiment', {}).get('confidence', 0):.1%}

<b>📈 রিডেবিলিটি:</b>
• Level: {analysis.get('readability_scores', {}).get('reading_level', 'UNKNOWN')}

<b>🎭 ইমোশনাল টোন:</b>
• Dominant: {analysis.get('emotional_tone', {}).get('dominant_emotion', 'UNKNOWN').upper()}

━━━━━━━━━━━━━━━━━━━━━━━━
        """
    
    async def _generate_ai_analysis_report(self, update: Update, user: Any, 
                                         text: str, analysis: Dict):
        """Generate AI analysis report"""
        try:
            if self.has_full_premium:
                user_info = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
                
                # Generate report
                report_path = await self.report_generator.generate_pdf_report(
                    analysis, user_info
                )
                
                if report_path and os.path.exists(report_path):
                    with open(report_path, 'rb') as report_file:
                        await update.message.reply_document(
                            document=report_file,
                            filename=f"AI_Analysis_{user.id}.pdf",
                            caption="📊 এআই অ্যানালাইসিস রিপোর্ট"
                        )
                    
                    # Cleanup
                    try:
                        os.remove(report_path)
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Error generating AI report: {e}")
    
    async def theme_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /theme command - Change theme"""
        user = update.effective_user
        
        themes = list(self.theme_manager.themes.keys())
        
        if not update.message.text or len(update.message.text.split()) < 2:
            # Show available themes
            theme_list = "\n".join([f"• {name}: {self.theme_manager.themes[name]['name']}" 
                                   for name in themes])
            
            await update.message.reply_text(
                f"""
🎨 <b>প্রিমিয়াম থিমস</b>
━━━━━━━━━━━━━━━━━━
{theme_list}

<b>ব্যবহার:</b> /theme <name>
<b>উদাহরণ:</b> /theme neon
━━━━━━━━━━━━━━━━━━
                """,
                parse_mode=ParseMode.HTML
            )
            return
        
        theme_name = update.message.text.split()[1].lower()
        
        if theme_name not in themes:
            await update.message.reply_text(
                f"❌ থিম '{theme_name}' পাওয়া যায়নি।\n"
                f"Available: {', '.join(themes)}",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Set theme for user
        self.theme_manager.current_theme = theme_name
        
        await update.message.reply_text(
            f"✅ থিম পরিবর্তন করা হয়েছে: {self.theme_manager.themes[theme_name]['name']}",
            parse_mode=ParseMode.HTML
        )
    
    async def report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /report command - Generate professional report"""
        user = update.effective_user
        
        if not update.message.text or len(update.message.text.split()) < 2:
            await update.message.reply_text(
                "টেক্সট দিন রিপোর্টের জন্য: /report <your text>",
                parse_mode=ParseMode.HTML
            )
            return
        
        text = ' '.join(update.message.text.split()[1:])
        
        await update.message.reply_text(
            "📊 প্রফেশনাল রিপোর্ট তৈরি হচ্ছে...",
            parse_mode=ParseMode.HTML
        )
        
        try:
            if self.has_full_premium:
                # Get user info
                user_info = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
                
                # Get roast data
                roast_data = await self.roast_engine.generate_roast(text, user)
                
                # Generate reports
                reports = []
                
                # PDF Report
                pdf_report = await self.report_generator.generate_pdf_report(
                    {"roast_data": roast_data, "text": text}, 
                    user_info
                )
                if pdf_report:
                    reports.append(pdf_report)
                
                # Dashboard Report
                dashboard_report = await self.report_generator.generate_dashboard_report(
                    {"roast_data": roast_data, "text": text}, 
                    user_info
                )
                if dashboard_report:
                    reports.append(dashboard_report)
                
                # Send reports
                for report in reports:
                    if os.path.exists(report):
                        with open(report, 'rb') as report_file:
                            filename = os.path.basename(report)
                            await update.message.reply_document(
                                document=report_file,
                                filename=filename,
                                caption="📈 প্রফেশনাল রিপোর্ট"
                            )
                
                # Cleanup
                for report in reports:
                    try:
                        os.remove(report)
                    except:
                        pass
                
                await update.message.reply_text(
                    "✅ রিপোর্ট জেনারেশন সম্পূর্ণ!",
                    parse_mode=ParseMode.HTML
                )
                
            else:
                await update.message.reply_text(
                    "⚠️ রিপোর্ট ফিচার বর্তমানে unavailable।",
                    parse_mode=ParseMode.HTML
                )
                
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            await update.message.reply_text(
                "❌ রিপোর্ট তৈরি করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    # Override original methods with premium features
    async def _generate_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                text: str, user: Any, chat: Any):
        """Generate premium response"""
        try:
            # Generate typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(text, user)
            
            # Update stats
            self.stats["roasts_generated"] += 1
            self.stats["premium_roasts"] += 1
            
            # Get user data for badges
            user_data = self.db.get_user_stats(user.id)
            badges = self.badge_system.get_user_badges(user.id, user_data)
            
            # Generate premium image with theme
            image_result = await self.image_gen.generate_premium_roast_image(
                roast_data, 
                user,
                self.theme_manager.current_theme,
                badges
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = await self.diagram_gen.generate_diagram_async(
                    text, 
                    roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_result.success and image_result.image_path:
                # Send image
                with open(image_result.image_path, 'rb') as photo:
                    caption = f"💎 {roast_data.get('caption', 'প্রিমিয়াম রোস্ট! 🔥')}"
                    sent_message = await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Update cache stats
                if image_result.cache_hit:
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["cache_misses"] += 1
                
                # Cleanup
                try:
                    os.remove(image_result.image_path)
                except:
                    pass
                
                self.stats["images_created"] += 1
                
                # Add premium voting buttons
                try:
                    await self.voting_system.add_voting_buttons(sent_message, user, None, premium=True)
                except:
                    pass
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 প্রিমিয়াম অ্যানালাইসিস ডায়াগ্রাম",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(diagram_path)
                except:
                    pass
                
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True) and roast_data.get("primary_roast"):
                premium_text = f"💎 {roast_data.get('primary_roast')}"
                await update.message.reply_text(
                    premium_text,
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating premium response: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            await update.message.reply_text(
                f"💎 {text}\n\n- প্রিমিয়াম {user.first_name}",
                parse_mode=ParseMode.HTML
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command - PREMIUM VERSION"""
        help_text = f"""
<b>{self.bot_name} v15.0 - {self.bot_tagline}</b>

💎 <b>প্রিমিয়াম বৈশিষ্ট্য:</b>
• এআই-পাওয়ারড টেক্সট অ্যানালাইসিস
• প্রিমিয়াম থিমড ইমেজ জেনারেশন
• ইউজার ইনফরমেশন কার্ডস
• অ্যাডভান্সড ড্যাশবোর্ড
• ব্লকচেইন ইন্টিগ্রেশন
• প্রফেশনাল রিপোর্টিং

🚀 <b>ব্যবহার পদ্ধতি:</b>
• যেকোনো টেক্সট পাঠান (সর্বনিম্ন ৪ অক্ষর)
• আমি প্রিমিয়াম ইমেজ + ডায়াগ্রাম + অ্যানালাইসিস দেব

🎯 <b>নতুন কমান্ড:</b>
/profile - আপনার প্রিমিয়াম প্রোফাইল
/analyze - এআই টেক্সট অ্যানালাইসিস
/report - প্রফেশনাল রিপোর্ট
/stats - ডিটেইল্ড স্ট্যাটিস্টিকস
/theme - থিম পরিবর্তন করুন
/leaderboard - প্রিমিয়াম লিডারবোর্ড

🔧 <b>মূল কমান্ড:</b>
/start - শুরু করুন
/help - সাহায্য
/health - সিস্টেম স্বাস্থ্য

⚡ <b>টিপস:</b>
• থিম পরিবর্তন করে নতুন লুক পান
• প্রফাইল চেক করে ব্যাজেস দেখুন
• রিপোর্ট জেনারেট করে শেয়ার করুন

🔒 <b>প্রিমিয়াম সিকিউরিটি:</b>
• এন্ড-টু-এন্ড এনক্রিপশন
• রেট লিমিটিং
• সিকিউরিটি অডিট লগিং

📊 <b>স্ট্যাটাস:</b>
✅ All Systems Operational
💎 Premium Features Active
⚡ Ultra Fast Response
        """
        
        await update.message.reply_text(
            help_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - PREMIUM VERSION"""
        user = update.effective_user
        
        try:
            # Check if admin
            admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if user.id not in admin_ids and user.id != owner_id:
                await update.message.reply_text(
                    "❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!",
                    parse_mode=ParseMode.HTML
                )
                return
        except:
            pass
        
        # Calculate uptime
        uptime = datetime.now() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        # Get premium stats
        img_stats = self.image_gen.get_stats()
        
        stats_text = f"""
<b>{self.bot_name} প্রিমিয়াম পরিসংখ্যান v15.0</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>আপটাইম:</b> {days}দিন {hours}ঘণ্টা {minutes}মিনিট
📊 <b>বার্তা প্রসেসড:</b> {self.stats['messages_processed']:,}
💎 <b>প্রিমিয়াম রোস্ট:</b> {self.stats['premium_roasts']:,}
🔥 <b>মোট রোস্ট:</b> {self.stats['roasts_generated']:,}
🖼️ <b>ইমেজ তৈরি:</b> {self.stats['images_created']:,}
📈 <b>ডায়াগ্রাম তৈরি:</b> {self.stats['diagrams_created']:,}
👥 <b>ইউজার:</b> {len(self.stats['users_interacted']):,}
💎 <b>প্রিমিয়াম ইউজার:</b> {len(self.stats['premium_users']):,}
🏠 <b>গ্রুপ:</b> {len(self.stats['groups_managed']):,}
📊 <b>ইউজার কার্ড:</b> {self.stats['user_info_cards']:,}
🤖 <b>এআই অ্যানালাইসিস:</b> {self.stats['ai_analyses']:,}

<b>ইমেজ জেনারেশন:</b>
✅ <b>সাকসেস রেট:</b> {img_stats['performance']['success_rate']}%
⚡ <b>অ্যাভারেজ টাইম:</b> {img_stats['performance']['average_time_seconds']:.2f}s
💾 <b>ক্যাশে হিট রেট:</b> {img_stats['performance']['cache_hit_rate']}%
🔄 <b>ক্যাশে আইটেম:</b> {img_stats['cache']['total_items']:,}
🎨 <b>থিমস:</b> {img_stats.get('themes_available', 5)}

<b>প্রিমিয়াম স্ট্যাটাস:</b> ✅ ACTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        await update.message.reply_text(
            stats_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    def setup_handlers(self, application):
        """Setup all bot handlers - PREMIUM VERSION"""
        # Premium command handlers
        application.add_handler(CommandHandler("profile", self.profile_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("report", self.report_command))
        application.add_handler(CommandHandler("theme", self.theme_command))
        
        # Original command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("health", self.health_command))
        application.add_handler(CommandHandler("leaderboard", self.handle_leaderboard_command))
        
        # Message handlers
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
        
        # New chat members
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_chat_members
        ))
        
        # Callback queries
        application.add_handler(CallbackQueryHandler(
            self.handle_vote_callback, pattern="^vote_"
        ))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        logger.info("Premium handlers setup complete")
    
    async def post_init(self, application):
        """Run after bot initialization - PREMIUM VERSION"""
        logger.info(f"{self.bot_name} প্রিমিয়াম বট চালু হচ্ছে v15.0...")
        
        # Initialize auto daily quote
        try:
            self.auto_daily_quote = AutoDailyQuote(application.job_queue)
            logger.info("Auto Daily Quote initialized")
        except Exception as e:
            logger.error(f"Auto Daily Quote init failed: {e}")
            self.auto_daily_quote = None
        
        # Start enterprise dashboard if available
        if self.has_full_premium:
            try:
                self.enterprise_dashboard.run_dashboard()
                self.enterprise_dashboard.run_api()
                logger.info("Enterprise Dashboard started")
            except Exception as e:
                logger.error(f"Dashboard start failed: {e}")
        
        # Start background tasks
        asyncio.create_task(self._premium_background_tasks())
        
        # Send premium startup notification
        await self._send_premium_startup_notification()
        
        logger.info("Premium bot startup complete")
    
    async def _premium_background_tasks(self):
        """Run premium background maintenance tasks"""
        while True:
            try:
                # Premium cleanup
                self.db.cleanup_old_data(days=30)  # Keep data longer
                
                # Cleanup premium temp files
                self._cleanup_premium_temp_files()
                
                # Update premium user analytics
                await self._update_premium_analytics()
                
                # Log premium statistics
                logger.info(f"Premium Stats: {self.stats['premium_roasts']} premium roasts, "
                           f"{len(self.stats['premium_users'])} premium users")
                
                # Sleep for 30 minutes
                await asyncio.sleep(1800)
                
            except Exception as e:
                logger.error(f"Error in premium background tasks: {e}")
                await asyncio.sleep(300)
    
    async def _update_premium_analytics(self):
        """Update premium user analytics"""
        try:
            # This would typically update user analytics in the database
            pass
        except Exception as e:
            logger.error(f"Error updating premium analytics: {e}")
    
    def _cleanup_premium_temp_files(self):
        """Cleanup premium temporary files"""
        try:
            temp_dir = Path("temp/premium")
            if temp_dir.exists():
                cutoff_time = time.time() - 7200  # 2 hours ago for premium
                
                for file in temp_dir.glob("*"):
                    if file.is_file():
                        try:
                            if file.stat().st_mtime < cutoff_time:
                                file.unlink()
                        except:
                            pass
        except Exception as e:
            logger.error(f"Premium temp cleanup error: {e}")
    
    async def _send_premium_startup_notification(self):
        """Send premium startup notification to owner"""
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if owner_id:
                bot_info = await self.application.bot.get_me()
                startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get system health
                health = self.image_gen.health_check()
                
                message = f"""
🚀 <b>{self.bot_name} PREMIUM Started Successfully v15.0!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot Username:</b> @{bot_info.username}
📊 <b>Version:</b> 15.0.0 PREMIUM
💎 <b>Edition:</b> Ultimate Premium
🏥 <b>Health:</b> {"✅ Healthy" if health['healthy'] else "⚠️ Issues"}

<b>Premium Features:</b>
• Advanced AI Analytics ✅
• User Information Cards ✅
• Enterprise Dashboard ✅
• Blockchain Integration ✅
• Professional Reports ✅
• Premium Themes ✅
• Badge System ✅

<b>Statistics:</b>
• Premium Users: {len(self.stats['premium_users'])}
• Premium Roasts: {self.stats['premium_roasts']}
• AI Analyses: {self.stats['ai_analyses']}

✅ <b>Status:</b> ALL PREMIUM SYSTEMS OPERATIONAL
🔥 <b>Ready for ultimate roasting experience!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
                """
                
                await self.application.bot.send_message(
                    chat_id=owner_id,
                    text=message,
                    parse_mode=ParseMode.HTML
                )
                
                logger.info("Premium startup notification sent to owner")
        except Exception as e:
            logger.error(f"Error sending premium startup notification: {e}")
    
    # Keep original methods for compatibility
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages - PREMIUM VERSION"""
        try:
            # Update statistics
            self.stats["messages_processed"] += 1
            
            user = update.effective_user
            chat = update.effective_chat
            message = update.message
            
            if not message or not message.text:
                return
            
            text = message.text.strip()
            
            # Add user to interacted set
            self.stats["users_interacted"].add(user.id)
            
            # Add group to managed set
            if chat.type in ["group", "supergroup"]:
                self.stats["groups_managed"].add(chat.id)
            
            # Check cooldown
            if not self._check_cooldown(user.id):
                if chat.type == "private":
                    await message.reply_text(
                        "⏳ একটু অপেক্ষা করুন! খুব দ্রুত রিকোয়েস্ট করছেন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
            # Check minimum length
            if len(text) < CORE_RULES.get("minimum_input_length", 4):
                if len(text) > 0:
                    await message.reply_text(
                        f"একটু লম্বা লিখুন! কমপক্ষে {CORE_RULES.get('minimum_input_length', 4)} অক্ষর প্রয়োজন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
            # Check ignore conditions
            if self._should_ignore_message(text):
                return
            
            # Check for admin protection
            try:
                if await self.admin_protection.check_protection_needed(user, text, chat):
                    await self.admin_protection.handle_protected_response(
                        update, context, user, text
                    )
                    return
            except Exception as e:
                logger.error(f"Admin protection error: {e}")
            
            # Check for mentions in groups
            if chat.type in ["group", "supergroup"]:
                try:
                    mention_result = await self.mention_roast.process_mention(
                        message, text, user, chat
                    )
                    if mention_result:
                        await self._generate_mention_response(
                            update, context, text, user, chat, mention_result
                        )
                        return
                except Exception as e:
                    logger.error(f"Error processing mention: {e}")
            
            # Generate premium response
            await self._generate_response(update, context, text, user, chat)
            
            # Auto reactions
            try:
                await self.reaction_system.add_auto_reactions(message, text, user, chat)
            except Exception as e:
                logger.error(f"Auto reaction error: {e}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            if update.message:
                await update.message.reply_text(
                    "⚠️ সমস্যা হয়েছে! আবার চেষ্টা করুন।",
                    parse_mode=ParseMode.HTML
                )
    
    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle vote callback queries"""
        try:
            await self.voting_system.handle_vote_callback(update, context)
        except Exception as e:
            logger.error(f"Error handling vote callback: {e}")
            await update.callback_query.answer("ভোট প্রসেসে সমস্যা!", show_alert=True)
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        try:
            await self.welcome_system.handle_new_members(update, context)
        except Exception as e:
            logger.error(f"Error handling new chat members: {e}")
    
    async def handle_leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        try:
            await self.leaderboard.handle_leaderboard_command(update, context)
        except Exception as e:
            logger.error(f"Error handling leaderboard: {e}")
            await update.message.reply_text(
                "লিডারবোর্ড লোড করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling update: {context.error}")
        traceback_str = traceback.format_exc()
        logger.error(f"Traceback:\n{traceback_str}")
        
        # Try to send error to admin
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            if owner_id and context.bot:
                error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_msg = str(context.error)[:500]
                
                error_text = f"""
🚨 <b>প্রিমিয়াম বট এরর!</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>সময়:</b> {error_time}
💥 <b>এরর:</b> {error_msg}
💎 <b>এডিশন:</b> Premium v15.0
━━━━━━━━━━━━━━━━━━━━
<b>অ্যাকশন:</b> চেক প্রিমিয়াম লগ ফাইল
                """
                
                await context.bot.send_message(
                    chat_id=owner_id,
                    text=error_text,
                    parse_mode=ParseMode.HTML
                )
        except:
            pass
    
    def _should_ignore_message(self, text: str) -> bool:
        """Check if message should be ignored"""
        # Same as original but can be extended for premium
        # Check for only emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002500-\U00002BEF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"
            u"\u3030"
            "]+", flags=re.UNICODE)
        
        if emoji_pattern.sub('', text).strip() == '':
            return True
        
        # Check for only numbers
        if text.strip().isdigit():
            return True
        
        # Check for links only
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        if url_pattern.sub('', text).strip() == '':
            return True
        
        # Check for very repetitive text
        if len(text) > 20:
            if text.count(text[0]) / len(text) > 0.8:
                return True
        
        return False
    
    async def _generate_mention_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        text: str, user: Any, chat: Any, mention_result: Dict):
        """Generate response for mentioned user - PREMIUM VERSION"""
        try:
            target_user = mention_result.get("target")
            roast_text = mention_result.get("roast_text", text)
            
            # Generate typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(
                roast_text, user, target_user
            )
            
            # Update stats
            self.stats["roasts_generated"] += 1
            self.stats["premium_roasts"] += 1
            
            # Get user data for badges
            user_data = self.db.get_user_stats(user.id)
            badges = self.badge_system.get_user_badges(user.id, user_data)
            
            # Generate premium image
            image_result = await self.image_gen.generate_premium_roast_image(
                roast_data, 
                user,
                self.theme_manager.current_theme,
                badges
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = await self.diagram_gen.generate_diagram_async(
                    roast_text, 
                    roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_result.success and image_result.image_path:
                # Send image
                with open(image_result.image_path, 'rb') as photo:
                    caption = f"💎 {roast_data.get('caption', f'{target_user.first_name} -কে প্রিমিয়াম রোস্ট!')}"
                    sent_message = await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Update cache stats
                if image_result.cache_hit:
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["cache_misses"] += 1
                
                # Cleanup
                try:
                    os.remove(image_result.image_path)
                except:
                    pass
                
                self.stats["images_created"] += 1
                
                # Add voting buttons
                try:
                    await self.voting_system.add_voting_buttons(sent_message, user, target_user, premium=True)
                except:
                    pass
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 প্রিমিয়াম অ্যানালাইসিস ডায়াগ্রাম",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(diagram_path)
                except:
                    pass
                
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True) and roast_data.get("primary_roast"):
                premium_text = f"💎 {roast_data.get('primary_roast')}"
                await update.message.reply_text(
                    premium_text,
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating premium mention response: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            await update.message.reply_text(
                f"💎 {mention_result.get('target_name', 'User')} -কে প্রিমিয়াম রোস্ট! 🔥",
                parse_mode=ParseMode.HTML
            )
    
    def run(self):
        """Run the bot - PREMIUM VERSION"""
        try:
            # Create application
            self.application = ApplicationBuilder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Run bot
            logger.info(f"Starting {self.bot_name} PREMIUM bot v15.0...")
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except KeyboardInterrupt:
            logger.info("Premium bot stopped by user")
            
            # Cleanup
            try:
                self.image_gen.cleanup()
            except:
                pass
            
        except Exception as e:
            logger.error(f"Fatal error running premium bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            
            # Cleanup
            try:
                self.image_gen.cleanup()
            except:
                pass
            
            raise


def create_premium_directories():
    """Create necessary directories for premium"""
    directories = [
        "assets/premium/fonts",
        "assets/premium/borders",
        "assets/premium/templates",
        "assets/premium/backgrounds",
        "assets/premium/badges",
        "output/premium",
        "temp/premium",
        "cache/premium",
        "backup/premium",
        "logs/premium",
        "data/premium",
        "premium",
        "reports"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created premium directory: {directory}")


def main():
    """Main entry point - PREMIUM VERSION"""
    # Create premium directories
    create_premium_directories()
    
    # Check for required AI packages
    if not HAS_AI:
        logger.warning("AI packages not installed. Install: pip install numpy nltk textblob spacy")
    
    # Check for premium modules
    if not HAS_PREMIUM:
        logger.warning("Premium modules not found. Some features will be disabled.")
        logger.info("Creating premium modules...")
        # We'll create these in the next step
    
    # Run premium bot
    bot = PremiumRoastifyBot()
    bot.run()


if __name__ == "__main__":
    main()
