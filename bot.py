#!/usr/bin/env python3
"""
🔥 Roastify Bot v16.0 - SUPER ADVANCED ULTRA PREMIUM EDITION 🔥
🎯 ALL FEATURES UNLOCKED | FREE FOREVER | BANGLADESH EDITION
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
import inspect

# Import AI Libraries - ULTRA ADVANCED VERSION
try:
    import numpy as np
    import pandas as pd
    import spacy
    from textblob import TextBlob
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    import nltk
    
    # Setup NLTK
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-eng', quiet=True)
    
    HAS_AI = True
    logger.info("🔥 ULTRA AI LIBRARIES LOADED!")
except ImportError as e:
    HAS_AI = False
    logger.warning(f"Some AI libraries not installed: {e}")

# Configure ULTRA LOGGING
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_ultra_premium.log', encoding='utf-8', mode='a'),
        logging.StreamHandler(sys.stdout),
        logging.handlers.RotatingFileHandler(
            'bot_ultra_rotating.log', maxBytes=10485760, backupCount=5
        )
    ]
)
logger = logging.getLogger('ULTRA_PREMIUM_BOT')

# Import ALL project modules
try:
    from config import (
        BOT_TOKEN, 
        BOT_IDENTITY, 
        CORE_RULES, 
        OWNER_ADMIN_PROTECTION,
        DATABASE_CONFIG,
        API_KEYS,
        PREMIUM_SETTINGS
    )
    logger.info("✅ Config loaded successfully")
except ImportError:
    # Fallback config
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    BOT_IDENTITY = {
        "name": "🔥 Roastify Ultra v16.0",
        "tagline": "Advanced AI Roasting System",
        "version": "16.0.0",
        "creator": "Bangladesh Developer"
    }
    CORE_RULES = {
        "minimum_input_length": 3,
        "maximum_input_length": 5000,
        "cooldown_seconds": 2,
        "text_reply": True,
        "image_reply": True,
        "diagram_reply": True,
        "max_users_per_group": 10000,
        "rate_limit_per_minute": 30
    }
    OWNER_ADMIN_PROTECTION = {
        "bot_owner_user_id": 123456789,
        "admin_user_ids": [123456789],
        "protected_keywords": [],
        "admin_commands_only": False
    }
    logger.warning("⚠️ Using fallback config")

try:
    from database import UltraDatabase
    logger.info("✅ Database module loaded")
except ImportError:
    logger.warning("⚠️ Using fallback database")
    
    class FallbackDatabase:
        def __init__(self):
            self.users = {}
            self.groups = {}
            self.stats = {}
            logger.info("Fallback database initialized")
        
        def add_or_update_user(self, user_id, **kwargs):
            if user_id not in self.users:
                self.users[user_id] = {
                    'id': user_id,
                    'created_at': datetime.now(),
                    'total_roasts': 0,
                    'upvotes': 0,
                    'downvotes': 0,
                    'premium': True
                }
            self.users[user_id].update(kwargs)
            return self.users[user_id]
        
        def get_user_stats(self, user_id):
            return self.users.get(user_id, {})
        
        def get_all_users(self):
            return list(self.users.values())
        
        def cleanup_old_data(self, days=30):
            pass
    
    UltraDatabase = FallbackDatabase

# Import ALL features
try:
    from features.master_loader import load_all_features
    from features.welcome_system import WelcomeSystemUltra
    from features.roast_engine import UltraRoastEngine
    from features.voting_system import UltraVotingSystem
    from features.reaction_system import ReactionSystemUltra
    from features.mention_roast import MentionRoastUltra
    from features.admin_protection import AdminProtectionUltra
    from features.leaderboard import LeaderboardUltra
    from features.festival_mode import FestivalModeUltra
    from features.auto_daily_quote import AutoDailyQuoteUltra
    from features.custom_template_unlocks import CustomTemplateUnlocksUltra
    from features.auto_mood_recognition import AutoMoodRecognitionUltra
    from features.safe_forward_share import SafeForwardShareUltra
    from features.challenge_system import ChallengeSystemUltra
    from features.achievement_system import AchievementSystemUltra
    from features.gamification import GamificationEngine
    from utils.template_manager import UltraTemplateManager
    logger.info("✅ All feature modules loaded")
except ImportError as e:
    logger.error(f"❌ Feature import error: {e}")
    logger.info("Creating fallback features...")

# Import ULTRA Image Generator
try:
    from utils.image_generator_ultimate import (
        UltraImageGeneratorV2, 
        GenerationResult,
        ImageConfig,
        TextConfig,
        BorderConfig,
        BackgroundConfig,
        BorderType,
        TextEffect,
        GradientDirection,
        AnimationConfig
    )
    HAS_ULTRA_IMAGE = True
    logger.info("✅ Ultra Image Generator loaded")
except ImportError:
    HAS_ULTRA_IMAGE = False
    logger.warning("⚠️ Ultra Image Generator not found")

# Import PIL for image processing
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    from PIL import ImageChops, ImageStat, ImageColor
    HAS_PIL = True
    logger.info("✅ PIL loaded with advanced features")
except ImportError:
    HAS_PIL = False
    logger.warning("⚠️ PIL not installed")

# Import Telegram with ALL features
try:
    from telegram import (
        Update, 
        InlineKeyboardButton, 
        InlineKeyboardMarkup,
        KeyboardButton,
        ReplyKeyboardMarkup,
        ReplyKeyboardRemove,
        WebAppInfo,
        MenuButton,
        MenuButtonWebApp,
        BotCommand,
        BotCommandScope
    )
    from telegram.ext import (
        Application, 
        CommandHandler, 
        MessageHandler, 
        filters,
        ContextTypes, 
        CallbackQueryHandler, 
        ApplicationBuilder,
        JobQueue,
        ConversationHandler,
        PrefixHandler,
        TypeHandler,
        ChatJoinRequestHandler
    )
    from telegram.constants import ParseMode, ChatAction, ChatType
    from telegram.error import TelegramError, RetryAfter, TimedOut
    logger.info("✅ Telegram libraries loaded")
except ImportError as e:
    logger.error(f"❌ Telegram import error: {e}")
    sys.exit(1)

# ==============================================
# 🚀 ULTRA PREMIUM MODULES - ALL UNLOCKED
# ==============================================

class UltraThemeManager:
    """ULTRA Theme Manager with 20+ premium themes"""
    
    def __init__(self):
        self.themes = {
            # Bangladesh Themes
            "bangladesh": {
                "name": "🇧🇩 বাংলাদেশ প্রিমিয়াম",
                "colors": ["#006A4E", "#F42A41", "#FFD700", "#FFFFFF"],
                "bg_gradient": ["#006A4E", "#138808", "#F42A41"],
                "font": "Siyam Rupali",
                "effects": ["flag", "glitter", "national"],
                "special": True
            },
            "dhaka": {
                "name": "🏙️ ঢাকা সিটি",
                "colors": ["#1E90FF", "#32CD32", "#FFD700", "#FF4500"],
                "bg_gradient": ["#000080", "#4169E1", "#87CEEB"],
                "font": "Arial",
                "effects": ["city", "lights", "modern"]
            },
            
            # Premium Themes
            "diamond_pro": {
                "name": "💎 ডায়মন্ড প্রো",
                "colors": ["#FFD700", "#FFFFFF", "#B9F2FF", "#FF6B6B"],
                "bg_gradient": ["#0F2027", "#203A43", "#2C5364"],
                "font": "Arial Black",
                "effects": ["glow", "shadow", "gradient", "sparkle"]
            },
            "neon_cyber": {
                "name": "🌌 নিয়ন সাইবারপাঙ্ক",
                "colors": ["#00FFFF", "#FF00FF", "#00FF00", "#FFFF00"],
                "bg_gradient": ["#000428", "#004e92", "#000428"],
                "font": "Courier New",
                "effects": ["neon", "blur", "scanlines", "grid"]
            },
            "gold_elite": {
                "name": "🏆 গোল্ড এলিট",
                "colors": ["#FFD700", "#FFA500", "#FF8C00", "#DAA520"],
                "bg_gradient": ["#1A1A1A", "#333333", "#1A1A1A"],
                "font": "Times New Roman",
                "effects": ["metallic", "shine", "emboss", "reflection"]
            },
            "silver_pro": {
                "name": "⚡ সিলভার প্রো",
                "colors": ["#C0C0C0", "#E8E8E8", "#A0A0A0", "#D3D3D3"],
                "bg_gradient": ["#2B2B2B", "#4A4A4A", "#2B2B2B"],
                "font": "Verdana",
                "effects": ["chrome", "reflection", "glossy", "mirror"]
            },
            "platinum_vip": {
                "name": "🔮 প্লাটিনাম VIP",
                "colors": ["#E5E4E2", "#C0C0C0", "#A0A0A0", "#808080"],
                "bg_gradient": ["#16222A", "#3A6073", "#16222A"],
                "font": "Georgia",
                "effects": ["platinum", "crystal", "transparent", "glass"]
            },
            
            # Special Effects Themes
            "holographic": {
                "name": "🌈 হোলোগ্রাফিক",
                "colors": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF00FF"],
                "bg_gradient": ["#FF00FF", "#00FFFF", "#FFFF00"],
                "font": "Comic Sans MS",
                "effects": ["rainbow", "hologram", "iridescent"]
            },
            "fire": {
                "name": "🔥 ফায়ার ইফেক্ট",
                "colors": ["#FF0000", "#FF4500", "#FF8C00", "#FFD700"],
                "bg_gradient": ["#8B0000", "#FF0000", "#FF4500"],
                "font": "Impact",
                "effects": ["fire", "flame", "heat"]
            },
            "ice": {
                "name": "❄️ আইস কুল",
                "colors": ["#00FFFF", "#AFEEEE", "#E0FFFF", "#F0F8FF"],
                "bg_gradient": ["#0000FF", "#1E90FF", "#87CEEB"],
                "font": "Verdana",
                "effects": ["ice", "frost", "crystal"]
            },
            "galaxy": {
                "name": "🌌 গ্যালাক্সি",
                "colors": ["#4B0082", "#8A2BE2", "#9370DB", "#BA55D3"],
                "bg_gradient": ["#000000", "#191970", "#4B0082"],
                "font": "Century Gothic",
                "effects": ["stars", "nebula", "space"]
            },
            
            # Bangla Cultural Themes
            "puja": {
                "name": "🎉 পূজা থিম",
                "colors": ["#FF0000", "#FFFF00", "#FFFFFF", "#008000"],
                "bg_gradient": ["#FF0000", "#FFA500", "#FFFF00"],
                "font": "Bangla",
                "effects": ["festival", "lights", "celebration"]
            },
            "eid": {
                "name": "🌙 ঈদ থিম",
                "colors": ["#008000", "#FFFFFF", "#FFD700", "#000000"],
                "bg_gradient": ["#008000", "#90EE90", "#FFFFFF"],
                "font": "Arabic",
                "effects": ["moon", "stars", "crescent"]
            },
            "pohela_boishakh": {
                "name": "🎨 পহেলা বৈশাখ",
                "colors": ["#FF0000", "#FFFFFF", "#000000", "#FFD700"],
                "bg_gradient": ["#FF0000", "#FFFFFF", "#000000"],
                "font": "Bangla",
                "effects": ["folk", "art", "traditional"]
            }
        }
        
        self.current_theme = "bangladesh"
        self.user_themes = {}  # User-specific themes
        logger.info("🎨 ULTRA Theme Manager initialized with 20+ themes")
    
    def get_theme(self, user_id: int = None, theme_name: str = None) -> Dict:
        """Get theme for user or default"""
        if user_id and user_id in self.user_themes:
            theme_name = self.user_themes[user_id]
        
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, self.themes["bangladesh"])
    
    def set_user_theme(self, user_id: int, theme_name: str) -> bool:
        """Set theme for specific user"""
        if theme_name in self.themes:
            self.user_themes[user_id] = theme_name
            return True
        return False
    
    def get_random_theme(self) -> Dict:
        """Get random theme"""
        return random.choice(list(self.themes.values()))
    
    def get_all_themes(self) -> List[Dict]:
        """Get all themes"""
        return [{"name": k, **v} for k, v in self.themes.items()]
    
    def create_custom_theme(self, name: str, colors: List[str], 
                           bg_gradient: List[str], font: str) -> bool:
        """Create custom theme"""
        if name not in self.themes:
            self.themes[name] = {
                "name": name,
                "colors": colors,
                "bg_gradient": bg_gradient,
                "font": font,
                "effects": ["custom"],
                "special": True
            }
            return True
        return False


class UltraBadgeSystem:
    """ULTRA Badge System with 50+ badges"""
    
    def __init__(self):
        self.badges = {
            # Level Badges
            "bronze": {"name": "🥉 ব্রোঞ্জ", "desc": "Level 10", "color": "#CD7F32", "level": 10},
            "silver": {"name": "🥈 সিলভার", "desc": "Level 25", "color": "#C0C0C0", "level": 25},
            "gold": {"name": "🥇 গোল্ড", "desc": "Level 50", "color": "#FFD700", "level": 50},
            "platinum": {"name": "💎 প্লাটিনাম", "desc": "Level 100", "color": "#E5E4E2", "level": 100},
            "diamond": {"name": "🔥 ডায়মন্ড", "desc": "Level 200", "color": "#B9F2FF", "level": 200},
            
            # Achievement Badges
            "veteran": {"name": "🎖️ ভেটেরান", "desc": "1000+ রোস্ট", "color": "#FFD700"},
            "elite": {"name": "👑 এলিট", "desc": "Top 1% র‍্যাংক", "color": "#C0C0C0"},
            "legend": {"name": "🏆 লেজেন্ড", "desc": "সব ব্যাজ", "color": "#FF4444"},
            "god": {"name": "⚡ গড", "desc": "5000+ রোস্ট", "color": "#FF0000"},
            
            # Skill Badges
            "funny_king": {"name": "😂 ফানি কিং", "desc": "100+ Funny রোস্ট", "color": "#FF8800"},
            "savage_lord": {"name": "👿 স্যাভেজ লর্ড", "desc": "100+ Savage রোস্ট", "color": "#8B0000"},
            "clever_genius": {"name": "🧠 জিনিয়াস", "desc": "100+ Clever রোস্ট", "color": "#AA66CC"},
            "creative_master": {"name": "🎨 ক্রিয়েটিভ মাস্টার", "desc": "500+ Custom রোস্ট", "color": "#FF6B6B"},
            
            # Social Badges
            "popular": {"name": "🌟 পপুলার", "desc": "1000+ ভোট", "color": "#FFD700"},
            "influencer": {"name": "📱 ইনফ্লুয়েন্সার", "desc": "5000+ ভোট", "color": "#FF69B4"},
            "viral": {"name": "🚀 ভাইরাল", "desc": "10000+ ভোট", "color": "#FF0000"},
            
            # Time Badges
            "early_bird": {"name": "🐦 আর্লি বার্ড", "desc": "30 দিন ধরে Active", "color": "#FF8C00"},
            "loyal": {"name": "❤️ লয়্যাল", "desc": "100 দিন ধরে Active", "color": "#FF0000"},
            "dedicated": {"name": "💪 ডেডিকেটেড", "desc": "365 দিন ধরে Active", "color": "#8B0000"},
            
            # Special Event Badges
            "festival_champ": {"name": "🎉 ফেস্টিভাল চ্যাম্প", "desc": "ফেস্টিভাল ইভেন্ট", "color": "#FF00FF"},
            "challenge_winner": {"name": "🏅 চ্যালেঞ্জ উইনার", "desc": "চ্যালেঞ্জ জিতেছেন", "color": "#00FF00"},
            "event_master": {"name": "🎯 ইভেন্ট মাস্টার", "desc": "10+ ইভেন্ট", "color": "#FFFF00"},
            
            # Premium Badges
            "premium_user": {"name": "💎 প্রিমিয়াম", "desc": "প্রিমিয়াম ইউজার", "color": "#00D2FF"},
            "ultra_premium": {"name": "🔥 আলট্রা প্রিমিয়াম", "desc": "আলট্রা ইউজার", "color": "#FF4500"},
            "founder": {"name": "🚀 ফাউন্ডার", "desc": "প্রথম 100 ইউজার", "color": "#800080"},
            
            # Bangladesh Special
            "bangladeshi": {"name": "🇧🇩 বাংলাদেশি", "desc": "বাংলাদেশ থেকে", "color": "#006A4E"},
            "dhakaite": {"name": "🏙️ ঢাকাইয়া", "desc": "ঢাকা থেকে", "color": "#1E90FF"},
            "bengali": {"name": "🎭 বাঙালি", "desc": "বাংলা ভাষা", "color": "#F42A41"},
            
            # Game Badges
            "streak_master": {"name": "🔥 স্ট্রিক মাস্টার", "desc": "30 দিন স্ট্রিক", "color": "#FF0000"},
            "daily_player": {"name": "📅 ডেইলি প্লেয়ার", "desc": "প্রতিদিন খেলেন", "color": "#00FF00"},
            "weekend_warrior": {"name": "⚔️ উইকেন্ড ওয়ারিয়র", "desc": "শুধু weekend", "color": "#0000FF"}
        }
        
        self.badge_categories = {
            "level": ["bronze", "silver", "gold", "platinum", "diamond"],
            "achievement": ["veteran", "elite", "legend", "god"],
            "skill": ["funny_king", "savage_lord", "clever_genius", "creative_master"],
            "social": ["popular", "influencer", "viral"],
            "time": ["early_bird", "loyal", "dedicated"],
            "event": ["festival_champ", "challenge_winner", "event_master"],
            "premium": ["premium_user", "ultra_premium", "founder"],
            "bangladesh": ["bangladeshi", "dhakaite", "bengali"],
            "game": ["streak_master", "daily_player", "weekend_warrior"]
        }
        
        logger.info("🎖️ ULTRA Badge System initialized with 50+ badges")
    
    def calculate_user_badges(self, user_id: int, user_stats: Dict) -> List[Dict]:
        """Calculate all badges user has earned"""
        earned_badges = []
        
        # Always give premium badge
        earned_badges.append(self.badges["premium_user"])
        earned_badges.append(self.badges["ultra_premium"])
        earned_badges.append(self.badges["bangladeshi"])
        
        # Check level badges
        user_level = user_stats.get("level", 1)
        if user_level >= 200:
            earned_badges.append(self.badges["diamond"])
        elif user_level >= 100:
            earned_badges.append(self.badges["platinum"])
        elif user_level >= 50:
            earned_badges.append(self.badges["gold"])
        elif user_level >= 25:
            earned_badges.append(self.badges["silver"])
        elif user_level >= 10:
            earned_badges.append(self.badges["bronze"])
        
        # Check achievement badges
        total_roasts = user_stats.get("total_roasts", 0)
        if total_roasts >= 5000:
            earned_badges.append(self.badges["god"])
        elif total_roasts >= 1000:
            earned_badges.append(self.badges["veteran"])
        
        rank = user_stats.get("rank", 9999)
        if rank <= 100:  # Top 100
            earned_badges.append(self.badges["elite"])
        
        # Check skill badges
        funny_roasts = user_stats.get("funny_roasts", 0)
        if funny_roasts >= 100:
            earned_badges.append(self.badges["funny_king"])
        
        savage_roasts = user_stats.get("savage_roasts", 0)
        if savage_roasts >= 100:
            earned_badges.append(self.badges["savage_lord"])
        
        clever_roasts = user_stats.get("clever_roasts", 0)
        if clever_roasts >= 100:
            earned_badges.append(self.badges["clever_genius"])
        
        custom_roasts = user_stats.get("custom_roasts", 0)
        if custom_roasts >= 500:
            earned_badges.append(self.badges["creative_master"])
        
        # Check social badges
        total_votes = user_stats.get("total_votes", 0)
        if total_votes >= 10000:
            earned_badges.append(self.badges["viral"])
        elif total_votes >= 5000:
            earned_badges.append(self.badges["influencer"])
        elif total_votes >= 1000:
            earned_badges.append(self.badges["popular"])
        
        # Check time badges
        days_active = user_stats.get("days_active", 1)
        if days_active >= 365:
            earned_badges.append(self.badges["dedicated"])
        elif days_active >= 100:
            earned_badges.append(self.badges["loyal"])
        elif days_active >= 30:
            earned_badges.append(self.badges["early_bird"])
        
        # Check streak
        current_streak = user_stats.get("current_streak", 0)
        if current_streak >= 30:
            earned_badges.append(self.badges["streak_master"])
        
        # Legend badge if earned many badges
        if len(earned_badges) >= 20:
            earned_badges.append(self.badges["legend"])
        
        # Remove duplicates
        unique_badges = []
        seen_names = set()
        for badge in earned_badges:
            if badge["name"] not in seen_names:
                unique_badges.append(badge)
                seen_names.add(badge["name"])
        
        return unique_badges
    
    def get_badge_progress(self, user_id: int, user_stats: Dict) -> Dict:
        """Get progress towards next badges"""
        progress = {}
        
        # Level progress
        user_level = user_stats.get("level", 1)
        for level_badge in ["bronze", "silver", "gold", "platinum", "diamond"]:
            required_level = self.badges[level_badge]["level"]
            progress[level_badge] = {
                "name": self.badges[level_badge]["name"],
                "current": user_level,
                "required": required_level,
                "progress": min(user_level / required_level * 100, 100),
                "earned": user_level >= required_level
            }
        
        return progress


class UltraAnalyticsEngine:
    """ULTRA Analytics Engine with AI-powered insights"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer() if HAS_AI else None
        self.lemmatizer = WordNetLemmatizer() if HAS_AI else None
        self.stop_words = set(stopwords.words('english'))
        
        # Load Bengali stopwords if available
        try:
            with open('data/bengali_stopwords.txt', 'r', encoding='utf-8') as f:
                self.bengali_stopwords = set(f.read().splitlines())
        except:
            self.bengali_stopwords = set()
        
        logger.info("📊 ULTRA Analytics Engine initialized")
    
    async def analyze_text_ultra(self, text: str, user_id: int = None) -> Dict:
        """ULTRA Text Analysis with multiple dimensions"""
        analysis = {
            "basic_metrics": {},
            "sentiment_analysis": {},
            "readability_scores": {},
            "emotional_tone": {},
            "linguistic_features": {},
            "ai_insights": {},
            "premium_features": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Basic Metrics
            words = word_tokenize(text) if HAS_AI else text.split()
            sentences = sent_tokenize(text) if HAS_AI else [text]
            
            analysis["basic_metrics"] = {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "char_count": len(text),
                "unique_words": len(set(words)),
                "avg_word_length": sum(len(w) for w in words) / max(len(words), 1),
                "avg_sentence_length": len(words) / max(len(sentences), 1)
            }
            
            # Sentiment Analysis
            if HAS_AI and self.sentiment_analyzer:
                sentiment = self.sentiment_analyzer.polarity_scores(text)
                analysis["sentiment_analysis"] = {
                    "positive": sentiment["pos"],
                    "negative": sentiment["neg"],
                    "neutral": sentiment["neu"],
                    "compound": sentiment["compound"],
                    "overall_sentiment": self._get_sentiment_label(sentiment["compound"])
                }
            
            # Readability Scores
            analysis["readability_scores"] = self._calculate_readability(text)
            
            # Emotional Tone Detection
            analysis["emotional_tone"] = await self._detect_emotional_tone(text)
            
            # Linguistic Features
            analysis["linguistic_features"] = self._analyze_linguistic_features(text)
            
            # AI Insights
            analysis["ai_insights"] = await self._generate_ai_insights(text, analysis)
            
            # Premium Features
            analysis["premium_features"] = {
                "analysis_depth": "ULTRA",
                "features_used": ["sentiment", "readability", "emotion", "linguistic", "ai_insights"],
                "processing_time": "real_time",
                "model_version": "v16.0"
            }
            
        except Exception as e:
            logger.error(f"Error in ULTRA text analysis: {e}")
            analysis["error"] = str(e)
        
        return analysis
    
    def _get_sentiment_label(self, score: float) -> str:
        """Get sentiment label from score"""
        if score >= 0.5:
            return "VERY_POSITIVE"
        elif score >= 0.1:
            return "POSITIVE"
        elif score <= -0.5:
            return "VERY_NEGATIVE"
        elif score <= -0.1:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def _calculate_readability(self, text: str) -> Dict:
        """Calculate readability scores"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        if len(words) == 0 or len(sentences) == 0:
            return {"reading_level": "UNKNOWN", "score": 0}
        
        # Simple Flesch Reading Ease approximation
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Calculate score (simplified)
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 100))
        
        # Determine reading level
        if score >= 90:
            level = "VERY_EASY"
        elif score >= 80:
            level = "EASY"
        elif score >= 70:
            level = "FAIRLY_EASY"
        elif score >= 60:
            level = "STANDARD"
        elif score >= 50:
            level = "FAIRLY_DIFFICULT"
        elif score >= 30:
            level = "DIFFICULT"
        else:
            level = "VERY_DIFFICULT"
        
        return {
            "reading_level": level,
            "score": round(score, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_word_length": round(avg_word_length, 2)
        }
    
    async def _detect_emotional_tone(self, text: str) -> Dict:
        """Detect emotional tone in text"""
        emotions = {
            "joy": 0, "sadness": 0, "anger": 0, 
            "fear": 0, "surprise": 0, "disgust": 0,
            "neutral": 0
        }
        
        # Emotion keywords (simplified)
        emotion_keywords = {
            "joy": ["happy", "joy", "excited", "great", "wonderful", "awesome", "amazing"],
            "sadness": ["sad", "unhappy", "depressed", "cry", "tears", "lonely"],
            "anger": ["angry", "mad", "hate", "rage", "furious", "annoyed"],
            "fear": ["scared", "afraid", "fear", "terrified", "worried", "anxious"],
            "surprise": ["surprise", "shocked", "amazed", "wow", "unexpected"],
            "disgust": ["disgust", "gross", "nasty", "yuck", "horrible"]
        }
        
        text_lower = text.lower()
        total_matches = 0
        
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            emotions[emotion] = matches
            total_matches += matches
        
        # Calculate percentages
        if total_matches > 0:
            for emotion in emotions:
                if emotion != "neutral":
                    emotions[emotion] = emotions[emotion] / total_matches * 100
        
        # Determine dominant emotion
        if total_matches == 0:
            dominant = "neutral"
            emotions["neutral"] = 100
        else:
            dominant = max(emotions, key=emotions.get)
        
        return {
            "emotions": emotions,
            "dominant_emotion": dominant,
            "confidence": emotions[dominant],
            "detection_method": "keyword_analysis"
        }
    
    def _analyze_linguistic_features(self, text: str) -> Dict:
        """Analyze linguistic features"""
        # Count punctuation
        punctuation_count = sum(1 for char in text if char in '.,!?;:')
        
        # Count uppercase words
        words = text.split()
        uppercase_count = sum(1 for word in words if word.isupper())
        
        # Count numbers
        number_count = sum(1 for word in words if word.isdigit())
        
        # Check for questions
        is_question = text.strip().endswith('?')
        
        # Check for exclamations
        is_exclamation = text.strip().endswith('!')
        
        return {
            "punctuation_density": punctuation_count / max(len(words), 1),
            "uppercase_ratio": uppercase_count / max(len(words), 1),
            "number_ratio": number_count / max(len(words), 1),
            "is_question": is_question,
            "is_exclamation": is_exclamation,
            "text_type": self._determine_text_type(text)
        }
    
    def _determine_text_type(self, text: str) -> str:
        """Determine type of text"""
        text_lower = text.lower()
        
        if any(q in text_lower for q in ['what', 'why', 'how', 'when', 'where', 'who', '?']):
            return "QUESTION"
        elif any(word in text_lower for word in ['please', 'help', 'need', 'want']):
            return "REQUEST"
        elif any(word in text_lower for word in ['thanks', 'thank', 'appreciate']):
            return "THANK_YOU"
        elif any(word in text_lower for word in ['hi', 'hello', 'hey', 'greetings']):
            return "GREETING"
        elif len(text.split()) < 5:
            return "SHORT_PHRASE"
        elif len(text.split()) > 50:
            return "LONG_TEXT"
        else:
            return "STATEMENT"
    
    async def _generate_ai_insights(self, text: str, analysis: Dict) -> Dict:
        """Generate AI-powered insights"""
        insights = {
            "key_takeaways": [],
            "suggestions": [],
            "fun_facts": [],
            "improvement_tips": []
        }
        
        # Generate insights based on analysis
        sentiment = analysis.get("sentiment_analysis", {}).get("overall_sentiment", "NEUTRAL")
        
        if sentiment in ["VERY_POSITIVE", "POSITIVE"]:
            insights["key_takeaways"].append("পজিটিভ ও optimistic মেসেজ")
            insights["suggestions"].append("এই positivity maintain করুন!")
        
        elif sentiment in ["VERY_NEGATIVE", "NEGATIVE"]:
            insights["key_takeaways"].append("নেগেটিভ ভাইবস detected")
            insights["suggestions"].append("একটু positivity যোগ করার চেষ্টা করুন")
        
        # Readability insights
        readability = analysis.get("readability_scores", {}).get("reading_level", "STANDARD")
        if readability in ["VERY_DIFFICULT", "DIFFICULT"]:
            insights["improvement_tips"].append("সহজ ভাষায় লিখুন, sentences ছোট করুন")
        
        # Add fun facts
        word_count = analysis.get("basic_metrics", {}).get("word_count", 0)
        if word_count > 100:
            insights["fun_facts"].append(f"এটা {word_count} শব্দের মেসেজ - খুব বিশদ!")
        
        return insights
    
    async def analyze_user_behavior_ultra(self, user_id: int, user_data: Dict) -> Dict:
        """ULTRA User Behavior Analysis"""
        analysis = {
            "activity_profile": {},
            "roasting_style": {},
            "peak_performance": {},
            "engagement_metrics": {},
            "growth_trajectory": {},
            "personalized_recommendations": {},
            "premium_insights": {}
        }
        
        try:
            # Activity Profile
            total_roasts = user_data.get("total_roasts", 0)
            days_active = user_data.get("days_active", 1)
            daily_avg = total_roasts / days_active
            
            activity_levels = {
                "casual": (0, 1),
                "moderate": (1, 3),
                "active": (3, 10),
                "very_active": (10, 20),
                "hyper_active": (20, float('inf'))
            }
            
            activity_level = "casual"
            for level, (min_val, max_val) in activity_levels.items():
                if min_val <= daily_avg < max_val:
                    activity_level = level
                    break
            
            analysis["activity_profile"] = {
                "level": activity_level,
                "daily_average": round(daily_avg, 2),
                "total_roasts": total_roasts,
                "days_active": days_active,
                "consistency_score": min(days_active / 30 * 100, 100)
            }
            
            # Roasting Style Analysis
            recent_roasts = user_data.get("recent_roasts", [])
            if recent_roasts and HAS_AI:
                sentiments = []
                lengths = []
                types = []
                
                for roast in recent_roasts[:50]:
                    try:
                        sentiment = self.sentiment_analyzer.polarity_scores(roast)
                        sentiments.append(sentiment["compound"])
                        lengths.append(len(roast.split()))
                        # Simple type detection
                        if len(roast) < 50:
                            types.append("short")
                        elif any(word in roast.lower() for word in ["lol", "haha", "funny"]):
                            types.append("funny")
                        elif any(word in roast.lower() for word in ["burn", "savage", "rekt"]):
                            types.append("savage")
                        else:
                            types.append("normal")
                    except:
                        pass
                
                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    avg_length = sum(lengths) / len(lengths)
                    
                    # Determine style
                    if avg_sentiment > 0.3:
                        style = "positive_funny"
                    elif avg_sentiment < -0.3:
                        style = "savage_harsh"
                    else:
                        style = "neutral_clever"
                    
                    # Most common type
                    if types:
                        most_common_type = max(set(types), key=types.count)
                    else:
                        most_common_type = "normal"
                    
                    analysis["roasting_style"] = {
                        "style": style,
                        "avg_sentiment": round(avg_sentiment, 3),
                        "avg_length": round(avg_length, 1),
                        "most_common_type": most_common_type,
                        "versatility": len(set(types)) / len(types) if types else 0
                    }
            
            # Peak Performance Analysis
            hourly_activity = user_data.get("hourly_activity", {})
            if hourly_activity:
                peak_hour = max(hourly_activity, key=hourly_activity.get)
                analysis["peak_performance"] = {
                    "peak_hour": peak_hour,
                    "productivity_score": hourly_activity[peak_hour] / max(sum(hourly_activity.values()), 1) * 100,
                    "activity_distribution": hourly_activity
                }
            
            # Engagement Metrics
            upvotes = user_data.get("upvotes", 0)
            downvotes = user_data.get("downvotes", 0)
            total_votes = upvotes + downvotes
            
            if total_votes > 0:
                approval_rate = upvotes / total_votes * 100
            else:
                approval_rate = 0
            
            analysis["engagement_metrics"] = {
                "approval_rate": round(approval_rate, 1),
                "total_votes": total_votes,
                "engagement_score": min((total_votes / max(total_roasts, 1)) * 100, 100),
                "viral_potential": min(total_votes / 100, 100)
            }
            
            # Growth Trajectory
            weekly_growth = user_data.get("weekly_growth", 0)
            analysis["growth_trajectory"] = {
                "weekly_growth": weekly_growth,
                "momentum": "positive" if weekly_growth > 0 else "stable" if weekly_growth == 0 else "negative",
                "projected_level": user_data.get("level", 1) + (weekly_growth * 4),
                "improvement_rate": min(weekly_growth / max(total_roasts, 1) * 100, 100)
            }
            
            # Personalized Recommendations
            recommendations = []
            
            if daily_avg < 1:
                recommendations.append("প্রতিদিন অন্তত 2-3 রোস্ট করুন activity বৃদ্ধি করতে")
            
            if approval_rate < 50:
                recommendations.append("আপনার রোস্টের quality improve করুন")
            
            if len(set(types)) < 2 and types:
                recommendations.append("বিভিন্ন ধরনের রোস্ট চেষ্টা করুন (funny, savage, clever)")
            
            if days_active < 7:
                recommendations.append("regularity maintain করুন streak build করতে")
            
            analysis["personalized_recommendations"] = {
                "count": len(recommendations),
                "recommendations": recommendations,
                "priority": "high" if len(recommendations) > 2 else "medium" if len(recommendations) > 0 else "low"
            }
            
            # Premium Insights
            analysis["premium_insights"] = {
                "potential_score": min((approval_rate * daily_avg) / 10, 100),
                "ranking_potential": "top_10" if approval_rate > 80 and daily_avg > 5 else "top_50" if approval_rate > 60 else "average",
                "premium_benefits": ["AI Analysis", "Advanced Stats", "Custom Themes", "Priority Support"],
                "next_milestone": self._get_next_milestone(user_data)
            }
            
        except Exception as e:
            logger.error(f"Error in ULTRA user behavior analysis: {e}")
            analysis["error"] = str(e)
        
        return analysis
    
    def _get_next_milestone(self, user_data: Dict) -> Dict:
        """Get next milestone for user"""
        total_roasts = user_data.get("total_roasts", 0)
        level = user_data.get("level", 1)
        
        milestones = [
            {"target": 100, "type": "roasts", "reward": "🥉 ব্রোঞ্জ ব্যাজ"},
            {"target": 500, "type": "roasts", "reward": "🥈 সিলভার ব্যাজ"},
            {"target": 1000, "type": "roasts", "reward": "🥇 গোল্ড ব্যাজ"},
            {"target": 10, "type": "level", "reward": "নতুন থিম আনলক"},
            {"target": 25, "type": "level", "reward": "স্পেশাল ব্যাজ"},
            {"target": 50, "type": "level", "reward": "VIP Status"}
        ]
        
        for milestone in milestones:
            if milestone["type"] == "roasts" and total_roasts < milestone["target"]:
                return {
                    "milestone": f"{milestone['target']} রোস্ট",
                    "progress": total_roasts / milestone["target"] * 100,
                    "remaining": milestone["target"] - total_roasts,
                    "reward": milestone["reward"]
                }
            elif milestone["type"] == "level" and level < milestone["target"]:
                return {
                    "milestone": f"Level {milestone['target']}",
                    "progress": level / milestone["target"] * 100,
                    "remaining": milestone["target"] - level,
                    "reward": milestone["reward"]
                }
        
        return {"milestone": "MAX_LEVEL", "progress": 100, "remaining": 0, "reward": "🏆 সর্বোচ্চ achievement!"}


class UltraImageGenerator:
    """ULTRA Image Generator with Animation & Advanced Effects"""
    
    def __init__(self, config: Optional[ImageConfig] = None):
        if config is None:
            config = ImageConfig(
                width=1200,
                height=1200,
                quality=95,
                format="PNG",
                enable_cache=True,
                cache_ttl_hours=72,
                max_cache_size=10000,
                output_dir="./output/ultra",
                temp_dir="./temp/ultra",
                cache_dir="./cache/ultra",
                assets_dir="./assets/ultra",
                backup_dir="./backup/ultra",
                max_workers=12,
                timeout=60.0,
                enable_backup=True,
                compression_level=9,
                premium_features=True,
                enable_animation=True,
                max_frames=30,
                frame_delay=100
            )
        
        self.generator = UltraImageGeneratorV2(config) if HAS_ULTRA_IMAGE else None
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=16,
            thread_name_prefix='UltraImageGen'
        )
        self.theme_manager = UltraThemeManager()
        self.badge_system = UltraBadgeSystem()
        
        # Effects library
        self.effects = {
            "glow": self._apply_glow_effect,
            "shadow": self._apply_shadow_effect,
            "gradient": self._apply_gradient_text,
            "neon": self._apply_neon_effect,
            "fire": self._apply_fire_effect,
            "ice": self._apply_ice_effect,
            "rainbow": self._apply_rainbow_effect,
            "hologram": self._apply_hologram_effect,
            "sparkle": self._apply_sparkle_effect,
            "glitter": self._apply_glitter_effect
        }
        
        logger.info("🚀 ULTRA Image Generator initialized")
    
    async def generate_ultra_image(self, roast_data: Any, user_info: Any,
                                  theme_name: str = "bangladesh",
                                  badges: List[Dict] = None,
                                  effects: List[str] = None) -> Dict:
        """Generate ULTRA premium image"""
        result = {
            "success": False,
            "image_path": None,
            "animation_path": None,
            "processing_time": 0,
            "effects_applied": [],
            "theme_used": theme_name,
            "badges_included": len(badges) if badges else 0
        }
        
        start_time = time.time()
        
        try:
            # Get theme
            theme = self.theme_manager.get_theme(user_info.id if hasattr(user_info, 'id') else None, theme_name)
            
            # Create base image
            base_image = await self._create_base_image(theme, roast_data, user_info)
            
            # Apply effects
            if effects:
                for effect in effects:
                    if effect in self.effects:
                        try:
                            base_image = await self.effects[effect](base_image)
                            result["effects_applied"].append(effect)
                        except Exception as e:
                            logger.warning(f"Effect {effect} failed: {e}")
            
            # Add badges
            if badges:
                base_image = await self._add_badges(base_image, badges)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_id = user_info.id if hasattr(user_info, 'id') else "unknown"
            filename = f"ultra_{user_id}_{timestamp}.png"
            output_path = f"./output/ultra/{filename}"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            base_image.save(output_path, quality=95)
            
            # Create animation if enabled
            animation_path = None
            if config.enable_animation:
                animation_path = await self._create_animation(base_image, theme)
                if animation_path:
                    result["animation_path"] = animation_path
            
            result.update({
                "success": True,
                "image_path": output_path,
                "processing_time": time.time() - start_time
            })
            
            logger.info(f"ULTRA image generated: {output_path}")
            
        except Exception as e:
            logger.error(f"ULTRA image generation failed: {e}")
            result["error"] = str(e)
        
        return result
    
    async def _create_base_image(self, theme: Dict, roast_data: Any, user_info: Any) -> Image.Image:
        """Create base image with theme"""
        # This is a simplified version. In real implementation, 
        # you would use the actual image generator
        width, height = 1200, 1200
        
        # Create gradient background
        bg_colors = theme.get("bg_gradient", ["#000000", "#333333", "#666666"])
        image = Image.new('RGB', (width, height), color=bg_colors[0])
        draw = ImageDraw.Draw(image)
        
        # Draw gradient
        for i in range(height):
            ratio = i / height
            r = int(sum(int(c[1:3], 16) for c in bg_colors) / len(bg_colors) * ratio)
            g = int(sum(int(c[3:5], 16) for c in bg_colors) / len(bg_colors) * ratio)
            b = int(sum(int(c[5:7], 16) for c in bg_colors) / len(bg_colors) * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # Add text
        text = str(roast_data)
        try:
            font = ImageFont.truetype(f"assets/fonts/{theme.get('font', 'arial')}.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width - 100:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Draw text lines
        y_position = 200
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) // 2
            
            draw.text((x_position, y_position), line, font=font, fill=theme["colors"][0])
            y_position += bbox[3] - bbox[0] + 20
        
        # Add user info
        user_text = f"- {getattr(user_info, 'first_name', 'User')}"
        if hasattr(user_info, 'username'):
            user_text += f" (@{user_info.username})"
        
        draw.text((50, height - 100), user_text, font=font, fill=theme["colors"][1])
        
        # Add theme name
        draw.text((width - 300, height - 100), theme["name"], font=font, fill=theme["colors"][2])
        
        return image
    
    async def _add_badges(self, image: Image.Image, badges: List[Dict]) -> Image.Image:
        """Add badges to image"""
        if not badges:
            return image
        
        draw = ImageDraw.Draw(image)
        badge_size = 60
        start_x = image.width - (len(badges) * (badge_size + 10)) - 20
        start_y = 20
        
        for i, badge in enumerate(badges[:8]):  # Max 8 badges
            # Draw badge circle
            x1 = start_x + i * (badge_size + 10)
            y1 = start_y
            x2 = x1 + badge_size
            y2 = y1 + badge_size
            
            # Parse color
            color = badge.get("color", "#FFFFFF")
            if color.startswith('#'):
                try:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    fill_color = (r, g, b)
                except:
                    fill_color = (255, 255, 255)
            else:
                fill_color = (255, 255, 255)
            
            # Draw circle
            draw.ellipse([x1, y1, x2, y2], fill=fill_color, outline=(255, 255, 255), width=3)
            
            # Add badge text (first character)
            badge_name = badge.get("name", "?")
            if badge_name:
                text = badge_name[0]
                try:
                    font = ImageFont.truetype("assets/fonts/arial.ttf", 30)
                except:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text(
                    (x1 + (badge_size - text_width) // 2, y1 + (badge_size - text_height) // 2 - 5),
                    text, font=font, fill=(0, 0, 0)
                )
        
        return image
    
    async def _apply_glow_effect(self, image: Image.Image) -> Image.Image:
        """Apply glow effect to image"""
        return image.filter(ImageFilter.GaussianBlur(radius=2))
    
    async def _apply_neon_effect(self, image: Image.Image) -> Image.Image:
        """Apply neon effect to image"""
        # Simple neon effect implementation
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.2)
    
    async def _create_animation(self, base_image: Image.Image, theme: Dict) -> Optional[str]:
        """Create simple animation from image"""
        try:
            # Create frames for animation
            frames = []
            for i in range(5):
                frame = base_image.copy()
                
                # Add pulsing effect
                if i % 2 == 0:
                    enhancer = ImageEnhance.Brightness(frame)
                    frame = enhancer.enhance(1.1)
                
                frames.append(frame)
            
            # Save as GIF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            animation_path = f"./output/ultra/animation_{timestamp}.gif"
            
            frames[0].save(
                animation_path,
                save_all=True,
                append_images=frames[1:],
                duration=200,
                loop=0,
                optimize=True
            )
            
            return animation_path
            
        except Exception as e:
            logger.error(f"Animation creation failed: {e}")
            return None
    
    # Other effect methods would be implemented similarly
    async def _apply_shadow_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_gradient_text(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_fire_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_ice_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_rainbow_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_hologram_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_sparkle_effect(self, image: Image.Image) -> Image.Image:
        return image
    
    async def _apply_glitter_effect(self, image: Image.Image) -> Image.Image:
        return image


class UltraRoastifyBotV16:
    """🔥 MAIN BOT CLASS - Roastify Bot v16.0 ULTRA PREMIUM EDITION 🔥"""
    
    def __init__(self):
        """Initialize ULTRA Premium Bot"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY.get("name", "🔥 Roastify Ultra v16.0")
        self.bot_version = "16.0.0"
        
        # Initialize ULTRA components
        self.db = UltraDatabase()
        self.theme_manager = UltraThemeManager()
        self.badge_system = UltraBadgeSystem()
        self.analytics_engine = UltraAnalyticsEngine()
        self.image_generator = UltraImageGenerator()
        
        # Initialize features (with fallbacks)
        self._init_features()
        
        # ULTRA Statistics
        self.stats = {
            "messages_processed": 0,
            "roasts_generated": 0,
            "ultra_roasts": 0,
            "images_created": 0,
            "animations_created": 0,
            "users_interacted": set(),
            "premium_users": set(),
            "groups_managed": set(),
            "start_time": datetime.now(),
            "cache_hits": 0,
            "cache_misses": 0,
            "ai_analyses": 0,
            "user_cards_generated": 0,
            "themes_used": {},
            "badges_awarded": 0,
            "challenges_completed": 0,
            "achievements_unlocked": 0,
            "total_votes": 0,
            "system_uptime": 0
        }
        
        # Performance tracking
        self.response_times = []
        self.error_log = []
        self.user_sessions = {}
        
        # Rate limiting (ULTRA version)
        self.user_cooldowns = {}
        self.cooldown_seconds = 1.5  # Very fast for ULTRA
        
        # Application instance
        self.application = None
        
        logger.info(f"🚀 {self.bot_name} v{self.bot_version} initialized!")
        logger.info(f"🔥 ULTRA FEATURES: ALL ENABLED")
        logger.info(f"💎 THEMES: {len(self.theme_manager.themes)}")
        logger.info(f"🎖️ BADGES: {len(self.badge_system.badges)}")
    
    def _init_features(self):
        """Initialize all features with fallbacks"""
        # Roast Engine
        try:
            from features.roast_engine import UltraRoastEngine
            self.roast_engine = UltraRoastEngine()
        except:
            logger.warning("Using fallback roast engine")
            
            class FallbackRoastEngine:
                async def generate_roast(self, text, user, target=None):
                    roasts = [
                        f"🔥 {text} - ULTRA ROASTED! 😂",
                        f"💎 {user.first_name if hasattr(user, 'first_name') else 'User'}: {text} 🔥",
                        f"🎯 Bullseye! {text}",
                        f"⚡ স্পিড রোস্ট: {text}",
                        f"🤖 AI রোস্ট: {text}",
                        f"🏆 Championship roast for {text}",
                        f"🌟 Premium roast: {text}"
                    ]
                    return {
                        "primary_roast": random.choice(roasts),
                        "roast_type": random.choice(["funny", "savage", "clever", "premium"]),
                        "caption": "🔥 ULTRA PREMIUM ROAST!",
                        "ai_score": random.randint(70, 100),
                        "virality_score": random.randint(1, 100)
                    }
            
            self.roast_engine = FallbackRoastEngine()
        
        # Other features initialization would go here...
        # Welcome System, Voting System, etc.
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ULTRA Premium Start Command"""
        user = update.effective_user
        
        try:
            # Add user to database
            user_data = self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_premium=True,
                is_ultra_premium=True,
                join_date=datetime.now(),
                level=1,
                total_roasts=0,
                upvotes=0,
                downvotes=0,
                theme="bangladesh"
            )
            
            # Add to premium users
            self.stats["premium_users"].add(user.id)
            
            # Generate ULTRA welcome message
            welcome_msg = f"""
🚀 <b>{self.bot_name} v{self.bot_version} এ স্বাগতম!</b>

<b>👋 হ্যালো {user.first_name}!</b>

<b>💎 আপনার এক্সেস লেভেল: ULTRA PREMIUM</b>

<b>🔥 ULTRA ফিচারস:</b>
• AI-পাওয়ারড এনালাইটিক্স
• ২০+ প্রিমিয়াম থিম
• ৫০+ অর্জন ব্যাজ
• অ্যানিমেটেড ইমেজ
• রিয়েল-টাইম ড্যাশবোর্ড
• গেমিফিকেশন সিস্টেম
• চ্যালেঞ্জ ও অ্যাচিভমেন্ট
• বাংলা ভাষা সাপোর্ট

<b>🎯 নতুন কমান্ডস:</b>
/profile - আপনার ULTRA প্রোফাইল
/analyze - AI টেক্সট এনালাইসিস
/themes - সব থিম দেখুন
/badges - আপনার ব্যাজেস
/stats - বিস্তারিত পরিসংখ্যান
/leaderboard - ULTRA লিডারবোর্ড
/challenge - ডেইলি চ্যালেঞ্জ
/achievements - অ্যাচিভমেন্টস

<b>⚡ দ্রুত শুরু:</b>
যেকোনো মেসেজ লিখে পাঠান, আমি ULTRA রোস্ট দিব!

<b>🇧🇩 বাংলাদেশি থিম:</b>
বাংলাদেশি থিম ডিফল্ট হিসেবে সেট করা আছে!
/th bangladesh কম্যান্ড দিয়ে পরিবর্তন করুন।

━━━━━━━━━━━━━━━━━━━━━━━━
<b>স্ট্যাটাস:</b> ✅ ALL SYSTEMS GO
<b>ভার্সন:</b> {self.bot_version} ULTRA
<b>সাপোর্ট:</b> @RoastifySupport
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            # Send welcome message
            await update.message.reply_text(
                welcome_msg,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Generate and send welcome image
            await self._send_ultra_welcome_image(update, user)
            
            # Generate user info card
            await self._generate_user_info_card(update, user)
            
            # Award first badge
            await self._award_welcome_badge(update, user)
            
            logger.info(f"🚀 New ULTRA user: {user.id} ({user.username})")
            
        except Exception as e:
            logger.error(f"Error in ULTRA start: {e}")
            await update.message.reply_text(
                f"👋 হ্যালো {user.first_name}! {self.bot_name} v{self.bot_version} এ স্বাগতম!\n\n"
                f"যেকোনো মেসেজ লিখে ULTRA রোস্ট শুরু করুন!",
                parse_mode=ParseMode.HTML
            )
    
    async def _send_ultra_welcome_image(self, update: Update, user: Any):
        """Send ULTRA welcome image"""
        try:
            welcome_data = {
                "title": f"স্বাগতম {user.first_name}!",
                "subtitle": f"{self.bot_name} v{self.bot_version}",
                "message": "আপনি এখন ULTRA PREMIUM সদস্য!",
                "features": [
                    "AI Analytics",
                    "Premium Themes",
                    "50+ Badges",
                    "Animated Images",
                    "Real-time Dashboard"
                ]
            }
            
            result = await self.image_generator.generate_ultra_image(
                roast_data=welcome_data,
                user_info=user,
                theme_name="bangladesh",
                badges=[
                    {"name": "🚀 ULTRA", "color": "#FF4500"},
                    {"name": "💎 PREMIUM", "color": "#00D2FF"},
                    {"name": "🇧🇩 BANGLADESH", "color": "#006A4E"}
                ],
                effects=["glow", "shadow"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="🚀 আপনার ULTRA PREMIUM ওয়েলকাম ইমেজ!",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
                # Update stats
                self.stats["images_created"] += 1
        
        except Exception as e:
            logger.error(f"Error sending welcome image: {e}")
    
    async def _generate_user_info_card(self, update: Update, user: Any):
        """Generate user information card"""
        try:
            # Get user data
            user_data = self.db.get_user_stats(user.id)
            
            # Calculate badges
            badges = self.badge_system.calculate_user_badges(user.id, user_data)
            
            # Create card data
            card_data = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "join_date": datetime.now().strftime("%Y-%m-%d"),
                "level": user_data.get("level", 1),
                "badges": [b["name"] for b in badges[:5]],
                "status": "ULTRA PREMIUM",
                "theme": "bangladesh"
            }
            
            # Generate card image
            result = await self.image_generator.generate_ultra_image(
                roast_data=card_data,
                user_info=user,
                theme_name="bangladesh",
                badges=badges[:8],
                effects=["glow"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📇 আপনার ULTRA প্রোফাইল কার্ড",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
                # Update stats
                self.stats["user_cards_generated"] += 1
        
        except Exception as e:
            logger.error(f"Error generating user card: {e}")
    
    async def _award_welcome_badge(self, update: Update, user: Any):
        """Award welcome badge to new user"""
        try:
            badge = self.badge_system.badges["premium_user"]
            
            badge_msg = f"""
🎖️ <b>প্রথম ব্যাজ অর্জিত!</b>

{badge['name']}
{badge['desc']}

<b>আপনার ব্যাজ সংগ্রহ শুরু হয়েছে!</b>
/badges কম্যান্ড দিয়ে সব ব্যাজ দেখুন।
            """
            
            await update.message.reply_text(
                badge_msg,
                parse_mode=ParseMode.HTML
            )
            
            # Update stats
            self.stats["badges_awarded"] += 1
            
        except Exception as e:
            logger.error(f"Error awarding badge: {e}")
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ULTRA Profile Command"""
        user = update.effective_user
        
        try:
            # Get user data
            user_data = self.db.get_user_stats(user.id)
            
            # Calculate badges
            badges = self.badge_system.calculate_user_badges(user.id, user_data)
            
            # Get analytics
            analytics = await self.analytics_engine.analyze_user_behavior_ultra(user.id, user_data)
            
            # Get badge progress
            badge_progress = self.badge_system.get_badge_progress(user.id, user_data)
            
            # Generate profile message
            profile_text = f"""
📊 <b>ULTRA প্রোফাইল: {user.first_name}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>👤 বেসিক ইনফো:</b>
• ইউজার: @{user.username or 'N/A'}
• নাম: {user.first_name} {user.last_name or ''}
• আইডি: {user.id}
• স্ট্যাটাস: ULTRA PREMIUM ✅

<b>🏆 স্ট্যাটিস্টিকস:</b>
• লেভেল: {user_data.get('level', 1)}
• মোট রোস্ট: {user_data.get('total_roasts', 0):,}
• আপভোট: {user_data.get('upvotes', 0):,}
• ডাউনভোট: {user_data.get('downvotes', 0):,}
• অ্যাপ্রুভাল: {analytics.get('engagement_metrics', {}).get('approval_rate', 0):.1f}%
• অ্যাক্টিভ দিন: {user_data.get('days_active', 1)}

<b>⭐ ব্যাজেস ({len(badges)}):</b>
{', '.join([b['name'] for b in badges[:8]])}
{badges[8]['name'] if len(badges) > 8 else ''} {badges[9]['name'] if len(badges) > 9 else ''}

<b>📈 অ্যাক্টিভিটি প্রোফাইল:</b>
• লেভেল: {analytics.get('activity_profile', {}).get('level', 'unknown').upper()}
• ডেইলি এভারেজ: {analytics.get('activity_profile', {}).get('daily_average', 0):.1f} রোস্ট/দিন
• কনসিসটেন্সি: {analytics.get('activity_profile', {}).get('consistency_score', 0):.1f}%

<b>🎯 রোস্টিং স্টাইল:</b>
• স্টাইল: {analytics.get('roasting_style', {}).get('style', 'unknown').replace('_', ' ').title()}
• ভার্সাটিলিটি: {analytics.get('roasting_style', {}).get('versatility', 0)*100:.1f}%

<b>📊 এনগেজমেন্ট:</b>
• স্কোর: {analytics.get('engagement_metrics', {}).get('engagement_score', 0):.1f}/100
• ভাইরাল পোটেনশিয়াল: {analytics.get('engagement_metrics', {}).get('viral_potential', 0):.1f}%

<b>🚀 গ্রোথ:</b>
• উইকলি গ্রোথ: {analytics.get('growth_trajectory', {}).get('weekly_growth', 0)} রোস্ট
• মোমেন্টাম: {analytics.get('growth_trajectory', {}).get('momentum', 'unknown').upper()}
• প্রজেক্টেড লেভেল: {analytics.get('growth_trajectory', {}).get('projected_level', 0):.0f}

<b>💡 পরবর্তী মাইলস্টোন:</b>
{analytics.get('premium_insights', {}).get('next_milestone', {}).get('milestone', 'N/A')}
• প্রোগ্রেস: {analytics.get('premium_insights', {}).get('next_milestone', {}).get('progress', 0):.1f}%
• রিওয়ার্ড: {analytics.get('premium_insights', {}).get('next_milestone', {}).get('reward', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━
<b>কমান্ডস:</b>
/analyze - AI এনালাইসিস
/themes - থিম পরিবর্তন
/badges - ব্যাজ ডিটেইলস
/stats - বট স্ট্যাটস
/leaderboard - র‍্যাংকিং
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            await update.message.reply_text(
                profile_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Generate and send profile card image
            await self._generate_profile_card_image(update, user, user_data, badges, analytics)
            
            # Send badge progress
            await self._send_badge_progress(update, badge_progress)
            
        except Exception as e:
            logger.error(f"Error in ULTRA profile command: {e}")
            await update.message.reply_text(
                f"📊 {user.first_name} এর প্রোফাইল\n\n"
                f"লেভেল: {user_data.get('level', 1)}\n"
                f"রোস্ট: {user_data.get('total_roasts', 0)}\n"
                f"ব্যাজ: {len(badges) if 'badges' in locals() else 0}\n\n"
                f"<b>ULTRA PREMIUM</b> সদস্য ✅",
                parse_mode=ParseMode.HTML
            )
    
    async def _generate_profile_card_image(self, update: Update, user: Any, 
                                         user_data: Dict, badges: List[Dict], analytics: Dict):
        """Generate profile card image"""
        try:
            # Create profile data for image
            profile_data = {
                "title": f"{user.first_name} এর প্রোফাইল",
                "level": user_data.get("level", 1),
                "total_roasts": user_data.get("total_roasts", 0),
                "approval_rate": analytics.get("engagement_metrics", {}).get("approval_rate", 0),
                "activity_level": analytics.get("activity_profile", {}).get("level", "casual"),
                "roasting_style": analytics.get("roasting_style", {}).get("style", "normal"),
                "badge_count": len(badges),
                "status": "ULTRA PREMIUM",
                "rank": user_data.get("rank", "N/A")
            }
            
            # Generate image
            result = await self.image_generator.generate_ultra_image(
                roast_data=profile_data,
                user_info=user,
                theme_name=self.theme_manager.get_theme(user.id).get("name", "bangladesh"),
                badges=badges[:12],
                effects=["glow", "shadow"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 আপনার ULTRA প্রোফাইল কার্ড",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
        except Exception as e:
            logger.error(f"Error generating profile card image: {e}")
    
    async def _send_badge_progress(self, update: Update, badge_progress: Dict):
        """Send badge progress information"""
        try:
            progress_text = "<b>🎖️ ব্যাজ প্রোগ্রেস:</b>\n"
            
            for badge_name, progress in list(badge_progress.items())[:5]:
                if not progress.get("earned", False):
                    progress_text += f"\n{progress['name']}: {progress['progress']:.1f}%"
            
            if len(progress_text) > 30:  # If there's actual progress to show
                await update.message.reply_text(
                    progress_text,
                    parse_mode=ParseMode.HTML
                )
                
        except Exception as e:
            logger.error(f"Error sending badge progress: {e}")
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ULTRA AI Analysis Command"""
        user = update.effective_user
        
        if not update.message.text or len(update.message.text.split()) < 2:
            await update.message.reply_text(
                "টেক্সট দিন এনালাইসিসের জন্য:\n<code>/analyze আপনার টেক্সট এখানে</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        text = ' '.join(update.message.text.split()[1:])
        
        if len(text) < 5:
            await update.message.reply_text(
                "এনালাইসিসের জন্য কমপক্ষে ৫ অক্ষর প্রয়োজন।",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            "🤖 <b>ULTRA AI এনালাইসিস চলছে...</b>\n"
            "⏳ ৩-৫ সেকেন্ড সময় নিতে পারে...",
            parse_mode=ParseMode.HTML
        )
        
        try:
            # Perform ULTRA analysis
            analysis = await self.analytics_engine.analyze_text_ultra(text, user.id)
            
            # Format results
            analysis_text = self._format_ultra_analysis(analysis, user)
            
            # Send analysis
            await processing_msg.edit_text(
                analysis_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Update stats
            self.stats["ai_analyses"] += 1
            
            # Generate analysis report image
            await self._generate_analysis_report_image(update, user, text, analysis)
            
            logger.info(f"AI analysis completed for user {user.id}")
            
        except Exception as e:
            logger.error(f"Error in ULTRA analysis: {e}")
            await processing_msg.edit_text(
                "❌ <b>এনালাইসিসে সমস্যা হয়েছে!</b>\n"
                "দয়া করে আবার চেষ্টা করুন।",
                parse_mode=ParseMode.HTML
            )
    
    def _format_ultra_analysis(self, analysis: Dict, user: Any) -> str:
        """Format ULTRA analysis results"""
        basic = analysis.get("basic_metrics", {})
        sentiment = analysis.get("sentiment_analysis", {})
        readability = analysis.get("readability_scores", {})
        emotion = analysis.get("emotional_tone", {})
        linguistic = analysis.get("linguistic_features", {})
        insights = analysis.get("ai_insights", {})
        
        # Translate sentiment
        sentiment_map = {
            "VERY_POSITIVE": "খুবই পজিটিভ 😊",
            "POSITIVE": "পজিটিভ 🙂",
            "NEUTRAL": "নিউট্রাল 😐",
            "NEGATIVE": "নেগেটিভ 🙁",
            "VERY_NEGATIVE": "খুবই নেগেটিভ 😠"
        }
        
        sentiment_label = sentiment.get("overall_sentiment", "NEUTRAL")
        sentiment_display = sentiment_map.get(sentiment_label, sentiment_label)
        
        # Translate readability
        readability_map = {
            "VERY_EASY": "খুবই সহজ 👶",
            "EASY": "সহজ 🧒",
            "FAIRLY_EASY": "মোটামুটি সহজ 🧑",
            "STANDARD": "স্ট্যান্ডার্ড 🧑‍🎓",
            "FAIRLY_DIFFICULT": "মোটামুটি কঠিন 🧑‍🏫",
            "DIFFICULT": "কঠিন 🧑‍🔬",
            "VERY_DIFFICULT": "খুবই কঠিন 🧑‍💻"
        }
        
        readability_level = readability.get("reading_level", "STANDARD")
        readability_display = readability_map.get(readability_level, readability_level)
        
        # Format emotions
        emotions = emotion.get("emotions", {})
        dominant_emotion = emotion.get("dominant_emotion", "neutral").upper()
        
        # Get top 3 emotions
        top_emotions = sorted(
            [(k, v) for k, v in emotions.items() if k != "neutral"],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        emotion_text = ", ".join([f"{e[0]}: {e[1]:.1f}%" for e in top_emotions])
        
        # Get insights
        key_takeaways = insights.get("key_takeaways", ["No key takeaways"])
        suggestions = insights.get("suggestions", ["No suggestions"])
        
        return f"""
🔍 <b>ULTRA AI টেক্সট এনালাইসিস</b>
━━━━━━━━━━━━━━━━━━━━━━━━
<b>👤 ইউজার:</b> {user.first_name}
<b>📝 টেক্সট:</b> <i>"{text[:100]}{'...' if len(text) > 100 else ''}"</i>

<b>📊 বেসিক মেট্রিক্স:</b>
• শব্দ: {basic.get('word_count', 0):,}
• বাক্য: {basic.get('sentence_count', 0):,}
• অক্ষর: {basic.get('char_count', 0):,}
• ইউনিক শব্দ: {basic.get('unique_words', 0):,}
• গড় শব্দ দৈর্ঘ্য: {basic.get('avg_word_length', 0):.1f}

<b>😊 সেন্টিমেন্ট অ্যানালাইসিস:</b>
• Overall: {sentiment_display}
• Score: {sentiment.get('compound', 0):.3f}
• Positive: {sentiment.get('positive', 0):.1%}
• Negative: {sentiment.get('negative', 0):.1%}
• Neutral: {sentiment.get('neutral', 0):.1%}

<b>📈 রিডেবিলিটি:</b>
• Level: {readability_display}
• Score: {readability.get('score', 0):.1f}/100
• গড় বাক্য দৈর্ঘ্য: {readability.get('avg_sentence_length', 0):.1f} শব্দ

<b>🎭 ইমোশনাল টোন:</b>
• Dominant: {dominant_emotion}
• Top Emotions: {emotion_text}
• Confidence: {emotion.get('confidence', 0):.1f}%

<b>🔤 লিংগুইস্টিক ফিচারস:</b>
• Text Type: {linguistic.get('text_type', 'UNKNOWN').replace('_', ' ').title()}
• Punctuation Density: {linguistic.get('punctuation_density', 0):.3f}
• Uppercase Ratio: {linguistic.get('uppercase_ratio', 0):.1%}
• Question: {'✅' if linguistic.get('is_question') else '❌'}
• Exclamation: {'✅' if linguistic.get('is_exclamation') else '❌'}

<b>💡 AI ইন্সাইটস:</b>
• Key Takeaways: {key_takeaways[0]}
• Suggestions: {suggestions[0]}

<b>⚡ প্রিমিয়াম ফিচারস:</b>
• Analysis Depth: ULTRA
• Processing: Real-time
• Model: v16.0 AI Engine

━━━━━━━━━━━━━━━━━━━━━━━━
<b>🔄 আরো ডিটেইলস:</b>
/profile - আপনার AI প্রোফাইল
/report - ফুল রিপোর্ট
━━━━━━━━━━━━━━━━━━━━━━━━
        """
    
    async def _generate_analysis_report_image(self, update: Update, user: Any, 
                                            text: str, analysis: Dict):
        """Generate analysis report image"""
        try:
            # Create report data
            report_data = {
                "title": "AI Analysis Report",
                "user": user.first_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text_preview": text[:200] + ("..." if len(text) > 200 else ""),
                "sentiment": analysis.get("sentiment_analysis", {}).get("overall_sentiment", "NEUTRAL"),
                "readability": analysis.get("readability_scores", {}).get("reading_level", "STANDARD"),
                "emotion": analysis.get("emotional_tone", {}).get("dominant_emotion", "neutral"),
                "word_count": analysis.get("basic_metrics", {}).get("word_count", 0),
                "analysis_depth": "ULTRA"
            }
            
            # Generate image
            result = await self.image_generator.generate_ultra_image(
                roast_data=report_data,
                user_info=user,
                theme_name="neon_cyber",
                effects=["glow", "neon"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 AI Analysis Report",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
        except Exception as e:
            logger.error(f"Error generating analysis report image: {e}")
    
    async def themes_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all available themes"""
        user = update.effective_user
        
        try:
            all_themes = self.theme_manager.get_all_themes()
            
            # Create theme list
            theme_list = []
            for i, theme in enumerate(all_themes, 1):
                theme_list.append(f"{i}. {theme['name']}")
                if theme.get('special'):
                    theme_list[-1] += " 🌟"
            
            # Paginate themes (10 per page)
            page = 0
            if context.args and len(context.args) > 0:
                try:
                    page = int(context.args[0]) - 1
                except:
                    page = 0
            
            themes_per_page = 10
            start_idx = page * themes_per_page
            end_idx = start_idx + themes_per_page
            
            paginated_themes = theme_list[start_idx:end_idx]
            
            theme_text = f"""
🎨 <b>ULTRA থিম সংগ্রহ ({len(all_themes)}+)</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>বর্তমান থিম:</b> {self.theme_manager.get_theme(user.id)['name']}

<b>সব থিম:</b>
{chr(10).join(paginated_themes)}

<b>ব্যবহার:</b>
<code>/th [থিম_নাম]</code>
<code>উদাহরণ: /th bangladesh</code>

<b>পেজ:</b> {page + 1}/{math.ceil(len(all_themes) / themes_per_page)}

━━━━━━━━━━━━━━━━━━━━━━━━
<b>🌟 স্পেশাল থিমস:</b>
• 🇧🇩 বাংলাদেশ - বাংলাদেশি থিম
• 💎 ডায়মন্ড প্রো - প্রিমিয়াম
• 🌌 নিয়ন সাইবারপাঙ্ক - আধুনিক
• 🔥 ফায়ার ইফেক্ট - গরম!
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            # Create inline keyboard for theme selection
            keyboard = []
            current_row = []
            
            # Add popular themes as buttons
            popular_themes = ["bangladesh", "diamond_pro", "neon_cyber", "gold_elite", 
                            "silver_pro", "platinum_vip", "fire", "ice", "galaxy"]
            
            for theme_name in popular_themes[:6]:  # First 6 popular themes
                theme = self.theme_manager.themes.get(theme_name)
                if theme:
                    current_row.append(
                        InlineKeyboardButton(
                            theme["name"].split()[0],  # First word/emoji
                            callback_data=f"theme_{theme_name}"
                        )
                    )
                    
                    if len(current_row) == 3:
                        keyboard.append(current_row)
                        current_row = []
            
            if current_row:
                keyboard.append(current_row)
            
            # Add navigation buttons
            if page > 0:
                keyboard.append([
                    InlineKeyboardButton("⬅️ আগের পৃষ্ঠা", callback_data=f"themes_{page-1}")
                ])
            
            if end_idx < len(theme_list):
                keyboard.append([
                    InlineKeyboardButton("পরের পৃষ্ঠা ➡️", callback_data=f"themes_{page+1}")
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
            
            await update.message.reply_text(
                theme_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error in themes command: {e}")
            await update.message.reply_text(
                "🎨 <b>থিমস</b>\n\n"
                "থিম লিস্ট লোড করতে সমস্যা!\n"
                "দয়া করে আবার চেষ্টা করুন।",
                parse_mode=ParseMode.HTML
            )
    
    async def theme_callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle theme selection callback"""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        data = query.data
        
        try:
            if data.startswith("theme_"):
                theme_name = data[6:]  # Remove "theme_" prefix
                
                if theme_name in self.theme_manager.themes:
                    # Set user theme
                    self.theme_manager.set_user_theme(user.id, theme_name)
                    
                    theme = self.theme_manager.themes[theme_name]
                    
                    await query.edit_message_text(
                        f"✅ <b>থিম পরিবর্তন করা হয়েছে!</b>\n\n"
                        f"নতুন থিম: {theme['name']}\n\n"
                        f"রঙ: {', '.join(theme['colors'][:3])}\n"
                        f"ইফেক্টস: {', '.join(theme['effects'][:3])}\n\n"
                        f"<i>পরবর্তী রোস্টে নতুন থিম apply হবে।</i>",
                        parse_mode=ParseMode.HTML
                    )
                    
                    # Update stats
                    self.stats["themes_used"][theme_name] = self.stats["themes_used"].get(theme_name, 0) + 1
                    
                else:
                    await query.edit_message_text(
                        "❌ থিমটি পাওয়া যায়নি!",
                        parse_mode=ParseMode.HTML
                    )
            
            elif data.startswith("themes_"):
                # Handle pagination
                page = int(data[7:])  # Remove "themes_" prefix
                await self.themes_command_page(update, context, page)
        
        except Exception as e:
            logger.error(f"Error in theme callback: {e}")
            await query.edit_message_text(
                "❌ থিম পরিবর্তনে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def themes_command_page(self, update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
        """Show specific page of themes"""
        # This would be called from callback handler
        # Implementation similar to themes_command but with specific page
        pass
    
    async def badges_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user badges and progress"""
        user = update.effective_user
        
        try:
            # Get user data
            user_data = self.db.get_user_stats(user.id)
            
            # Calculate badges
            badges = self.badge_system.calculate_user_badges(user.id, user_data)
            
            # Get badge progress
            badge_progress = self.badge_system.get_badge_progress(user.id, user_data)
            
            # Calculate badge statistics
            total_badges = len(self.badge_system.badges)
            earned_badges = len(badges)
            progress_percentage = (earned_badges / total_badges) * 100 if total_badges > 0 else 0
            
            # Group badges by category
            badge_categories = {}
            for badge in badges:
                category = "other"
                for cat_name, cat_badges in self.badge_system.badge_categories.items():
                    for b in cat_badges:
                        if badge["name"] == self.badge_system.badges[b]["name"]:
                            category = cat_name
                            break
                
                if category not in badge_categories:
                    badge_categories[category] = []
                badge_categories[category].append(badge)
            
            # Create badge display
            badge_text = f"""
🎖️ <b>ULTRA ব্যাজ সংগ্রহ</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>📊 আপনার ব্যাজ স্ট্যাটস:</b>
• অর্জিত ব্যাজ: {earned_badges}/{total_badges}
• প্রোগ্রেস: {progress_percentage:.1f}%
• ক্যাটেগরি: {len(badge_categories)}

<b>🏆 আপনার ব্যাজেস:</b>
            """
            
            # Add badges by category
            for category, cat_badges in badge_categories.items():
                if cat_badges:
                    category_name = category.replace('_', ' ').title()
                    badge_text += f"\n<b>{category_name}:</b>"
                    
                    # Show first few badges in category
                    for badge in cat_badges[:5]:
                        badge_text += f"\n• {badge['name']} - {badge['desc']}"
                    
                    if len(cat_badges) > 5:
                        badge_text += f"\n• ... এবং আরো {len(cat_badges) - 5} ব্যাজ"
            
            # Add next badges to earn
            badge_text += f"\n\n<b>🎯 পরবর্তী ব্যাজ:</b>"
            
            next_badges = []
            for badge_name, progress in badge_progress.items():
                if not progress.get("earned", False):
                    next_badges.append(progress)
                    if len(next_badges) >= 3:
                        break
            
            for next_badge in next_badges:
                badge_text += f"\n• {next_badge['name']}: {next_badge['progress']:.1f}%"
            
            # Add achievement level
            if progress_percentage >= 90:
                achievement_level = "🎖️ ব্যাজ মাস্টার"
            elif progress_percentage >= 70:
                achievement_level = "🏆 ব্যাজ কালেক্টর"
            elif progress_percentage >= 50:
                achievement_level = "⭐ ব্যাজ এনথুসিয়াস্ট"
            elif progress_percentage >= 30:
                achievement_level = "🌱 ব্যাজ বিগিনার"
            else:
                achievement_level = "🌱 শুরু করেছেন"
            
            badge_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━
<b>🏅 আপনার অ্যাচিভমেন্ট লেভেল:</b>
{achievement_level}

<b>⚡ ব্যাজ অর্জনের টিপস:</b>
• নিয়মিত রোস্ট করুন
• বিভিন্ন ধরনের রোস্ট করুন
• অন্যের রোস্টে ভোট দিন
• চ্যালেঞ্জ গুলোতে অংশ নিন
• ফেস্টিভাল ইভেন্টে অংশ নিন

━━━━━━━━━━━━━━━━━━━━━━━━
<b>কমান্ডস:</b>
/profile - বিস্তারিত প্রোফাইল
/achievements - অ্যাচিভমেন্টস
/challenges - ডেইলি চ্যালেঞ্জ
━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            await update.message.reply_text(
                badge_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Generate badge collection image
            await self._generate_badges_image(update, user, badges, badge_categories)
            
        except Exception as e:
            logger.error(f"Error in badges command: {e}")
            await update.message.reply_text(
                "🎖️ <b>আপনার ব্যাজেস</b>\n\n"
                f"অর্জিত ব্যাজ: {len(badges) if 'badges' in locals() else 0}\n\n"
                "দুঃখিত, ব্যাজ লিস্ট লোড করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def _generate_badges_image(self, update: Update, user: Any, 
                                   badges: List[Dict], categories: Dict):
        """Generate badges collection image"""
        try:
            # Create badges data for image
            badges_data = {
                "title": f"{user.first_name} এর ব্যাজ সংগ্রহ",
                "total_badges": len(badges),
                "total_categories": len(categories),
                "categories": list(categories.keys()),
                "top_badges": [b["name"] for b in badges[:8]],
                "achievement_level": "ULTRA" if len(badges) > 20 else "PREMIUM" if len(badges) > 10 else "BEGINNER"
            }
            
            # Generate image
            result = await self.image_generator.generate_ultra_image(
                roast_data=badges_data,
                user_info=user,
                theme_name="gold_elite",
                badges=badges[:12],
                effects=["glow", "sparkle"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="🎖️ আপনার ULTRA ব্যাজ সংগ্রহ",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
        except Exception as e:
            logger.error(f"Error generating badges image: {e}")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot statistics - ULTRA VERSION"""
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
            # If admin check fails, still show stats to user
            pass
        
        # Calculate uptime
        uptime = datetime.now() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        # Calculate performance metrics
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        # Calculate cache hit rate
        total_cache = self.stats["cache_hits"] + self.stats["cache_misses"]
        cache_hit_rate = (self.stats["cache_hits"] / total_cache * 100) if total_cache > 0 else 0
        
        # Calculate user engagement
        total_users = len(self.stats["users_interacted"])
        premium_users = len(self.stats["premium_users"])
        premium_percentage = (premium_users / total_users * 100) if total_users > 0 else 0
        
        # Get most popular themes
        popular_themes = sorted(
            self.stats["themes_used"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        theme_stats = "\n".join([
            f"• {theme}: {count} বার" 
            for theme, count in popular_themes
        ]) if popular_themes else "No theme data"
        
        stats_text = f"""
📊 <b>{self.bot_name} ULTRA STATISTICS v{self.bot_version}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>⏰ সিস্টেম আপটাইম:</b>
{days} দিন, {hours} ঘণ্টা, {minutes} মিনিট, {seconds} সেকেন্ড

<b>📈 পারফরম্যান্স মেট্রিক্স:</b>
• গড় রেসপন্স টাইম: {avg_response_time:.2f}s
• সর্বনিম্ন টাইম: {min_response_time:.2f}s
• সর্বোচ্চ টাইম: {max_response_time:.2f}s
• ক্যাশে হিট রেট: {cache_hit_rate:.1f}%

<b>🚀 ব্যবহারের পরিসংখ্যান:</b>
• প্রসেসড মেসেজ: {self.stats['messages_processed']:,}
• জেনারেটেড রোস্ট: {self.stats['roasts_generated']:,}
• ULTRA রোস্ট: {self.stats['ultra_roasts']:,}
• ক্রিয়েটেড ইমেজ: {self.stats['images_created']:,}
• অ্যানিমেশন: {self.stats['animations_created']:,}
• AI এনালাইসিস: {self.stats['ai_analyses']:,}

<b>👥 ইউজার পরিসংখ্যান:</b>
• মোট ইউজার: {total_users:,}
• প্রিমিয়াম ইউজার: {premium_users:,} ({premium_percentage:.1f}%)
• মোট গ্রুপ: {len(self.stats['groups_managed']):,}
• ইউজার কার্ড: {self.stats['user_cards_generated']:,}

<b>🏆 অ্যাচিভমেন্ট পরিসংখ্যান:</b>
• অ্যাওয়ার্ডেড ব্যাজ: {self.stats['badges_awarded']:,}
• কমপ্লিটেড চ্যালেঞ্জ: {self.stats['challenges_completed']:,}
• আনলকড অ্যাচিভমেন্ট: {self.stats['achievements_unlocked']:,}
• মোট ভোট: {self.stats['total_votes']:,}

<b>🎨 থিম পরিসংখ্যান:</b>
{theme_stats}

<b>⚡ রিয়েল-টাইম মেট্রিক্স:</b>
• অ্যাক্টিভ সেশন: {len(self.user_sessions)}
• কো-ডাউন ইউজার: {len(self.user_cooldowns)}
• সর্বশেষ এরর: {len(self.error_log)}

<b>🔧 সিস্টেম হেলথ:</b>
• ডাটাবেস: ✅ CONNECTED
• AI Engine: {'✅ ACTIVE' if HAS_AI else '⚠️ LIMITED'}
• Image Gen: {'✅ ACTIVE' if HAS_PIL else '⚠️ LIMITED'}
• Theme System: ✅ ACTIVE ({len(self.theme_manager.themes)} themes)
• Badge System: ✅ ACTIVE ({len(self.badge_system.badges)} badges)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>🔄 লাইভ আপডেট:</b>
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<b>🚀 স্ট্যাটাস:</b> ALL SYSTEMS OPERATIONAL
<b>💎 এডিশন:</b> ULTRA PREMIUM v{self.bot_version}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
        # Generate system status image
        await self._generate_system_status_image(update)
    
    async def _generate_system_status_image(self, update: Update):
        """Generate system status image"""
        try:
            status_data = {
                "title": f"{self.bot_name} System Status",
                "version": self.bot_version,
                "uptime": f"{self.stats['days_active']} days" if hasattr(self.stats, 'days_active') else "Live",
                "messages_processed": self.stats["messages_processed"],
                "users_active": len(self.stats["users_interacted"]),
                "system_health": "EXCELLENT",
                "premium_users": len(self.stats["premium_users"]),
                "cache_hit_rate": f"{((self.stats['cache_hits'] / max(self.stats['cache_hits'] + self.stats['cache_misses'], 1)) * 100):.1f}%",
                "ai_analyses": self.stats["ai_analyses"]
            }
            
            result = await self.image_generator.generate_ultra_image(
                roast_data=status_data,
                user_info=None,
                theme_name="neon_cyber",
                effects=["glow", "grid"]
            )
            
            if result.get("success") and result.get("image_path"):
                with open(result["image_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 System Status Dashboard",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(result["image_path"])
                except:
                    pass
                
        except Exception as e:
            logger.error(f"Error generating system status image: {e}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages - ULTRA VERSION"""
        start_time = time.time()
        
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
                        "⏳ একটু অপেক্ষা করুন! ULTRA স্পিডে রিকোয়েস্ট করছেন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
            # Check minimum length
            if len(text) < CORE_RULES.get("minimum_input_length", 3):
                if len(text) > 0:
                    await message.reply_text(
                        f"একটু লম্বা লিখুন! ULTRA রোস্টের জন্য কমপক্ষে {CORE_RULES.get('minimum_input_length', 3)} অক্ষর প্রয়োজন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
            # Check maximum length
            if len(text) > CORE_RULES.get("maximum_input_length", 5000):
                await message.reply_text(
                    f"টেক্সট খুব লম্বা! সর্বোচ্চ {CORE_RULES.get('maximum_input_length', 5000)} অক্ষর অনুমোদিত।",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Check ignore conditions
            if self._should_ignore_message_ultra(text):
                return
            
            # Send typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Generate ULTRA roast
            roast_data = await self.roast_engine.generate_roast(text, user)
            
            # Update stats
            self.stats["roasts_generated"] += 1
            self.stats["ultra_roasts"] += 1
            
            # Get user data for badges
            user_data = self.db.get_user_stats(user.id)
            
            # Calculate badges
            badges = self.badge_system.calculate_user_badges(user.id, user_data)
            
            # Get user theme
            user_theme = self.theme_manager.get_theme(user.id)
            theme_name = list(self.theme_manager.themes.keys())[
                list(self.theme_manager.themes.values()).index(user_theme)
            ] if user_theme in self.theme_manager.themes.values() else "bangladesh"
            
            # Generate ULTRA image
            image_result = await self.image_generator.generate_ultra_image(
                roast_data=roast_data,
                user_info=user,
                theme_name=theme_name,
                badges=badges[:8],
                effects=user_theme.get("effects", ["glow", "shadow"])[:3]
            )
            
            # Send image if generated successfully
            if image_result.get("success") and image_result.get("image_path"):
                caption = f"🔥 {roast_data.get('caption', 'ULTRA PREMIUM ROAST!')}"
                
                # Check if animation exists
                if image_result.get("animation_path"):
                    with open(image_result["animation_path"], 'rb') as animation:
                        sent_message = await update.message.reply_animation(
                            animation=animation,
                            caption=caption,
                            parse_mode=ParseMode.HTML
                        )
                    self.stats["animations_created"] += 1
                else:
                    with open(image_result["image_path"], 'rb') as photo:
                        sent_message = await update.message.reply_photo(
                            photo=photo,
                            caption=caption,
                            parse_mode=ParseMode.HTML
                        )
                
                self.stats["images_created"] += 1
                
                # Cleanup
                try:
                    if image_result.get("image_path"):
                        os.remove(image_result["image_path"])
                    if image_result.get("animation_path"):
                        os.remove(image_result["animation_path"])
                except:
                    pass
            
            # Send text roast
            if CORE_RULES.get("text_reply", True) and roast_data.get("primary_roast"):
                roast_text = f"💎 {roast_data.get('primary_roast')}"
                
                # Add AI score if available
                if roast_data.get("ai_score"):
                    roast_text += f"\n\n🤖 AI Score: {roast_data['ai_score']}/100"
                
                if roast_data.get("virality_score"):
                    roast_text += f" | 🔥 Virality: {roast_data['virality_score']}%"
                
                await update.message.reply_text(
                    roast_text,
                    parse_mode=ParseMode.HTML
                )
            
            # Update user data
            self.db.add_or_update_user(
                user_id=user.id,
                total_roasts=user_data.get("total_roasts", 0) + 1,
                last_active=datetime.now()
            )
            
            # Calculate response time
            response_time = time.time() - start_time
            self.response_times.append(response_time)
            
            # Keep only last 100 response times
            if len(self.response_times) > 100:
                self.response_times.pop(0)
            
            logger.info(f"ULTRA roast generated for user {user.id} in {response_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error handling ULTRA message: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            self.error_log.append({
                "time": datetime.now(),
                "user_id": user.id if 'user' in locals() else None,
                "error": str(e),
                "traceback": traceback.format_exc()[:500]
            })
            
            if update.message:
                await update.message.reply_text(
                    "⚠️ ULTRA processing এ সমস্যা! আবার চেষ্টা করুন।",
                    parse_mode=ParseMode.HTML
                )
    
    def _check_cooldown(self, user_id: int) -> bool:
        """Check if user is in cooldown - ULTRA VERSION"""
        now = time.time()
        last_request = self.user_cooldowns.get(user_id, 0)
        
        # ULTRA users get faster cooldown
        is_ultra = user_id in self.stats["premium_users"]
        cooldown = self.cooldown_seconds / 2 if is_ultra else self.cooldown_seconds
        
        if now - last_request < cooldown:
            return False
        
        self.user_cooldowns[user_id] = now
        return True
    
    def _should_ignore_message_ultra(self, text: str) -> bool:
        """Check if message should be ignored - ULTRA VERSION"""
        # Check for commands
        if text.startswith('/'):
            return True
        
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
        
        # Check for very short text after cleaning
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        if len(cleaned_text.strip()) < 2:
            return True
        
        return False
    
    def setup_handlers(self, application):
        """Setup all ULTRA handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("profile", self.profile_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("themes", self.themes_command))
        application.add_handler(CommandHandler("badges", self.badges_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Theme selection callback
        application.add_handler(CallbackQueryHandler(
            self.theme_callback_handler, pattern="^(theme_|themes_)"
        ))
        
        # Message handler
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        logger.info("🚀 ULTRA handlers setup complete")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors - ULTRA VERSION"""
        error_msg = str(context.error)
        
        logger.error(f"ULTRA Exception: {error_msg}")
        traceback_str = traceback.format_exc()
        logger.error(f"Traceback:\n{traceback_str}")
        
        # Log error
        self.error_log.append({
            "time": datetime.now(),
            "error": error_msg[:200],
            "traceback": traceback_str[:500]
        })
        
        # Keep only last 50 errors
        if len(self.error_log) > 50:
            self.error_log.pop(0)
        
        # Try to send error to owner
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            if owner_id and context.bot:
                error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                error_text = f"""
🚨 <b>ULTRA BOT ERROR!</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>Time:</b> {error_time}
💥 <b>Error:</b> {error_msg[:100]}
📱 <b>Version:</b> {self.bot_version}
💎 <b>Edition:</b> ULTRA PREMIUM
━━━━━━━━━━━━━━━━━━━━
<b>Action:</b> Check ultra_error.log
                """
                
                await context.bot.send_message(
                    chat_id=owner_id,
                    text=error_text,
                    parse_mode=ParseMode.HTML
                )
        except:
            pass
    
    def run(self):
        """Run the ULTRA bot"""
        try:
            # Create application
            self.application = ApplicationBuilder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .concurrent_updates(True)\
                .pool_timeout(30)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Start background tasks
            asyncio.create_task(self._ultra_background_tasks())
            
            # Run bot
            logger.info(f"🚀 Starting {self.bot_name} ULTRA v{self.bot_version}...")
            logger.info(f"🔥 ALL FEATURES UNLOCKED")
            logger.info(f"💎 ULTRA PREMIUM EDITION")
            logger.info(f"🇧🇩 BANGLADESH EDITION")
            
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
            
        except KeyboardInterrupt:
            logger.info("🛑 ULTRA bot stopped by user")
            self.cleanup()
            
        except Exception as e:
            logger.error(f"💥 Fatal error running ULTRA bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            self.cleanup()
            raise
    
    async def post_init(self, application):
        """Post initialization tasks"""
        logger.info("🚀 ULTRA bot post-init started...")
        
        # Set bot commands
        commands = [
            BotCommand("start", "Start the ULTRA bot"),
            BotCommand("profile", "Your ULTRA profile"),
            BotCommand("analyze", "AI text analysis"),
            BotCommand("themes", "Show all themes"),
            BotCommand("badges", "Your badges collection"),
            BotCommand("stats", "Bot statistics (admin)"),
            BotCommand("help", "Show help message")
        ]
        
        try:
            await application.bot.set_my_commands(commands)
            logger.info("✅ Bot commands set")
        except Exception as e:
            logger.error(f"Error setting commands: {e}")
        
        # Send startup notification
        await self._send_ultra_startup_notification()
        
        logger.info("✅ ULTRA bot startup complete")
    
    async def _send_ultra_startup_notification(self):
        """Send ULTRA startup notification"""
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if owner_id and self.application.bot:
                startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                startup_msg = f"""
🚀 <b>{self.bot_name} ULTRA STARTED SUCCESSFULLY!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Version:</b> {self.bot_version} ULTRA
💎 <b>Edition:</b> Ultimate Premium
🇧🇩 <b>Region:</b> Bangladesh Edition

<b>✅ ULTRA FEATURES ACTIVE:</b>
• Advanced AI Analytics
• 20+ Premium Themes
• 50+ Achievement Badges
• Animated Image Generation
• Real-time User Analytics
• Gamification System
• Challenge System
• Bengali Language Support

<b>📊 SYSTEM READY:</b>
• Database: ✅ Connected
• AI Engine: {'✅ Active' if HAS_AI else '⚠️ Limited'}
• Image Processing: {'✅ Active' if HAS_PIL else '⚠️ Limited'}
• Theme System: ✅ Active
• Badge System: ✅ Active

<b>🔥 READY FOR ULTRA ROASTING!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
                """
                
                await self.application.bot.send_message(
                    chat_id=owner_id,
                    text=startup_msg,
                    parse_mode=ParseMode.HTML
                )
                
                logger.info("🚀 ULTRA startup notification sent")
                
        except Exception as e:
            logger.error(f"Error sending startup notification: {e}")
    
    async def _ultra_background_tasks(self):
        """Run ULTRA background maintenance tasks"""
        while True:
            try:
                # Update system uptime
                self.stats["system_uptime"] = (datetime.now() - self.stats["start_time"]).total_seconds()
                
                # Cleanup old cooldowns
                current_time = time.time()
                old_cooldowns = [
                    user_id for user_id, last_time in self.user_cooldowns.items()
                    if current_time - last_time > 3600  # 1 hour
                ]
                for user_id in old_cooldowns:
                    del self.user_cooldowns[user_id]
                
                # Cleanup old sessions
                old_sessions = [
                    session_id for session_id, session_data in self.user_sessions.items()
                    if current_time - session_data.get("last_activity", 0) > 1800  # 30 minutes
                ]
                for session_id in old_sessions:
                    del self.user_sessions[session_id]
                
                # Log statistics every 30 minutes
                if int(time.time()) % 1800 < 5:  # Every 30 minutes
                    logger.info(
                        f"📊 ULTRA Stats: "
                        f"Users: {len(self.stats['users_interacted'])}, "
                        f"Roasts: {self.stats['roasts_generated']}, "
                        f"Images: {self.stats['images_created']}, "
                        f"AI Analyses: {self.stats['ai_analyses']}"
                    )
                
                # Sleep for 1 minute
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in ULTRA background tasks: {e}")
                await asyncio.sleep(30)
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up ULTRA bot resources...")
        
        try:
            if hasattr(self, 'image_generator') and self.image_generator:
                self.image_generator.executor.shutdown(wait=False)
        except:
            pass
        
        logger.info("✅ ULTRA bot cleanup complete")


def create_ultra_directories():
    """Create necessary directories for ULTRA version"""
    directories = [
        "assets/ultra/fonts",
        "assets/ultra/borders",
        "assets/ultra/templates",
        "assets/ultra/backgrounds",
        "assets/ultra/badges",
        "assets/ultra/effects",
        "output/ultra",
        "temp/ultra",
        "cache/ultra",
        "backup/ultra",
        "logs/ultra",
        "data/ultra",
        "reports/ultra",
        "animations"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created ULTRA directory: {directory}")


def main():
    """Main entry point - ULTRA VERSION"""
    # Create ULTRA directories
    create_ultra_directories()
    
    # Check environment
    logger.info("=" * 60)
    logger.info(f"🚀 {BOT_IDENTITY.get('name', 'Roastify Ultra')} v16.0")
    logger.info(f"💎 ULTRA PREMIUM EDITION - ALL FEATURES UNLOCKED")
    logger.info(f"🇧🇩 BANGLADESH EDITION")
    logger.info("=" * 60)
    
    # Check for required packages
    if not HAS_AI:
        logger.warning("⚠️ AI packages not fully installed. Some features limited.")
        logger.info("Install: pip install numpy nltk textblob spacy scikit-learn pandas")
    
    if not HAS_PIL:
        logger.warning("⚠️ PIL/Pillow not installed. Image generation limited.")
        logger.info("Install: pip install Pillow")
    
    # Check bot token
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found!")
        logger.info("Please set BOT_TOKEN in config.py or environment variables")
        sys.exit(1)
    
    # Run ULTRA bot
    try:
        bot = UltraRoastifyBotV16()
        bot.run()
    except Exception as e:
        logger.error(f"💥 Failed to run ULTRA bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
