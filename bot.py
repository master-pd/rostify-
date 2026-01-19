#!/usr/bin/env python3
"""
Main Roastify Telegram Bot - FINAL COMPLETE VERSION
Advanced professional bot with ALL features - FIXED ALL ERRORS
"""

import os
import sys
import logging
import json
import traceback
import re
import random
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import bot components
try:
    from config import BOT_TOKEN, BOT_IDENTITY, CORE_RULES
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
    from utils.image_generator import ImageGenerator
    from utils.template_manager import TemplateManager
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

# Import Telegram libraries
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        filters,
        ContextTypes,
        JobQueue
    )
    from telegram.constants import ParseMode
except ImportError:
    logger.error("Telegram library not installed. Install with: pip install python-telegram-bot")
    sys.exit(1)


class RoastifyBot:
    """Main Roastify Bot Class - FINAL COMPLETE VERSION WITH ALL FIXES"""
    
    def __init__(self):
        """Initialize the bot with ALL features"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY["name"]
        self.bot_tagline = BOT_IDENTITY["tagline"]
        
        # Initialize components
        self.db = get_database()
        self.image_gen = ImageGenerator()
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
        self.auto_daily_quote = None  # Will be initialized with job_queue
        
        try:
            self.custom_unlocks = CustomTemplateUnlocks()
        except:
            self.custom_unlocks = None
            logger.warning("CustomTemplateUnlocks initialization failed, continuing without it")
        
        # Load all features dynamically
        try:
            self.features = load_all_features()
        except Exception as e:
            logger.error(f"Error loading features: {e}")
            self.features = {}
        
        # Statistics - FIXED: Using sets for unique tracking
        self.stats = {
            "messages_processed": 0,
            "roasts_generated": 0,
            "images_created": 0,
            "users_interacted_set": set(),  # Use set for unique users
            "groups_managed_set": set(),    # Use set for unique groups
            "start_time": datetime.now()
        }
        
        # Application instance
        self.application = None
        
        logger.info(f"Initialized {self.bot_name} Bot with ALL features")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        try:
            # Add/update user in database
            self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            welcome_message = await self.welcome_system.get_welcome_message(user, chat)
            
            if update.message:
                await update.message.reply_text(
                    welcome_message,
                    parse_mode=ParseMode.HTML
                )
            
            logger.info(f"New start from user {user.id} in chat {chat.id}")
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            if update.message:
                await update.message.reply_text(
                    "স্বাগতম! 🎉 আমি Roastify Bot, আপনার টেক্সটকে স্টাইলিশ রোস্টে রূপান্তর করি!",
                    parse_mode=ParseMode.HTML
                )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
<b>{self.bot_name} - {self.bot_tagline}</b>

🤖 <b>কিভাবে ব্যবহার করবেন:</b>
• যেকোনো টেক্সট পাঠান (সর্বনিম্ন ৪ অক্ষর)
• আমি এটিকে স্টাইলিশ 3D ইমেজ রোস্টে রূপান্তর করব
• কোন কমান্ডের প্রয়োজন নেই!

🎯 <b>প্রধান বৈশিষ্ট্য:</b>
• স্মার্ট টেক্সট বিশ্লেষণ ও রোস্টিং
• র্যান্ডম বর্ডার/ফন্ট সহ 3D ইমেজ জেনারেশন
• মুড ভিত্তিক অটো ইমোজি রিএকশন
• রোস্টের জন্য ইনলাইন ভোটিং সিস্টেম
• ব্যবহারকারী লিডারবোর্ড
• গ্রুপে @মেনশন ভিত্তিক রোস্টিং
• ফেস্টিভাল থিম ও স্পেশাল মোড
• টেমপ্লেট আনলক সিস্টেম
• নিরাপদ ফরওয়ার্ড শেয়ারিং
• দৈনিক উক্তি পোস্ট

👥 <b>গ্রুপ বৈশিষ্ট্য:</b>
• নতুন সদস্যদের ইমেজ সহ স্বাগতম
• @মেনশন দিয়ে নির্দিষ্ট ব্যবহারকারীকে রোস্ট করুন
• বার্তায় অটো-রিএকশন
• গ্রুপ পরিসংখ্যান ও লিডারবোর্ড

🔧 <b>কমান্ড:</b>
/start - বট শুরু করুন
/help - সাহায্য দেখুন
/stats - বট পরিসংখ্যান (অ্যাডমিন)
/leaderboard - ব্যবহারকারী র্যাঙ্কিং দেখুন
/unlocks - টেমপ্লেট আনলক প্রোগ্রেস দেখুন
/quote - দৈনিক রোস্ট উক্তি পান
/mood - বার্তার মুড বিশ্লেষণ করুন

⚡ <b>টিপস:</b>
• গ্রুপে @মেনশন ব্যবহার করে টার্গেটেড রোস্ট করুন
• ভোট দিয়ে বটের উন্নতি করুন
• বিশেষ টেমপ্লেট আনলক করতে সক্রিয় থাকুন
• নিয়মিত লিডারবোর্ড চেক করুন

🔒 <b>গোপনীয়তা:</b>
• ব্যক্তিগত তথ্য কখনও সংরক্ষণ করা হয় না
• সমস্ত শেয়ার করা কন্টেন্ট গোপনীয়তা-ফিল্টার করা
• কোন বার্তা লগিং নেই

মজাদার রোস্টিংয়ের জন্য তৈরি! ❤️
        """
        
        if update.message:
            await update.message.reply_text(
                help_text,
                parse_mode=ParseMode.HTML
            )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        user = update.effective_user
        
        try:
            # Check if user is admin/owner
            from config import OWNER_ADMIN_PROTECTION
            if user.id != OWNER_ADMIN_PROTECTION["bot_owner_user_id"] and \
               user.id not in OWNER_ADMIN_PROTECTION["admin_user_ids"]:
                await update.message.reply_text("❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!")
                return
            
            # Calculate uptime
            uptime = datetime.now() - self.stats["start_time"]
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            
            # Get database stats
            total_users = self.db.get_total_users()
            total_votes = self.db.get_total_votes()
            total_templates = self.db.get_total_template_usage()
            
            # Get unique counts from sets
            unique_users = len(self.stats["users_interacted_set"])
            unique_groups = len(self.stats["groups_managed_set"])
            
            stats_text = f"""
<b>{self.bot_name} পরিসংখ্যান</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>আপটাইম:</b> {days}দিন {hours}ঘণ্টা {minutes}মিনিট {seconds}সেকেন্ড
📊 <b>প্রসেসকৃত বার্তা:</b> {self.stats['messages_processed']:,}
🔥 <b>জেনারেট করা রোস্ট:</b> {self.stats['roasts_generated']:,}
🖼️ <b>তৈরি করা ছবি:</b> {self.stats['images_created']:,}
👥 <b>ইন্টারঅ্যাক্ট করা ইউজার:</b> {unique_users:,}
🏠 <b>ব্যবস্থাপনাধীন গ্রুপ:</b> {unique_groups:,}
━━━━━━━━━━━━━━━━━━━━
<b>ডাটাবেস পরিসংখ্যান:</b>
• মোট ইউজার: {total_users:,}
• মোট ভোট: {total_votes:,}
• ব্যবহৃত টেমপ্লেট: {total_templates:,}
━━━━━━━━━━━━━━━━━━━━
<b>বৈশিষ্ট্য স্ট্যাটাস:</b>
• অটো রিএকশন: ✅
• ভোটিং সিস্টেম: ✅
• লিডারবোর্ড: ✅
• ফেস্টিভাল মোড: ✅
• মুড রিকগনিশন: ✅
• টেমপ্লেট আনলক: ✅
• সেফ ফরওয়ার্ড: ✅
━━━━━━━━━━━━━━━━━━━━
<b>সিস্টেম স্ট্যাটাস:</b> ✅ অপারেশনাল
            """
            
            await update.message.reply_text(
                stats_text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error in stats command: {e}")
            await update.message.reply_text(
                "পরিসংখ্যান লোড করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        try:
            await self.leaderboard.handle_leaderboard_command(update, context)
        except Exception as e:
            logger.error(f"Error in leaderboard command: {e}")
            await update.message.reply_text(
                "লিডারবোর্ড লোড করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def unlocks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unlocks command"""
        try:
            if self.custom_unlocks:
                await self.custom_unlocks.show_unlock_progress(update, context)
            else:
                await update.message.reply_text(
                    "টেমপ্লেট আনলক সিস্টেম এখন উপলব্ধ নেই।",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logger.error(f"Error in unlocks command: {e}")
            await update.message.reply_text(
                "আনলক তথ্য লোড করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        try:
            if self.auto_daily_quote:
                await self.auto_daily_quote.manual_post_quote(
                    update.effective_chat.id, context
                )
            else:
                await update.message.reply_text(
                    "দৈনিক উক্তি সিস্টেম এখনও ইনিশিয়ালাইজ হয়নি!",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logger.error(f"Error in quote command: {e}")
            await update.message.reply_text(
                "উক্তি লোড করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def mood_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mood command"""
        try:
            # Check if replying to a message
            if update.message.reply_to_message:
                text = update.message.reply_to_message.text or ""
            else:
                # Use the text after command
                text = ' '.join(context.args) if context.args else ""
            
            if not text:
                await update.message.reply_text(
                    "মুড অ্যানালাইসিস করার জন্য কিছু টেক্সট দাও বা রিপ্লাই দাও!\n\n"
                    "উদাহরণ:\n"
                    "<code>/mood আমি আজ খুব খুশি</code>\n"
                    "অথবা কোন বার্তায় রিপ্লাই দিয়ে <code>/mood</code> লিখুন",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Analyze mood
            mood_analysis = self.mood_recognition.analyze_mood(
                text, update.effective_user.id
            )
            
            # Send analysis
            await self.mood_recognition.send_mood_analysis(
                update.effective_chat.id, mood_analysis, context
            )
            
        except Exception as e:
            logger.error(f"Error in mood command: {e}")
            await update.message.reply_text(
                "মুড অ্যানালাইসিস করতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    async def forward_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /forward command"""
        try:
            await self.safe_forward.safe_forward(update, context)
        except Exception as e:
            logger.error(f"Error in forward command: {e}")
            await update.message.reply_text(
                "ফরওয়ার্ড করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def share_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /share command"""
        try:
            await self.safe_forward.safe_share_roast(update, context)
        except Exception as e:
            logger.error(f"Error in share command: {e}")
            await update.message.reply_text(
                "শেয়ার করতে সমস্যা হয়েছে!",
                parse_mode=ParseMode.HTML
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages - MAIN MESSAGE HANDLER"""
        try:
            # Update statistics
            self.stats["messages_processed"] += 1
            
            user = update.effective_user
            chat = update.effective_chat
            message = update.message
            
            if not message or not message.text:
                return
            
            text = message.text.strip()
            
            # Add/update user in database
            try:
                self.db.add_or_update_user(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
            except Exception as e:
                logger.error(f"Error adding user to database: {e}")
            
            # Update users interacted (using set for unique tracking) - FIXED
            self.stats["users_interacted_set"].add(user.id)
            
            # Update group count if in group
            if chat.type in ["group", "supergroup"]:
                self.stats["groups_managed_set"].add(chat.id)
            
            # Check for admin protection triggers
            try:
                if await self.admin_protection.check_protection_needed(user, text, chat):
                    await self.admin_protection.handle_protected_response(
                        update, context, user, text
                    )
                    return
            except Exception as e:
                logger.error(f"Error in admin protection: {e}")
            
            # Check minimum length
            if len(text) < CORE_RULES["minimum_input_length"]:
                if len(text) > 0:
                    try:
                        short_response = await self.roast_engine.get_short_response(text, user)
                        await message.reply_text(short_response, parse_mode=ParseMode.HTML)
                    except:
                        short_responses = [
                            f"একটু লম্বা লিখো {user.first_name}... কমপক্ষে {CORE_RULES['minimum_input_length']} অক্ষর!",
                            f"ওহহ! {user.first_name}, আরও কিছু লিখতে হবে!",
                            f"এত ছোট কেন {user.first_name}? আরেকটু লম্বা করে লিখো!"
                        ]
                        await message.reply_text(random.choice(short_responses))
                return
            
            # Check ignore conditions
            if self._should_ignore_message(text):
                logger.info(f"Ignoring message from {user.id}: {text[:50]}...")
                return
            
            # Analyze mood
            try:
                mood_analysis = self.mood_recognition.analyze_mood(text, user.id)
            except:
                mood_analysis = None
                logger.warning("Mood analysis failed, continuing without it")
            
            # Check for mentions in groups
            if chat.type in ["group", "supergroup"] and message.entities:
                try:
                    mention_result = await self.mention_roast.process_mention(
                        message, text, user, chat
                    )
                    if mention_result:
                        # Generate roast for mentioned user
                        await self._generate_roast_response(
                            update, context, text, user, chat, 
                            target_user=mention_result["target"],
                            mood_analysis=mood_analysis
                        )
                        return
                except Exception as e:
                    logger.error(f"Error processing mention: {e}")
            
            # Generate regular roast
            await self._generate_roast_response(
                update, context, text, user, chat, mood_analysis=mood_analysis
            )
            
            # Auto-reactions
            try:
                await self.reaction_system.add_auto_reactions(message, text, user, chat)
            except Exception as e:
                logger.error(f"Error adding auto reactions: {e}")
            
            # Check for template unlocks
            try:
                if self.custom_unlocks:
                    new_unlocks = await self.custom_unlocks.check_unlocks(user.id)
                    if new_unlocks:
                        await self.custom_unlocks.notify_unlocks(user.id, new_unlocks, context)
            except Exception as e:
                logger.error(f"Error checking template unlocks: {e}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            error_traceback = traceback.format_exc()
            logger.error(f"Full traceback:\n{error_traceback}")
            
            # Check ADMIN_IDS specifically
            try:
                from config import OWNER_ADMIN_PROTECTION
                admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
                logger.error(f"DEBUG - ADMIN_IDS: {admin_ids}")
            except Exception as debug_err:
                logger.error(f"DEBUG - Error checking ADMIN_IDS: {debug_err}")
            
            if update.message:
                try:
                    error_responses = [
                        "⚠️ ওহহ! কিছু একটা গোলমাল হয়ে গেছে! আবার চেষ্টা করো 😅",
                        "😬 উফ! টেকনিক্যাল সমস্যা! একটু পরে আবার চেষ্টা করো",
                        "🤔 হুমম... কিছু একটা ঠিক নেই! আবার ট্রাই করো"
                    ]
                    await update.message.reply_text(
                        random.choice(error_responses),
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
    
    def _should_ignore_message(self, text: str) -> bool:
        """Check if message should be ignored"""
        # Check for only emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # Chinese char
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
            u"\ufe0f"  # dingbats
            u"\u3030"
                           "]+", flags=re.UNICODE)
        
        # Remove emojis and check if text is empty
        text_without_emojis = emoji_pattern.sub('', text).strip()
        if text_without_emojis == '':
            return True
        
        # Check for only numbers
        if text.strip().isdigit():
            return True
        
        # Check for links only
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text_without_urls = url_pattern.sub('', text).strip()
        if text_without_urls == '':
            return True
        
        # Check for very common single words
        common_single_words = ['হাই', 'হেলো', 'hello', 'hi', 'bye', 'বিদায়', 'ok', 'ঠিক', 'হ্যাঁ', 'না']
        if text.lower().strip() in common_single_words:
            return True
        
        return False
    
    async def _generate_roast_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     text: str, user: Any, chat: Any, target_user: Any = None,
                                     mood_analysis: Dict = None):
        """Generate and send roast response"""
        try:
            # Get roast content
            roast_data = await self.roast_engine.generate_roast(
                text, user, target_user
            )
            
            # Adjust based on mood if available
            if mood_analysis and self.mood_recognition:
                try:
                    roast_data = self.mood_recognition.adjust_roast_based_on_mood(
                        roast_data, mood_analysis
                    )
                except:
                    pass  # Continue without mood adjustment
            
            # Apply festival effects if active
            if self.festival_mode and self.festival_mode.is_festival_active():
                try:
                    festival_greeting = self.festival_mode.get_festival_greeting()
                    if festival_greeting:
                        roast_data["primary_roast"] = f"{festival_greeting}\n{roast_data['primary_roast']}"
                    
                    # Get festival template
                    festival_template = self.festival_mode.get_festival_template()
                    if festival_template:
                        roast_data["template_category"] = festival_template
                except:
                    pass  # Continue without festival effects
            
            # Generate image
            try:
                image_path = await self.image_gen.generate_roast_image(
                    roast_data, user, target_user
                )
            except Exception as img_error:
                logger.error(f"Error generating image: {img_error}")
                # Send text-only response
                caption = roast_data.get("caption", "কিছু একটা ভুল হয়েছে!")
                if "mood_note" in roast_data:
                    caption += f"\n\n{roast_data['mood_note']}"
                
                await update.message.reply_text(
                    caption,
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Apply festival effects to image
            if image_path and self.festival_mode and self.festival_mode.is_festival_active():
                try:
                    from PIL import Image
                    image = Image.open(image_path)
                    image = self.festival_mode.apply_festival_effects(image)
                    image.save(image_path, 'PNG', quality=95)
                except Exception as e:
                    logger.error(f"Error applying festival effects: {e}")
            
            # Update statistics
            self.stats["roasts_generated"] += 1
            self.stats["images_created"] += 1
            try:
                self.db.increment_roast_count(user.id)
            except:
                pass
            
            # Send response with image
            if update.message and image_path and os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as photo:
                        # Create inline keyboard for voting
                        keyboard = None
                        try:
                            keyboard = await self.voting_system.create_vote_keyboard(
                                update.update_id, user.id, chat.id
                            )
                        except:
                            pass  # Continue without voting keyboard
                        
                        # Prepare caption
                        caption = roast_data.get("caption", "")
                        
                        # Add mood note if available
                        if "mood_note" in roast_data:
                            caption += f"\n\n{roast_data['mood_note']}"
                        
                        # Add user mention if target
                        if target_user:
                            caption += f"\n\n🎯 টার্গেট: {target_user.first_name}"
                        
                        # Send photo with caption
                        await update.message.reply_photo(
                            photo=photo,
                            caption=caption[:1024],  # Telegram caption limit
                            reply_markup=keyboard,
                            parse_mode=ParseMode.HTML
                        )
                except Exception as send_error:
                    logger.error(f"Error sending photo: {send_error}")
                    # Fallback to text
                    await update.message.reply_text(
                        roast_data.get("caption", "কিছু একটা ভুল হয়েছে!"),
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup temporary file
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    pass
            elif update.message:
                # Fallback if image generation failed
                await update.message.reply_text(
                    roast_data.get("caption", "কিছু একটা ভুল হয়েছে!"),
                    parse_mode=ParseMode.HTML
                )
            
            # Record template usage
            try:
                self.db.record_template_usage(
                    roast_data.get("template_name", "default"),
                    user.id,
                    chat.id
                )
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error generating roast response: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback: {traceback_str}")
            
            if update.message:
                try:
                    await update.message.reply_text(
                        "⚠️ রোস্ট তৈরি করতে সমস্যা হচ্ছে! আবার চেষ্টা করো 😅",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
    
    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle vote callback queries"""
        try:
            await self.voting_system.handle_vote_callback(update, context)
        except Exception as e:
            logger.error(f"Error handling vote callback: {e}")
            try:
                await update.callback_query.answer("ভোট প্রসেস করতে সমস্যা হয়েছে!")
            except:
                pass
    
    async def handle_leaderboard_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle leaderboard callback queries"""
        try:
            await self.leaderboard.handle_leaderboard_callback(update, context)
        except Exception as e:
            logger.error(f"Error handling leaderboard callback: {e}")
            try:
                await update.callback_query.answer("লিডারবোর্ড লোড করতে সমস্যা হয়েছে!")
            except:
                pass
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        try:
            await self.welcome_system.handle_new_members(update, context)
        except Exception as e:
            logger.error(f"Error handling new chat members: {e}")
            # Send simple welcome message as fallback
            try:
                new_members = update.message.new_chat_members
                for member in new_members:
                    if member.id == context.bot.id:
                        await update.message.reply_text(
                            "ধন্যবাদ! আমাকে গ্রুপে অ্যাড করার জন্য! 🎉\n"
                            "আমি Roastify Bot - আপনার টেক্সটকে স্টাইলিশ রোস্টে রূপান্তর করি!\n\n"
                            "শুধু আমাকে কিছু লিখে পাঠান, আমি রোস্ট করে দেব! 😎",
                            parse_mode=ParseMode.HTML
                        )
                    else:
                        await update.message.reply_text(
                            f"স্বাগতম {member.first_name}! 🎉\n"
                            f"গ্রুপে রোস্টিং মজা উপভোগ করুন!",
                            parse_mode=ParseMode.HTML
                        )
            except:
                pass
    
    async def handle_left_chat_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when someone leaves the chat"""
        try:
            user = update.message.left_chat_member
            chat = update.effective_chat
            
            # Don't send goodbye if it's the bot itself
            if user.id == context.bot.id:
                return
            
            goodbye_messages = [
                f"👋 {user.first_name} চলে গেল! রোস্টের মজা আর পাবে না!",
                f"😢 {user.first_name} আমাদের ছেড়ে চলে গেল!",
                f"🚪 {user.first_name} দরজা বন্ধ করে চলে গেল!",
                f"🌅 বিদায় {user.first_name}! আবার আসবে আশা করি!",
                f"💨 {user.first_name} উড়াল দিল! শূন্যতা রয়ে গেল!",
                f"👋 বিদায় {user.first_name}! ভালো থেকো!"
            ]
            
            await update.message.reply_text(
                random.choice(goodbye_messages),
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error handling left chat member: {e}")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling update: {context.error}")
        traceback_str = traceback.format_exc()
        logger.error(f"Full traceback:\n{traceback_str}")
        
        # Try to notify user about error
        try:
            if update and hasattr(update, 'effective_message'):
                await update.effective_message.reply_text(
                    "😅 উফ! কিছু একটা গোলমাল হয়ে গেছে! আবার চেষ্টা করো।",
                    parse_mode=ParseMode.HTML
                )
        except:
            pass
    
    def setup_handlers(self, application: Application):
        """Setup all bot handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("leaderboard", self.leaderboard_command))
        application.add_handler(CommandHandler("unlocks", self.unlocks_command))
        application.add_handler(CommandHandler("quote", self.quote_command))
        application.add_handler(CommandHandler("mood", self.mood_command))
        application.add_handler(CommandHandler("forward", self.forward_command))
        application.add_handler(CommandHandler("share", self.share_command))
        
        # Admin commands (from admin protection)
        try:
            application.add_handler(CommandHandler("protect", 
                lambda u, c: self.admin_protection.handle_admin_command(u, c)))
            application.add_handler(CommandHandler("unprotect", 
                lambda u, c: self.admin_protection.handle_admin_command(u, c)))
            application.add_handler(CommandHandler("warnings", 
                lambda u, c: self.admin_protection.handle_admin_command(u, c)))
            application.add_handler(CommandHandler("resetwarnings", 
                lambda u, c: self.admin_protection.handle_admin_command(u, c)))
            application.add_handler(CommandHandler("protectedlist", 
                lambda u, c: self.admin_protection.handle_admin_command(u, c)))
        except:
            logger.warning("Admin protection handlers not available")
        
        # Message handlers
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
        
        # New chat members
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_chat_members
        ))
        
        # Left chat member
        application.add_handler(MessageHandler(
            filters.StatusUpdate.LEFT_CHAT_MEMBER, self.handle_left_chat_member
        ))
        
        # Callback query handlers
        application.add_handler(CallbackQueryHandler(self.handle_vote_callback, pattern="^vote_"))
        application.add_handler(CallbackQueryHandler(self.handle_leaderboard_callback, pattern="^leaderboard_"))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        logger.info("All handlers setup complete")
    
    async def post_init(self, application: Application):
        """Run after bot initialization"""
        logger.info(f"{self.bot_name} bot is starting up...")
        
        # Initialize job-based features
        try:
            self.auto_daily_quote = AutoDailyQuote(application.job_queue)
            logger.info("Auto Daily Quote system initialized")
        except Exception as e:
            logger.error(f"Error initializing Auto Daily Quote: {e}")
            self.auto_daily_quote = None
        
        # Start background tasks
        asyncio.create_task(self._background_tasks())
        
        # Send startup notification to owner
        await self._send_startup_notification()
        
        # Check for active festival
        try:
            festival = self.festival_mode.check_festival()
            if festival:
                logger.info(f"Active festival: {festival['name']}")
        except:
            pass
        
        logger.info("Bot startup complete - ALL systems operational")
    
    async def _background_tasks(self):
        """Run background maintenance tasks"""
        while True:
            try:
                # Cleanup old data every hour
                try:
                    self.db.cleanup_old_data(days=7)
                except:
                    pass
                
                # Backup database every 6 hours
                if datetime.now().hour % 6 == 0 and datetime.now().minute < 5:
                    backup_path = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    try:
                        self.db.backup_database(backup_path)
                    except:
                        pass
                
                # Update leaderboard cache every 30 minutes
                if datetime.now().minute % 30 == 0:
                    await self._update_leaderboard_cache()
                
                # Check for festival changes
                try:
                    self.festival_mode.check_festival()
                except:
                    pass
                
                # Record system stats daily at midnight
                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    await self._record_daily_stats()
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(300)  # Sleep 5 minutes on error
    
    async def _update_leaderboard_cache(self):
        """Update leaderboard cache"""
        try:
            leaderboard_types = ["most_roasted", "most_reacted", "most_votes"]
            for lb_type in leaderboard_types:
                data = self.db.get_leaderboard(lb_type, limit=20)
                self.db.cache_leaderboard(lb_type, data)
        except Exception as e:
            logger.error(f"Error updating leaderboard cache: {e}")
    
    async def _record_daily_stats(self):
        """Record daily system statistics"""
        try:
            stats = {
                "total_users": self.db.get_total_users(),
                "total_messages": self.stats["messages_processed"],
                "total_roasts": self.stats["roasts_generated"],
                "total_votes": self.db.get_total_votes(),
                "total_reactions": self.stats.get("reactions_sent", 0),
                "uptime_seconds": int((datetime.now() - self.stats["start_time"]).total_seconds()),
                "unique_users": len(self.stats["users_interacted_set"]),
                "unique_groups": len(self.stats["groups_managed_set"])
            }
            
            self.db.record_system_stats(stats)
            logger.info("Recorded daily system stats")
            
        except Exception as e:
            logger.error(f"Error recording daily stats: {e}")
    
    async def _send_startup_notification(self):
        """Send startup notification to owner"""
        try:
            from config import OWNER_ADMIN_PROTECTION
            owner_id = OWNER_ADMIN_PROTECTION["bot_owner_user_id"]
            
            bot_info = await self.application.bot.get_me()
            startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get system info
            try:
                import platform
                import psutil
                
                system_info = f"""
Platform: {platform.system()} {platform.release()}
Python: {platform.python_version()}
CPU: {psutil.cpu_count()} cores
Memory: {psutil.virtual_memory().total // (1024**3)} GB
                """
            except:
                system_info = "System info not available"
            
            message = f"""
🚀 <b>{self.bot_name} Started Successfully!</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot Username:</b> @{bot_info.username}
📊 <b>Version:</b> 3.0.0
━━━━━━━━━━━━━━━━━━━━
<b>System Info:</b>
{system_info}
━━━━━━━━━━━━━━━━━━━━
✅ <b>Status:</b> All {len(self.features)} features operational
🔥 <b>Ready for roasting!</b>
            """
            
            await self.application.bot.send_message(
                chat_id=owner_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            
            logger.info("Startup notification sent to owner")
        except Exception as e:
            logger.error(f"Error sending startup notification: {e}")
    
    async def shutdown(self):
        """Clean shutdown of the bot"""
        logger.info("Shutting down bot...")
        
        # Record final stats
        try:
            await self._record_daily_stats()
        except:
            pass
        
        # Close database connection
        try:
            self.db.close()
        except:
            pass
        
        # Cleanup temporary files
        self._cleanup_temp_files()
        
        logger.info("Bot shutdown complete")
    
    def _cleanup_temp_files(self):
        """Cleanup temporary files"""
        try:
            temp_files = glob.glob("temp/*.png") + glob.glob("temp/*.jpg") + glob.glob("temp/*.jpeg")
            for file in temp_files:
                try:
                    os.remove(file)
                except:
                    pass
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def run(self):
        """Run the bot"""
        try:
            # Create application
            self.application = Application.builder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Run bot
            logger.info(f"Starting {self.bot_name} bot...")
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error running bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            raise
        finally:
            # Ensure cleanup on exit
            try:
                asyncio.run(self.shutdown())
            except:
                pass


def main():
    """Main entry point"""
    # Check for bot token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Please set your bot token in config.py")
        sys.exit(1)
    
    # Create all directories
    directories = [
        "assets/fonts",
        "assets/borders", 
        "assets/templates",
        "assets/backgrounds",
        "data",
        "temp",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create default assets if missing
    create_default_assets()
    
    # Run bot
    bot = RoastifyBot()
    bot.run()


def create_default_assets():
    """Create default asset files if missing"""
    try:
        # Create sample font files list
        fonts_file = "assets/fonts/font_list.txt"
        if not os.path.exists(fonts_file):
            with open(fonts_file, "w", encoding="utf-8") as f:
                f.write("# Default font list\n")
                f.write("# Add your .ttf or .otf font files here\n")
                f.write("# Example: Kalpurush.ttf\n")
                f.write("# Download Bangla fonts from: https://www.omicronlab.com/bangla-fonts.html\n")
                f.write("\n# You can also use system fonts for English text\n")
        
        # Create sample borders list
        borders_file = "assets/borders/border_list.txt"
        if not os.path.exists(borders_file):
            with open(borders_file, "w", encoding="utf-8") as f:
                f.write("# Default border list\n")
                f.write("# Add your border images here (PNG recommended)\n")
                f.write("# Border images will be created automatically on first run\n")
        
        # Create templates configuration
        templates_file = "assets/templates/templates.json"
        if not os.path.exists(templates_file):
            default_templates = {
                "cartoon_roast": [
                    {"name": "cartoon_1", "style": "funny", "elements": ["bubble", "cartoon_bg"]},
                    {"name": "cartoon_2", "style": "sarcastic", "elements": ["speech_bubble", "colorful"]}
                ],
                "neon_savage": [
                    {"name": "neon_1", "style": "savage", "elements": ["neon_glow", "dark_bg"]},
                    {"name": "neon_2", "style": "bold", "elements": ["bright_neon", "grid"]}
                ],
                "basic": [
                    {"name": "basic_1", "style": "simple", "elements": ["clean", "minimal"]}
                ]
            }
            with open(templates_file, "w", encoding="utf-8") as f:
                json.dump(default_templates, f, indent=2, ensure_ascii=False)
        
        # Create data files
        data_files = [
            "data/daily_quotes.json",
            "data/unlockable_templates.json", 
            "data/mood_patterns.json",
            "data/privacy_patterns.json",
            "data/festivals.json"
        ]
        
        for file in data_files:
            if not os.path.exists(file):
                with open(file, "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=2, ensure_ascii=False)
        
        print("✅ Default assets created successfully!")
        print("📁 Please add Bangla fonts to assets/fonts/")
        print("🖼️ Add border images to assets/borders/ (or they will be auto-created)")
        print("🔧 Bot is ready to run!")
        print("🚀 Run: python bot.py")
        
    except Exception as e:
        print(f"⚠️ Error creating default assets: {e}")
        print("Continuing with bot startup...")


if __name__ == "__main__":
    main()
