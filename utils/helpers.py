"""
Helper functions for Roastify Premium
"""

import re
import random
import string
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib

def generate_random_id(length: int = 8) -> str:
    """Generate random ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def calculate_time_ago(dt: datetime) -> str:
    """Calculate human readable time ago"""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} বছর আগে"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} মাস আগে"
    elif diff.days > 0:
        return f"{diff.days} দিন আগে"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} ঘন্টা আগে"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} মিনিট আগে"
    else:
        return "কিছুক্ষণ আগে"

def format_number(num: int) -> str:
    """Format number with commas"""
    return f"{num:,}"

def create_hash(text: str) -> str:
    """Create hash from text"""
    return hashlib.md5(text.encode()).hexdigest()

def chunk_text(text: str, max_length: int = 2000) -> List[str]:
    """Split text into chunks"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        # Find last space within limit
        split_at = text.rfind(' ', 0, max_length)
        if split_at == -1:
            split_at = max_length
        
        chunks.append(text[:split_at])
        text = text[split_at:].strip()
    
    return chunks

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def is_valid_url(text: str) -> bool:
    """Check if text is a valid URL"""
    url_pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(text))
