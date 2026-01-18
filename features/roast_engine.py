#!/usr/bin/env python3
"""
Roast Engine - Core roasting logic for Roastify Bot
"""

import random
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import ROAST_ENGINE, ROAST_PHRASES, TEMPLATES
except ImportError:
    logger.error("Config module not found")
    sys.exit(1)


class RoastEngine:
    """Main engine for generating roasts"""
    
    def __init__(self):
        """Initialize roast engine"""
        self.config = ROAST_ENGINE
        self.roast_phrases = ROAST_PHRASES
        self.templates_config = TEMPLATES
        
        # Load roast categories
        self.categories = self._load_categories()
        
        # Track recent roasts for variation
        self.recent_roasts = []
        self.recent_templates = []
        
        logger.info("Roast Engine initialized")
    
    def _load_categories(self) -> Dict:
        """Load roast categories and phrases"""
        categories = {
            "sentence_logic": {
                "keywords": ["কারণ", "তাই", "কিন্তু", "যদি", "তাহলে"],
                "phrases": [
                    "তোমার লজিক দেখে মনে হচ্ছে গণিতের বই উলটে পালটে দেখছ!",
                    "এমন চিন্তা করলে যে, ব্রেন সেলগুলো আত্মহত্যা করবে!",
                    "কথার মধ্যে লজিক খুঁজে পাচ্ছি না, হয়তো অন্য ডাইমেনশনে আছে!",
                    "তোমার যুক্তি শুনে আইনস্টাইনও কাঁদবে!",
                    "এত জটিল চিন্তা করে মাথা গরম করছ কেন, সহজভাবে বল!"
                ]
            },
            "overconfidence": {
                "keywords": ["আমি", "সেরা", "দারুন", "একদম", "পারফেক্ট"],
                "phrases": [
                    "আত্মবিশ্বাস ভালো, কিন্তু এরকম অতি আত্মবিশ্বাস বিপজ্জনক!",
                    "মনে হচ্ছে নিজের কথায় নিজেই বিশ্বাস করে ফেলেছ!",
                    "এত কনফিডেন্ট হলে সাবধান, রিয়েলিটি চেক দরকার!",
                    "হুম, বলার স্টাইল দেখে মনে হচ্ছে অনেক বড় কিছু!",
                    "কথায় আত্মবিশ্বাস দেখে ভালো লাগল, কিন্তু বাস্তবতা অন্য কথা বলে!"
                ]
            },
            "common_lies": {
                "keywords": ["আসলে", "সত্যি", "কসম", "প্রমিজ", "নো লাই"],
                "phrases": [
                    "কথাটা ঠিক সত্যি বলার মতো শোনাচ্ছে না!",
                    "এবার একটু সত্যি কথা বলো না, সবসময় মিথ্যা কেন?",
                    "তোমার কথা শুনে পিনোকিওর নাক বড় হয়ে যাবে!",
                    "মিথ্যা বলতে এত সুন্দর করে, শিল্পী হতে পারতে!",
                    "সত্যি বলতে চেষ্টা করো, মিথ্যার ওজন বেশি!"
                ]
            },
            "daily_habits": {
                "keywords": ["ঘুম", "খাওয়া", "গেম", "ফোন", "টিভি"],
                "phrases": [
                    "দৈনন্দিন রুটিন শুনে মনে হচ্ছে একঘেয়ে জীবন!",
                    "এভাবে চললে তো জীবন শূন্য হয়ে যাবে!",
                    "রুটিনে একটু ভ্যারাইটি এনো, নয়তো বিরক্তিকর হয়ে যাবে!",
                    "দৈনন্দিন কাজের মধ্যে নতুনত্ব আনো, জীবন রঙিন হবে!",
                    "একই কাজ বারবার করলে রোবট মনে হবে!"
                ]
            },
            "self_claims": {
                "keywords": ["ভালো", "স্মার্ট", "হ্যান্ডসাম", "সুন্দর", "ট্যালেন্টেড"],
                "phrases": [
                    "নিজের প্রশংসা নিজে করলে সত্যি বিশ্বাসযোগ্য হয় না!",
                    "এত self-praise দেখে লজ্জা লাগে না?",
                    "অন্যের কাছ থেকে প্রশংসা শুনতে মিষ্টি লাগে, নিজে বললে নয়!",
                    "নিজের গুণগান করা বন্ধ করো, অন্যদের বলতে দাও!",
                    "Self-claim কমিয়ে দাও, authenticity বাড়বে!"
                ]
            }
        }
        
        # Add phrases from config if available
        if self.roast_phrases.get("primary"):
            for category in categories.values():
                category["phrases"].extend(self.roast_phrases["primary"][:3])
        
        return categories
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize input text"""
        # Remove links
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\u0980-\u09FF.,!?\-]', '', text)
        
        return text.strip()
    
    def _detect_category(self, text: str) -> str:
        """Detect which roast category the text belongs to"""
        text_lower = text.lower()
        
        # Count keyword matches for each category
        category_scores = {}
        for category_name, category_data in self.categories.items():
            score = 0
            for keyword in category_data["keywords"]:
                if keyword.lower() in text_lower:
                    score += 1
            category_scores[category_name] = score
        
        # Also check for specific patterns
        if len(text.split()) < 6:
            category_scores["sentence_logic"] += 2
        
        if "আমি" in text and any(word in text for word in ["সেরা", "ভালো", "দারুন"]):
            category_scores["overconfidence"] += 3
        
        if any(word in text.lower() for word in ["সত্যি", "কসম", "প্রমিজ"]):
            category_scores["common_lies"] += 2
        
        # Select category with highest score
        if category_scores:
            selected_category = max(category_scores.items(), key=lambda x: x[1])[0]
            if category_scores[selected_category] > 0:
                return selected_category
        
        # Default to sentence_logic
        return "sentence_logic"
    
    def _select_template_category(self, text: str, user: Any = None) -> str:
        """Select template category based on text and context"""
        text_lower = text.lower()
        
        # Check for funny content
        funny_keywords = ["হাসি", "মজা", "😂", "🤣", "হাহা"]
        if any(keyword in text_lower for keyword in funny_keywords):
            return "cartoon_roast"
        
        # Check for attitude
        attitude_keywords = ["আমি", "boss", "king", "সেরা", "একদম"]
        if any(keyword in text_lower for keyword in attitude_keywords):
            return "neon_savage"
        
        # Check for emotional content
        emotional_keywords = ["দুঃখ", "কষ্ট", "একা", "😢", "😭"]
        if any(keyword in text_lower for keyword in emotional_keywords):
            return "dark_sarcastic"
        
        # Check for short/simple text
        if len(text.split()) < 8:
            return "minimal_mock"
        
        # Check time of day
        current_hour = datetime.now().hour
        if 19 <= current_hour <= 23 or 0 <= current_hour <= 5:
            return "neon_savage"
        
        # Default based on random selection
        categories = list(self.templates_config["template_categories"].keys())
        return random.choice(categories)
    
    def _get_primary_roast(self, category: str, text: str) -> str:
        """Get primary roast line"""
        if category in self.categories:
            phrases = self.categories[category]["phrases"]
            
            # Filter out recently used phrases
            available = [p for p in phrases if p not in self.recent_roasts[-10:]]
            if not available:
                available = phrases
            
            selected = random.choice(available)
            
            # Add to recent roasts
            self.recent_roasts.append(selected)
            if len(self.recent_roasts) > 20:
                self.recent_roasts.pop(0)
            
            return selected
        
        # Fallback phrase
        return "তোমার কথায় বিশেষত্ব আছে, কিন্তু বুঝতে সময় লাগবে!"
    
    def _get_secondary_roast(self, category: str, text: str) -> str:
        """Get secondary roast line"""
        secondary_phrases = [
            "চিন্তা করে দেখো, হয়তো বুঝতে পারবে!",
            "এবার একটু ভিন্নভাবে চিন্তা করো!",
            "মজা করছি, কিন্তু সত্যি কথাই বলছি!",
            "কথাগুলো মাথায় রাখো, কাজে লাগবে!",
            "এবারের মতো ক্ষমা করলাম, পরেরবার নয়!",
            "বুদ্ধি দিয়ে উত্তর দিলে কেউ কিছু বলবে না!",
            "একটু সিরিয়াস হও, জীবন রসিকতা নয়!",
            "মাথা ঠান্ডা রেখো, ভালো থেকো!",
            "পরেরবার আরও ভালো উত্তর আশা করছি!",
            "তোমার জন্য শুভকামনা রইল!"
        ]
        
        # Add category-specific secondary phrases
        if category == "overconfidence":
            secondary_phrases.extend([
                "আত্মবিশ্বাস রাখো, কিন্তু অতি নয়!",
                "বাস্তবতা মেনে নেওয়াও এক ধরনের বুদ্ধিমত্তা!"
            ])
        elif category == "common_lies":
            secondary_phrases.extend([
                "সত্যি কথা বলতে শেখো, জীবন সহজ হবে!",
                "মিথ্যার চেয়ে কষ্টকর সত্য ভালো!"
            ])
        
        return random.choice(secondary_phrases)
    
    def _get_emoji_layer(self, category: str, text: str) -> str:
        """Get appropriate emojis for the roast"""
        emoji_sets = {
            "sentence_logic": ["🤔", "🧠", "💭", "❓", "⁉️"],
            "overconfidence": ["😎", "🔥", "💪", "🚀", "🌟"],
            "common_lies": ["🤥", "🎭", "🃏", "✨", "👃"],
            "daily_habits": ["😴", "🍔", "🎮", "📱", "🛌"],
            "self_claims": ["🪞", "👑", "🎖️", "🏆", "💫"]
        }
        
        if category in emoji_sets:
            return random.choice(emoji_sets[category])
        
        # Default emojis
        default_emojis = ["😈", "👻", "🤖", "👾", "💀"]
        return random.choice(default_emojis)
    
    def _should_use_profile_photo(self, text: str, user: Any) -> bool:
        """Determine if profile photo should be used"""
        text_lower = text.lower()
        
        # Check conditions from config
        conditions = [
            len(text.split()) < 8,  # Short text
            any(word in text_lower for word in ["আমি", "নিজে", "স্বয়ং"]),  # Self-reference
            any(word in text_lower for word in ["মন", "হৃদয়", "আত্মা"]),  # Emotional
            any(emoji in text for emoji in ["❤️", "😍", "🥰", "😢", "😭"])  # Emotional emojis
        ]
        
        return any(conditions)
    
    async def generate_roast(self, text: str, user: Any, target_user: Any = None) -> Dict:
        """Generate a complete roast response"""
        try:
            # Sanitize text
            sanitized_text = self._sanitize_text(text)
            
            # Detect category
            category = self._detect_category(sanitized_text)
            
            # Select template category
            template_category = self._select_template_category(sanitized_text, user)
            
            # Get roast components
            primary_roast = self._get_primary_roast(category, sanitized_text)
            secondary_roast = self._get_secondary_roast(category, sanitized_text)
            emoji_layer = self._get_emoji_layer(category, sanitized_text)
            
            # Determine if profile photo should be used
            use_profile_photo = self._should_use_profile_photo(sanitized_text, user)
            
            # Prepare user info
            user_info = f"@{user.username}" if user.username else user.first_name
            if target_user:
                target_info = f"@{target_user.username}" if target_user.username else target_user.first_name
                user_display = f"{user_info} → {target_info}"
            else:
                user_display = user_info
            
            # Create caption with HTML formatting
            caption = f"""
<b>{primary_roast}</b>

{secondary_roast}

{emoji_layer}

👤 <i>{user_display}</i>
🕐 {datetime.now().strftime("%H:%M")}
            """.strip()
            
            # Prepare roast data
            roast_data = {
                "original_text": text,
                "sanitized_text": sanitized_text,
                "category": category,
                "template_category": template_category,
                "primary_roast": primary_roast,
                "secondary_roast": secondary_roast,
                "emoji_layer": emoji_layer,
                "caption": caption,
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "target_user": target_user.id if target_user else None,
                "use_profile_photo": use_profile_photo,
                "timestamp": datetime.now().isoformat(),
                "template_name": f"{template_category}_{random.randint(1, 100)}"
            }
            
            logger.info(f"Generated roast for user {user.id}: {category}")
            return roast_data
            
        except Exception as e:
            logger.error(f"Error generating roast: {e}")
            
            # Return fallback roast data
            return {
                "original_text": text,
                "sanitized_text": text[:100],
                "category": "fallback",
                "template_category": "minimal_mock",
                "primary_roast": "কিছু একটা সমস্যা হয়েছে! আবার চেষ্টা করো!",
                "secondary_roast": "বট ঠিক কাজ করছে, তোমার বার্তায় সমস্যা!",
                "emoji_layer": "😅",
                "caption": f"<b>কিছু একটা সমস্যা হয়েছে!</b>\n\nআবার চেষ্টা করো! 😅\n\n👤 {user.first_name}",
                "user_id": user.id,
                "use_profile_photo": False,
                "template_name": "fallback_1"
            }
    
    async def get_short_response(self, text: str, user: Any) -> str:
        """Get response for very short messages"""
        short_responses = [
            f"{user.first_name}, আরও কিছু লিখো না! কমপক্ষে ৪ অক্ষর চাই! 😏",
            "এত সংক্ষিপ্ত? একটু বিস্তারিত বলো! 📝",
            "হুম... আরেকটু লিখলে ভালো হতো! 🤔",
            "এত ছোট বার্তায় রোস্ট করার মতো কিছু পাইনি! 😅",
            "৪ অক্ষরের বেশি লিখো, রোস্ট দিয়ে দিব! 🔥"
        ]
        
        # Check if text is too short
        if len(text.strip()) == 0:
            return "কিছু লিখো তো! শূন্য বার্তায় রোস্ট হয় না! 😐"
        
        if len(text.strip()) == 1:
            return "একটা অক্ষর? সত্যি? 😂"
        
        if len(text.strip()) == 2:
            return "দুই অক্ষরে জীবন গল্প বলা যায় না! ✌️"
        
        if len(text.strip()) == 3:
            return "তিন অক্ষর... প্রায় পৌঁছে গেছ! আরেকটু! 📈"
        
        return random.choice(short_responses)
    
    def get_roast_stats(self) -> Dict:
        """Get statistics about roast generation"""
        return {
            "total_categories": len(self.categories),
            "recent_roasts_count": len(self.recent_roasts),
            "categories": list(self.categories.keys()),
            "phrases_per_category": {
                cat: len(data["phrases"]) for cat, data in self.categories.items()
            }
        }