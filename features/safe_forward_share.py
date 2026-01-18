#!/usr/bin/env python3
"""
Safe Forward Share System for Roastify Bot
Safely forwards and shares content with privacy protection
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import EXTRA_FEATURES
    from utils.text_processor import TextProcessor
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class SafeForwardShare:
    """Manages safe forwarding and sharing of content"""
    
    def __init__(self):
        """Initialize safe forward share system"""
        self.config = EXTRA_FEATURES.get("safe_forward_share", {})
        self.text_processor = TextProcessor()
        
        # Privacy patterns to remove
        self.privacy_patterns = self._load_privacy_patterns()
        
        logger.info("Safe Forward Share system initialized")
    
    def _load_privacy_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for privacy-sensitive information"""
        patterns = {
            "phone_numbers": [
                r'\b\d{11}\b',  # Bangladeshi phone numbers
                r'\b\d{10}\b',  # Indian phone numbers
                r'\+\d{1,3}[\s-]?\d{5,15}',  # International numbers
                r'\b01\d{9}\b'  # Common BD format
            ],
            "email_addresses": [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            "personal_ids": [
                r'\b\d{10,12}\b',  # National ID numbers
                r'\b\d{16}\b',  # Credit card numbers (simplified)
                r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'  # Credit cards with separators
            ],
            "addresses": [
                r'\bhouse\s+no\.?\s*\d+',  # House numbers
                r'\broad\s+no\.?\s*\d+',  # Road numbers
                r'\bblock\s+[A-Z]\b',  # Block letters
                r'\bapartment\s+\d+\b',  # Apartment numbers
            ],
            "names": [
                # These would need context - handled differently
            ]
        }
        
        # Load from file if exists
        import os
        patterns_file = "data/privacy_patterns.json"
        if os.path.exists(patterns_file):
            try:
                import json
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    file_patterns = json.load(f)
                    patterns.update(file_patterns)
            except Exception as e:
                logger.error(f"Error loading privacy patterns: {e}")
        
        return patterns
    
    async def safe_forward(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Safely forward a message with privacy protection"""
        try:
            message = update.message
            
            # Check if message is a reply to forward
            if not message.reply_to_message:
                await message.reply_text(
                    "রিপ্লাই দিয়ে ফরওয়ার্ড করতে চাওয়া মেসেজ সিলেক্ট করো!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            source_message = message.reply_to_message
            
            # Check permissions
            if not await self._check_forward_permissions(message, source_message):
                await message.reply_text(
                    "❌ এই মেসেজ ফরওয়ার্ড করার পারমিশন নেই!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Process message for safe forwarding
            processed = await self._process_for_safe_forward(source_message)
            
            # Get target chat (from command arguments or current chat)
            target_chat = await self._get_target_chat(message, context)
            
            if not target_chat:
                await message.reply_text(
                    "❌ টার্গেট চ্যাট খুঁজে পাওয়া যায়নি!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Forward the processed message
            success = await self._forward_to_chat(processed, target_chat, context)
            
            if success:
                await message.reply_text(
                    "✅ মেসেজ সেফলি ফরওয়ার্ড করা হয়েছে!",
                    parse_mode=ParseMode.HTML
                )
                logger.info(f"Safe forwarded message to chat {target_chat.id}")
            else:
                await message.reply_text(
                    "❌ ফরওয়ার্ড করতে সমস্যা হয়েছে!",
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error in safe forward: {e}")
            await update.message.reply_text(
                "ফরওয়ার্ড করতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    async def _check_forward_permissions(self, message: Message, 
                                        source_message: Message) -> bool:
        """Check if user has permission to forward message"""
        try:
            user = message.from_user
            chat = message.chat
            
            # Check if user is admin in group
            if chat.type in ["group", "supergroup"]:
                member = await chat.get_member(user.id)
                if member.status not in ["administrator", "creator"]:
                    # Non-admins can only forward their own messages
                    if source_message.from_user.id != user.id:
                        return False
            
            # Check message age (prevent forwarding very old messages)
            message_age = (message.date - source_message.date).total_seconds()
            if message_age > 604800:  # 7 days
                # Can't forward messages older than 7 days
                return False
            
            # Check if message contains restricted content
            if await self._has_restricted_content(source_message):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking forward permissions: {e}")
            return False
    
    async def _has_restricted_content(self, message: Message) -> bool:
        """Check if message contains restricted content"""
        # Check text
        if message.text:
            text = message.text.lower()
            restricted_terms = [
                "পাসওয়ার্ড", "পাসওয়ার্ড", "secret", "confidential",
                "private", "গোপন", "রহস্য", "secret"
            ]
            
            for term in restricted_terms:
                if term in text:
                    return True
        
        # Check for documents/files
        if message.document or message.photo or message.video:
            # Don't allow forwarding of media files by default
            return True
        
        return False
    
    async def _process_for_safe_forward(self, message: Message) -> Dict[str, Any]:
        """Process message to remove privacy-sensitive information"""
        processed = {
            "original_message": message,
            "safe_text": "",
            "safe_caption": "",
            "media": None,
            "has_media": False,
            "forward_info_removed": False
        }
        
        # Process text
        if message.text:
            processed["safe_text"] = self._sanitize_text(message.text)
            processed["forward_info_removed"] = True
        
        # Process caption for media messages
        if message.caption:
            processed["safe_caption"] = self._sanitize_text(message.caption)
            processed["forward_info_removed"] = True
        
        # Handle media
        if message.photo:
            processed["media"] = message.photo[-1]  # Highest resolution
            processed["has_media"] = True
        elif message.video:
            processed["media"] = message.video
            processed["has_media"] = True
        elif message.document:
            # Only allow certain document types
            doc = message.document
            allowed_types = ['.txt', '.pdf', '.jpg', '.png', '.jpeg']
            if any(doc.file_name.endswith(ext) for ext in allowed_types):
                processed["media"] = doc
                processed["has_media"] = True
        
        # Add disclaimer
        disclaimer = "\n\n🔒 <i>প্রাইভেসি প্রোটেক্টেড - পার্সোনাল ইনফরমেশন রিমুভড</i>"
        
        if processed["safe_text"]:
            processed["safe_text"] += disclaimer
        elif processed["safe_caption"]:
            processed["safe_caption"] += disclaimer
        
        return processed
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text to remove privacy-sensitive information"""
        if not text:
            return ""
        
        sanitized = text
        
        # Remove privacy patterns
        for category, patterns in self.privacy_patterns.items():
            for pattern in patterns:
                try:
                    sanitized = re.sub(pattern, f"[{category.upper()} REMOVED]", 
                                     sanitized, flags=re.IGNORECASE)
                except:
                    pass
        
        # Remove @mentions (keep only the name part)
        sanitized = re.sub(r'@(\w+)', r'\1', sanitized)
        
        # Remove phone numbers (additional patterns)
        phone_patterns = [
            r'(\+?৮৮)?০১[৩-৯]\d{8}',  # Bengali numerals
            r'(\+?88)?01[3-9]\d{8}',   # English numerals
        ]
        
        for pattern in phone_patterns:
            sanitized = re.sub(pattern, '[PHONE REMOVED]', sanitized)
        
        # Remove email addresses
        sanitized = re.sub(r'\S+@\S+\.\S+', '[EMAIL REMOVED]', sanitized)
        
        # Remove potential location data
        location_indicators = [
            'location:', 'loc:', 'lat:', 'lon:', 'gps:', 'coordinates:'
        ]
        
        for indicator in location_indicators:
            if indicator in sanitized.lower():
                # Remove the entire line containing location data
                lines = sanitized.split('\n')
                lines = [line for line in lines if indicator not in line.lower()]
                sanitized = '\n'.join(lines)
        
        return sanitized.strip()
    
    async def _get_target_chat(self, message: Message, 
                              context: ContextTypes.DEFAULT_TYPE) -> Optional[Chat]:
        """Get target chat for forwarding"""
        try:
            # Check command arguments
            if context.args:
                target = context.args[0]
                
                # Check if it's a chat ID
                if target.lstrip('-').isdigit():
                    chat_id = int(target)
                    try:
                        return await context.bot.get_chat(chat_id)
                    except:
                        pass
                
                # Check if it's a username
                if target.startswith('@'):
                    try:
                        return await context.bot.get_chat(target)
                    except:
                        pass
            
            # Default to current chat
            return message.chat
            
        except Exception as e:
            logger.error(f"Error getting target chat: {e}")
            return None
    
    async def _forward_to_chat(self, processed: Dict, target_chat: Chat, 
                              context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Forward processed message to target chat"""
        try:
            if processed["has_media"] and processed["media"]:
                # Forward media with safe caption
                if processed["safe_caption"]:
                    caption = processed["safe_caption"]
                else:
                    caption = "🔒 সেফ শেয়ার্ড কন্টেন্ট"
                
                # Determine media type
                media = processed["media"]
                
                if hasattr(media, 'file_id'):  # Photo, Video, Document
                    if hasattr(media, 'width'):  # Photo
                        await context.bot.send_photo(
                            chat_id=target_chat.id,
                            photo=media.file_id,
                            caption=caption,
                            parse_mode=ParseMode.HTML
                        )
                    elif hasattr(media, 'duration'):  # Video
                        await context.bot.send_video(
                            chat_id=target_chat.id,
                            video=media.file_id,
                            caption=caption,
                            parse_mode=ParseMode.HTML
                        )
                    else:  # Document
                        await context.bot.send_document(
                            chat_id=target_chat.id,
                            document=media.file_id,
                            caption=caption,
                            parse_mode=ParseMode.HTML
                        )
                
                return True
                
            else:
                # Forward text only
                if processed["safe_text"]:
                    text = processed["safe_text"]
                else:
                    text = "🔒 প্রাইভেসি প্রোটেক্টেড মেসেজ"
                
                await context.bot.send_message(
                    chat_id=target_chat.id,
                    text=text,
                    parse_mode=ParseMode.HTML
                )
                
                return True
            
        except Exception as e:
            logger.error(f"Error forwarding to chat: {e}")
            return False
    
    async def safe_share_roast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Safely share a roast with other users"""
        try:
            message = update.message
            
            # Check if message is a reply to a roast
            if not message.reply_to_message:
                await message.reply_text(
                    "শেয়ার করতে চাওয়া রোস্ট মেসেজে রিপ্লাই দাও!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            roast_message = message.reply_to_message
            
            # Check if it's actually a roast message
            if not await self._is_roast_message(roast_message):
                await message.reply_text(
                    "এটি রোস্ট মেসেজ নয়! শুধু রোস্ট মেসেজ শেয়ার করা যায়।",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Process roast for sharing
            share_data = await self._prepare_roast_for_sharing(roast_message)
            
            # Get share target
            target_info = await self._get_share_target(message, context)
            
            if not target_info:
                await message.reply_text(
                    "শেয়ার টার্গেট স্পেসিফাই করো! (ইউজারনেম বা রিপ্লাই)",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Share the roast
            success = await self._share_roast(share_data, target_info, context)
            
            if success:
                await message.reply_text(
                    f"✅ রোস্ট {target_info['type']} এ শেয়ার করা হয়েছে!",
                    parse_mode=ParseMode.HTML
                )
                logger.info(f"Shared roast to {target_info['target']}")
            else:
                await message.reply_text(
                    "❌ শেয়ার করতে সমস্যা হয়েছে!",
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error in safe share roast: {e}")
            await update.message.reply_text(
                "শেয়ার করতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    async def _is_roast_message(self, message: Message) -> bool:
        """Check if message is a roast message"""
        # Check if message has photo (roasts always have images)
        if not message.photo:
            return False
        
        # Check caption for roast indicators
        if message.caption:
            caption = message.caption.lower()
            roast_indicators = ["রোস্ট", "roast", "🔥", "😈", "রোস্টিফাই"]
            
            for indicator in roast_indicators:
                if indicator in caption:
                    return True
        
        return False
    
    async def _prepare_roast_for_sharing(self, message: Message) -> Dict[str, Any]:
        """Prepare roast message for sharing"""
        # Get the roast image
        roast_photo = message.photo[-1] if message.photo else None
        
        # Process caption
        original_caption = message.caption or ""
        
        # Remove user-specific information
        safe_caption = self._sanitize_roast_caption(original_caption)
        
        # Add share attribution
        share_note = "\n\n🔄 <i>রোস্টিফাই থেকে শেয়ার্ড</i>"
        safe_caption += share_note
        
        return {
            "photo": roast_photo,
            "caption": safe_caption,
            "original_message_id": message.message_id,
            "original_chat_id": message.chat.id
        }
    
    def _sanitize_roast_caption(self, caption: str) -> str:
        """Sanitize roast caption for sharing"""
        if not caption:
            return ""
        
        # Remove user IDs and specific mentions
        lines = caption.split('\n')
        safe_lines = []
        
        for line in lines:
            # Remove lines with user IDs
            if any(keyword in line.lower() for keyword in ["user:", "id:", "user_id"]):
                continue
            
            # Remove specific mention patterns
            if '@' in line and any(term in line.lower() for term in ['mention', 'target']):
                continue
            
            # Keep the line
            safe_lines.append(line)
        
        return '\n'.join(safe_lines)
    
    async def _get_share_target(self, message: Message, 
                               context: ContextTypes.DEFAULT_TYPE) -> Optional[Dict]:
        """Get target for sharing"""
        try:
            # Check if replying to a user's message
            if message.reply_to_message and message.reply_to_message.from_user:
                target_user = message.reply_to_message.from_user
                return {
                    "type": "user",
                    "target": target_user.id,
                    "name": target_user.first_name
                }
            
            # Check command arguments
            if context.args:
                target = context.args[0]
                
                # Check if it's a user ID
                if target.isdigit():
                    user_id = int(target)
                    try:
                        user = await context.bot.get_chat(user_id)
                        return {
                            "type": "user",
                            "target": user.id,
                            "name": user.first_name
                        }
                    except:
                        pass
                
                # Check if it's a username
                if target.startswith('@'):
                    try:
                        user = await context.bot.get_chat(target)
                        return {
                            "type": "user",
                            "target": user.id,
                            "name": user.first_name
                        }
                    except:
                        pass
                
                # Check if it's a group/channel
                if target.startswith('-') or target.startswith('@'):
                    try:
                        chat = await context.bot.get_chat(target)
                        return {
                            "type": "chat",
                            "target": chat.id,
                            "name": chat.title
                        }
                    except:
                        pass
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting share target: {e}")
            return None
    
    async def _share_roast(self, share_data: Dict, target_info: Dict, 
                          context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Share roast to target"""
        try:
            if share_data["photo"]:
                await context.bot.send_photo(
                    chat_id=target_info["target"],
                    photo=share_data["photo"].file_id,
                    caption=share_data["caption"],
                    parse_mode=ParseMode.HTML
                )
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error sharing roast: {e}")
            return False
    
    def add_privacy_pattern(self, category: str, pattern: str) -> bool:
        """Add custom privacy pattern"""
        try:
            if category not in self.privacy_patterns:
                self.privacy_patterns[category] = []
            
            self.privacy_patterns[category].append(pattern)
            
            # Save to file
            import json
            patterns_file = "data/privacy_patterns.json"
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.privacy_patterns, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Added privacy pattern for category: {category}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding privacy pattern: {e}")
            return False
    
    def get_privacy_stats(self) -> Dict[str, Any]:
        """Get privacy system statistics"""
        total_patterns = sum(len(patterns) for patterns in self.privacy_patterns.values())
        
        return {
            "total_pattern_categories": len(self.privacy_patterns),
            "total_patterns": total_patterns,
            "categories": list(self.privacy_patterns.keys()),
            "patterns_per_category": {
                category: len(patterns) 
                for category, patterns in self.privacy_patterns.items()
            }
        }