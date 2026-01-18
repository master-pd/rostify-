#!/usr/bin/env python3
"""
Roastify Bot - Complete Configuration
All settings in one file, no .env needed
"""

import os
from datetime import time
from typing import Dict, List, Any, Tuple

# ==================== BOT TOKEN ====================
# ⚠️ IMPORTANT: Replace with your bot token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ==================== BOT IDENTITY ====================
BOT_IDENTITY = {
    "name": "Roastify",
    "username_suggestions": ["@top_roast_bot"],
    "tagline": "তুমি লেখো, বাকি অপমান আমরা করবো 😈",
    "one_line_pitch": "No-command Bangla roast + 3D graphics image generator with smart social features"
}

# ==================== CORE RULES ====================
CORE_RULES = {
    "slash_commands": False,
    "minimum_input_length": 4,
    "ignore_conditions": ["input_length <= 3", "only_emoji", "only_numbers", "contains_only_link"],
    "response_type": ["Image", "text", "diagram"],
    "text_reply": True,
    "image_reply": True,
    "diagram_reply": True
}

# ==================== INPUT PROCESSING ====================
INPUT_PROCESSING = {
    "steps": [
        "receive_user_text",
        "sanitize_text",
        "length_check",
        "pattern_detection",
        "roast_category_selection",
        "template_selection",
        "image_rendering"
    ],
    "sanitization": {
        "remove_links": True,
        "remove_sensitive_words": True,
        "normalize_whitespace": True
    }
}

# ==================== ROAST ENGINE ====================
ROAST_ENGINE = {
    "style": "Funny, Sarcastic, Professional",
    "allowed_roast_targets": [
        "sentence_logic",
        "overconfidence",
        "common_lies",
        "daily_habits",
        "self_claims"
    ],
    "disallowed_roast_targets": [
        "religion", "race", "body", "family", "gender",
        "sexuality", "disability", "politics"
    ],
    "roast_layers": {
        "primary_roast": "Big bold main line",
        "secondary_roast": "Small sarcastic sub line",
        "emoji_layer": "Contextual funny emoji"
    }
}

# ==================== IMAGE GENERATION ====================
IMAGE_GENERATION = {
    "type": "3D Styled Text Imaging",
    "ai_generation": False,
    "render_method": "Layer-based visual composition",
    "visual_elements": {
        "text_depth": True,
        "shadow_layers": 3,
        "glow_effect": True,
        "cinematic_lighting": True,
        "background_blur": True
    },
    "image_resolution": (1080, 1080),
    "formats": ["PNG"],
    "quality": 95
}

# ==================== TEMPLATES ====================
TEMPLATES = {
    "total_templates": 50,
    "template_categories": {
        "cartoon_roast": 12,
        "neon_savage": 10,
        "dark_sarcastic": 8,
        "minimal_mock": 8,
        "poster_style": 12
    },
    "rotation_rule": "Randomized with repetition avoidance",
    "same_input_variation": True,
    "unlockable_templates": True
}

# ==================== PROFILE PHOTO USAGE ====================
PROFILE_PHOTO_USAGE = {
    "enabled": True,
    "conditions": [
        "short_emotional_text",
        "attitude_claim",
        "self_identity_line"
    ],
    "processing": {
        "crop_style": "Circle",
        "blur_background": True,
        "glass_effect": True
    }
}

# ==================== TIME BASED BEHAVIOR ====================
TIME_BASED_BEHAVIOR = {
    "day_mode": {
        "time_range": (6, 0, 18, 59),  # 06:00 - 18:59
        "theme": "Soft Light",
        "colors": {
            "primary": (255, 255, 255),
            "secondary": (240, 240, 240),
            "text": (30, 30, 30),
            "accent": (70, 130, 180)
        }
    },
    "night_mode": {
        "time_range": (19, 0, 5, 59),   # 19:00 - 05:59
        "theme": "Dark Neon",
        "colors": {
            "primary": (20, 20, 40),
            "secondary": (40, 40, 60),
            "text": (220, 220, 255),
            "accent": (255, 105, 180)
        }
    }
}

# ==================== VOTE SYSTEM ====================
VOTE_SYSTEM = {
    "enabled": True,
    "vote_type": "Inline Button",
    "options": ["🔥 Funny", "😐 Mid", "💀 Savage"],
    "vote_rules": {
        "one_vote_per_user": True,
        "vote_window_seconds": 300,
        "self_vote_allowed": False
    },
    "vote_effects": {
        "high_funny_votes": "Increase similar roast weight",
        "high_mid_votes": "Neutral template balance",
        "high_savage_votes": "Unlock stronger roast tone"
    }
}

# ==================== MENTION TARGETED ROAST ====================
MENTION_TARGETED_ROAST = {
    "enabled": True,
    "trigger_conditions": {
        "chat_type": ["group", "supergroup"],
        "mention_required": True,
        "minimum_input_length": 4
    },
    "target_logic": {
        "target_user": "mentioned_user",
        "exclude_sender": True,
        "exclude_bot": True,
        "exclude_self_mention": True
    },
    "roast_tone": "Funny"
}

# ==================== OWNER ADMIN PROTECTION ====================
OWNER_ADMIN_PROTECTION = {
    "enabled": True,
    "bot_owner_user_id": 6454347745,  # Replace with your Telegram ID
    "admin_user_ids": [],  # Add additional admin IDs here
    "trigger_conditions": [
        "gali", "অপমান", "রোজ", "বিরক্ত করা", "হুমকি"
    ],
    "target_logic": "sender_of_trigger_message",
    "strict_protection": True,
    "roast_tone": "Funny / Safe",
    "cooldown_seconds": 120
}

# ==================== TOPIC BASED REACTION ====================
TOPIC_BASED_REACTION = {
    "enabled": True,
    "trigger_conditions": {
        "minimum_input_length": 4,
        "ignore_conditions": [
            "very_short_messages",
            "links_only",
            "emoji_only",
            "messages_from_protected_users"
        ]
    },
    "topic_detection": {
        "keywords_based": True,
        "context_analysis": True,
        "categories": {
            "funny": ["মজা", "হাসি", "😂", "🤣"],
            "sad": ["দুঃখ", "একাকী", "😭", "😢"],
            "love": ["ভালোবাসা", "tumi", "❤️", "😍"],
            "motivation": ["সফলতা", "উদ্যোগ", "💪", "🔥"],
            "attitude": ["আমি", "boss", "hero", "😎"]
        }
    },
    "reaction_library": {
        "funny": ["😂", "🤣", "😹"],
        "sad": ["😢", "😭", "☹️"],
        "love": ["❤️", "😍", "🥰"],
        "motivation": ["💪", "🔥", "🏆"],
        "attitude": ["😎", "🤘", "😏"]
    },
    "cooldown_seconds": 15,
    "max_reactions_per_user_per_hour": 20
}

# ==================== WELCOME MESSAGES ====================
WELCOME_MESSAGES = {
    "enabled": True,
    "messages": [
        "🎉 স্বাগতম! রোস্টের জন্য প্রস্তুত হও!",
        "👋 হ্যালো! অপেক্ষা করছিলাম তোমার জন্য!",
        "🔥 নতুন শিকার পাওয়া গেছে!",
        "😈 এবার তোমার পালা রোস্ট খাওয়ার!",
        "🌟 অভিনন্দন! রোস্টিফাই পরিবারে স্বাগতম!"
    ],
    "group_welcome": True,
    "private_welcome": True,
    "new_member_welcome": True,
    "randomize": True
}

# ==================== BORDERS CONFIG ====================
BORDERS = {
    "enabled": True,
    "border_files": [
        "border_1.png", "border_2.png", "border_3.png", "border_4.png",
        "border_5.png", "border_6.png", "border_7.png", "border_8.png",
        "border_9.png", "border_10.png"
    ],
    "random_selection": True,
    "no_repeat_until": 5,
    "auto_generate": True
}

# ==================== FONTS CONFIG ====================
FONTS = {
    "enabled": True,
    "font_files": [
        "font_1.ttf", "font_2.ttf", "font_3.ttf", "font_4.ttf",
        "font_5.ttf", "font_6.otf", "font_7.ttf", "font_8.otf"
    ],
    "random_selection": True,
    "no_repeat_until": 3,
    "default_fallbacks": ["Arial", "Helvetica", "Times New Roman"]
}

# ==================== EXTRA FEATURES ====================
EXTRA_FEATURES = {
    "auto_daily_quote_roast": {
        "enabled": True,
        "daily_time": "12:00",
        "group_post": True,
        "private_post": False
    },
    "user_leaderboard": {
        "enabled": True,
        "tracks": ["most_roasted", "most_reacted", "most_votes"],
        "display_interval": "daily",
        "auto_post": True
    },
    "custom_template_unlocks": {
        "enabled": True,
        "unlock_condition": "votes/activity",
        "notify_user": True
    },
    "festival_event_mode": {
        "enabled": True,
        "themes": ["Pohela Boishakh", "Eid", "Durga Puja", "Christmas", "Halloween", "New Year"],
        "auto_detect": True,
        "special_effects": True
    },
    "reaction_combo": {
        "enabled": True,
        "max_combo_per_message": 3,
        "randomized": True
    },
    "auto_mood_recognition": {
        "enabled": True,
        "analysis_factors": ["text_tone", "emoji_usage", "punctuation", "keyword_patterns"],
        "adjust_roasts": True,
        "notify_user": False
    },
    "safe_forward_share": {
        "enabled": True,
        "strip_personal_info": True,
        "require_admin_for_groups": True
    }
}

# ==================== DEPLOYMENT ====================
DEPLOYMENT = {
    "termux_allowed": False,
    "always_online": True,
    "uptime_requirement": "24/7",
    "auto_restart": True,
    "backup_interval_hours": 6,
    "cleanup_interval_hours": 24,
    "recommended_free_hosting": ["Render", "Railway", "Fly.io", "Koyeb", "PythonAnywhere"]
}

# ==================== PRIVACY AND SAFETY ====================
PRIVACY_AND_SAFETY = {
    "store_user_messages": False,
    "store_votes": True,
    "store_template_stats": True,
    "log_reactions": False,
    "high_privacy_mode": True,
    "data_retention_days": 30,
    "strict_do_not": [
        "Never attack owner/admin",
        "Never use offensive content",
        "Never spam",
        "Never store personal info",
        "Never share user data"
    ]
}

# ==================== DATABASE CONFIG ====================
DATABASE_CONFIG = {
    "path": "data/database.db",
    "backup_interval": 21600,  # 6 hours
    "max_backups": 24,
    "cleanup_days": 30,
    "auto_vacuum": True
}

# ==================== RANDOMIZATION SETTINGS ====================
RANDOMIZATION = {
    "template_selection": True,
    "border_selection": True,
    "font_selection": True,
    "welcome_message": True,
    "response_style": True,
    "roast_phrases": True,
    "emoji_usage": True
}

# ==================== ROAST PHRASES DATABASE ====================
ROAST_PHRASES = {
    "primary": [
        "এত বড় কথা বলার আগে মাথাটা ঠান্ডা করো!",
        "তোমার কথায় লজিকের ছিটেফোঁটাও নেই!",
        "এমন চিন্তা করলে ব্রেন সেল মরে যাবে!",
        "তুমি যেভাবে ভাবছো, বাস্তবতা সেরকম না!",
        "তোমার আত্মবিশ্বাস দেখে তো মনে হচ্ছে!",
        "হুম... একটু ভেবে বলো না!",
        "কথাগুলো আবার চিন্তা করে বলো দেখি!",
        "এবার সত্যি কথা বলো, মিথ্যা কেন?",
        "তোমার যুক্তি শুনে আইনস্টাইনও কাঁদবে!",
        "সহজভাবে বলো, জটিল করো না!"
    ],
    "secondary": [
        "চিন্তা করে বলো, না হলে পরে লজ্জা পাবে!",
        "বুদ্ধি দিয়ে বললে কেউ কিছু বলবে না!",
        "এবার একটু ভেবে চিন্তে উত্তর দাও!",
        "মজা করছি, কিন্তু সত্যি কথাই বলছি!",
        "কথাগুলো মাথায় রেখো, কাজে লাগবে!",
        "এবারের মতো ক্ষমা করলাম, পরেরবার নয়!",
        "একটু সিরিয়াস হও, জীবন রসিকতা নয়!",
        "মাথা ঠান্ডা রেখো, ভালো থেকো!",
        "পরেরবার আরও ভালো উত্তর আশা করছি!",
        "তোমার জন্য শুভকামনা রইল!"
    ]
}

# ==================== PATHS ====================
PATHS = {
    "root": os.path.dirname(os.path.abspath(__file__)),
    "assets": "assets/",
    "fonts": "assets/fonts/",
    "borders": "assets/borders/",
    "templates": "assets/templates/",
    "backgrounds": "assets/backgrounds/",
    "data": "data/",
    "temp": "temp/",
    "logs": "logs/",
    "backups": "backups/"
}

# ==================== LOGGING CONFIG ====================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/bot.log",
    "max_size_mb": 10,
    "backup_count": 5
}

# ==================== COOLDOWN SETTINGS ====================
COOLDOWN_SETTINGS = {
    "message": 2,
    "reaction": 15,
    "vote": 120,
    "mention": 60,
    "admin_response": 120,
    "welcome": 30,
    "leaderboard": 300
}

# ==================== PERFORMANCE SETTINGS ====================
PERFORMANCE = {
    "max_image_size_mb": 5,
    "image_quality": 95,
    "cache_templates": True,
    "cache_fonts": True,
    "cache_borders": True,
    "clean_temp_files_hours": 1,
    "max_temp_files": 100
}

# ==================== ERROR HANDLING ====================
ERROR_HANDLING = {
    "max_retries": 3,
    "retry_delay": 5,
    "notify_owner_on_error": True,
    "auto_recover": True,
    "log_all_errors": True
}

# ==================== BACKUP SETTINGS ====================
BACKUP_SETTINGS = {
    "enabled": True,
    "interval_hours": 6,
    "max_backups": 24,
    "compress": True,
    "notify_on_backup": False
}

# ==================== SECURITY SETTINGS ====================
SECURITY = {
    "max_message_length": 1000,
    "max_username_length": 32,
    "ban_keywords": ["hack", "spam", "scam", "virus", "malware"],
    "rate_limit_per_user": 60,
    "rate_limit_per_chat": 100,
    "block_suspicious_users": True
}

# ==================== BOT BEHAVIOR ====================
BOT_BEHAVIOR = {
    "respond_to_mentions": True,
    "respond_in_groups": True,
    "respond_in_private": True,
    "auto_update_stats": True,
    "send_typing_action": True,
    "delete_temp_files": True,
    "notify_new_features": True
}

# ==================== TESTING MODE ====================
TESTING_MODE = {
    "enabled": False,
    "log_all_messages": False,
    "simulate_only": False,
    "test_user_ids": [],
    "test_chat_ids": []
}

# ==================== UPDATE SETTINGS ====================
UPDATE_SETTINGS = {
    "check_for_updates": True,
    "auto_update": False,
    "notify_owner_updates": True,
    "github_repo": "yourusername/roastify-bot"
}

# ==================== MONETIZATION (Optional) ====================
MONETIZATION = {
    "enabled": False,
    "premium_features": [],
    "donation_links": [],
    "sponsor_message": ""
}

# ==================== API KEYS (For future expansion) ====================
API_KEYS = {
    "openai": "",  # For AI features if added later
    "unsplash": "",  # For background images
    "translate": ""  # For translation features
}

# ==================== VALIDATE CONFIG ====================
def validate_config():
    """Validate configuration on startup"""
    errors = []
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("❌ BOT_TOKEN not set. Get from @BotFather")
    
    if not isinstance(OWNER_ADMIN_PROTECTION["bot_owner_user_id"], int):
        errors.append("❌ bot_owner_user_id must be an integer")
    
    if not all(isinstance(admin_id, int) for admin_id in OWNER_ADMIN_PROTECTION["admin_user_ids"]):
        errors.append("❌ admin_user_ids must contain integers only")
    
    # Validate paths exist
    for path_key, path_value in PATHS.items():
        if path_key != "root":
            full_path = os.path.join(PATHS["root"], path_value)
            if not os.path.exists(full_path):
                try:
                    os.makedirs(full_path, exist_ok=True)
                    print(f"✅ Created directory: {full_path}")
                except Exception as e:
                    errors.append(f"❌ Cannot create directory {full_path}: {e}")
    
    if errors:
        print("\n".join(errors))
        return False
    
    return True

# Validate on import
if __name__ != "__main__":
    validate_config()