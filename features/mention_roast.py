#!/usr/bin/env python3
"""
Mention Roast System for Roastify Bot
Handles @mentions in groups for targeted roasting
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from telegram import Update, Message, User
from telegram.ext import ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import MENTION_TARGETED_ROAST
    from database import get_database
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class MentionRoast:
    """Manages mention-based roasting in groups"""
    
    def __init__(self):
        """Initialize mention roast system"""
        self.config = MENTION_TARGETED_ROAST
        self.db = get_database()
        
        # Track recent mention roasts to prevent spam
        self.recent_mentions = {}  # (user_id, target_id) -> timestamp
        
        logger.info("Mention Roast System initialized")
    
    async def process_mention(self, message: Message, text: str, 
                             sender: User, chat: Any) -> Optional[Dict]:
        """Process message for mentions and prepare roast"""
        try:
            # Check if mention roasting is enabled
            if not self.config["enabled"]:
                return None
            
            # Check chat type
            allowed_chats = self.config["trigger_conditions"]["chat_type"]
            if chat.type not in allowed_chats:
                return None
            
            # Check minimum length
            min_length = self.config["trigger_conditions"]["minimum_input_length"]
            if len(text.strip()) < min_length:
                return None
            
            # Check if mention is required
            if self.config["trigger_conditions"]["mention_required"]:
                if not message.entities:
                    return None
            
            # Extract mentioned users
            mentioned_users = self._extract_mentioned_users(message, sender)
            
            if not mentioned_users:
                return None
            
            # Apply target logic
            target_user = self._select_target_user(mentioned_users, sender, chat)
            
            if not target_user:
                return None
            
            # Check cooldown
            if self._check_mention_cooldown(sender.id, target_user.id):
                logger.debug(f"Mention cooldown active for {sender.id} -> {target_user.id}")
                return None
            
            # Update cooldown
            self._update_mention_cooldown(sender.id, target_user.id)
            
            # Prepare roast data
            roast_data = {
                "target": target_user,
                "mentioned_users": mentioned_users,
                "original_text": text,
                "is_mention_roast": True
            }
            
            logger.info(f"Mention roast prepared: {sender.id} -> {target_user.id}")
            return roast_data
            
        except Exception as e:
            logger.error(f"Error processing mention: {e}")
            return None
    
    def _extract_mentioned_users(self, message: Message, sender: User) -> List[User]:
        """Extract mentioned users from message entities"""
        mentioned_users = []
        
        if not message.entities:
            return mentioned_users
        
        for entity in message.entities:
            if entity.type == "mention":
                # Extract username from text
                username = message.text[entity.offset:entity.offset + entity.length]
                # We'll need the actual User object, which requires fetching
                # For now, we'll handle this in the calling function
                pass
            elif entity.type == "text_mention":
                # Entity has user information
                if entity.user:
                    mentioned_users.append(entity.user)
        
        # Also check for @mentions in text (fallback)
        if not mentioned_users:
            # Parse @mentions from text
            mention_pattern = r'@(\w+)'
            mentions = re.findall(mention_pattern, message.text or "")
            
            # Note: To get User objects for these, we need to fetch from chat
            # This is simplified - in production, fetch user info
        
        return mentioned_users
    
    def _select_target_user(self, mentioned_users: List[User], 
                           sender: User, chat: Any) -> Optional[User]:
        """Select target user based on configuration rules"""
        target_logic = self.config["target_logic"]
        selected_target = None
        
        # Get target selection logic
        target_type = target_logic.get("target_user", "mentioned_user")
        
        if target_type == "mentioned_user":
            # Select first mentioned user
            if mentioned_users:
                selected_target = mentioned_users[0]
        
        elif target_type == "random_mentioned":
            # Select random mentioned user
            import random
            if mentioned_users:
                selected_target = random.choice(mentioned_users)
        
        # Apply exclusions
        if selected_target:
            # Exclude sender if configured
            if target_logic.get("exclude_sender", True) and selected_target.id == sender.id:
                return None
            
            # Exclude bots if configured
            if target_logic.get("exclude_bot", True) and selected_target.is_bot:
                return None
            
            # Exclude self-mention (bot mentioning itself)
            if target_logic.get("exclude_self_mention", True):
                # Check if bot is mentioned
                from config import BOT_TOKEN
                # We need bot's own user info here
                # This check should be done in the calling context
        
        return selected_target
    
    def _check_mention_cooldown(self, sender_id: int, target_id: int) -> bool:
        """Check if mention cooldown is active"""
        key = (sender_id, target_id)
        
        if key in self.recent_mentions:
            import time
            last_time = self.recent_mentions[key]
            current_time = time.time()
            
            # Cooldown of 60 seconds
            if current_time - last_time < 60:
                return True
        
        return False
    
    def _update_mention_cooldown(self, sender_id: int, target_id: int):
        """Update mention cooldown timestamp"""
        import time
        key = (sender_id, target_id)
        self.recent_mentions[key] = time.time()
        
        # Clean old entries (older than 5 minutes)
        current_time = time.time()
        old_keys = [k for k, v in self.recent_mentions.items() 
                   if current_time - v > 300]
        
        for key in old_keys:
            del self.recent_mentions[key]
    
    async def generate_mention_roast(self, roast_data: Dict, 
                                     sender: User) -> Dict:
        """Generate special roast for mentioned user"""
        try:
            target_user = roast_data["target"]
            original_text = roast_data["original_text"]
            
            # Remove mentions from text for analysis
            cleaned_text = self._remove_mentions(original_text)
            
            # Generate roast based on mention context
            roast_content = self._get_mention_roast_content(
                cleaned_text, sender, target_user
            )
            
            # Add mention-specific elements
            roast_content["is_mention_roast"] = True
            roast_content["target_user"] = target_user
            roast_content["sender"] = sender
            
            # Set appropriate template
            roast_content["template_category"] = self._select_mention_template(
                cleaned_text, sender, target_user
            )
            
            return roast_content
            
        except Exception as e:
            logger.error(f"Error generating mention roast: {e}")
            # Fallback to regular roast
            return await self._get_fallback_roast(sender, target_user)
    
    def _remove_mentions(self, text: str) -> str:
        """Remove @mentions from text"""
        # Remove @username mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove bot command mentions
        text = re.sub(r'/[\w@]+', '', text)
        
        # Clean up extra spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _get_mention_roast_content(self, text: str, sender: User, 
                                  target: User) -> Dict:
        """Get roast content for mention context"""
        import random
        
        # Get sender and target names
        sender_name = f"@{sender.username}" if sender.username else sender.first_name
        target_name = f"@{target.username}" if target.username else target.first_name
        
        # Mention-specific roast templates
        mention_roasts = [
            {
                "primary": f"{sender_name} তো {target_name}কে টার্গেট করেই বসে আছে! 😏",
                "secondary": "এবার পালা রোস্ট খাওয়ার! ধৈর্য ধরো!",
                "emoji": "🎯"
            },
            {
                "primary": f"হুম... {sender_name} vs {target_name}! 🔥",
                "secondary": "এই লড়াইয়ের রেফারি আমি! কে জিতবে দেখা যাক!",
                "emoji": "⚔️"
            },
            {
                "primary": f"{target_name}, তোমার নামে রোস্টের অর্ডার এসেছে! 😈",
                "secondary": f"{sender_name}এর থেকে বিশেষ রিকোয়েস্ট!",
                "emoji": "📦"
            },
            {
                "primary": f"তথ্য পাওয়া গেছে: {sender_name} → {target_name} 🎯",
                "secondary": "টার্গেট লক! রোস্ট প্রস্তুত!",
                "emoji": "🔒"
            },
            {
                "primary": f"{target_name}, সাবধান! {sender_name} রোস্ট মিসাইল ছুড়েছে! 💥",
                "secondary": "ডিফেন্স সিস্টেম একটিভ! মজা হবে!",
                "emoji": "🚀"
            }
        ]
        
        # Select random roast
        selected = random.choice(mention_roasts)
        
        # Add context from original text if available
        if text and len(text) > 10:
            context_part = text[:50] + "..." if len(text) > 50 else text
            selected["context"] = f"কথাটা ছিল: '{context_part}'"
        
        return {
            "primary_roast": selected["primary"],
            "secondary_roast": selected["secondary"],
            "emoji_layer": selected["emoji"],
            "context": selected.get("context", "")
        }
    
    def _select_mention_template(self, text: str, sender: User, 
                                target: User) -> str:
        """Select template category for mention roast"""
        import random
        
        # Mention-specific templates
        mention_templates = ["neon_savage", "poster_style", "dark_sarcastic"]
        
        # Check text tone for template selection
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["লড়াই", "যুদ্ধ", "ফাইট", "বিরোধ"]):
            return "neon_savage"
        
        if any(word in text_lower for word in ["মজা", "হাসি", "জোক", "কমেডি"]):
            return "cartoon_roast"
        
        if any(word in text_lower for word in ["সিরিয়াস", "গুরুত্বপূর্ণ", "জরুরী"]):
            return "dark_sarcastic"
        
        return random.choice(mention_templates)
    
    async def _get_fallback_roast(self, sender: User, target: User) -> Dict:
        """Get fallback roast if mention-specific generation fails"""
        sender_name = f"@{sender.username}" if sender.username else sender.first_name
        target_name = f"@{target.username}" if target.username else target.first_name
        
        return {
            "primary_roast": f"{sender_name} {target_name}কে রোস্ট করতে চায়! 😂",
            "secondary_roast": "রোস্ট প্রস্তুত! সামনে আসো!",
            "emoji_layer": "🎤",
            "template_category": "cartoon_roast",
            "is_mention_roast": True,
            "target_user": target,
            "sender": sender
        }
    
    async def handle_self_mention(self, message: Message, context: ContextTypes.DEFAULT_TYPE):
        """Handle when bot is mentioned"""
        try:
            bot_user = await context.bot.get_me()
            chat = message.chat
            
            # Check if bot is mentioned
            if message.entities:
                for entity in message.entities:
                    if entity.type == "mention":
                        mentioned_text = message.text[entity.offset:entity.offset + entity.length]
                        if mentioned_text.lower() == f"@{bot_user.username}".lower():
                            # Bot is mentioned
                            await self._respond_to_bot_mention(message, context)
                            return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error handling self mention: {e}")
            return False
    
    async def _respond_to_bot_mention(self, message: Message, 
                                      context: ContextTypes.DEFAULT_TYPE):
        """Respond when bot is mentioned"""
        responses = [
            "হ্যাঁ আমাকে ডাকছ? 😊 রোস্ট চাওয়ার জন্য শুধু কাউকে mention করো!",
            "আমি এখানে! 😎 কাউকে mention করে রোস্ট শুরু করো!",
            "রোস্টিফাই প্রস্তুত! 🎯 কাকে রোস্ট করতে চাও?",
            "ডাক শুনেই ছুটে এলাম! 💨 কে টার্গেট?",
            "বট একটিভ! 🤖 mention করে বলো কে রোস্ট খাবে!"
        ]
        
        import random
        response = random.choice(responses)
        
        await message.reply_text(response)
    
    def get_mention_stats(self, user_id: int = None) -> Dict:
        """Get mention statistics"""
        # This would track how many times a user has mentioned others
        # and how many times they've been mentioned
        
        # For now, return placeholder stats
        return {
            "total_mentions_processed": len(self.recent_mentions),
            "active_mention_pairs": len(self.recent_mentions)
        }
    
    async def cleanup_old_mentions(self):
        """Cleanup old mention data"""
        import time
        current_time = time.time()
        
        # Remove mentions older than 1 hour
        old_keys = [k for k, v in self.recent_mentions.items() 
                   if current_time - v > 3600]
        
        for key in old_keys:
            del self.recent_mentions[key]
        
        if old_keys:
            logger.info(f"Cleaned {len(old_keys)} old mentions")