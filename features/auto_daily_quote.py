#!/usr/bin/env python3
"""
Auto Daily Quote System for Roastify Bot
Posts daily roast quotes automatically
"""

import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, time
from telegram import Update
from telegram.ext import ContextTypes, JobQueue
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import EXTRA_FEATURES
    from utils.image_generator import ImageGenerator
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class AutoDailyQuote:
    """Manages automatic daily quote posting"""
    
    def __init__(self, job_queue: JobQueue = None):
        """Initialize auto daily quote system"""
        self.config = EXTRA_FEATURES.get("auto_daily_quote_roast", {})
        self.job_queue = job_queue
        self.image_gen = ImageGenerator()
        
        # Daily quotes database
        self.daily_quotes = self._load_quotes()
        
        # Track posted quotes
        self.posted_quotes = []
        
        # Schedule jobs if enabled
        if self.config.get("enabled", False) and job_queue:
            self._schedule_jobs()
        
        logger.info("Auto Daily Quote system initialized")
    
    def _load_quotes(self) -> List[Dict]:
        """Load daily quotes"""
        quotes = [
            {
                "quote": "যারা সবসময় হাসে, তাদের রোস্ট খেতেও মজা লাগে! 😂",
                "author": "রোস্ট মাস্টার",
                "category": "funny"
            },
            {
                "quote": "রাগ করলে রোস্টের স্বাদ বাড়ে, শান্ত থাকলে মজা কমে! 😈",
                "author": "রোস্ট গুরু",
                "category": "savage"
            },
            {
                "quote": "প্রতিদিন একটা রোস্ট, মন ভালো রাখবে অফুরন্ত! 🎯",
                "author": "রোস্টিফাই",
                "category": "motivation"
            },
            {
                "quote": "রোস্ট খাওয়ার সময় কেউ যদি বিরক্ত হয়, তাদেরকেও রোস্ট দাও! 🔥",
                "author": "রোস্ট রাজা",
                "category": "attitude"
            },
            {
                "quote": "হাসতে হাসতে রোস্ট খাও, জীবন সুন্দর হয়ে যাবে! ✨",
                "author": "রোস্ট ম্যাজিক",
                "category": "positive"
            },
            {
                "quote": "রোস্ট শুধু অপমান নয়, মজার মাধ্যমে শিক্ষা! 📚",
                "author": "রোস্ট অধ্যাপক",
                "category": "wisdom"
            },
            {
                "quote": "যে রোস্ট খেতে পারে, সে জীবনেও সব সামলাতে পারে! 💪",
                "author": "রোস্ট যোদ্ধা",
                "category": "inspiration"
            },
            {
                "quote": "রোজ একটু রোস্ট, মন ভালো আর দেহ ফ্রেশ! 🌟",
                "author": "রোস্ট ডাক্তার",
                "category": "health"
            },
            {
                "quote": "রোস্টের ভয় পেলে জীবনে এগুতে পারবে না! 🚀",
                "author": "রোস্ট ফিলোসফার",
                "category": "philosophy"
            },
            {
                "quote": "মজা করে রোস্ট খাও, গম্ভীর হয়ে রাগ কোরো না! 😊",
                "author": "রোস্ট বন্ধু",
                "category": "friendly"
            }
        ]
        
        # Load from file if exists
        import os
        quotes_file = "data/daily_quotes.json"
        if os.path.exists(quotes_file):
            try:
                import json
                with open(quotes_file, 'r', encoding='utf-8') as f:
                    file_quotes = json.load(f)
                    quotes.extend(file_quotes)
            except Exception as e:
                logger.error(f"Error loading quotes file: {e}")
        
        return quotes
    
    def _schedule_jobs(self):
        """Schedule daily quote jobs"""
        try:
            # Parse time from config
            post_time = self.config.get("daily_time", "12:00")
            hour, minute = map(int, post_time.split(':'))
            
            # Schedule job
            self.job_queue.run_daily(
                self._post_daily_quote,
                time=time(hour=hour, minute=minute, tzinfo=None),
                name="daily_quote"
            )
            
            logger.info(f"Scheduled daily quote at {post_time}")
            
        except Exception as e:
            logger.error(f"Error scheduling jobs: {e}")
    
    async def _post_daily_quote(self, context: ContextTypes.DEFAULT_TYPE):
        """Post daily quote to all registered chats"""
        try:
            # Get quote
            quote = self._get_daily_quote()
            if not quote:
                logger.warning("No quote available")
                return
            
            # Generate quote image
            image_path = await self._generate_quote_image(quote)
            
            # Prepare message
            message = f"""
📅 <b>দৈনিক রোস্ট উক্তি</b> 📅
━━━━━━━━━━━━━━━━━━━━

"{quote['quote']}"

- <i>{quote['author']}</i>

━━━━━━━━━━━━━━━━━━━━
🎯 আজকের থিম: {quote['category']}
⏰ সময়: {datetime.now().strftime("%H:%M")}
            """
            
            # Post to groups if enabled
            if self.config.get("group_post", True):
                await self._post_to_all_groups(context, message, image_path)
            
            # Post to private if enabled
            if self.config.get("private_post", False):
                await self._post_to_subscribed_users(context, message, image_path)
            
            # Cleanup
            if image_path:
                import os
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            logger.info("Posted daily quote")
            
        except Exception as e:
            logger.error(f"Error posting daily quote: {e}")
    
    def _get_daily_quote(self) -> Optional[Dict]:
        """Get a quote that hasn't been posted recently"""
        # Filter out recently posted quotes
        available = [q for q in self.daily_quotes 
                    if q not in self.posted_quotes[-30:]]  # Last 30 days
        
        if not available:
            # Reset if all quotes used recently
            self.posted_quotes.clear()
            available = self.daily_quotes
        
        # Select random quote
        quote = random.choice(available)
        
        # Add to posted list
        self.posted_quotes.append(quote)
        
        return quote
    
    async def _generate_quote_image(self, quote: Dict) -> Optional[str]:
        """Generate image for quote"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # Create image
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (25, 25, 112))  # Midnight blue
            
            draw = ImageDraw.Draw(image)
            
            # Load font
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 60)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 40)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 30)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Title
            title = "📅 দৈনিক রোস্ট উক্তি 📅"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 80), title, font=font_large, fill=(255, 215, 0))
            
            # Quote text (wrapped)
            quote_text = f'"{quote["quote"]}"'
            wrapped_lines = self._wrap_text(draw, quote_text, font_medium, width - 200)
            
            y_offset = 200
            for line in wrapped_lines:
                line_bbox = draw.textbbox((0, 0), line, font=font_medium)
                line_width = line_bbox[2] - line_bbox[0]
                line_x = (width - line_width) // 2
                draw.text((line_x, y_offset), line, font=font_medium, fill=(255, 255, 255))
                y_offset += 60
            
            # Author
            author_text = f"- {quote['author']}"
            author_bbox = draw.textbbox((0, 0), author_text, font=font_medium)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = (width - author_width) // 2
            draw.text((author_x, y_offset + 40), author_text, font=font_medium, fill=(255, 105, 180))
            
            # Category and time
            info_y = height - 150
            category_text = f"থিম: {quote['category']}"
            time_text = f"সময়: {datetime.now().strftime('%H:%M')}"
            
            draw.text((100, info_y), category_text, font=font_small, fill=(200, 200, 200))
            draw.text((width - 300, info_y), time_text, font=font_small, fill=(200, 200, 200))
            
            # Footer
            footer = "রোস্টিফাই বট - রোজ নতুন রোস্ট!"
            footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
            footer_width = footer_bbox[2] - footer_bbox[0]
            footer_x = (width - footer_width) // 2
            draw.text((footer_x, height - 80), footer, font=font_small, fill=(150, 150, 150))
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"daily_quote_{datetime.now().strftime('%Y%m%d')}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating quote image: {e}")
            return None
    
    def _wrap_text(self, draw: ImageDraw, text: str, font: ImageFont, 
                  max_width: int) -> List[str]:
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    async def _post_to_all_groups(self, context: ContextTypes.DEFAULT_TYPE, 
                                 message: str, image_path: str = None):
        """Post to all groups the bot is in"""
        # This would require storing group IDs in database
        # For now, this is a placeholder
        pass
    
    async def _post_to_subscribed_users(self, context: ContextTypes.DEFAULT_TYPE, 
                                       message: str, image_path: str = None):
        """Post to subscribed users"""
        # This would require storing user subscriptions in database
        # For now, this is a placeholder
        pass
    
    async def manual_post_quote(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Manually post daily quote to specific chat"""
        try:
            quote = self._get_daily_quote()
            if not quote:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="❌ আজকের জন্য কোনো উক্তি নেই!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Generate image
            image_path = await self._generate_quote_image(quote)
            
            # Prepare message
            message = f"""
📅 <b>দৈনিক রোস্ট উক্তি</b> 📅
━━━━━━━━━━━━━━━━━━━━

"{quote['quote']}"

- <i>{quote['author']}</i>

━━━━━━━━━━━━━━━━━━━━
🎯 থিম: {quote['category']}
            """
            
            # Send message
            if image_path:
                with open(image_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=message,
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                import os
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=ParseMode.HTML
                )
            
            logger.info(f"Manually posted quote to chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error manually posting quote: {e}")
    
    def add_quote(self, quote: str, author: str, category: str = "general") -> bool:
        """Add new quote to database"""
        try:
            new_quote = {
                "quote": quote,
                "author": author,
                "category": category,
                "added_date": datetime.now().isoformat()
            }
            
            self.daily_quotes.append(new_quote)
            
            # Save to file
            import json
            quotes_file = "data/daily_quotes.json"
            
            # Load existing quotes from file
            file_quotes = []
            import os
            if os.path.exists(quotes_file):
                with open(quotes_file, 'r', encoding='utf-8') as f:
                    file_quotes = json.load(f)
            
            # Add new quote
            file_quotes.append(new_quote)
            
            # Save back to file
            with open(quotes_file, 'w', encoding='utf-8') as f:
                json.dump(file_quotes, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Added new quote by {author}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding quote: {e}")
            return False
    
    def get_quote_stats(self) -> Dict[str, Any]:
        """Get quote statistics"""
        return {
            "total_quotes": len(self.daily_quotes),
            "posted_recently": len(self.posted_quotes),
            "categories": list(set(q["category"] for q in self.daily_quotes))
        }