"""
Welcome System for new users
"""

import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class WelcomeSystem:
    """System for welcoming new users"""
    
    def __init__(self):
        logger.info("WelcomeSystem initialized")
    
    async def handle_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        try:
            new_members = update.message.new_chat_members
            
            for member in new_members:
                # Skip if the new member is the bot itself
                if member.id == context.bot.id:
                    continue
                
                welcome_message = self._generate_welcome_message(member)
                await update.message.reply_text(
                    welcome_message,
                    parse_mode="HTML"
                )
                
                logger.info(f"Welcomed new user: {member.first_name} (ID: {member.id})")
                
        except Exception as e:
            logger.error(f"Error in welcome system: {e}")
    
    def _generate_welcome_message(self, user) -> str:
        """Generate welcome message"""
        welcome_messages = [
            f"🎉 স্বাগতম <b>{user.first_name}</b>! রোস্টিফাই কমিউনিটিতে আপনাকে স্বাগতম!",
            f"🔥 আসসালামু আলাইকুম <b>{user.first_name}</b>! রোস্টের জগতে আপনাকে স্বাগতম!",
            f"🤖 হ্যালো <b>{user.first_name}</b>! প্রিমিয়াম রোস্টিং এক্সপেরিয়েন্সের জন্য প্রস্তুত হোন!",
            f"💎 ওহো <b>{user.first_name}</b>! রোস্টিফাই প্রিমিয়ামে আপনাকে স্বাগতম!"
        ]
        
        import random
        return random.choice(welcome_messages)
