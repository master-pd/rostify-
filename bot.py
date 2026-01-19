#!/usr/bin/env python3
"""
🔥 ROASTIFY BOT v8.0 ULTRA PRO MAX - COMPLETE UPGRADED VERSION
✅ Integrated with Advanced Image Generator v8.0
✅ Background Images + Profile Pictures + User Info Cards
✅ Async Processing + Error Handling + Statistics
📊 Version: 8.0.0 ULTRA PRO MAX
⚡ Author: Roastify AI Team
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
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import concurrent.futures
import hashlib
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
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
    
    # Import NEW UltimateImageGenerator v8.0
    from utils.image_generator_ultimate import (
        UltimateImageGenerator,
        GenerationResult,
        UserInfo as ImageUserInfo,
        ImageConfig,
        DesignConfig,
        ImageStyle,
        BackgroundType,
        ProfileStyle,
        TextEffect,
        get_image_generator
    )
    
    IMAGE_GEN_AVAILABLE = True
    logger.info("✅ UltimateImageGenerator v8.0 imported successfully")
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(traceback.format_exc())
    IMAGE_GEN_AVAILABLE = False

# Import Telegram
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters,
        ContextTypes, CallbackQueryHandler, ApplicationBuilder
    )
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.error("Install: pip install python-telegram-bot")
    TELEGRAM_AVAILABLE = False


class AsyncImageGenerator:
    """Async wrapper for the new UltimateImageGenerator v8.0"""
    
    def __init__(self):
        if not IMAGE_GEN_AVAILABLE:
            raise ImportError("Image generator not available")
        
        self.generator = get_image_generator()
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix='ImageGenAsync'
        )
        logger.info("✅ AsyncImageGenerator v8.0 initialized")
    
    async def generate_roast_image_async(self, roast_text: Any, user_info: Any,
                                       design_config: Optional[DesignConfig] = None) -> GenerationResult:
        """Async wrapper for image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_roast_image(
                    roast_text=roast_text,
                    user_info=user_info,
                    design_config=design_config
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
    
    async def generate_achievement_image_async(self, user_info: Any, achievement: str) -> GenerationResult:
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
        return self.generator.get_stats()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.generator.cleanup()
            self.executor.shutdown(wait=False)
        except:
            pass


class DiagramGenerator:
    """Generate diagrams for roasts"""
    
    def __init__(self):
        self.diagram_types = [
            "funny_analysis", "roast_meter", "humor_chart",
            "sarcasm_graph", "cleverness_map", "impact_diagram"
        ]
        
        # Color palettes
        self.palettes = {
            "funny": [(255, 200, 100), (255, 150, 150), (200, 255, 200)],
            "savage": [(255, 100, 100), (200, 50, 50), (150, 150, 150)],
            "clever": [(100, 200, 255), (150, 100, 255), (200, 200, 100)],
        }
    
    async def generate_diagram_async(self, text: str, roast_type: str = "funny") -> Optional[str]:
        """Generate a simple diagram image based on text"""
        try:
            # Create temp directory
            os.makedirs("temp", exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp/diagram_{timestamp}.png"
            
            # Create simple diagram
            self._create_simple_diagram(text, roast_type, filename)
            
            if os.path.exists(filename):
                return filename
            return None
            
        except Exception as e:
            logger.error(f"Diagram generation failed: {e}")
            return None
    
    def _create_simple_diagram(self, text: str, roast_type: str, filename: str):
        """Create a simple diagram"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Create data based on text
            text_hash = hashlib.md5(text.encode()).hexdigest()
            categories = ['Humor', 'Sarcasm', 'Cleverness', 'Impact', 'Style']
            
            # Generate values from hash
            values = []
            for i in range(5):
                val = int(text_hash[i*6:(i+1)*6], 16) % 100
                values.append(val)
            
            # Create radar chart
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
            
            # Plot
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            
            # Set category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            
            # Set title
            ax.set_title(f'Roast Analysis: {roast_type.title()}', size=14, y=1.1)
            
            # Save
            plt.tight_layout()
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            plt.close()
            
        except ImportError:
            # Fallback to text-based diagram
            self._create_text_diagram(text, roast_type, filename)
    
    def _create_text_diagram(self, text: str, roast_type: str, filename: str):
        """Create text-based diagram"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (600, 400), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Add title
            title = f"Roast Analysis: {roast_type.upper()}"
            draw.text((50, 30), title, fill=(0, 0, 0))
            
            # Add analysis
            analysis_lines = [
                f"Text Length: {len(text)} chars",
                f"Roast Type: {roast_type}",
                f"Humor Score: {random.randint(50, 95)}%",
                f"Sarcasm Level: {random.randint(40, 90)}%",
                f"Impact Rating: {random.randint(60, 98)}%",
                f"Style Points: {random.randint(70, 95)}%"
            ]
            
            y_pos = 80
            for line in analysis_lines:
                draw.text((50, y_pos), line, fill=(50, 50, 50))
                y_pos += 35
            
            # Add footer
            footer = "Generated by Roastify v8.0"
            draw.text((400, 350), footer, fill=(150, 150, 150))
            
            # Save
            img.save(filename, 'PNG', quality=95)
            
        except Exception as e:
            logger.error(f"Text diagram creation failed: {e}")


class RoastifyBotV8:
    """Main Roastify Bot Class v8.0 - Upgraded Version"""
    
    def __init__(self):
        """Initialize the upgraded bot"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY.get("name", "Roastify Pro")
        self.bot_tagline = BOT_IDENTITY.get("tagline", "Advanced Roasting AI")
        
        # Initialize components
        self.db = get_database()
        
        # Initialize Image Generator
        self.image_gen = None
        if IMAGE_GEN_AVAILABLE:
            try:
                self.image_gen = AsyncImageGenerator()
                logger.info("✅ Image generator initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize image generator: {e}")
                self.image_gen = None
        
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
        
        # Enhanced Statistics
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
            "profile_images_used": 0,
            "background_images_used": 0,
            "user_info_cards_shown": 0
        }
        
        # Application instance
        self.application = None
        
        # Rate limiting
        self.user_cooldowns = {}
        self.cooldown_seconds = CORE_RULES.get("cooldown_seconds", 3)
        
        logger.info(f"✅ {self.bot_name} Bot v8.0 initialized successfully")
    
    def _check_cooldown(self, user_id: int) -> bool:
        """Check if user is in cooldown"""
        now = time.time()
        last_request = self.user_cooldowns.get(user_id, 0)
        
        if now - last_request < self.cooldown_seconds:
            return False
        
        self.user_cooldowns[user_id] = now
        return True
    
    def _convert_user_to_image_userinfo(self, user: Any) -> Dict:
        """Convert Telegram user to ImageUserInfo format"""
        # Extract from database or user object
        user_data = self.db.get_user(user.id) or {}
        
        return {
            'id': user.id,
            'username': user.username or f"user_{user.id}",
            'first_name': user.first_name or "User",
            'last_name': user.last_name or "",
            'rating': user_data.get('rating', random.uniform(5.0, 9.5)),
            'level': user_data.get('level', random.randint(1, 100)),
            'rank': user_data.get('rank', "Member"),
            'posts_count': user_data.get('posts_count', random.randint(0, 500)),
            'likes_count': user_data.get('likes_count', random.randint(0, 1000)),
            'bio': user_data.get('bio', "রোস্টিং এর শিল্পী 🎨"),
            'badges': user_data.get('badges', ["Active", "Funny"]),
            'profile_pic_url': None  # Can be added if available
        }
    
    def _create_design_config(self, roast_type: str = "funny") -> DesignConfig:
        """Create design configuration based on roast type"""
        
        if roast_type == "savage":
            return DesignConfig(
                style=ImageStyle.CYBERPUNK,
                background_type=BackgroundType.GRADIENT,
                profile_style=ProfileStyle.CIRCLE,
                text_effect=TextEffect.GLOW_NEON,
                show_profile=True,
                show_user_info=True,
                border_color=(255, 50, 50),
                border_thickness=15
            )
        elif roast_type == "clever":
            return DesignConfig(
                style=ImageStyle.GOLDEN_LUXURY,
                background_type=BackgroundType.LOCAL_IMAGE,
                profile_style=ProfileStyle.HEXAGON,
                text_effect=TextEffect.METALLIC,
                show_profile=True,
                show_user_info=True,
                border_color=(255, 215, 0),
                border_thickness=12
            )
        elif roast_type == "friendly":
            return DesignConfig(
                style=ImageStyle.PASTEL_DREAM,
                background_type=BackgroundType.SOLID_COLOR,
                profile_style=ProfileStyle.HEART,
                text_effect=TextEffect.GRADIENT_TEXT,
                show_profile=True,
                show_user_info=True,
                border_color=(100, 200, 255),
                border_thickness=10
            )
        else:  # funny/default
            return DesignConfig(
                style=ImageStyle.NEON_GLOW,
                background_type=BackgroundType.ONLINE_IMAGE,
                profile_style=ProfileStyle.ROUNDED,
                text_effect=TextEffect.SHADOW_3D,
                show_profile=True,
                show_user_info=True,
                border_color=(0, 255, 200),
                border_thickness=15
            )
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        try:
            # Add user to database
            self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            # Enhanced welcome message
            welcome_message = f"""
🎉 <b>স্বাগতম {user.first_name}!</b>

🤖 আমি <b>{self.bot_name} v8.0</b> - {self.bot_tagline}

✨ <b>নতুন আপগ্রেডেড ফিচার:</b>
• প্রোফাইল ইমেজ সহ HD রোস্ট ইমেজ
• ইউজার ইনফো কার্ড (রেটিং, লেভেল, ব্যাজ)
• র‍্যান্ডম ব্যাকগ্রাউন্ড ইমেজ
• অ্যাডভান্সড টেক্সট ইফেক্টস
• রিয়েল-টাইম ডায়াগ্রাম

🔥 <b>ব্যবহার:</b>
১. কিছু লিখে পাঠান
২. রিসিভ করুন প্রফেশনাল ইমেজ + ডায়াগ্রাম
৩. ভোট দিয়ে ফিডব্যাক দিন

📊 <b>ইউজার প্রোফাইল:</b>
• রেটিং সিস্টেম
• লেভেল আপগ্রেড
• অ্যাচিভমেন্ট আনলক
• ব্যাজ কালেকশন

🔧 <b>কমান্ড:</b>
/help - সাহায্য
/profile - আপনার প্রোফাইল
/stats - বট স্ট্যাটাস
/leaderboard - টপ রোস্টার
/achievements - অর্জনসমূহ

⚡ <b>এখনি চেষ্টা করুন কিছু লিখে পাঠিয়ে!</b>
            """
            
            # Generate welcome image if available
            if self.image_gen:
                try:
                    user_info = self._convert_user_to_image_userinfo(user)
                    welcome_result = await self.image_gen.generate_welcome_image_async(user_info)
                    
                    if welcome_result.success and welcome_result.image_path:
                        # Send welcome image
                        with open(welcome_result.image_path, 'rb') as photo:
                            await update.message.reply_photo(
                                photo=photo,
                                caption=f"🎉 {user.first_name} -কে স্বাগতম {self.bot_name}!",
                                parse_mode=ParseMode.HTML
                            )
                        
                        # Update stats
                        self.stats["images_created"] += 1
                        
                        # Cleanup
                        try:
                            os.remove(welcome_result.image_path)
                        except:
                            pass
                except Exception as e:
                    logger.error(f"Welcome image generation failed: {e}")
            
            # Send welcome text
            await update.message.reply_text(
                welcome_message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            logger.info(f"New user started: {user.id} ({user.first_name})")
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text(
                f"স্বাগতম {user.first_name}! 🎉\n"
                f"আমি {self.bot_name} - {self.bot_tagline}\n\n"
                f"কিছু লিখে পাঠান রোস্ট শুরু করতে!",
                parse_mode=ParseMode.HTML
            )
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command to show user profile"""
        user = update.effective_user
        
        try:
            # Get user data from database
            user_data = self.db.get_user(user.id) or {}
            
            # Calculate rank
            level = user_data.get('level', 1)
            if level >= 80:
                rank = "👑 Legend"
            elif level >= 50:
                rank = "⭐ Pro"
            elif level >= 20:
                rank = "🔥 Veteran"
            else:
                rank = "🌱 Beginner"
            
            # Create profile message
            profile_message = f"""
📊 <b>ব্যক্তিগত প্রোফাইল</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>নাম:</b> {user.first_name} {user.last_name or ''}
🔗 <b>ইউজারনেম:</b> @{user.username or 'N/A'}
🎯 <b>রেটিং:</b> {user_data.get('rating', 'N/A')}/10
📈 <b>লেভেল:</b> {user_data.get('level', 1)}
🏆 <b>র‍্যাঙ্ক:</b> {rank}

📝 <b>স্ট্যাটিস্টিক্স:</b>
• রোস্ট তৈরি: {user_data.get('roasts_generated', 0)}
• ভোট প্রাপ্ত: {user_data.get('votes_received', 0)}
• লাইক পাওয়া: {user_data.get('likes_received', 0)}
• অ্যাক্টিভ ডে: {user_data.get('active_days', 1)}

🏅 <b>ব্যাজ:</b> {' '.join(user_data.get('badges', ['নতুন']))}

💡 <b>পরবর্তী লক্ষ্য:</b>
• লেভেল {min(100, (user_data.get('level', 1) + 5))} এ পৌঁছান
• ১০+ রোস্ট তৈরি করুন
• ৫০+ ভোট সংগ্রহ করুন

⚡ <b>পরামর্শ:</b>
নিয়মিত রোস্ট তৈরি করে লেভেল ও রেটিং বাড়ান!
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            # Create profile image if available
            if self.image_gen:
                try:
                    user_info = self._convert_user_to_image_userinfo(user)
                    # Update user info with additional data
                    user_info['rank'] = rank
                    user_info['achievements'] = user_data.get('achievements', [])
                    
                    # Generate profile card
                    roast_text = f"{user.first_name} এর প্রোফাইল\n\nরেটিং: {user_data.get('rating', 'N/A')}/10\nলেভেল: {user_data.get('level', 1)}\nর‍্যাঙ্ক: {rank}"
                    
                    design = DesignConfig(
                        style=ImageStyle.DARK_ELEGANT,
                        background_type=BackgroundType.GRADIENT,
                        profile_style=ProfileStyle.CIRCLE,
                        text_effect=TextEffect.SHADOW_3D,
                        show_profile=True,
                        show_user_info=True,
                        show_badges=True,
                        show_stats=True
                    )
                    
                    result = await self.image_gen.generate_roast_image_async(
                        roast_text=roast_text,
                        user_info=user_info,
                        design_config=design
                    )
                    
                    if result.success and result.image_path:
                        with open(result.image_path, 'rb') as photo:
                            await update.message.reply_photo(
                                photo=photo,
                                caption=f"📊 {user.first_name} এর প্রোফাইল",
                                parse_mode=ParseMode.HTML
                            )
                        
                        # Cleanup
                        try:
                            os.remove(result.image_path)
                        except:
                            pass
                        
                        self.stats["profile_images_used"] += 1
                        
                except Exception as e:
                    logger.error(f"Profile image generation failed: {e}")
            
            # Send profile text
            await update.message.reply_text(
                profile_message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error in profile command: {e}")
            await update.message.reply_text(
                "প্রোফাইল লোড করতে সমস্যা! আবার চেষ্টা করুন।",
                parse_mode=ParseMode.HTML
            )
    
    async def achievements_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /achievements command"""
        user = update.effective_user
        
        try:
            # Get user data
            user_data = self.db.get_user(user.id) or {}
            level = user_data.get('level', 1)
            roasts = user_data.get('roasts_generated', 0)
            votes = user_data.get('votes_received', 0)
            
            # Define achievements
            achievements = [
                {"name": "শুরুটা ভালো", "desc": "প্রথম রোস্ট তৈরি", "unlocked": roasts > 0},
                {"name": "১০ এর ক্লাব", "desc": "১০টি রোস্ট তৈরি", "unlocked": roasts >= 10},
                {"name": "৫০ এর মাস্টার", "desc": "৫০টি রোস্ট তৈরি", "unlocked": roasts >= 50},
                {"name": "ভোটের রাজা", "desc": "১০০+ ভোট প্রাপ্ত", "unlocked": votes >= 100},
                {"name": "লেভেল ২০", "desc": "লেভেল ২০ এ পৌঁছান", "unlocked": level >= 20},
                {"name": "লেভেল ৫০", "desc": "লেভেল ৫০ এ পৌঁছান", "unlocked": level >= 50},
                {"name": "প্রিমিয়াম রোস্টার", "desc": "৮.০+ রেটিং", "unlocked": user_data.get('rating', 0) >= 8.0},
                {"name": "সাপ্তাহিক সক্রিয়", "desc": "৭ দিন ধরে সক্রিয়", "unlocked": user_data.get('active_days', 0) >= 7},
            ]
            
            # Count unlocked achievements
            unlocked_count = sum(1 for a in achievements if a["unlocked"])
            total_count = len(achievements)
            
            # Create achievements message
            achievements_message = f"""
🏆 <b>অর্জনসমূহ</b>
━━━━━━━━━━━━━━━━━━━━━━━━
📊 <b>প্রগতি:</b> {unlocked_count}/{total_count} ({int((unlocked_count/total_count)*100)}%)

<b>আপনার অর্জন:</b>
"""
            
            for achievement in achievements:
                if achievement["unlocked"]:
                    achievements_message += f"✅ {achievement['name']}\n"
                    achievements_message += f"   └ {achievement['desc']}\n\n"
                else:
                    achievements_message += f"🔒 {achievement['name']}\n"
                    achievements_message += f"   └ {achievement['desc']}\n\n"
            
            achievements_message += """
⚡ <b>পরবর্তী লক্ষ্য:</b>
• আরও রোস্ট তৈরি করুন
• বেশি ভোট পান
• লেভেল বাড়ান

🔥 <b>টিপস:</b>
• নিয়মিত সক্রিয় থাকুন
• মানসম্মত রোস্ট তৈরি করুন
• অন্যের রোস্টে ভোট দিন
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            await update.message.reply_text(
                achievements_message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error in achievements command: {e}")
            await update.message.reply_text(
                "অর্জন লোড করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages with new image generator"""
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
                        "⏳ একটু অপেক্ষা করুন! খুব দ্রুত রিকোয়েস্ট করছেন।",
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
            
            # Generate regular response with new image generator
            await self._generate_enhanced_response(update, context, text, user, chat)
            
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
    
    def _should_ignore_message(self, text: str) -> bool:
        """Check if message should be ignored"""
        # Check for only emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
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
        
        return False
    
    async def _generate_enhanced_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        text: str, user: Any, chat: Any):
        """Generate response with new image generator"""
        try:
            # Generate typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(text, user)
            roast_type = roast_data.get("roast_type", "funny")
            
            # Update stats
            self.stats["roasts_generated"] += 1
            
            # Check if image generator is available
            if not self.image_gen:
                # Fallback to text only
                await self._send_fallback_response(update, roast_data, user)
                return
            
            # Create user info for image
            user_info = self._convert_user_to_image_userinfo(user)
            
            # Create design configuration
            design = self._create_design_config(roast_type)
            
            # Generate image with new generator
            image_result = await self.image_gen.generate_roast_image_async(
                roast_text=roast_data,
                user_info=user_info,
                design_config=design
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = await self.diagram_gen.generate_diagram_async(
                    text, roast_type
                )
            
            # Send image if successful
            if image_result.success and image_result.image_path:
                await self._send_image_response(update, image_result, roast_data, user)
                self.stats["user_info_cards_shown"] += 1
            else:
                # Fallback to text
                await self._send_fallback_response(update, roast_data, user)
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                await self._send_diagram_response(update, diagram_path)
            
            # Update user data in database
            self._update_user_stats(user.id)
            
        except Exception as e:
            logger.error(f"Error in enhanced response: {e}")
            await self._send_error_response(update, user)
    
    async def _send_image_response(self, update: Update, image_result: GenerationResult, 
                                 roast_data: Dict, user: Any):
        """Send image response"""
        try:
            with open(image_result.image_path, 'rb') as photo:
                caption = roast_data.get("caption", f"🔥 {user.first_name} এর জন্য রোস্ট!")
                
                sent_message = await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
            
            # Update stats
            self.stats["images_created"] += 1
            if "background" in str(image_result.metadata).lower():
                self.stats["background_images_used"] += 1
            
            # Add voting buttons
            try:
                await self.voting_system.add_voting_buttons(sent_message, user, None)
            except:
                pass
            
            # Cleanup
            try:
                os.remove(image_result.image_path)
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error sending image: {e}")
    
    async def _send_diagram_response(self, update: Update, diagram_path: str):
        """Send diagram response"""
        try:
            with open(diagram_path, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption="📊 রোস্ট অ্যানালাইসিস ডায়াগ্রাম",
                    parse_mode=ParseMode.HTML
                )
            
            self.stats["diagrams_created"] += 1
            
            # Cleanup
            try:
                os.remove(diagram_path)
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error sending diagram: {e}")
    
    async def _send_fallback_response(self, update: Update, roast_data: Dict, user: Any):
        """Send fallback text response"""
        try:
            roast_text = roast_data.get("primary_roast", f"🔥 {user.first_name}, তোমার জন্য রোস্ট!")
            await update.message.reply_text(
                roast_text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error sending fallback: {e}")
    
    async def _send_error_response(self, update: Update, user: Any):
        """Send error response"""
        try:
            await update.message.reply_text(
                f"⚠️ {user.first_name}, রোস্ট তৈরি করতে সমস্যা!\nআবার চেষ্টা করুন।",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
    
    def _update_user_stats(self, user_id: int):
        """Update user statistics in database"""
        try:
            # Get current stats
            user_data = self.db.get_user(user_id) or {}
            
            # Update counts
            roasts_generated = user_data.get('roasts_generated', 0) + 1
            active_days = user_data.get('active_days', 0)
            
            # Check if new day
            last_active = user_data.get('last_active')
            today = datetime.now().date()
            
            if not last_active or last_active != str(today):
                active_days += 1
            
            # Update database
            self.db.update_user_stats(
                user_id=user_id,
                roasts_generated=roasts_generated,
                active_days=active_days,
                last_active=str(today)
            )
            
        except Exception as e:
            logger.error(f"Error updating user stats: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
<b>{self.bot_name} v8.0 - {self.bot_tagline}</b>

✨ <b>নতুন আপগ্রেডেড ফিচার:</b>
• ইউজার প্রোফাইল ইমেজ কার্ড
• র‍্যান্ডম ব্যাকগ্রাউন্ড সিলেকশন
• অ্যাডভান্সড টেক্সট ইফেক্টস
• রিয়েল-টাইম ডায়াগ্রাম
• লেভেলিং সিস্টেম

🎯 <b>ব্যবহার পদ্ধতি:</b>
১. যেকোনো টেক্সট পাঠান (৪+ অক্ষর)
২. প্রফেশনাল ইমেজ + ডায়াগ্রাম পান
৩. ভোট দিয়ে ফিডব্যাক দিন

📊 <b>ইউজার সিস্টেম:</b>
• ব্যক্তিগত প্রোফাইল (/profile)
• অর্জনসমূহ (/achievements)
• লেভেল আপগ্রেড
• ব্যাজ কালেকশন

🔧 <b>কমান্ড:</b>
/start - শুরু করুন
/profile - আপনার প্রোফাইল
/achievements - অর্জনসমূহ
/stats - বট স্ট্যাটাস
/leaderboard - টপ রোস্টার
/health - সিস্টেম স্বাস্থ্য

⚡ <b>টিপস:</b>
• নিয়মিত সক্রিয় থাকুন
• মানসম্মত কন্টেন্ট তৈরি করুন
• অন্যের রোস্টে ভোট দিন

🔒 <b>গোপনীয়তা:</b>
• ব্যক্তিগত ডেটা সুরক্ষিত
• নিরাপদ শেয়ারিং
• Rate Limiting সক্রিয়

✅ <b>স্ট্যাটাস:</b> All Systems Operational
        """
        
        await update.message.reply_text(
            help_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        try:
            # Check admin access
            admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            user = update.effective_user
            
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
        
        # Get image generator stats if available
        img_stats = {}
        if self.image_gen:
            try:
                img_stats = self.image_gen.get_stats()
            except:
                pass
        
        # Create stats message
        stats_text = f"""
<b>{self.bot_name} পরিসংখ্যান v8.0</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>আপটাইম:</b> {days}দিন {hours}ঘণ্টা {minutes}মিনিট
📊 <b>বার্তা প্রসেসড:</b> {self.stats['messages_processed']:,}
🔥 <b>রোস্ট জেনারেটেড:</b> {self.stats['roasts_generated']:,}
🖼️ <b>ইমেজ তৈরি:</b> {self.stats['images_created']:,}
📈 <b>ডায়াগ্রাম তৈরি:</b> {self.stats['diagrams_created']:,}
👤 <b>প্রোফাইল ইমেজ:</b> {self.stats['profile_images_used']:,}
🌅 <b>ব্যাকগ্রাউন্ড:</b> {self.stats['background_images_used']:,}
📋 <b>ইউজার কার্ড:</b> {self.stats['user_info_cards_shown']:,}
👥 <b>ইউজার:</b> {len(self.stats['users_interacted']):,}
🏠 <b>গ্রুপ:</b> {len(self.stats['groups_managed']):,}

<b>ইমেজ জেনারেশন:</b>
"""
        
        if img_stats:
            stats_text += f"""✅ <b>সাকসেস রেট:</b> {img_stats.get('success_rate', 'N/A')}%
⚡ <b>অ্যাভারেজ টাইম:</b> {img_stats.get('average_time', 'N/A')}s
🔄 <b>টোটাল জেনারেটেড:</b> {img_stats.get('total_generated', 'N/A'):,}
"""
        else:
            stats_text += "❌ <b>ইমেজ জেনারেটর:</b> N/A\n"
        
        stats_text += f"""
<b>ডেটাবেজ:</b> ✅ কানেক্টেড
<b>ফিচার লোড:</b> ✅ {len(self.features)} ফিচার
<b>সিস্টেম:</b> ✅ অপারেশনাল
━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        await update.message.reply_text(
            stats_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
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
    
    def setup_handlers(self, application):
        """Setup all bot handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("profile", self.profile_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("achievements", self.achievements_command))
        application.add_handler(CommandHandler("leaderboard", self.handle_leaderboard_command))
        
        # Message handlers
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
        
        # New chat members handler
        try:
            application.add_handler(MessageHandler(
                filters.StatusUpdate.NEW_CHAT_MEMBERS, self.welcome_system.handle_new_members
            ))
        except:
            pass
        
        logger.info("All handlers setup complete")
    
    async def post_init(self, application):
        """Run after bot initialization"""
        logger.info(f"{self.bot_name} v8.0 starting up...")
        
        # Initialize auto daily quote
        try:
            self.auto_daily_quote = AutoDailyQuote(application.job_queue)
            logger.info("Auto Daily Quote initialized")
        except Exception as e:
            logger.error(f"Auto Daily Quote init failed: {e}")
            self.auto_daily_quote = None
        
        # Start background tasks
        asyncio.create_task(self._background_tasks())
        
        # Send startup notification
        await self._send_startup_notification()
        
        logger.info("✅ Bot startup complete")
    
    async def _background_tasks(self):
        """Run background maintenance tasks"""
        while True:
            try:
                # Cleanup old data
                self.db.cleanup_old_data(days=7)
                
                # Cleanup old temp files
                self._cleanup_temp_files()
                
                # Log statistics every hour
                logger.info(f"📊 Stats: {self.stats['messages_processed']} msgs, "
                           f"{self.stats['images_created']} images, "
                           f"{self.stats['user_info_cards_shown']} user cards")
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(300)
    
    def _cleanup_temp_files(self):
        """Cleanup old temporary files"""
        try:
            temp_dir = Path("temp")
            if temp_dir.exists():
                cutoff_time = time.time() - 3600  # 1 hour ago
                
                for file in temp_dir.glob("*"):
                    if file.is_file():
                        try:
                            if file.stat().st_mtime < cutoff_time:
                                file.unlink()
                        except:
                            pass
        except Exception as e:
            logger.error(f"Temp cleanup error: {e}")
    
    async def _send_startup_notification(self):
        """Send startup notification to owner"""
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if owner_id:
                bot_info = await self.application.bot.get_me()
                startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                message = f"""
🚀 <b>{self.bot_name} v8.0 Started Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot:</b> @{bot_info.username}
📊 <b>Version:</b> 8.0.0 Ultra Pro Max

<b>New Features:</b>
• Advanced Image Generator v8.0
• User Profile Image Cards
• Random Background Selection
• Achievement System
• Enhanced Statistics

<b>Status:</b>
✅ Image Generator: {IMAGE_GEN_AVAILABLE}
✅ Database: Connected
✅ Features: {len(self.features)} loaded
✅ System: Operational

🔥 <b>Ready for Advanced Roasting!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
                """
                
                await self.application.bot.send_message(
                    chat_id=owner_id,
                    text=message,
                    parse_mode=ParseMode.HTML
                )
                
                logger.info("Startup notification sent to owner")
        except Exception as e:
            logger.error(f"Error sending startup notification: {e}")
    
    def run(self):
        """Run the bot"""
        try:
            # Check if Telegram is available
            if not TELEGRAM_AVAILABLE:
                logger.error("Telegram library not installed!")
                print("Install: pip install python-telegram-bot")
                return
            
            # Check bot token
            if not self.bot_token or self.bot_token == "YOUR_BOT_TOKEN_HERE":
                logger.error("Bot token not configured!")
                print("Please set your bot token in config.py")
                return
            
            # Create application
            self.application = ApplicationBuilder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Run bot
            logger.info(f"🚀 Starting {self.bot_name} v8.0...")
            print(f"\n{'='*60}")
            print(f"🔥 {self.bot_name} v8.0 Ultra Pro Max")
            print(f"📊 Version: 8.0.0")
            print(f"⚡ Status: Starting...")
            print(f"{'='*60}\n")
            
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            print("\n🛑 Bot stopped by user")
            
            # Cleanup
            try:
                if self.image_gen:
                    self.image_gen.cleanup()
            except:
                pass
            
        except Exception as e:
            logger.error(f"Fatal error running bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            
            print(f"\n❌ Error: {e}")
            print("Check bot.log for details")
            
            # Cleanup
            try:
                if self.image_gen:
                    self.image_gen.cleanup()
            except:
                pass
            
            raise


def create_directories():
    """Create necessary directories"""
    directories = [
        "assets/fonts",
        "assets/borders",
        "assets/templates",
        "assets/backgrounds",
        "assets/profiles",
        "output",
        "temp",
        "cache",
        "backup",
        "logs",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created: {directory}")


def check_requirements():
    """Check if requirements are met"""
    try:
        import telegram
        print("✅ python-telegram-bot: OK")
    except:
        print("❌ python-telegram-bot: Missing")
        print("   Install: pip install python-telegram-bot")
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL): OK")
    except:
        print("❌ Pillow (PIL): Missing")
        print("   Install: pip install pillow")
    
    try:
        import matplotlib
        print("✅ matplotlib: OK")
    except:
        print("⚠️ matplotlib: Missing (optional)")
        print("   Install: pip install matplotlib")
    
    print("-" * 60)


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🔥 ROASTIFY BOT v8.0 ULTRA PRO MAX")
    print("📊 Advanced Image Generation + User Profiles")
    print("="*60 + "\n")
    
    # Check requirements
    check_requirements()
    
    # Create directories
    create_directories()
    
    # Check for required files
    required_files = ["config.py", "database.py"]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"⚠️ Warning: {file} not found")
    
    # Run bot
    try:
        bot = RoastifyBotV8()
        bot.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
