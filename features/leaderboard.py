#!/usr/bin/env python3
"""
Leaderboard System for Roastify Bot
Tracks user statistics and generates leaderboards
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import EXTRA_FEATURES
    from database import get_database
    from utils.image_generator import ImageGenerator
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class Leaderboard:
    """Manages user leaderboards and statistics"""
    
    def __init__(self):
        """Initialize leaderboard system"""
        self.config = EXTRA_FEATURES.get("user_leaderboard", {})
        self.db = get_database()
        self.image_gen = ImageGenerator()
        
        # Leaderboard types
        self.leaderboard_types = {
            "most_roasted": "সবচেয়ে বেশি রোস্ট খেয়েছে",
            "most_roasts_sent": "সবচেয়ে বেশি রোস্ট দিয়েছে",
            "most_reacted": "সবচেয়ে বেশি রিঅ্যাকশন পেয়েছে",
            "most_votes": "সবচেয়ে বেশি ভোট পেয়েছে",
            "most_active": "সবচেয়ে বেশি একটিভ"
        }
        
        # Cache for leaderboard data
        self.leaderboard_cache = {}
        self.cache_timeout = 300  # 5 minutes
        
        logger.info("Leaderboard System initialized")
    
    async def get_leaderboard(self, leaderboard_type: str = "most_roasted", 
                             period: str = "all_time", limit: int = 10) -> List[Dict]:
        """Get leaderboard data"""
        try:
            cache_key = f"{leaderboard_type}_{period}_{limit}"
            
            # Check cache
            if cache_key in self.leaderboard_cache:
                cached_data, cached_time = self.leaderboard_cache[cache_key]
                if (datetime.now() - cached_time).seconds < self.cache_timeout:
                    return cached_data
            
            # Get data from database
            data = await self._fetch_leaderboard_data(leaderboard_type, period, limit)
            
            # Cache the results
            self.leaderboard_cache[cache_key] = (data, datetime.now())
            
            # Clean old cache entries
            self._clean_cache()
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    async def _fetch_leaderboard_data(self, leaderboard_type: str, 
                                     period: str, limit: int) -> List[Dict]:
        """Fetch leaderboard data from database"""
        try:
            if leaderboard_type == "most_roasted":
                return await self._get_most_roasted(period, limit)
            elif leaderboard_type == "most_roasts_sent":
                return await self._get_most_roasts_sent(period, limit)
            elif leaderboard_type == "most_reacted":
                return await self._get_most_reacted(period, limit)
            elif leaderboard_type == "most_votes":
                return await self._get_most_votes(period, limit)
            elif leaderboard_type == "most_active":
                return await self._get_most_active(period, limit)
            else:
                return await self._get_most_roasted(period, limit)
                
        except Exception as e:
            logger.error(f"Error fetching leaderboard data: {e}")
            return []
    
    async def _get_most_roasted(self, period: str, limit: int) -> List[Dict]:
        """Get users with most roasts received"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, first_name, roast_count
                FROM users
                WHERE roast_count > 0
                ORDER BY roast_count DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.db.cursor.fetchall()
            
            leaderboard_data = []
            for i, (user_id, username, first_name, roast_count) in enumerate(results, 1):
                leaderboard_data.append({
                    'rank': i,
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'score': roast_count,
                    'metric': 'রোস্ট খেয়েছে'
                })
            
            return leaderboard_data
            
        except Exception as e:
            logger.error(f"Error getting most roasted: {e}")
            return []
    
    async def _get_most_roasts_sent(self, period: str, limit: int) -> List[Dict]:
        """Get users with most roasts sent"""
        # This requires tracking roasts sent, which we need to add to database
        # For now, return placeholder
        return []
    
    async def _get_most_reacted(self, period: str, limit: int) -> List[Dict]:
        """Get users with most reactions received"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, first_name, reaction_count
                FROM users
                WHERE reaction_count > 0
                ORDER BY reaction_count DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.db.cursor.fetchall()
            
            leaderboard_data = []
            for i, (user_id, username, first_name, reaction_count) in enumerate(results, 1):
                leaderboard_data.append({
                    'rank': i,
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'score': reaction_count,
                    'metric': 'রিঅ্যাকশন পেয়েছে'
                })
            
            return leaderboard_data
            
        except Exception as e:
            logger.error(f"Error getting most reacted: {e}")
            return []
    
    async def _get_most_votes(self, period: str, limit: int) -> List[Dict]:
        """Get users with most votes received"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, first_name, vote_count
                FROM users
                WHERE vote_count > 0
                ORDER BY vote_count DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.db.cursor.fetchall()
            
            leaderboard_data = []
            for i, (user_id, username, first_name, vote_count) in enumerate(results, 1):
                leaderboard_data.append({
                    'rank': i,
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'score': vote_count,
                    'metric': 'ভোট পেয়েছে'
                })
            
            return leaderboard_data
            
        except Exception as e:
            logger.error(f"Error getting most votes: {e}")
            return []
    
    async def _get_most_active(self, period: str, limit: int) -> List[Dict]:
        """Get most active users based on last activity"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, first_name, 
                       julianday('now') - julianday(last_active) as days_since_active,
                       roast_count + vote_count + reaction_count as total_score
                FROM users
                WHERE last_active IS NOT NULL
                ORDER BY days_since_active ASC, total_score DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.db.cursor.fetchall()
            
            leaderboard_data = []
            for i, (user_id, username, first_name, days_since, total_score) in enumerate(results, 1):
                leaderboard_data.append({
                    'rank': i,
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'score': total_score,
                    'metric': 'একটিভ স্কোর',
                    'days_since_active': round(days_since, 1)
                })
            
            return leaderboard_data
            
        except Exception as e:
            logger.error(f"Error getting most active: {e}")
            return []
    
    def _clean_cache(self):
        """Clean old cache entries"""
        try:
            current_time = datetime.now()
            keys_to_remove = []
            
            for key, (_, cached_time) in self.leaderboard_cache.items():
                if (current_time - cached_time).seconds > self.cache_timeout * 2:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.leaderboard_cache[key]
            
            if keys_to_remove:
                logger.debug(f"Cleaned {len(keys_to_remove)} cache entries")
                
        except Exception as e:
            logger.error(f"Error cleaning cache: {e}")
    
    async def generate_leaderboard_image(self, leaderboard_type: str = "most_roasted",
                                        period: str = "all_time", 
                                        limit: int = 10) -> Optional[str]:
        """Generate leaderboard image"""
        try:
            # Get leaderboard data
            data = await self.get_leaderboard(leaderboard_type, period, limit)
            
            if not data:
                return None
            
            # Get leaderboard title
            title = self.leaderboard_types.get(leaderboard_type, "লিডারবোর্ড")
            
            # Create image data
            image_data = {
                "title": title,
                "period": period,
                "data": data,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Generate image
            image_path = await self.image_gen.generate_diagram_image(image_data)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error generating leaderboard image: {e}")
            return None
    
    async def post_daily_leaderboard(self, chat_id: int, 
                                     context: ContextTypes.DEFAULT_TYPE):
        """Post daily leaderboard to chat"""
        try:
            # Check if enabled
            if not self.config.get("enabled", True):
                return
            
            # Check display interval
            display_interval = self.config.get("display_interval", "daily")
            if display_interval != "daily":
                return
            
            # Generate leaderboard image
            image_path = await self.generate_leaderboard_image(
                "most_roasted", "daily", 10
            )
            
            if not image_path:
                return
            
            # Prepare message
            message = f"""
🏆 <b>দৈনিক লিডারবোর্ড</b> 🏆
━━━━━━━━━━━━━━━━━━━━
আজকে যারা সবচেয়ে বেশি রোস্ট খেয়েছে!
তোমার নাম দেখতে চাও? আরও রোস্ট খাও! 😈

<i>আপডেট: {datetime.now().strftime("%H:%M")}</i>
            """
            
            # Send to chat
            with open(image_path, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=message,
                    parse_mode=ParseMode.HTML
                )
            
            # Cleanup temp file
            import os
            if os.path.exists(image_path):
                os.remove(image_path)
            
            logger.info(f"Posted daily leaderboard to chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error posting daily leaderboard: {e}")
    
    async def handle_leaderboard_command(self, update: Update, 
                                         context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        try:
            user = update.effective_user
            chat = update.effective_chat
            
            # Parse arguments
            args = context.args
            leaderboard_type = "most_roasted"
            period = "all_time"
            
            if args:
                if args[0] in self.leaderboard_types:
                    leaderboard_type = args[0]
                
                if len(args) > 1:
                    period = args[1]
            
            # Create inline keyboard for leaderboard types
            keyboard = []
            row = []
            
            for i, (lb_type, lb_name) in enumerate(self.leaderboard_types.items(), 1):
                callback_data = f"leaderboard_{lb_type}_{period}"
                button_text = lb_name.split()[-1]  # Last word
                
                row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
                
                if i % 3 == 0:
                    keyboard.append(row)
                    row = []
            
            if row:
                keyboard.append(row)
            
            # Add period selection
            period_keyboard = [
                [
                    InlineKeyboardButton("সব সময়", callback_data=f"leaderboard_{leaderboard_type}_all_time"),
                    InlineKeyboardButton("সাপ্তাহিক", callback_data=f"leaderboard_{leaderboard_type}_weekly"),
                    InlineKeyboardButton("দৈনিক", callback_data=f"leaderboard_{leaderboard_type}_daily")
                ]
            ]
            
            keyboard.extend(period_keyboard)
            
            # Generate leaderboard image
            image_path = await self.generate_leaderboard_image(
                leaderboard_type, period, 10
            )
            
            if image_path:
                with open(image_path, 'rb') as photo:
                    message = await update.message.reply_photo(
                        photo=photo,
                        caption=f"<b>{self.leaderboard_types[leaderboard_type]}</b>\n\nলোড হচ্ছে...",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                import os
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                message = await update.message.reply_text(
                    f"<b>{self.leaderboard_types[leaderboard_type]}</b>\n\nলিডারবোর্ড ডাটা লোড হচ্ছে...",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.HTML
                )
            
            # Store message ID for updates
            context.user_data["leaderboard_message_id"] = message.message_id
            
        except Exception as e:
            logger.error(f"Error handling leaderboard command: {e}")
            await update.message.reply_text(
                "লিডারবোর্ড দেখাতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    async def handle_leaderboard_callback(self, update: Update, 
                                          context: ContextTypes.DEFAULT_TYPE):
        """Handle leaderboard callback queries"""
        try:
            query = update.callback_query
            data = query.data
            
            # Parse callback data
            parts = data.split('_')
            
            if len(parts) < 3:
                await query.answer("Invalid data!")
                return
            
            leaderboard_type = parts[1]
            period = parts[2]
            
            # Generate updated leaderboard
            image_path = await self.generate_leaderboard_image(
                leaderboard_type, period, 10
            )
            
            if image_path:
                with open(image_path, 'rb') as photo:
                    # Update message with new photo
                    await query.message.edit_media(
                        media=InputMediaPhoto(
                            media=photo,
                            caption=f"<b>{self.leaderboard_types.get(leaderboard_type, 'লিডারবোর্ড')}</b>\n\nপিরিয়ড: {period}"
                        ),
                        reply_markup=query.message.reply_markup
                    )
                
                # Cleanup
                import os
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                # Update just the caption
                await query.message.edit_caption(
                    caption=f"<b>{self.leaderboard_types.get(leaderboard_type, 'লিডারবোর্ড')}</b>\n\nপিরিয়ড: {period}\n\nডাটা পাওয়া যায়নি!",
                    reply_markup=query.message.reply_markup
                )
            
            await query.answer(f"{self.leaderboard_types.get(leaderboard_type, 'লিডারবোর্ড')} লোড করা হলো!")
            
        except Exception as e:
            logger.error(f"Error handling leaderboard callback: {e}")
            await query.answer("আপডেট করতে সমস্যা! 😢")
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get detailed statistics for a user"""
        try:
            self.db.cursor.execute('''
                SELECT username, first_name, last_name,
                       roast_count, vote_count, reaction_count,
                       last_active, created_at
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            result = self.db.cursor.fetchone()
            
            if not result:
                return {"error": "User not found"}
            
            (username, first_name, last_name, roast_count, 
             vote_count, reaction_count, last_active, created_at) = result
            
            # Calculate additional stats
            total_score = roast_count + vote_count + reaction_count
            
            # Get rank in most roasted
            self.db.cursor.execute('''
                SELECT COUNT(*) + 1
                FROM users
                WHERE roast_count > ?
            ''', (roast_count,))
            
            roast_rank = self.db.cursor.fetchone()[0]
            
            # Format dates
            if last_active:
                last_active_str = datetime.fromisoformat(last_active).strftime("%Y-%m-%d %H:%M")
            else:
                last_active_str = "কখনো না"
            
            if created_at:
                created_str = datetime.fromisoformat(created_at).strftime("%Y-%m-%d")
            else:
                created_str = "অজানা"
            
            return {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "stats": {
                    "roast_count": roast_count,
                    "roast_rank": roast_rank,
                    "vote_count": vote_count,
                    "reaction_count": reaction_count,
                    "total_score": total_score
                },
                "activity": {
                    "last_active": last_active_str,
                    "member_since": created_str
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {"error": str(e)}
    
    async def generate_user_stats_image(self, user_id: int) -> Optional[str]:
        """Generate image with user statistics"""
        try:
            # Get user stats
            stats = await self.get_user_stats(user_id)
            
            if "error" in stats:
                return None
            
            # Create image
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (25, 25, 112))  # Midnight blue
            
            draw = ImageDraw.Draw(image)
            
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 60)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 40)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 30)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # User info
            user_name = stats["first_name"]
            if stats["username"]:
                user_name += f" (@{stats['username']})"
            
            # Title
            title = f"{user_name} - স্ট্যাটিস্টিকস"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 50), title, font=font_large, fill=(255, 215, 0))
            
            # Stats
            y_offset = 180
            stats_texts = [
                f"রোস্ট খেয়েছে: {stats['stats']['roast_count']} (র‌্য‌াংক #{stats['stats']['roast_rank']})",
                f"ভোট পেয়েছে: {stats['stats']['vote_count']}",
                f"রিঅ্যাকশন পেয়েছে: {stats['stats']['reaction_count']}",
                f"টোটাল স্কোর: {stats['stats']['total_score']}",
                "",
                f"শেষ একটিভ: {stats['activity']['last_active']}",
                f"সদস্য শুরু: {stats['activity']['member_since']}"
            ]
            
            for text in stats_texts:
                if text:  # Skip empty lines
                    draw.text((100, y_offset), text, font=font_medium, fill=(220, 220, 255))
                    y_offset += 60
                else:
                    y_offset += 30
            
            # Draw score bars
            y_offset += 30
            max_score = max(stats['stats']['roast_count'], 
                           stats['stats']['vote_count'],
                           stats['stats']['reaction_count'],
                           1)  # Prevent division by zero
            
            # Roast count bar
            roast_width = int((stats['stats']['roast_count'] / max_score) * 400)
            draw.rectangle([100, y_offset, 100 + roast_width, y_offset + 30], 
                          fill=(255, 69, 0))
            draw.text((520, y_offset), "রোস্ট", font=font_small, fill=(255, 255, 255))
            y_offset += 50
            
            # Vote count bar
            vote_width = int((stats['stats']['vote_count'] / max_score) * 400)
            draw.rectangle([100, y_offset, 100 + vote_width, y_offset + 30], 
                          fill=(50, 205, 50))
            draw.text((520, y_offset), "ভোট", font=font_small, fill=(255, 255, 255))
            y_offset += 50
            
            # Reaction count bar
            react_width = int((stats['stats']['reaction_count'] / max_score) * 400)
            draw.rectangle([100, y_offset, 100 + react_width, y_offset + 30], 
                          fill(255, 105, 180))
            draw.text((520, y_offset), "রিঅ্যাকশন", font=font_small, fill=(255, 255, 255))
            
            # Footer
            footer = f"আপডেট: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
            footer_width = footer_bbox[2] - footer_bbox[0]
            footer_x = (width - footer_width) // 2
            draw.text((footer_x, height - 80), footer, font=font_small, fill=(150, 150, 150))
            
            # Bot signature
            signature = "Roastify Bot - লিডারবোর্ড"
            sig_bbox = draw.textbbox((0, 0), signature, font=font_small)
            sig_width = sig_bbox[2] - sig_bbox[0]
            sig_x = (width - sig_width) // 2
            draw.text((sig_x, height - 120), signature, font=font_small, fill=(255, 105, 180))
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"user_stats_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating user stats image: {e}")
            return None
    
    async def reset_daily_stats(self):
        """Reset daily statistics"""
        try:
            # This would reset daily counters in database
            # For now, just log
            logger.info("Daily stats reset (placeholder)")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting daily stats: {e}")
            return False