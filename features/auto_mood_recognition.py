#!/usr/bin/env python3
"""
Auto Mood Recognition for Roastify Bot
Analyzes text mood and adjusts responses accordingly
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

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


class AutoMoodRecognition:
    """Analyzes message mood and adjusts bot behavior"""
    
    def __init__(self):
        """Initialize mood recognition system"""
        self.config = EXTRA_FEATURES.get("auto_mood_recognition", {})
        self.text_processor = TextProcessor()
        
        # Mood database
        self.mood_patterns = self._load_mood_patterns()
        
        # Mood history tracking
        self.user_mood_history = {}  # user_id -> list of moods
        
        logger.info("Auto Mood Recognition system initialized")
    
    def _load_mood_patterns(self) -> Dict[str, Dict]:
        """Load mood recognition patterns"""
        patterns = {
            "happy": {
                "keywords": ["হাসি", "খুশি", "আনন্দ", "ভালো", "মজা", "উৎসব", "পার্টি"],
                "emojis": ["😂", "🤣", "😊", "😄", "😁", "🥰", "😍", "🎉", "✨"],
                "punctuation": ["!", "!!", "!!!"],
                "weight": 1.0
            },
            "sad": {
                "keywords": ["দুঃখ", "কষ্ট", "বিরক্ত", "হতাশ", "কান্না", "মন খারাপ"],
                "emojis": ["😢", "😭", "😔", "😞", "😩", "🥺", "💔"],
                "punctuation": ["...", "…"],
                "weight": 1.0
            },
            "angry": {
                "keywords": ["রাগ", "ক্রোধ", "গোস্সা", "বিরক্তি", "হুমকি", "ঝগড়া"],
                "emojis": ["😠", "😡", "🤬", "👿", "💢"],
                "punctuation": ["!", "!!", "!!!"],
                "weight": 1.2
            },
            "excited": {
                "keywords": ["উত্তেজিত", "উদ্বিগ্ন", "অপেক্ষা", "সাসপেন্স", "রোমাঞ্চ"],
                "emojis": ["😲", "🤯", "😱", "🎊", "🔥", "⚡"],
                "punctuation": ["!", "!!", "!!!", "?", "?!"],
                "weight": 1.1
            },
            "romantic": {
                "keywords": ["ভালোবাসা", "প্রেম", "হার্ট", "রোমান্টিক", "মিষ্টি"],
                "emojis": ["❤️", "💕", "💖", "💗", "💘", "😘", "🥰"],
                "punctuation": ["~", "...", "♥"],
                "weight": 0.9
            },
            "sarcastic": {
                "keywords": ["বিদ্রূপ", "মিথ্যা প্রশংসা", "উল্টা কথা", "ট্রল"],
                "emojis": ["😏", "😒", "🙄", "😌", "🤨"],
                "punctuation": [".", "..", "..."],
                "weight": 1.3
            },
            "curious": {
                "keywords": ["কী", "কেন", "কেমন", "কখন", "কোথায়", "জানতে চাই"],
                "emojis": ["🤔", "🧐", "❓", "⁉️", "💭"],
                "punctuation": ["?", "??", "???"],
                "weight": 1.0
            },
            "grateful": {
                "keywords": ["ধন্যবাদ", "শুক্রিয়া", "কৃতজ্ঞ", "অনুগ্রহ", "সাহায্য"],
                "emojis": ["🙏", "😇", "🤗", "💝", "🎁"],
                "punctuation": ["!", "!!"],
                "weight": 0.8
            }
        }
        
        # Load from file if exists
        import os
        patterns_file = "data/mood_patterns.json"
        if os.path.exists(patterns_file):
            try:
                import json
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    file_patterns = json.load(f)
                    patterns.update(file_patterns)
            except Exception as e:
                logger.error(f"Error loading mood patterns: {e}")
        
        return patterns
    
    def analyze_mood(self, text: str, user_id: int = None) -> Dict[str, Any]:
        """Analyze mood from text"""
        try:
            # Initialize scores
            mood_scores = {mood: 0.0 for mood in self.mood_patterns}
            
            # Convert text to lowercase for matching
            text_lower = text.lower()
            
            # Analyze based on different factors
            analysis_factors = self.config.get("analysis_factors", [])
            
            if "text_tone" in analysis_factors:
                mood_scores = self._analyze_text_tone(text_lower, mood_scores)
            
            if "emoji_usage" in analysis_factors:
                mood_scores = self._analyze_emojis(text, mood_scores)
            
            if "punctuation" in analysis_factors:
                mood_scores = self._analyze_punctuation(text, mood_scores)
            
            if "keyword_patterns" in analysis_factors:
                mood_scores = self._analyze_keywords(text_lower, mood_scores)
            
            # Apply weights
            for mood, score in mood_scores.items():
                weight = self.mood_patterns[mood].get("weight", 1.0)
                mood_scores[mood] = score * weight
            
            # Get primary mood (highest score)
            primary_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
            primary_score = mood_scores[primary_mood]
            
            # Get secondary moods (other significant scores)
            secondary_moods = []
            for mood, score in mood_scores.items():
                if mood != primary_mood and score > 0.3:
                    secondary_moods.append((mood, score))
            
            # Sort secondary moods by score
            secondary_moods.sort(key=lambda x: x[1], reverse=True)
            
            # Calculate confidence
            total_score = sum(mood_scores.values())
            confidence = (primary_score / total_score * 100) if total_score > 0 else 0
            
            # Store in history if user_id provided
            if user_id:
                self._store_mood_history(user_id, primary_mood, confidence)
            
            return {
                "primary_mood": primary_mood,
                "primary_score": primary_score,
                "confidence": confidence,
                "secondary_moods": secondary_moods[:3],  # Top 3
                "all_scores": mood_scores,
                "text_length": len(text)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing mood: {e}")
            return {
                "primary_mood": "neutral",
                "primary_score": 1.0,
                "confidence": 100,
                "secondary_moods": [],
                "all_scores": {"neutral": 1.0},
                "text_length": len(text)
            }
    
    def _analyze_text_tone(self, text: str, mood_scores: Dict) -> Dict:
        """Analyze text tone for mood"""
        # Simple sentiment analysis
        positive_words = ["ভাল", "সুন্দর", "দারুন", "অসাধারণ", "চমৎকার", 
                         "খুশি", "আনন্দ", "প্রশংসা", "ধন্যবাদ"]
        negative_words = ["খারাপ", "মন্দ", "দুঃখ", "কষ্ট", "বিরক্ত", 
                         "হতাশ", "অসন্তুষ্ট", "সমস্যা", "ত্রুটি"]
        
        for word in positive_words:
            if word in text:
                mood_scores["happy"] += 0.5
                mood_scores["grateful"] += 0.3
        
        for word in negative_words:
            if word in text:
                mood_scores["sad"] += 0.5
                mood_scores["angry"] += 0.2
        
        # Check for questions
        if "?" in text:
            mood_scores["curious"] += 0.7
        
        # Check for excitement markers
        if "!" in text:
            exclamation_count = text.count("!")
            if exclamation_count >= 3:
                mood_scores["excited"] += 1.0
                mood_scores["happy"] += 0.5
            elif exclamation_count >= 2:
                mood_scores["excited"] += 0.7
            else:
                mood_scores["excited"] += 0.3
        
        return mood_scores
    
    def _analyze_emojis(self, text: str, mood_scores: Dict) -> Dict:
        """Analyze emojis for mood"""
        # Extract emojis
        import emoji
        emojis = [c for c in text if c in emoji.EMOJI_DATA]
        
        for emoji_char in emojis:
            # Check which mood pattern this emoji belongs to
            for mood, pattern in self.mood_patterns.items():
                if emoji_char in pattern.get("emojis", []):
                    mood_scores[mood] += 1.0
        
        return mood_scores
    
    def _analyze_punctuation(self, text: str, mood_scores: Dict) -> Dict:
        """Analyze punctuation for mood"""
        # Count punctuation marks
        punctuation_marks = {
            "!": ("excited", "happy", "angry"),
            "?": ("curious", "sarcastic"),
            "...": ("sad", "thoughtful"),
            "!!": ("excited", "angry"),
            "??": ("curious", "confused"),
            "!?": ("surprised", "curious"),
            "?!": ("surprised", "curious")
        }
        
        for mark, moods in punctuation_marks.items():
            count = text.count(mark)
            if count > 0:
                for mood in moods:
                    if mood in mood_scores:
                        mood_scores[mood] += count * 0.3
        
        return mood_scores
    
    def _analyze_keywords(self, text: str, mood_scores: Dict) -> Dict:
        """Analyze keywords for mood"""
        for mood, pattern in self.mood_patterns.items():
            keywords = pattern.get("keywords", [])
            for keyword in keywords:
                if keyword in text:
                    # Count occurrences
                    count = text.count(keyword)
                    mood_scores[mood] += count * 0.5
        
        return mood_scores
    
    def _store_mood_history(self, user_id: int, mood: str, confidence: float):
        """Store mood analysis in history"""
        try:
            if user_id not in self.user_mood_history:
                self.user_mood_history[user_id] = []
            
            mood_entry = {
                "mood": mood,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }
            
            self.user_mood_history[user_id].append(mood_entry)
            
            # Keep only last 100 entries per user
            if len(self.user_mood_history[user_id]) > 100:
                self.user_mood_history[user_id] = self.user_mood_history[user_id][-100:]
            
        except Exception as e:
            logger.error(f"Error storing mood history: {e}")
    
    def get_user_mood_trend(self, user_id: int) -> Dict[str, Any]:
        """Get mood trend for user"""
        try:
            if user_id not in self.user_mood_history:
                return {
                    "total_analyses": 0,
                    "most_common_mood": "unknown",
                    "mood_distribution": {},
                    "average_confidence": 0
                }
            
            history = self.user_mood_history[user_id]
            
            # Count mood occurrences
            mood_counts = {}
            total_confidence = 0
            
            for entry in history:
                mood = entry["mood"]
                confidence = entry["confidence"]
                
                if mood not in mood_counts:
                    mood_counts[mood] = 0
                
                mood_counts[mood] += 1
                total_confidence += confidence
            
            # Find most common mood
            most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else "unknown"
            
            # Calculate percentages
            total_entries = len(history)
            mood_distribution = {}
            for mood, count in mood_counts.items():
                percentage = (count / total_entries) * 100
                mood_distribution[mood] = {
                    "count": count,
                    "percentage": round(percentage, 1)
                }
            
            # Average confidence
            avg_confidence = total_confidence / total_entries if total_entries > 0 else 0
            
            return {
                "total_analyses": total_entries,
                "most_common_mood": most_common_mood,
                "mood_distribution": mood_distribution,
                "average_confidence": round(avg_confidence, 1),
                "recent_moods": [entry["mood"] for entry in history[-10:]]  # Last 10 moods
            }
            
        except Exception as e:
            logger.error(f"Error getting mood trend: {e}")
            return {
                "total_analyses": 0,
                "most_common_mood": "unknown",
                "mood_distribution": {},
                "average_confidence": 0,
                "recent_moods": []
            }
    
    def adjust_roast_based_on_mood(self, roast_data: Dict, mood_analysis: Dict) -> Dict:
        """Adjust roast based on detected mood"""
        try:
            primary_mood = mood_analysis["primary_mood"]
            confidence = mood_analysis["confidence"]
            
            # Only adjust if confidence is high enough
            if confidence < 50:
                return roast_data
            
            # Adjust based on mood
            adjustments = {
                "happy": {
                    "tone_adjustment": "playful",
                    "emoji_add": "😊",
                    "intensity_multiplier": 0.7
                },
                "sad": {
                    "tone_adjustment": "gentle",
                    "emoji_add": "🤗",
                    "intensity_multiplier": 0.5
                },
                "angry": {
                    "tone_adjustment": "calm",
                    "emoji_add": "😌",
                    "intensity_multiplier": 0.6
                },
                "excited": {
                    "tone_adjustment": "energetic",
                    "emoji_add": "🎉",
                    "intensity_multiplier": 1.2
                },
                "romantic": {
                    "tone_adjustment": "sweet",
                    "emoji_add": "❤️",
                    "intensity_multiplier": 0.8
                },
                "sarcastic": {
                    "tone_adjustment": "witty",
                    "emoji_add": "😏",
                    "intensity_multiplier": 1.3
                },
                "curious": {
                    "tone_adjustment": "explanatory",
                    "emoji_add": "🤔",
                    "intensity_multiplier": 0.9
                },
                "grateful": {
                    "tone_adjustment": "appreciative",
                    "emoji_add": "🙏",
                    "intensity_multiplier": 0.7
                }
            }
            
            if primary_mood in adjustments:
                adjustment = adjustments[primary_mood]
                
                # Apply adjustments to roast data
                roast_data["mood_adjusted"] = True
                roast_data["detected_mood"] = primary_mood
                roast_data["mood_confidence"] = confidence
                
                # Add mood-specific emoji
                if "emoji_layer" in roast_data:
                    roast_data["emoji_layer"] += f" {adjustment['emoji_add']}"
                
                # Adjust template based on mood
                roast_data["template_category"] = self._get_mood_template(primary_mood)
                
                # Add mood note to caption
                mood_notes = {
                    "happy": "হাসি খুশি থাকো! 😊",
                    "sad": "মন খারাপ করো না! 🤗",
                    "angry": "শান্ত হও! সব ঠিক হবে! 😌",
                    "excited": "উত্তেজিত হওয়া ভালো! 🎉",
                    "romantic": "ভালোবাসা সবসময় জিতবে! ❤️",
                    "sarcastic": "বিদ্রূপ ভালো, তবে পরিমিত! 😏",
                    "curious": "জানতে চাওয়া জ্ঞানের শুরু! 🤔",
                    "grateful": "কৃতজ্ঞতা সুন্দর গুণ! 🙏"
                }
                
                if primary_mood in mood_notes:
                    roast_data["mood_note"] = mood_notes[primary_mood]
            
            return roast_data
            
        except Exception as e:
            logger.error(f"Error adjusting roast for mood: {e}")
            return roast_data
    
    def _get_mood_template(self, mood: str) -> str:
        """Get appropriate template category for mood"""
        mood_templates = {
            "happy": "cartoon_roast",
            "sad": "dark_sarcastic",
            "angry": "minimal_mock",
            "excited": "neon_savage",
            "romantic": "poster_style",
            "sarcastic": "dark_sarcastic",
            "curious": "minimal_mock",
            "grateful": "cartoon_roast"
        }
        
        return mood_templates.get(mood, "cartoon_roast")
    
    async def send_mood_analysis(self, chat_id: int, mood_analysis: Dict, 
                                context: ContextTypes.DEFAULT_TYPE):
        """Send mood analysis to chat"""
        try:
            primary_mood = mood_analysis["primary_mood"]
            confidence = mood_analysis["confidence"]
            secondary_moods = mood_analysis["secondary_moods"]
            
            # Mood descriptions
            mood_descriptions = {
                "happy": "খুশি এবং আনন্দিত 😊",
                "sad": "দুঃখিত বা মন খারাপ 😢",
                "angry": "রাগান্বিত বা বিরক্ত 😠",
                "excited": "উত্তেজিত বা উদ্দীপ্ত 😲",
                "romantic": "রোমান্টিক বা প্রেমময় ❤️",
                "sarcastic": "বিদ্রূপাত্মক বা ট্রল 😏",
                "curious": "কৌতূহলী বা জানতে আগ্রহী 🤔",
                "grateful": "কৃতজ্ঞ বা ধন্যবাদপূর্ণ 🙏"
            }
            
            # Create analysis message
            message = f"""
🧠 <b>মুড অ্যানালাইসিস রিপোর্ট</b> 🧠
━━━━━━━━━━━━━━━━━━━━━━

<b>প্রাইমারি মুড:</b> {mood_descriptions.get(primary_mood, primary_mood)}
<b>কনফিডেন্স লেভেল:</b> {confidence:.1f}%

"""
            
            # Add secondary moods if any
            if secondary_moods:
                message += "<b>সেকেন্ডারি মুডস:</b>\n"
                for mood, score in secondary_moods[:3]:
                    desc = mood_descriptions.get(mood, mood)
                    percentage = (score / sum(mood_analysis["all_scores"].values())) * 100
                    message += f"• {desc}: {percentage:.1f}%\n"
            
            # Add interpretation
            interpretations = {
                "happy": "তুমি ভালো মেজাজে আছো! এটা রোস্ট খাওয়ার জন্য পারফেক্ট সময়! 😄",
                "sad": "মন খারাপ? চিন্তা নেই, রোস্ট খেলে মন ভালো হয়ে যাবে! 🤗",
                "angry": "রাগ করছ? শান্ত হও, হালকা রোস্ট দিয়ে মেজাজ ফ্রেশ করি! 😌",
                "excited": "উত্তেজিত হওয়া ভালো! চলো এক্সাইটিং রোস্ট দেই! 🎉",
                "romantic": "রোমান্টিক মুড! এবার রোমান্টিক স্টাইলে রোস্ট দেই! ❤️",
                "sarcastic": "বিদ্রূপ করছ? আমিও পারি! দেখিয়ে দিই কে বেটার! 😏",
                "curious": "জানতে চাও? রোস্টের মাধ্যমে নতুন কিছু শিখি! 🤔",
                "grateful": "কৃতজ্ঞতা দেখাচ্ছো? খুব ভালো গুণ! এরকম থাকো! 🙏"
            }
            
            if primary_mood in interpretations:
                message += f"\n{interpretations[primary_mood]}"
            
            # Send message
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML"
            )
            
            logger.info(f"Sent mood analysis to chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error sending mood analysis: {e}")
    
    def add_custom_mood_pattern(self, mood_name: str, pattern_data: Dict) -> bool:
        """Add custom mood pattern"""
        try:
            # Validate required fields
            required_fields = ["keywords", "emojis", "punctuation"]
            for field in required_fields:
                if field not in pattern_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add to mood patterns
            pattern_data.setdefault("weight", 1.0)
            self.mood_patterns[mood_name] = pattern_data
            
            # Save to file
            import json
            patterns_file = "data/mood_patterns.json"
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.mood_patterns, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Added custom mood pattern: {mood_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding custom mood pattern: {e}")
            return False
    
    def get_mood_stats(self) -> Dict[str, Any]:
        """Get mood analysis statistics"""
        total_analyses = 0
        mood_counts = {}
        
        for user_id, history in self.user_mood_history.items():
            total_analyses += len(history)
            for entry in history:
                mood = entry["mood"]
                if mood not in mood_counts:
                    mood_counts[mood] = 0
                mood_counts[mood] += 1
        
        return {
            "total_users_analyzed": len(self.user_mood_history),
            "total_analyses": total_analyses,
            "mood_distribution": mood_counts,
            "available_moods": list(self.mood_patterns.keys()),
            "average_history_length": total_analyses / max(1, len(self.user_mood_history))
        }