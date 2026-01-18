#!/usr/bin/env python3
"""
Helper Functions for Roastify Bot
Various utility functions used throughout the bot
"""

import os
import sys
import json
import random
import string
import logging
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Helpers:
    """Collection of helper functions"""
    
    @staticmethod
    def generate_id(length: int = 8) -> str:
        """Generate random ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp as string"""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_time_delta(seconds: int) -> str:
        """Format seconds to human readable time"""
        if seconds < 60:
            return f"{seconds} সেকেন্ড"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} মিনিট"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} ঘন্টা"
        else:
            days = seconds // 86400
            return f"{days} দিন"
    
    @staticmethod
    def safe_filename(text: str, max_length: int = 50) -> str:
        """Convert text to safe filename"""
        # Remove unsafe characters
        safe = ''.join(c for c in text if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        # Replace spaces with underscores
        safe = safe.replace(' ', '_')
        
        # Limit length
        if len(safe) > max_length:
            safe = safe[:max_length]
        
        return safe
    
    @staticmethod
    def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        
        # Try to break at word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.7:
            truncated = truncated[:last_space]
        
        return truncated.rstrip() + ellipsis
    
    @staticmethod
    def parse_duration(duration_str: str) -> Optional[int]:
        """Parse duration string to seconds"""
        try:
            if not duration_str:
                return None
            
            # Remove whitespace
            duration_str = duration_str.strip().lower()
            
            # Parse different formats
            if duration_str.endswith('s'):
                return int(duration_str[:-1])
            elif duration_str.endswith('m'):
                return int(duration_str[:-1]) * 60
            elif duration_str.endswith('h'):
                return int(duration_str[:-1]) * 3600
            elif duration_str.endswith('d'):
                return int(duration_str[:-1]) * 86400
            else:
                # Try to parse as integer seconds
                return int(duration_str)
                
        except ValueError:
            return None
    
    @staticmethod
    def calculate_md5(filepath: str) -> Optional[str]:
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating MD5: {e}")
            return None
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False
    
    @staticmethod
    def clean_temp_files(temp_dir: str, max_age_hours: int = 24):
        """Clean old temporary files"""
        try:
            current_time = datetime.now()
            
            for filename in os.listdir(temp_dir):
                filepath = os.path.join(temp_dir, filename)
                
                if os.path.isfile(filepath):
                    # Get file creation/modification time
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    # Check if file is old
                    if (current_time - file_time).total_seconds() > max_age_hours * 3600:
                        try:
                            os.remove(filepath)
                            logger.debug(f"Cleaned temp file: {filename}")
                        except Exception as e:
                            logger.error(f"Error removing temp file {filename}: {e}")
                            
        except Exception as e:
            logger.error(f"Error cleaning temp files: {e}")
    
    @staticmethod
    def load_json(filepath: str, default: Any = None) -> Any:
        """Load JSON file with error handling"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON {filepath}: {e}")
        
        return default
    
    @staticmethod
    def save_json(filepath: str, data: Any, indent: int = 2) -> bool:
        """Save data to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"Error saving JSON {filepath}: {e}")
            return False
    
    @staticmethod
    def format_number(num: Union[int, float]) -> str:
        """Format number with Bengali suffixes"""
        if num < 1000:
            return str(num)
        elif num < 100000:
            return f"{num/1000:.1f} হাজার"
        elif num < 10000000:
            return f"{num/100000:.1f} লাখ"
        else:
            return f"{num/10000000:.1f} কোটি"
    
    @staticmethod
    def get_random_color() -> Tuple[int, int, int]:
        """Generate random RGB color"""
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    @staticmethod
    def get_random_pastel_color() -> Tuple[int, int, int]:
        """Generate random pastel color"""
        return (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
    
    @staticmethod
    def get_random_dark_color() -> Tuple[int, int, int]:
        """Generate random dark color"""
        return (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )
    
    @staticmethod
    def get_contrast_color(bg_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get contrasting text color for background"""
        # Calculate luminance
        luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]) / 255
        
        # Return black or white based on luminance
        if luminance > 0.5:
            return (0, 0, 0)  # Black
        else:
            return (255, 255, 255)  # White
    
    @staticmethod
    def chunk_list(lst: List, chunk_size: int) -> List[List]:
        """Split list into chunks"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def flatten_list(lst: List[List]) -> List:
        """Flatten nested list"""
        return [item for sublist in lst for item in sublist]
    
    @staticmethod
    def remove_duplicates_preserve_order(lst: List) -> List:
        """Remove duplicates while preserving order"""
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]
    
    @staticmethod
    def get_file_size(filepath: str) -> Optional[str]:
        """Get human readable file size"""
        try:
            size = os.path.getsize(filepath)
            
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            
            return f"{size:.1f} TB"
        except Exception as e:
            logger.error(f"Error getting file size: {e}")
            return None
    
    @staticmethod
    def is_valid_url(text: str) -> bool:
        """Check if text is a valid URL"""
        import re
        
        url_pattern = re.compile(
            r'^(https?://)?'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(text))
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        import re
        
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.findall(text)
    
    @staticmethod
    def get_bangla_number(num: int) -> str:
        """Convert number to Bengali numerals"""
        bengali_digits = {
            '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
            '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
        }
        
        num_str = str(num)
        bengali_str = ''.join(bengali_digits.get(digit, digit) for digit in num_str)
        
        return bengali_str
    
    @staticmethod
    def get_random_bangla_quote() -> str:
        """Get random Bengali quote"""
        quotes = [
            "যতক্ষণ শ্বাস, ততক্ষণ আশ।",
            "পরিশ্রম সৌভাগ্যের প্রসূতি।",
            "জ্ঞান অর্জনের কোনো শেষ নেই।",
            "সময়ের এক ফোঁড়, অসময়ের দশ ফোঁড়।",
            "যা ভালো তার জন্য অপেক্ষা করুন।",
            "সাফল্য আসে ধৈর্য্যের সঙ্গে।",
            "ভালোবাসা সব বাধা দূর করে।",
            "আত্মবিশ্বাসই সফলতার চাবিকাঠি।",
            "ছোট ছোট বিন্দুই সাগর সৃষ্টি করে।",
            "আশা হারালেই সব শেষ।"
        ]
        
        return random.choice(quotes)
    
    @staticmethod
    def get_random_encouragement() -> str:
        """Get random encouragement message in Bengali"""
        encouragements = [
            "তুমি পারবে! 💪",
            "একটু চেষ্টা করো! ✨",
            "হাল ছাড়ো না! 🌟",
            "সফলতা তোমার জন্য অপেক্ষা করছে! 🏆",
            "আত্মবিশ্বাস রাখো! 😎",
            "একদিন সফল হবেই! 🚀",
            "মাথা উঁচু করে চলো! 👑",
            "পরিশ্রম কখনো ব্যর্থ হয় না! 🔥",
            "ভালো কাজ চালিয়ে যাও! 👍",
            "তোমার মধ্যে অনেক সম্ভাবনা! 💫"
        ]
        
        return random.choice(encouragements)
    
    @staticmethod
    def create_progress_bar(percentage: float, width: int = 20) -> str:
        """Create ASCII progress bar"""
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def calculate_percentage(part: int, whole: int) -> float:
        """Calculate percentage"""
        if whole == 0:
            return 0.0
        return (part / whole) * 100
    
    @staticmethod
    def mask_string(text: str, visible_chars: int = 4) -> str:
        """Mask string for privacy"""
        if len(text) <= visible_chars:
            return text
        
        masked = text[:visible_chars] + "*" * (len(text) - visible_chars)
        return masked
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate random password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        import re
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information"""
        import platform
        import psutil
        
        info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage('/')._asdict()
        }
        
        return info
    
    @staticmethod
    def backup_file(filepath: str, backup_dir: str = "backups") -> Optional[str]:
        """Create backup of a file"""
        try:
            if not os.path.exists(filepath):
                return None
            
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filename}.backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Copy file
            import shutil
            shutil.copy2(filepath, backup_path)
            
            logger.info(f"Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    @staticmethod
    def rotate_backups(backup_dir: str, max_backups: int = 10):
        """Rotate old backups"""
        try:
            if not os.path.exists(backup_dir):
                return
            
            # Get all backup files
            backups = []
            for filename in os.listdir(backup_dir):
                if filename.endswith('.backup'):
                    filepath = os.path.join(backup_dir, filename)
                    backups.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (oldest first)
            backups.sort(key=lambda x: x[1])
            
            # Remove old backups
            while len(backups) > max_backups:
                oldest = backups.pop(0)
                try:
                    os.remove(oldest[0])
                    logger.debug(f"Removed old backup: {oldest[0]}")
                except Exception as e:
                    logger.error(f"Error removing backup {oldest[0]}: {e}")
                    
        except Exception as e:
            logger.error(f"Error rotating backups: {e}")