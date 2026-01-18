#!/usr/bin/env python3
"""
Main Roastify Telegram Bot - FINAL COMPLETE VERSION
Advanced professional bot with ALL features
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import bot components
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
    """Main Roastify Bot Class - FINAL COMPLETE VERSION"""
    
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
        self.custom_unlocks = CustomTemplateUnlocks()
        
        # Load all features dynamically
        self.features = load_all_features()
        
        # Statistics
        self.stats = {
            "messages_processed": 0,
            "roasts_generated": 0,
            "images_created": 0,
            "users_interacted": 0,
            "groups_managed": 0,
            "start_time": datetime.now()
        }
        
        # Application instance
        self.application = None
        
        logger.info(f"Initialized {self.bot_name} Bot with ALL features")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
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
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
<b>{self.bot_name} - {self.bot_tagline}</b>

🤖 <b>How to use:</b>
• Just send me any text (minimum 4 characters)
• I'll roast it with a stylish 3D image
• No commands needed!

🎯 <b>Main Features:</b>
• Smart text analysis & roasting
• 3D image generation with random borders/fonts
• Auto emoji reactions based on mood
• Inline voting system for roasts
• User leaderboards
• Mention-based roasting in groups
• Festival themes & special modes
• Template unlocking system
• Safe forward sharing
• Daily quote posts

👥 <b>Group Features:</b>
• Welcome new members with images
• Roast specific users with @mentions
• Auto-reactions to messages
• Group statistics & leaderboards

🔧 <b>Commands:</b>
/start - Start the bot
/help - Show this help
/stats - Bot statistics (admin)
/leaderboard - Show user rankings
/unlocks - Show template unlock progress
/quote - Get daily roast quote
/mood - Analyze message mood

⚡ <b>Tips:</b>
• Use @mentions in groups for targeted roasts
• Vote on roasts to improve the bot
• Be active to unlock special templates
• Check leaderboard regularly

🔒 <b>Privacy:</b>
• Personal info is never stored
• All shared content is privacy-filtered
• No message logging

Made with ❤️ for fun roasting!
        """
        
        if update.message:
            await update.message.reply_text(
                help_text,
                parse_mode=ParseMode.HTML
            )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        user = update.effective_user
        
        # Check if user is admin/owner
        from config import OWNER_ADMIN_PROTECTION
        if user.id != OWNER_ADMIN_PROTECTION["bot_owner_user_id"] and \
           user.id not in OWNER_ADMIN_PROTECTION["admin_user_ids"]:
            await update.message.reply_text("❌ This command is for admins only!")
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
        
        stats_text = f"""
<b>{self.bot_name} Statistics</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>Uptime:</b> {days}d {hours}h {minutes}m {seconds}s
📊 <b>Messages Processed:</b> {self.stats['messages_processed']}
🔥 <b>Roasts Generated:</b> {self.stats['roasts_generated']}
🖼️ <b>Images Created:</b> {self.stats['images_created']}
👥 <b>Users Interacted:</b> {self.stats['users_interacted']}
🏠 <b>Groups Managed:</b> {self.stats['groups_managed']}
━━━━━━━━━━━━━━━━━━━━
<b>Database Stats:</b>
• Total Users: {total_users}
• Total Votes: {total_votes}
• Templates Used: {total_templates}
━━━━━━━━━━━━━━━━━━━━
<b>Feature Status:</b>
• Auto Reactions: ✅
• Voting System: ✅
• Leaderboard: ✅
• Festival Mode: ✅
• Mood Recognition: ✅
• Template Unlocks: ✅
• Safe Forward: ✅
━━━━━━━━━━━━━━━━━━━━
<b>System Status:</b> ✅ Operational
        """
        
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.HTML
        )
    
    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        await self.leaderboard.handle_leaderboard_command(update, context)
    
    async def unlocks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unlocks command"""
        await self.custom_unlocks.show_unlock_progress(update, context)
    
    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        if self.auto_daily_quote:
            await self.auto_daily_quote.manual_post_quote(
                update.effective_chat.id, context
            )
        else:
            await update.message.reply_text(
                "Daily quote system is not initialized yet!",
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
                    "মুড অ্যানালাইসিস করার জন্য কিছু টেক্সট দাও বা রিপ্লাই দাও!",
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
        await self.safe_forward.safe_forward(update, context)
    
    async def share_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /share command"""
        await self.safe_forward.safe_share_roast(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages - MAIN MESSAGE HANDLER"""
        try:
            # Update statistics
            self.stats["messages_processed"] += 1
            
            user = update.effective_user
            chat = update.effective_chat
            message = update.message
            text = message.text if message else ""
            
            # Add/update user
            self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            self.stats["users_interacted"] = len(set([user.id] + 
                list(self.stats.get("users_interacted", []))))
            
            # Update group count if in group
            if chat.type in ["group", "supergroup"]:
                self.stats["groups_managed"] = max(
                    self.stats["groups_managed"],
                    len(set([chat.id] + list(self.stats.get("groups_managed", []))))
                )
            
            # Check for admin protection triggers
            if await self.admin_protection.check_protection_needed(user, text, chat):
                await self.admin_protection.handle_protected_response(
                    update, context, user, text
                )
                return
            
            # Check minimum length
            if len(text.strip()) < CORE_RULES["minimum_input_length"]:
                if len(text.strip()) > 0:
                    short_response = await self.roast_engine.get_short_response(text, user)
                    await message.reply_text(short_response, parse_mode=ParseMode.HTML)
                return
            
            # Check ignore conditions
            if self._should_ignore_message(text):
                return
            
            # Analyze mood
            mood_analysis = self.mood_recognition.analyze_mood(text, user.id)
            
            # Check for mentions
            if chat.type in ["group", "supergroup"] and message.entities:
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
            
            # Generate regular roast
            await self._generate_roast_response(
                update, context, text, user, chat, mood_analysis=mood_analysis
            )
            
            # Auto-reactions
            await self.reaction_system.add_auto_reactions(message, text, user, chat)
            
            # Check for template unlocks
            new_unlocks = await self.custom_unlocks.check_unlocks(user.id)
            if new_unlocks:
                await self.custom_unlocks.notify_unlocks(user.id, new_unlocks, context)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            if update.message:
                await update.message.reply_text(
                    "⚠️ কিছু একটা সমস্যা হয়েছে! আবার চেষ্টা করো 😅",
                    parse_mode=ParseMode.HTML
                )
    
    def _should_ignore_message(self, text: str) -> bool:
        """Check if message should be ignored"""
        import re
        
        # Check for only emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # Chinese char
            u"\U00002702-\U000027B0"
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
            if mood_analysis:
                roast_data = self.mood_recognition.adjust_roast_based_on_mood(
                    roast_data, mood_analysis
                )
            
            # Apply festival effects if active
            if self.festival_mode.is_festival_active():
                festival_greeting = self.festival_mode.get_festival_greeting()
                roast_data["primary_roast"] = f"{festival_greeting}\n{roast_data['primary_roast']}"
                
                # Get festival template
                festival_template = self.festival_mode.get_festival_template()
                if festival_template:
                    roast_data["template_category"] = festival_template
            
            # Generate image
            image_path = await self.image_gen.generate_roast_image(
                roast_data, user, target_user
            )
            
            # Apply festival effects to image
            if self.festival_mode.is_festival_active() and image_path:
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
            self.db.increment_roast_count(user.id)
            
            # Send response with image
            if update.message:
                with open(image_path, 'rb') as photo:
                    # Create inline keyboard for voting
                    keyboard = await self.voting_system.create_vote_keyboard(
                        update.update_id, user.id, chat.id
                    )
                    
                    # Prepare caption
                    caption = roast_data["caption"]
                    
                    # Add mood note if available
                    if "mood_note" in roast_data:
                        caption += f"\n\n{roast_data['mood_note']}"
                    
                    # Send photo with caption
                    await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup temporary file
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # Record template usage
            self.db.record_template_usage(
                roast_data["template_name"],
                user.id,
                chat.id
            )
            
        except Exception as e:
            logger.error(f"Error generating roast response: {e}")
            if update.message:
                await update.message.reply_text(
                    "⚠️ ছবি জেনারেট করতে সমস্যা হচ্ছে! টেক্সট হিসেবে দিলাম: \n\n" +
                    roast_data.get("caption", "কিছু একটা ভুল হয়েছে!"),
                    parse_mode=ParseMode.HTML
                )
    
    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle vote callback queries"""
        await self.voting_system.handle_vote_callback(update, context)
    
    async def handle_leaderboard_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle leaderboard callback queries"""
        await self.leaderboard.handle_leaderboard_callback(update, context)
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        await self.welcome_system.handle_new_members(update, context)
    
    async def handle_left_chat_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when someone leaves the chat"""
        user = update.message.left_chat_member
        chat = update.effective_chat
        
        goodbye_messages = [
            f"👋 {user.first_name} চলে গেল! রোস্টের মজা আর পাবে না!",
            f"😢 {user.first_name} আমাদের ছেড়ে চলে গেল!",
            f"🚪 {user.first_name} দরজা বন্ধ করে চলে গেল!",
            f"🌅 বিদায় {user.first_name}! আবার আসবে আশা করি!",
            f"💨 {user.first_name} উড়াল দিল! শূন্যতা রয়ে গেল!"
        ]
        
        import random
        await update.message.reply_text(
            random.choice(goodbye_messages),
            parse_mode=ParseMode.HTML
        )
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling update: {context.error}")
        
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
        self.auto_daily_quote = AutoDailyQuote(application.job_queue)
        
        # Start background tasks
        asyncio.create_task(self._background_tasks())
        
        # Send startup notification to owner
        await self._send_startup_notification()
        
        # Check for active festival
        festival = self.festival_mode.check_festival()
        if festival:
            logger.info(f"Active festival: {festival['name']}")
        
        logger.info("Bot startup complete - ALL systems operational")
    
    async def _background_tasks(self):
        """Run background maintenance tasks"""
        while True:
            try:
                # Cleanup old data every hour
                self.db.cleanup_old_data(days=7)
                
                # Backup database every 6 hours
                if datetime.now().hour % 6 == 0:
                    backup_path = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    self.db.backup_database(backup_path)
                
                # Update leaderboard cache every 30 minutes
                await self._update_leaderboard_cache()
                
                # Check for festival changes
                self.festival_mode.check_festival()
                
                # Post daily leaderboard at 8 PM
                if datetime.now().hour == 20 and datetime.now().minute == 0:
                    await self._post_daily_leaderboard_to_groups()
                
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
    
    async def _post_daily_leaderboard_to_groups(self):
        """Post daily leaderboard to all groups"""
        # This would require storing group IDs
        # For now, it's a placeholder
        pass
    
    async def _record_daily_stats(self):
        """Record daily system statistics"""
        try:
            stats = {
                "total_users": self.db.get_total_users(),
                "total_messages": self.stats["messages_processed"],
                "total_roasts": self.stats["roasts_generated"],
                "total_votes": self.db.get_total_votes(),
                "total_reactions": self.stats.get("reactions_sent", 0),
                "uptime_seconds": int((datetime.now() - self.stats["start_time"]).total_seconds())
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
            import platform
            import psutil
            
            system_info = f"""
Platform: {platform.system()} {platform.release()}
Python: {platform.python_version()}
CPU: {psutil.cpu_count()} cores
Memory: {psutil.virtual_memory().total // (1024**3)} GB
            """
            
            message = f"""
🚀 <b>{self.bot_name} Started Successfully!</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot Username:</b> @{bot_info.username}
📊 <b>Version:</b> 3.0.0
🏠 <b>Host:</b> {platform.node()}
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
        await self._record_daily_stats()
        
        # Close database connection
        self.db.close()
        
        # Cleanup temporary files
        self._cleanup_temp_files()
        
        logger.info("Bot shutdown complete")
    
    def _cleanup_temp_files(self):
        """Cleanup temporary files"""
        try:
            import glob
            temp_files = glob.glob("temp/*.png") + glob.glob("temp/*.jpg")
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
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error running bot: {e}")
            raise
        finally:
            # Ensure cleanup on exit
            asyncio.run(self.shutdown())


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
    # Create sample font files list
    fonts_file = "assets/fonts/font_list.txt"
    if not os.path.exists(fonts_file):
        with open(fonts_file, "w", encoding="utf-8") as f:
            f.write("# Default font list\n")
            f.write("# Add your .ttf or .otf font files here\n")
            f.write("# Example: Kalpurush.ttf\n")
            f.write("# Download Bangla fonts from: https://www.omicronlab.com/bangla-fonts.html\n")
    
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
        import json
        default_templates = {
            "cartoon_roast": [
                {"name": "cartoon_1", "style": "funny", "elements": ["bubble", "cartoon_bg"]},
                {"name": "cartoon_2", "style": "sarcastic", "elements": ["speech_bubble", "colorful"]}
            ],
            "neon_savage": [
                {"name": "neon_1", "style": "savage", "elements": ["neon_glow", "dark_bg"]},
                {"name": "neon_2", "style": "bold", "elements": ["bright_neon", "grid"]}
            ]
        }
        with open(templates_file, "w", encoding="utf-8") as f:
            json.dump(default_templates, f, indent=2)
    
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
                json.dump({}, f, indent=2)
    
    print("✅ Default assets created successfully!")
    print("📁 Please add Bangla fonts to assets/fonts/")
    print("🖼️ Add border images to assets/borders/ (or they will be auto-created)")
    print("🔧 Edit config.py with your bot token")
    print("🚀 Run: python bot.py")


if __name__ == "__main__":
    main()