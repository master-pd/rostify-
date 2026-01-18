#!/usr/bin/env python3
"""
Admin Protection System for Roastify Bot
Protects owner and admins from abusive messages
"""

import logging
import re
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import OWNER_ADMIN_PROTECTION
    from database import get_database
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class AdminProtection:
    """Protects bot owner and admins from abuse"""
    
    def __init__(self):
        """Initialize admin protection system"""
        self.config = OWNER_ADMIN_PROTECTION
        self.db = get_database()
        
        # Track protected users
        self.protected_users = set()
        self.protected_users.add(self.config["bot_owner_user_id"])
        self.protected_users.update(self.config["admin_user_ids"])
        
        # Cooldown tracking for protected responses
        self.response_cooldowns = {}  # user_id -> timestamp
        
        # Abusive message tracking
        self.abuse_warnings = {}  # user_id -> warning_count
        
        logger.info(f"Admin Protection initialized for {len(self.protected_users)} users")
    
    async def check_protection_needed(self, user: Any, text: str, chat: Any) -> bool:
        """Check if protection is needed for a message"""
        try:
            # Check if user is protected
            if user.id not in self.protected_users:
                return False
            
            # Check if message contains trigger conditions
            text_lower = text.lower()
            
            for trigger in self.config["trigger_conditions"]:
                if trigger in text_lower:
                    logger.info(f"Protection triggered for user {user.id}: {trigger}")
                    return True
            
            # Check for abusive patterns
            if self._contains_abusive_patterns(text):
                logger.info(f"Abusive pattern detected for user {user.id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking protection: {e}")
            return False
    
    def _contains_abusive_patterns(self, text: str) -> bool:
        """Check for abusive language patterns"""
        text_lower = text.lower()
        
        # Common abusive patterns (Bengali)
        abusive_patterns = [
            r'বোকা', r'গাধা', r'হাঁদা', r'নষ্ট', r'খারাপ',
            r'ভালো নয়', r'অপছন্দ', r'ঘৃণা', r'শত্রু'
        ]
        
        for pattern in abusive_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Check for excessive negativity
        negative_words = ['না', 'নেই', 'খারাপ', 'ভুল', 'ত্রুটি', 'সমস্যা']
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count >= 3:
            return True
        
        return False
    
    async def handle_protected_response(self, update: Update, 
                                        context: ContextTypes.DEFAULT_TYPE,
                                        user: Any, text: str):
        """Handle response for protected user messages"""
        try:
            # Check cooldown
            if self._check_response_cooldown(user.id):
                logger.debug(f"Response cooldown active for user {user.id}")
                return
            
            # Get appropriate response based on context
            response = await self._get_protected_response(user, text)
            
            # Send response
            if update.message:
                await update.message.reply_text(
                    response,
                    parse_mode="HTML"
                )
            
            # Update cooldown
            self._update_response_cooldown(user.id)
            
            # Track warning
            self._track_warning(user.id)
            
            logger.info(f"Sent protected response to user {user.id}")
            
        except Exception as e:
            logger.error(f"Error handling protected response: {e}")
    
    async def _get_protected_response(self, user: Any, text: str) -> str:
        """Get appropriate response for protected user"""
        import random
        
        # Different response types based on tone
        tone = self.config["roast_tone"]
        
        if "Funny" in tone:
            responses = [
                f"ওহো {user.first_name}! এত রাগ দেখাচ্ছ কেন? 😅\n"
                "রাগ করলে রোস্ট আরও শক্ত হবে! 😈",
                
                f"শান্ত হও {user.first_name}! 😊\n"
                "রাগ নয়, রোস্ট খাও! আবার চেষ্টা করো!",
                
                f"হুম... {user.first_name} মেজাজ দেখাচ্ছ! 😏\n"
                "ভালো কথা বললে ভালো রোস্ট পাবে!",
                
                f"এত চাপ নিও না {user.first_name}! 🌟\n"
                "হাসি খুশি থাকো, রোস্ট মজা নাও!",
                
                f"কথাগুলো একটু নরম করে বলো {user.first_name}! 🤗\n"
                "শান্তভাবে বললে আমি ভালো বুঝব!"
            ]
        
        elif "Safe" in tone:
            responses = [
                f"দেখি {user.first_name}, কথা একটু শান্তভাবে বলো। 😊",
                
                f"রাগ নয় {user.first_name}, ভালো ব্যবহার করো। 👍",
                
                f"কথাগুলো ভেবে চিন্তে বলো {user.first_name}। 🤔",
                
                f"শান্তভাবে বললে আমি সহজে বুঝতে পারব {user.first_name}। ✨",
                
                f"আমি তোমাকে সাহায্য করতে চাই {user.first_name}। "
                "কথাগুলো ভালোভাবে বলো। ❤️"
            ]
        
        else:
            # Mixed tone
            responses = [
                f"ওহ {user.first_name}! রাগ করছ? 😅 চিন্তা নেই, "
                "আমি সব বুঝি! আবার বলো ভালো করে!",
                
                f"হাসি খুশি থাকো {user.first_name}! 🌟 "
                "ভালো কথা বললে ভালো উত্তর পাবে!",
                
                f"রাগ করলে রোস্ট বাড়বে {user.first_name}! 😈 "
                "শান্ত হও, মজা নাও!",
                
                f"কথাগুলো একটু মিষ্টি করে বলো {user.first_name}! 🍬 "
                "তাহলে আমি ভালো বুঝব!"
            ]
        
        # Check warning level
        warning_count = self.abuse_warnings.get(user.id, 0)
        
        if warning_count >= 3:
            # Serious warning
            serious_responses = [
                f"⚠️ <b>সতর্কতা!</b> {user.first_name}, "
                "তুমি বারবার রাগ দেখাচ্ছ! শেষ সতর্কতা!",
                
                f"⛔ {user.first_name}, অপব্যবহার বন্ধ করো! "
                "না হলে ব্যবস্থা নেওয়া হবে!"
            ]
            responses = serious_responses
        
        return random.choice(responses)
    
    def _check_response_cooldown(self, user_id: int) -> bool:
        """Check if response cooldown is active"""
        cooldown_seconds = self.config.get("cooldown_seconds", 120)
        
        if user_id in self.response_cooldowns:
            last_time = self.response_cooldowns[user_id]
            time_diff = (datetime.now() - last_time).total_seconds()
            
            if time_diff < cooldown_seconds:
                return True
        
        return False
    
    def _update_response_cooldown(self, user_id: int):
        """Update response cooldown timestamp"""
        self.response_cooldowns[user_id] = datetime.now()
        
        # Clean old cooldowns
        self._clean_old_cooldowns()
    
    def _clean_old_cooldowns(self):
        """Clean old cooldown entries"""
        current_time = datetime.now()
        old_users = []
        
        for user_id, last_time in self.response_cooldowns.items():
            time_diff = (current_time - last_time).total_seconds()
            if time_diff > 3600:  # 1 hour
                old_users.append(user_id)
        
        for user_id in old_users:
            del self.response_cooldowns[user_id]
    
    def _track_warning(self, user_id: int):
        """Track warning for abusive behavior"""
        if user_id not in self.abuse_warnings:
            self.abuse_warnings[user_id] = 0
        
        self.abuse_warnings[user_id] += 1
        
        # Reset warnings after 24 hours
        # In production, this should be in database with timestamps
        
        logger.info(f"Warning #{self.abuse_warnings[user_id]} for user {user_id}")
    
    def reset_warnings(self, user_id: int) -> bool:
        """Reset warnings for a user"""
        if user_id in self.abuse_warnings:
            del self.abuse_warnings[user_id]
            logger.info(f"Reset warnings for user {user_id}")
            return True
        return False
    
    def get_warning_count(self, user_id: int) -> int:
        """Get warning count for a user"""
        return self.abuse_warnings.get(user_id, 0)
    
    async def add_protected_user(self, user_id: int) -> bool:
        """Add user to protected list"""
        try:
            self.protected_users.add(user_id)
            
            # Update config if persistent storage needed
            # For now, it's runtime only
            
            logger.info(f"Added user {user_id} to protected list")
            return True
            
        except Exception as e:
            logger.error(f"Error adding protected user: {e}")
            return False
    
    async def remove_protected_user(self, user_id: int) -> bool:
        """Remove user from protected list"""
        try:
            if user_id == self.config["bot_owner_user_id"]:
                logger.warning("Cannot remove bot owner from protected list")
                return False
            
            if user_id in self.protected_users:
                self.protected_users.remove(user_id)
                logger.info(f"Removed user {user_id} from protected list")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error removing protected user: {e}")
            return False
    
    def is_user_protected(self, user_id: int) -> bool:
        """Check if user is protected"""
        return user_id in self.protected_users
    
    async def handle_admin_command(self, update: Update, 
                                   context: ContextTypes.DEFAULT_TYPE):
        """Handle admin-only commands"""
        try:
            user = update.effective_user
            
            # Check if user is admin
            if not self.is_user_protected(user.id):
                await update.message.reply_text(
                    "❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!",
                    parse_mode="HTML"
                )
                return
            
            # Parse command
            command = update.message.text.split()[0].lower()
            
            if command == "/protect":
                await self._handle_protect_command(update, context)
            elif command == "/unprotect":
                await self._handle_unprotect_command(update, context)
            elif command == "/warnings":
                await self._handle_warnings_command(update, context)
            elif command == "/resetwarnings":
                await self._handle_reset_warnings_command(update, context)
            elif command == "/protectedlist":
                await self._handle_protected_list_command(update, context)
            
        except Exception as e:
            logger.error(f"Error handling admin command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    async def _handle_protect_command(self, update: Update, 
                                      context: ContextTypes.DEFAULT_TYPE):
        """Handle /protect command"""
        try:
            # Get mentioned user or reply target
            target_user = None
            
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
            elif context.args:
                # Parse user ID from args
                try:
                    user_id = int(context.args[0])
                    # Fetch user info (simplified)
                    target_user = type('obj', (object,), {'id': user_id, 'first_name': f'User_{user_id}'})
                except ValueError:
                    await update.message.reply_text(
                        "❌ ভুল ইউজার আইডি!",
                        parse_mode="HTML"
                    )
                    return
            
            if not target_user:
                await update.message.reply_text(
                    "❌ ইউজার mention করো বা রিপ্লাই দাও!",
                    parse_mode="HTML"
                )
                return
            
            # Add to protected list
            success = await self.add_protected_user(target_user.id)
            
            if success:
                await update.message.reply_text(
                    f"✅ {target_user.first_name} কে প্রটেক্টেড লিস্টে যোগ করা হলো!",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text(
                    f"❌ {target_user.first_name} কে প্রটেক্টেড লিস্টে যোগ করতে সমস্যা!",
                    parse_mode="HTML"
                )
                
        except Exception as e:
            logger.error(f"Error handling protect command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    async def _handle_unprotect_command(self, update: Update, 
                                        context: ContextTypes.DEFAULT_TYPE):
        """Handle /unprotect command"""
        try:
            # Similar to protect command but remove
            target_user = None
            
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
            elif context.args:
                try:
                    user_id = int(context.args[0])
                    target_user = type('obj', (object,), {'id': user_id, 'first_name': f'User_{user_id}'})
                except ValueError:
                    await update.message.reply_text(
                        "❌ ভুল ইউজার আইডি!",
                        parse_mode="HTML"
                    )
                    return
            
            if not target_user:
                await update.message.reply_text(
                    "❌ ইউজার mention করো বা রিপ্লাই দাও!",
                    parse_mode="HTML"
                )
                return
            
            # Remove from protected list
            success = await self.remove_protected_user(target_user.id)
            
            if success:
                await update.message.reply_text(
                    f"✅ {target_user.first_name} কে প্রটেক্টেড লিস্ট থেকে সরানো হলো!",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text(
                    f"❌ {target_user.first_name} কে প্রটেক্টেড লিস্ট থেকে সরাতে সমস্যা!",
                    parse_mode="HTML"
                )
                
        except Exception as e:
            logger.error(f"Error handling unprotect command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    async def _handle_warnings_command(self, update: Update, 
                                       context: ContextTypes.DEFAULT_TYPE):
        """Handle /warnings command"""
        try:
            target_user = None
            
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
            elif context.args:
                try:
                    user_id = int(context.args[0])
                    target_user = type('obj', (object,), {'id': user_id, 'first_name': f'User_{user_id}'})
                except ValueError:
                    await update.message.reply_text(
                        "❌ ভুল ইউজার আইডি!",
                        parse_mode="HTML"
                    )
                    return
            else:
                # Show current user's warnings
                target_user = update.effective_user
            
            warning_count = self.get_warning_count(target_user.id)
            
            if warning_count == 0:
                message = f"✅ {target_user.first_name} এর কোনো সতর্কতা নেই!"
            else:
                message = (
                    f"⚠️ <b>সতর্কতা রিপোর্ট</b>\n\n"
                    f"👤 <b>ইউজার:</b> {target_user.first_name}\n"
                    f"📊 <b>সতর্কতা সংখ্যা:</b> {warning_count}\n\n"
                )
                
                if warning_count >= 3:
                    message += "🚨 <b>গুরুতর সতর্কতা!</b> ব্যবস্থা নেওয়া প্রয়োজন!"
                elif warning_count == 2:
                    message += "⚠️ দ্বিতীয় সতর্কতা! সাবধান!"
                else:
                    message += "ℹ️ প্রথম সতর্কতা। মনোযোগ দাও!"
            
            await update.message.reply_text(
                message,
                parse_mode="HTML"
            )
            
        except Exception as e:
            logger.error(f"Error handling warnings command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    async def _handle_reset_warnings_command(self, update: Update, 
                                             context: ContextTypes.DEFAULT_TYPE):
        """Handle /resetwarnings command"""
        try:
            target_user = None
            
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
            elif context.args:
                try:
                    user_id = int(context.args[0])
                    target_user = type('obj', (object,), {'id': user_id, 'first_name': f'User_{user_id}'})
                except ValueError:
                    await update.message.reply_text(
                        "❌ ভুল ইউজার আইডি!",
                        parse_mode="HTML"
                    )
                    return
            else:
                await update.message.reply_text(
                    "❌ ইউজার mention করো বা রিপ্লাই দাও!",
                    parse_mode="HTML"
                )
                return
            
            success = self.reset_warnings(target_user.id)
            
            if success:
                await update.message.reply_text(
                    f"✅ {target_user.first_name} এর সব সতর্কতা রিসেট করা হলো!",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text(
                    f"ℹ️ {target_user.first_name} এর কোনো সতর্কতা নেই!",
                    parse_mode="HTML"
                )
                
        except Exception as e:
            logger.error(f"Error handling reset warnings command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    async def _handle_protected_list_command(self, update: Update, 
                                             context: ContextTypes.DEFAULT_TYPE):
        """Handle /protectedlist command"""
        try:
            if not self.protected_users:
                await update.message.reply_text(
                    "ℹ️ কোনো প্রটেক্টেড ইউজার নেই!",
                    parse_mode="HTML"
                )
                return
            
            # Format protected users list
            user_list = []
            for user_id in sorted(self.protected_users):
                if user_id == self.config["bot_owner_user_id"]:
                    user_list.append(f"👑 Owner: {user_id}")
                else:
                    user_list.append(f"🛡️ Admin: {user_id}")
            
            message = (
                f"🛡️ <b>প্রটেক্টেড ইউজার লিস্ট</b>\n\n"
                f"মোট: {len(self.protected_users)} জন\n\n"
            )
            message += "\n".join(user_list)
            
            await update.message.reply_text(
                message,
                parse_mode="HTML"
            )
            
        except Exception as e:
            logger.error(f"Error handling protected list command: {e}")
            await update.message.reply_text(
                "কমান্ড প্রসেস করতে সমস্যা! 😢",
                parse_mode="HTML"
            )
    
    def get_protection_stats(self) -> Dict[str, Any]:
        """Get protection system statistics"""
        return {
            "protected_users_count": len(self.protected_users),
            "active_warnings": len(self.abuse_warnings),
            "total_warnings": sum(self.abuse_warnings.values()),
            "active_cooldowns": len(self.response_cooldowns),
            "bot_owner_id": self.config["bot_owner_user_id"],
            "admin_ids": list(self.config["admin_user_ids"])
        }
    
    async def cleanup_old_data(self):
        """Cleanup old protection data"""
        try:
            # Clean old cooldowns
            self._clean_old_cooldowns()
            
            # For production, warnings should have timestamps
            # and be cleaned based on age
            
            logger.debug("Cleaned protection system data")
            
        except Exception as e:
            logger.error(f"Error cleaning protection data: {e}")