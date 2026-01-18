#!/usr/bin/env python3
"""
Voting System for Roastify Bot
Handles inline voting buttons and vote tracking
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import VOTE_SYSTEM
    from database import get_database
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class VotingSystem:
    """Manages voting system for roast messages"""
    
    def __init__(self):
        """Initialize voting system"""
        self.config = VOTE_SYSTEM
        self.db = get_database()
        
        # Track active votes
        self.active_votes = {}  # message_id -> vote_data
        
        logger.info("Voting System initialized")
    
    async def create_vote_keyboard(self, update_id: int, user_id: int, 
                                  chat_id: int) -> InlineKeyboardMarkup:
        """Create inline keyboard for voting"""
        keyboard = []
        
        for option in self.config["options"]:
            # Parse emoji and text
            emoji = option.split()[0] if ' ' in option else option
            text = option.split()[1] if ' ' in option else option
            
            # Create callback data: vote_{update_id}_{vote_type}
            callback_data = f"vote_{update_id}_{emoji}"
            
            keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
        
        # Add extra info button
        keyboard.append([
            InlineKeyboardButton("📊 Stats", callback_data=f"vote_stats_{update_id}"),
            InlineKeyboardButton("❌ Close", callback_data=f"vote_close_{update_id}")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle vote callback queries"""
        query = update.callback_query
        user = update.effective_user
        data = query.data
        
        try:
            # Parse callback data
            parts = data.split('_')
            
            if len(parts) < 3:
                await query.answer("Invalid vote data!")
                return
            
            action = parts[0]
            update_id = parts[1]
            
            if action == "vote":
                # Handle vote submission
                vote_type = parts[2]
                await self._process_vote(query, user, update_id, vote_type, context)
                
            elif action == "vote_stats":
                # Show vote statistics
                await self._show_vote_stats(query, update_id)
                
            elif action == "vote_close":
                # Close voting
                await self._close_voting(query)
                
        except Exception as e:
            logger.error(f"Error handling vote callback: {e}")
            await query.answer("Error processing vote!")
    
    async def _process_vote(self, query: Any, user: Any, update_id: str, 
                           vote_type: str, context: ContextTypes.DEFAULT_TYPE):
        """Process a vote submission"""
        try:
            message = query.message
            message_id = message.message_id
            chat_id = message.chat_id
            
            # Check if user already voted
            if self.db.check_vote_exists(user.id, message_id):
                await query.answer("তুমি ইতিমধ্যে ভোট দিয়েছ! 🗳️")
                return
            
            # Check cooldown
            cooldown_key = f"vote_{chat_id}"
            if self.db.check_cooldown(user.id, cooldown_key):
                await query.answer("অপেক্ষা করো কিছুক্ষণ! ⏳")
                return
            
            # Record vote
            success = self.db.add_vote(user.id, chat_id, message_id, vote_type)
            
            if success:
                # Update message with new vote count
                await self._update_vote_display(query, message_id, chat_id, vote_type)
                
                # Set cooldown
                self.db.set_cooldown(user.id, cooldown_key, 
                                   self.config["vote_rules"]["vote_window_seconds"])
                
                # Send thank you message
                await query.answer(f"ধন্যবাদ! {vote_type} ভোটের জন্য! 👍")
                
                # Apply vote effects
                await self._apply_vote_effects(vote_type, message_id, chat_id)
                
                logger.info(f"User {user.id} voted {vote_type} on message {message_id}")
            else:
                await query.answer("ভোট দিতে সমস্যা হয়েছে! 😢")
                
        except Exception as e:
            logger.error(f"Error processing vote: {e}")
            await query.answer("ভোট প্রসেসিং error!")
    
    async def _update_vote_display(self, query: Any, message_id: int, 
                                  chat_id: int, new_vote_type: str):
        """Update the message with new vote counts"""
        try:
            # Get current vote counts
            vote_counts = self._get_vote_counts(message_id)
            
            # Update keyboard with counts
            keyboard = []
            
            for option in self.config["options"]:
                emoji = option.split()[0] if ' ' in option else option
                text = option.split()[1] if ' ' in option else option
                
                # Get count for this option
                count = vote_counts.get(emoji, 0)
                
                # Create button text with count
                button_text = f"{option} ({count})"
                callback_data = f"vote_{message_id}_{emoji}"
                
                keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
            
            # Add extra buttons
            keyboard.append([
                InlineKeyboardButton("📊 Stats", callback_data=f"vote_stats_{message_id}"),
                InlineKeyboardButton("❌ Close", callback_data=f"vote_close_{message_id}")
            ])
            
            # Update message
            await query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
        except Exception as e:
            logger.error(f"Error updating vote display: {e}")
    
    def _get_vote_counts(self, message_id: int) -> Dict[str, int]:
        """Get vote counts for a message"""
        try:
            # Query database for votes on this message
            self.db.cursor.execute('''
                SELECT vote_type, COUNT(*) as count
                FROM votes
                WHERE message_id = ?
                GROUP BY vote_type
            ''', (message_id,))
            
            results = self.db.cursor.fetchall()
            
            vote_counts = {}
            for vote_type, count in results:
                # Extract emoji from vote_type
                emoji = vote_type
                vote_counts[emoji] = count
            
            return vote_counts
            
        except Exception as e:
            logger.error(f"Error getting vote counts: {e}")
            return {}
    
    async def _show_vote_stats(self, query: Any, message_id: str):
        """Show vote statistics for a message"""
        try:
            vote_counts = self._get_vote_counts(int(message_id))
            
            if not vote_counts:
                stats_text = "এখনো কোনো ভোট পড়েনি! প্রথম ভোট দাও! 🗳️"
            else:
                total_votes = sum(vote_counts.values())
                
                # Create stats text
                stats_lines = ["📊 <b>ভোট পরিসংখ্যান:</b>"]
                stats_lines.append("━━━━━━━━━━━━━━━━━━")
                
                for option in self.config["options"]:
                    emoji = option.split()[0] if ' ' in option else option
                    text = option.split()[1] if ' ' in option else option
                    
                    count = vote_counts.get(emoji, 0)
                    percentage = (count / total_votes * 100) if total_votes > 0 else 0
                    
                    # Create progress bar
                    bar_length = 10
                    filled = int(percentage / 100 * bar_length)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    
                    stats_lines.append(f"{emoji} {text}: {count} ভোট ({percentage:.1f}%)")
                    stats_lines.append(f"   [{bar}]")
                
                stats_lines.append(f"\n<b>মোট ভোট:</b> {total_votes}")
                stats_text = "\n".join(stats_lines)
            
            await query.answer(stats_text, show_alert=True)
            
        except Exception as e:
            logger.error(f"Error showing vote stats: {e}")
            await query.answer("স্ট্যাটস দেখাতে সমস্যা! 😢", show_alert=True)
    
    async def _close_voting(self, query: Any):
        """Close voting for a message"""
        try:
            # Remove inline keyboard
            await query.message.edit_reply_markup(reply_markup=None)
            await query.answer("ভোটিং বন্ধ করা হলো! ✅")
            
        except Exception as e:
            logger.error(f"Error closing voting: {e}")
            await query.answer("বন্ধ করতে সমস্যা! 😢")
    
    async def _apply_vote_effects(self, vote_type: str, message_id: int, chat_id: int):
        """Apply effects based on vote type"""
        try:
            effects = self.config["vote_effects"]
            
            if "🔥" in vote_type and "high_funny_votes" in effects:
                # Increase funny roast weight
                self._adjust_template_weight("cartoon_roast", 1.2)
                logger.info(f"Increased funny template weight")
                
            elif "💀" in vote_type and "high_savage_votes" in effects:
                # Unlock stronger roast tone
                self._adjust_template_weight("neon_savage", 1.3)
                logger.info(f"Increased savage template weight")
                
            elif "😐" in vote_type and "high_mid_votes" in effects:
                # Neutral balance
                self._reset_template_weights()
                logger.info(f"Reset template weights to neutral")
                
        except Exception as e:
            logger.error(f"Error applying vote effects: {e}")
    
    def _adjust_template_weight(self, template_category: str, multiplier: float):
        """Adjust template selection weights"""
        # This would typically update a weights dictionary or database
        # For now, we'll log it
        logger.info(f"Adjusting {template_category} weight by {multiplier}x")
    
    def _reset_template_weights(self):
        """Reset all template weights to default"""
        logger.info("Resetting all template weights to default")
    
    async def get_top_voted_messages(self, chat_id: int, limit: int = 5) -> List[Dict]:
        """Get top voted messages in a chat"""
        try:
            self.db.cursor.execute('''
                SELECT message_id, COUNT(*) as vote_count,
                       GROUP_CONCAT(vote_type) as vote_types
                FROM votes
                WHERE chat_id = ?
                GROUP BY message_id
                ORDER BY vote_count DESC
                LIMIT ?
            ''', (chat_id, limit))
            
            results = self.db.cursor.fetchall()
            
            top_messages = []
            for message_id, vote_count, vote_types in results:
                # Parse vote types
                types_list = vote_types.split(',') if vote_types else []
                
                top_messages.append({
                    'message_id': message_id,
                    'vote_count': vote_count,
                    'vote_types': types_list
                })
            
            return top_messages
            
        except Exception as e:
            logger.error(f"Error getting top voted messages: {e}")
            return []
    
    async def generate_vote_stats_image(self, chat_id: int) -> Optional[str]:
        """Generate an image with vote statistics"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # Get vote statistics
            top_messages = await self.get_top_voted_messages(chat_id, 10)
            
            if not top_messages:
                return None
            
            # Create image
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (240, 248, 255))  # Alice blue
            
            draw = ImageDraw.Draw(image)
            
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 60)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 40)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 30)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Title
            title = "🏆 ভোট পরিসংখ্যান 🏆"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 50), title, font=font_large, fill=(25, 25, 112))
            
            # Subtitle
            subtitle = f"শীর্ষ {len(top_messages)} রোস্ট"
            sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
            sub_width = sub_bbox[2] - sub_bbox[0]
            sub_x = (width - sub_width) // 2
            draw.text((sub_x, 130), subtitle, font=font_medium, fill=(100, 100, 100))
            
            # Draw vote rankings
            y_offset = 220
            for i, msg in enumerate(top_messages, 1):
                # Rank number
                rank_text = f"{i}."
                draw.text((100, y_offset), rank_text, font=font_medium, fill=(0, 0, 0))
                
                # Vote count
                votes_text = f"ভোট: {msg['vote_count']}"
                draw.text((200, y_offset), votes_text, font=font_medium, fill=(0, 100, 0))
                
                # Message ID (shortened)
                msg_id_text = f"ID: ...{str(msg['message_id'])[-6:]}"
                draw.text((400, y_offset), msg_id_text, font=font_small, fill=(100, 100, 100))
                
                y_offset += 70
            
            # Draw summary
            total_votes = sum(msg['vote_count'] for msg in top_messages)
            summary = f"মোট ভোট: {total_votes}"
            sum_bbox = draw.textbbox((0, 0), summary, font=font_medium)
            sum_width = sum_bbox[2] - sum_bbox[0]
            sum_x = (width - sum_width) // 2
            draw.text((sum_x, y_offset + 40), summary, font=font_medium, fill=(139, 0, 0))
            
            # Footer
            footer = f"আপডেট: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
            footer_width = footer_bbox[2] - footer_bbox[0]
            footer_x = (width - footer_width) // 2
            draw.text((footer_x, height - 100), footer, font=font_small, fill=(150, 150, 150))
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"vote_stats_{chat_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating vote stats image: {e}")
            return None
    
    async def cleanup_old_votes(self, days_old: int = 30):
        """Cleanup votes older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            self.db.cursor.execute('''
                DELETE FROM votes
                WHERE voted_at < ?
            ''', (cutoff_date,))
            
            self.db.conn.commit()
            
            deleted_count = self.db.cursor.rowcount
            logger.info(f"Cleaned up {deleted_count} old votes")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old votes: {e}")
            return 0