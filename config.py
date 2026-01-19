"""
Premium Configuration for Roastify Bot v15.0
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

# Bot Identity
BOT_IDENTITY = {
    "name": "Roastify Premium",
    "tagline": "Ultimate Roasting Experience v15.0",
    "version": "15.0.0",
    "edition": "Premium",
    "developer": "Roastify Team",
    "website": "https://roastify.example.com",
    "support": "@roastify_support"
}

# Bot Token (Set in .env)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Core Rules
CORE_RULES = {
    "minimum_input_length": 3,
    "maximum_input_length": 1000,
    "cooldown_seconds": 2,
    "diagram_reply": True,
    "text_reply": True,
    "image_quality": 95,
    "premium_features": True,
    "cache_enabled": True,
    "cache_ttl_hours": 24,
    "max_cache_size": 5000,
    "rate_limit_per_minute": 30,
    "auto_cleanup_hours": 24
}

# Admin Protection
OWNER_ADMIN_PROTECTION = {
    "bot_owner_user_id": 123456789,  # Replace with your ID
    "admin_user_ids": [123456789],   # Add admin IDs
    "moderator_ids": [],             # Moderator IDs
    "protected_words": ["admin", "owner", "moderator", "developer"],
    "enable_protection": True,
    "protection_response": "⚠️ This action is protected."
}

# Premium Settings
PREMIUM_CONFIG = {
    "default_theme": "diamond",
    "available_themes": ["diamond", "neo", "gold", "silver", "platinum", "royal", "galaxy"],
    "max_badges_display": 10,
    "card_quality": 100,
    "enable_ai_analytics": True,
    "enable_blockchain": True,
    "enable_dashboard": True,
    "enable_reports": True,
    "enable_user_cards": True,
    "auto_generate_cards": True,
    "premium_cooldown_reduction": 0.5,  # 50% faster
    "max_premium_users": 1000
}

# Image Generation Settings
IMAGE_CONFIG = {
    "default_width": 1200,
    "default_height": 1200,
    "quality": 100,
    "format": "PNG",
    "enable_watermark": True,
    "watermark_text": "Roastify Premium v15.0",
    "watermark_opacity": 30,
    "max_file_size_mb": 10
}

# Database Settings
DATABASE_CONFIG = {
    "type": "sqlite",  # sqlite, json, or postgresql
    "path": "database/roastify.db",
    "backup_interval_hours": 24,
    "max_backups": 30
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/roastify.log",
    "max_file_size_mb": 10,
    "backup_count": 5
}

# API Settings (if needed)
API_CONFIG = {
    "enable_api": False,
    "api_host": "0.0.0.0",
    "api_port": 8000,
    "api_key_required": True,
    "rate_limit_per_ip": 100
}

# Theme Colors
THEME_COLORS = {
    "diamond": {"primary": "#FFD700", "secondary": "#FFFFFF", "bg": ["#0F2027", "#203A43", "#2C5364"]},
    "neo": {"primary": "#00FFFF", "secondary": "#FF00FF", "bg": ["#000428", "#004e92", "#000428"]},
    "gold": {"primary": "#FFD700", "secondary": "#FFA500", "bg": ["#1A1A1A", "#333333", "#1A1A1A"]},
    "silver": {"primary": "#C0C0C0", "secondary": "#E8E8E8", "bg": ["#2B2B2B", "#4A4A4A", "#2B2B2B"]}
}

# Achievement System
ACHIEVEMENTS = {
    "first_roast": {"name": "First Roast", "xp": 100},
    "roast_master": {"name": "Roast Master", "xp": 1000, "requirement": 100},
    "popular": {"name": "Popular", "xp": 500, "requirement": 500},
    "veteran": {"name": "Veteran", "xp": 1000, "requirement": 1000},
    "legend": {"name": "Legend", "xp": 5000, "requirement": 5000}
}
