#!/usr/bin/env python3
"""
Roastify Bot Configuration Template
Copy this to config.py and update with your values
"""

# ==================== BOT TOKEN ====================
# Get this from @BotFather on Telegram
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ==================== BOT IDENTITY ====================
BOT_IDENTITY = {
    "name": "Roastify",
    "username_suggestions": ["@top_roast_bot"],
    "tagline": "তুমি লেখো, বাকি অপমান আমরা করবো 😈",
    "one_line_pitch": "No-command Bangla roast + 3D graphics image generator with smart social features"
}

# ==================== ADMIN SETTINGS ====================
# Your Telegram user ID (get from @userinfobot)
OWNER_USER_ID = 6454347745  # Replace with your ID

# Additional admin IDs
ADMIN_USER_IDS = []  # Add more admin IDs here

# ==================== DATABASE ====================
DATABASE_PATH = "data/database.db"

# ==================== IMAGE SETTINGS ====================
IMAGE_RESOLUTION = (1080, 1080)
IMAGE_QUALITY = 95

# ==================== TEMPLATES ====================
TEMPLATE_COUNT = 50
TEMPLATE_CATEGORIES = {
    "cartoon_roast": 12,
    "neon_savage": 10,
    "dark_sarcastic": 8,
    "minimal_mock": 8,
    "poster_style": 12
}

# ==================== RANDOMIZATION ====================
RANDOMIZATION_SETTINGS = {
    "templates": True,
    "borders": True,
    "fonts": True,
    "welcome_messages": True,
    "reactions": True
}

# ==================== COOLDOWNS ====================
COOLDOWN_SETTINGS = {
    "message": 2,  # seconds
    "reaction": 15,  # seconds
    "vote": 120,  # seconds
    "mention": 60,  # seconds
    "admin_response": 120  # seconds
}

# ==================== PATHS ====================
PATHS = {
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

# Add other configuration sections from the main config.py as needed
# Copy from config.py and paste here