#!/usr/bin/env python3
"""
Reaction System for Roastify Bot
Auto-detects message mood and adds appropriate emoji reactions
"""

import random
import re
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import TOPIC_BASED_REACTION, EXTRA_FEATURES
    from database import get_database
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class ReactionSystem:
    """Manages auto-reactions to messages"""
    
    def __init__(self):
        """Initialize reaction system"""
        self.config = TOPIC_BASED_REACTION
        self.extra_config = EXTRA_FEATURES
        self.db = get_database()
        
        # Initialize reaction library
        self.reaction_lib = self._initialize_reaction_library()
        
        # Track recent reactions to prevent spam
        self.user_reaction_counts = {}  # user_id -> count
        self.last_reaction_reset = datetime.now()
        
        # Cooldown tracking
        self.reaction_cooldowns = {}  # chat_id -> last_reaction_time
        
        logger.info("Reaction System initialized")
    
    def _initialize_reaction_library(self) -> Dict[str, List[str]]:
        """Initialize the reaction emoji library"""
        # Start with config library
        reaction_lib = self.config.get("reaction_library", {}).copy()
        
        # Add extra reactions if missing
        if "general" not in reaction_lib:
            reaction_lib["general"] = ["👍", "👏", "🎯", "💯", "🔥"]
        
        if "question" not in reaction_lib:
            reaction_lib["question"] = ["🤔", "❓", "⁉️", "💭"]
        
        if "surprise" not in reaction_lib:
            reaction_lib["surprise"] = ["😲", "🤯", "🎉", "✨"]
        
        if "sad" not in reaction_lib:
            reaction_lib["sad"] = ["😢", "😭", "💔", "☹️"]
        
        # Add combo reactions
        reaction_lib["combos"] = {
            "funny_combo": ["😂", "🤣", "😹"],
            "love_combo": ["❤️", "😍", "🥰"],
            "fire_combo": ["🔥", "💥", "✨"],
            "mind_blown": ["🤯", "💥", "⚡"]
        }
        
        return reaction_lib
    
    def _detect_topic(self, text: str) -> List[str]:
        """Detect topics in text"""
        text_lower = text.lower()
        detected_topics = []
        
        # Check each topic category
        topic_categories = self.config.get("topic_detection", {}).get("categories", {})
        
        for topic, keywords in topic_categories.items():
            # Check for keywords
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_topics.append(topic)
                    break
        
        # Check for emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            "]+", flags=re.UNICODE)
        
        emojis = emoji_pattern.findall(text)
        for emoji in emojis:
            # Map emoji to topic
            emoji_topic = self._map_emoji_to_topic(emoji)
            if emoji_topic and emoji_topic not in detected_topics:
                detected_topics.append(emoji_topic)
        
        # Check punctuation for sentiment
        if "?" in text:
            detected_topics.append("question")
        if "!" in text and text.count("!") >= 2:
            detected_topics.append("excited")
        if "..." in text or "…" in text:
            detected_topics.append("thoughtful")
        
        # If no specific topic detected, use general
        if not detected_topics:
            detected_topics.append("general")
        
        return detected_topics
    
    def _map_emoji_to_topic(self, emoji: str) -> Optional[str]:
        """Map emoji to reaction topic"""
        emoji_to_topic = {
            "😂": "funny", "🤣": "funny", "😹": "funny",
            "😢": "sad", "😭": "sad", "😔": "sad",
            "❤️": "love", "😍": "love", "🥰": "love",
            "💪": "motivation", "🔥": "motivation", "🏆": "motivation",
            "😎": "attitude", "🤘": "attitude", "😏": "attitude",
            "🤔": "question", "❓": "question", "⁉️": "question",
            "😲": "surprise", "🤯": "surprise", "🎉": "surprise"
        }
        
        return emoji_to_topic.get(emoji)
    
    def _analyze_text_tone(self, text: str) -> Dict[str, float]:
        """Analyze text tone and sentiment"""
        text_lower = text.lower()
        
        # Simple sentiment analysis
        positive_words = ["ভাল", "খুশি", "আনন্দ", "সুন্দর", "দারুন", "অসাধারণ"]
        negative_words = ["খারাপ", "দুঃখ", "কষ্ট", "বিরক্ত", "হতাশ"]
        
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate excitement level
        excitement = text.count("!") / max(len(text.split()), 1)
        
        # Calculate question score
        question_score = 1 if "?" in text else 0
        
        return {
            "positive": positive_score,
            "negative": negative_score,
            "excitement": excitement,
            "question": question_score
        }
    
    def _get_reactions_for_topic(self, topic: str, tone: Dict = None) -> List[str]:
        """Get appropriate reactions for a topic"""
        reactions = []
        
        # Get base reactions for topic
        if topic in self.reaction_lib:
            reactions.extend(self.reaction_lib[topic])
        
        # Adjust based on tone if provided
        if tone:
            if tone["positive"] > tone["negative"]:
                reactions.extend(["👍", "👌", "✨"])
            if tone["excitement"] > 0.1:
                reactions.extend(["🎉", "🔥", "⚡"])
            if tone["question"] > 0:
                reactions.extend(["🤔", "❓"])
        
        # Remove duplicates
        reactions = list(dict.fromkeys(reactions))
        
        return reactions
    
    def _check_cooldown(self, chat_id: int) -> bool:
        """Check if cooldown is active for a chat"""
        current_time = datetime.now()
        cooldown_seconds = self.config.get("cooldown_seconds", 15)
        
        if chat_id in self.reaction_cooldowns:
            last_time = self.reaction_cooldowns[chat_id]
            time_diff = (current_time - last_time).total_seconds()
            
            if time_diff < cooldown_seconds:
                return True  # Cooldown active
        
        return False  # No cooldown
    
    def _update_user_reaction_count(self, user_id: int) -> bool:
        """Update user reaction count and check limit"""
        current_hour = datetime.now().hour
        
        # Reset counts hourly
        if current_hour != self.last_reaction_reset.hour:
            self.user_reaction_counts = {}
            self.last_reaction_reset = datetime.now()
        
        # Initialize or get count
        if user_id not in self.user_reaction_counts:
            self.user_reaction_counts[user_id] = 0
        
        # Check limit
        max_reactions = self.config.get("max_reactions_per_user_per_hour", 20)
        if self.user_reaction_counts[user_id] >= max_reactions:
            return False
        
        # Increment count
        self.user_reaction_counts[user_id] += 1
        return True
    
    def _should_ignore_message(self, text: str, user: Any) -> bool:
        """Check if message should be ignored for reactions"""
        # Check ignore conditions from config
        ignore_conditions = self.config.get("trigger_conditions", {}).get("ignore_conditions", [])
        
        if "very_short_messages" in ignore_conditions and len(text.strip()) < 3:
            return True
        
        if "links_only" in ignore_conditions:
            # Check if message contains only links
            import re
            url_pattern = re.compile(r'https?://\S+|www\.\S+')
            if url_pattern.sub('', text).strip() == '':
                return True
        
        if "emoji_only" in ignore_conditions:
            # Check if message contains only emojis
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF"
                "]+", flags=re.UNICODE)
            if emoji_pattern.sub('', text).strip() == '':
                return True
        
        # Check for protected users (implement based on your criteria)
        # if "messages_from_protected_users" in ignore_conditions:
        #     if self._is_protected_user(user.id):
        #         return True
        
        return False
    
    async def add_auto_reactions(self, message: Any, text: str, 
                                user: Any, chat: Any) -> bool:
        """Add auto-reactions to a message"""
        try:
            # Check if reaction system is enabled
            if not self.config.get("enabled", True):
                return False
            
            # Check ignore conditions
            if self._should_ignore_message(text, user):
                return False
            
            # Check minimum length
            min_length = self.config.get("trigger_conditions", {}).get("minimum_input_length", 4)
            if len(text.strip()) < min_length:
                return False
            
            # Check cooldown
            if self._check_cooldown(chat.id):
                return False
            
            # Check user reaction limit
            if not self._update_user_reaction_count(user.id):
                logger.debug(f"User {user.id} reached reaction limit")
                return False
            
            # Detect topics and tone
            topics = self._detect_topic(text)
            tone = self._analyze_text_tone(text)
            
            # Get reactions for detected topics
            all_reactions = []
            for topic in topics[:3]:  # Limit to top 3 topics
                reactions = self._get_reactions_for_topic(topic, tone)
                all_reactions.extend(reactions)
            
            # Remove duplicates and limit
            all_reactions = list(dict.fromkeys(all_reactions))
            max_reactions = 3  # Limit reactions per message
            
            # Check for combo reactions if enabled
            if self.extra_config.get("reaction_combo", {}).get("enabled", False):
                combo_reactions = self._get_combo_reactions(topics, tone)
                if combo_reactions:
                    # Replace some reactions with combo
                    all_reactions = combo_reactions[:max_reactions]
            
            # Limit number of reactions
            reactions_to_add = all_reactions[:max_reactions]
            
            if not reactions_to_add:
                reactions_to_add = ["👍"]  # Default reaction
            
            # Add reactions to message
            for reaction in reactions_to_add:
                try:
                    await message.react(reaction)
                    # Small delay between reactions
                    import asyncio
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Could not add reaction {reaction}: {e}")
            
            # Update cooldown
            self.reaction_cooldowns[chat.id] = datetime.now()
            
            # Update database
            self.db.cursor.execute('''
                UPDATE users 
                SET reaction_count = reaction_count + ?
                WHERE user_id = ?
            ''', (len(reactions_to_add), user.id))
            self.db.conn.commit()
            
            logger.info(f"Added {len(reactions_to_add)} reactions to message from user {user.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding auto-reactions: {e}")
            return False
    
    def _get_combo_reactions(self, topics: List[str], tone: Dict) -> List[str]:
        """Get combo reactions based on topics and tone"""
        combos = self.reaction_lib.get("combos", {})
        selected_combos = []
        
        # Check for combo conditions
        if "funny" in topics and tone.get("positive", 0) > 0:
            selected_combos.extend(combos.get("funny_combo", []))
        
        if "love" in topics:
            selected_combos.extend(combos.get("love_combo", []))
        
        if tone.get("excitement", 0) > 0.2:
            selected_combos.extend(combos.get("fire_combo", []))
        
        if "surprise" in topics and tone.get("excitement", 0) > 0.3:
            selected_combos.extend(combos.get("mind_blown", []))
        
        # Randomize if multiple combos available
        if selected_combos:
            # Get random combo (first 3 emojis from a random combo)
            import random
            combo_keys = list(combos.keys())
            if combo_keys:
                random_combo = random.choice(combo_keys)
                return combos[random_combo]
        
        return selected_combos[:3]  # Limit to 3 emojis
    
    async def add_custom_reaction(self, message: Any, emoji: str) -> bool:
        """Add a custom reaction to a message"""
        try:
            await message.react(emoji)
            return True
        except Exception as e:
            logger.error(f"Error adding custom reaction: {e}")
            return False
    
    async def remove_reaction(self, message: Any, emoji: str) -> bool:
        """Remove a reaction from a message"""
        try:
            await message.remove_reaction(emoji)
            return True
        except Exception as e:
            logger.error(f"Error removing reaction: {e}")
            return False
    
    def get_reaction_stats(self, user_id: int = None) -> Dict:
        """Get reaction statistics"""
        try:
            if user_id:
                # Get user-specific stats
                self.db.cursor.execute('''
                    SELECT reaction_count FROM users WHERE user_id = ?
                ''', (user_id,))
                result = self.db.cursor.fetchone()
                
                if result:
                    return {
                        "user_id": user_id,
                        "total_reactions": result[0],
                        "hourly_limit": self.config.get("max_reactions_per_user_per_hour", 20),
                        "current_hour_count": self.user_reaction_counts.get(user_id, 0)
                    }
                else:
                    return {"error": "User not found"}
            else:
                # Get overall stats
                self.db.cursor.execute('''
                    SELECT SUM(reaction_count) as total_reactions,
                           COUNT(*) as users_with_reactions
                    FROM users WHERE reaction_count > 0
                ''')
                result = self.db.cursor.fetchone()
                
                return {
                    "total_reactions": result[0] or 0,
                    "users_with_reactions": result[1] or 0,
                    "active_users_current_hour": len(self.user_reaction_counts)
                }
                
        except Exception as e:
            logger.error(f"Error getting reaction stats: {e}")
            return {"error": str(e)}
    
    async def reset_user_reaction_count(self, user_id: int) -> bool:
        """Reset reaction count for a user"""
        try:
            if user_id in self.user_reaction_counts:
                self.user_reaction_counts[user_id] = 0
                return True
            return False
        except Exception as e:
            logger.error(f"Error resetting user reaction count: {e}")
            return False
    
    async def get_top_reacted_users(self, limit: int = 10) -> List[Dict]:
        """Get top users by reactions received"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, first_name, reaction_count
                FROM users
                WHERE reaction_count > 0
                ORDER BY reaction_count DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.db.cursor.fetchall()
            
            top_users = []
            for user_id, username, first_name, reaction_count in results:
                top_users.append({
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'reaction_count': reaction_count
                })
            
            return top_users
            
        except Exception as e:
            logger.error(f"Error getting top reacted users: {e}")
            return []
    
    async def cleanup_old_data(self):
        """Cleanup old reaction data"""
        try:
            # Reset hourly counts if hour changed
            current_hour = datetime.now().hour
            if current_hour != self.last_reaction_reset.hour:
                self.user_reaction_counts = {}
                self.last_reaction_reset = datetime.now()
                logger.info("Reset hourly reaction counts")
            
            # Clean old cooldowns (older than 1 hour)
            current_time = datetime.now()
            old_cooldowns = []
            
            for chat_id, last_time in list(self.reaction_cooldowns.items()):
                time_diff = (current_time - last_time).total_seconds()
                if time_diff > 3600:  # 1 hour
                    old_cooldowns.append(chat_id)
            
            for chat_id in old_cooldowns:
                del self.reaction_cooldowns[chat_id]
            
            if old_cooldowns:
                logger.info(f"Cleaned {len(old_cooldowns)} old cooldowns")
                
        except Exception as e:
            logger.error(f"Error cleaning up reaction data: {e}")