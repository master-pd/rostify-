#!/usr/bin/env python3
"""
Welcome System for Roastify Bot
Handles welcome messages for bot start, group addition, and new members
"""

import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import WELCOME_MESSAGES, BOT_IDENTITY
    from utils.image_generator import ImageGenerator
    from database import get_database
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class WelcomeSystem:
    """Manages welcome messages and greetings"""
    
    def __init__(self):
        """Initialize welcome system"""
        self.config = WELCOME_MESSAGES
        self.db = get_database()
        self.image_gen = ImageGenerator()
        
        # Welcome message templates
        self.welcome_templates = {
            "private_start": [
                "🎉 <b>স্বাগতম {name}!</b>\n\n"
                "আমি <b>{bot_name}</b> - তোমার ব্যক্তিগত রোস্টিং বট! 😈\n\n"
                "💬 <b>কিভাবে ব্যবহার করবো:</b>\n"
                "• শুধু আমাকে কোনো টেক্সট পাঠাও (৪ অক্ষরের বেশি)\n"
                "• আমি রোস্ট দিয়ে দিব ৩D ইমেজ সহ\n"
                "• কোনো কমান্ড লাগবে না!\n\n"
                "🔥 <b>ফিচারসমূহ:</b>\n"
                "• স্মার্ট টেক্সট অ্যানালাইসিস\n"
                "• ৩D ইমেজ জেনারেশন\n"
                "• ভোটিং সিস্টেম\n"
                "• লিডারবোর্ড\n"
                "• অটো রিঅ্যাকশন\n\n"
                "তৈরি তো? প্রথম রোস্ট পাঠাও! 👇",
                
                "👋 <b>হ্যালো {name}!</b>\n\n"
                "রোস্টিফাই এ তোমাকে স্বাগতম! 😎\n"
                "আমি তোমার প্রতিটি মেসেজকে রোস্ট করে দিব স্টাইলিশ ইমেজ সহ!\n\n"
                "<b>নিয়ম:</b>\n"
                "✓ কমপক্ষে ৪ অক্ষর লিখো\n"
                "✓ কোনো লিংক পাঠিও না\n"
                "✓ অপমানজনক টার্গেট করো না\n\n"
                "চলো শুরু করি! প্রথম টেক্সট পাঠাও 🔥",
                
                "😈 <b>একজন নতুন শিকার পেলাম!</b>\n\n"
                "হ্যাঁ {name}, তুমি ঠিক শুনেছ!\n"
                "আমি {bot_name}, বাংলার সবচেয়ে স্মার্ট রোস্টিং বট!\n\n"
                "তোমার যেকোনো টেক্সটকে আমি:\n"
                "🎯 বিশ্লেষণ করব\n"
                "🖼️ ৩D ইমেজ বানাব\n"
                "🔥 রোস্ট করে দিব\n\n"
                "দেরি কিসের? শুরু করো! 💪"
            ],
            
            "group_added": [
                "🤖 <b>রোস্টিফাই গ্রুপে যোগদান করল!</b>\n\n"
                "গ্রুপের সবাইকে রোস্টের স্বাদ দিতে তৈরি! 😈\n\n"
                "<b>গ্রুপে কীভাবে কাজ করবো:</b>\n"
                "• সবার মেসেজ রোস্ট করব\n"
                "• মেম্বারদের mention করে roast করতে পারবে\n"
                "• অটো রিঅ্যাকশন দিব\n"
                "• লিডারবোর্ড দেখাব\n\n"
                "এখনই কাউকে mention করে রোস্ট করো! @username",
                
                "🎯 <b>নতুন গ্রুপ, নতুন শিকার!</b>\n\n"
                "রোস্টিফাই এখন এই গ্রুপে একটিভ!\n"
                "প্রতিটি মেসেজকে স্টাইলিশ রোস্টে পরিণত করব!\n\n"
                "<b>দ্রষ্টব্য:</b>\n"
                "• মিনিমাম ৪ অক্ষর চাই\n"
                "• গ্রুপের যেকোনো member কে mention করো\n"
                "• ভোট দিয়ে রেট করো\n\n"
                "গ্রুপের নাম: <b>{chat_title}</b>\n"
                "মোট মেম্বার: {member_count}",
                
                "🔥 <b>রোস্ট পার্টি শুরু!</b>\n\n"
                "এই গ্রুপের জন্য রোস্টিফাই একটিভ!\n"
                "সবাইকে সামনে আসতে বলো, রোস্ট খাওয়ার পালা! 😂\n\n"
                "<i>পিএস: আমাকে ব্যক্তিগতেও ব্যবহার করতে পারো!</i>"
            ],
            
            "new_member": [
                "🎊 <b>গ্রুপে স্বাগতম {new_member}!</b>\n\n"
                "তোমাকে দেখে খুশি হলাম! 😊\n"
                "এখন তুমিও রোস্টের মজা উপভোগ করতে পারবে!\n\n"
                "<b>দ্রুত টিপস:</b>\n"
                "• আমাকে mention করে রোস্ট চাইতে পারো\n"
                "• অন্যদের মেসেজে ভোট দিতে পারো\n"
                "• লিডারবোর্ডে উঠার চেষ্টা করো!\n\n"
                "স্বাগতম আবার! 👋",
                
                "🌟 <b>নতুন সদস্য এলো!</b>\n\n"
                "{new_member} আমাদের পরিবারে যোগ দিল!\n"
                "রোস্টের রাজ্যে তোমাকে স্বাগতম! 😈\n\n"
                "তোমার প্রথম রোস্টের জন্য:\n"
                "১. কিছু লিখো (৪+ অক্ষর)\n"
                "২. বা অন্যকে mention করো\n"
                "৩. ইমেজ সহ রোস্ট পেয়ে যাবে!\n\n"
                "আনন্দে থাকো! 🎉",
                
                "👤 <b>নতুন ফেস!</b>\n\n"
                "{new_member} আমাদের সঙ্গে!\n"
                "রোস্টিফাইয়ের বিশেষ অভ্যর্থনা তোমার জন্য!\n\n"
                "<i>'আমি রোস্ট খেতে ভয় পাই না!'</i>\n"
                "— লিখে দেখিয়ে দাও উপরে! 💪\n\n"
                "স্বাগতম ভাই/বোন! 🤗"
            ]
        }
        
        logger.info("Welcome System initialized")
    
    async def get_welcome_message(self, user: Any, chat: Any) -> str:
        """Get appropriate welcome message based on context"""
        if chat.type == "private":
            # Private chat welcome
            template_type = "private_start"
            templates = self.welcome_templates[template_type]
            
            selected = random.choice(templates)
            welcome_text = selected.format(
                name=user.first_name,
                bot_name=BOT_IDENTITY["name"]
            )
            
        else:
            # Group chat welcome (bot added to group)
            template_type = "group_added"
            templates = self.welcome_templates[template_type]
            
            selected = random.choice(templates)
            welcome_text = selected.format(
                chat_title=chat.title,
                member_count=await self._get_chat_member_count(chat)
            )
        
        return welcome_text
    
    async def handle_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new members joining a group"""
        if not self.config["new_member_welcome"]:
            return
        
        try:
            chat = update.effective_chat
            new_members = update.message.new_chat_members
            
            for member in new_members:
                # Skip if the new member is the bot itself
                if member.id == context.bot.id:
                    await self._handle_bot_added_to_group(update, context)
                    continue
                
                # Skip if member is a bot
                if member.is_bot:
                    continue
                
                # Get welcome message for new member
                welcome_text = await self._get_new_member_welcome(member, chat)
                
                # Generate welcome image
                image_path = await self._generate_welcome_image(member, chat)
                
                # Send welcome message
                if image_path:
                    with open(image_path, 'rb') as photo:
                        await update.message.reply_photo(
                            photo=photo,
                            caption=welcome_text,
                            parse_mode=ParseMode.HTML
                        )
                    
                    # Cleanup temp file
                    import os
                    if os.path.exists(image_path):
                        os.remove(image_path)
                else:
                    await update.message.reply_text(
                        welcome_text,
                        parse_mode=ParseMode.HTML
                    )
                
                logger.info(f"Welcomed new member {member.id} to chat {chat.id}")
                
                # Update database
                self.db.add_or_update_user(
                    user_id=member.id,
                    username=member.username,
                    first_name=member.first_name,
                    last_name=member.last_name
                )
                
        except Exception as e:
            logger.error(f"Error handling new members: {e}")
    
    async def _handle_bot_added_to_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot being added to a group"""
        try:
            chat = update.effective_chat
            
            # Get group added welcome message
            welcome_text = await self.get_welcome_message(None, chat)
            
            # Generate group welcome image
            image_path = await self._generate_group_welcome_image(chat)
            
            if image_path:
                with open(image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=welcome_text,
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup temp file
                import os
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                await update.message.reply_text(
                    welcome_text,
                    parse_mode=ParseMode.HTML
                )
            
            logger.info(f"Bot added to group {chat.id}")
            
        except Exception as e:
            logger.error(f"Error handling bot group addition: {e}")
    
    async def _get_new_member_welcome(self, member: Any, chat: Any) -> str:
        """Get welcome message for new member"""
        templates = self.welcome_templates["new_member"]
        selected = random.choice(templates)
        
        member_name = f"@{member.username}" if member.username else member.first_name
        
        return selected.format(
            new_member=member_name,
            chat_title=chat.title if chat.title else "এই গ্রুপ"
        )
    
    async def _generate_welcome_image(self, member: Any, chat: Any) -> Optional[str]:
        """Generate welcome image for new member"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # Create image
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (25, 25, 112))  # Midnight blue
            
            draw = ImageDraw.Draw(image)
            
            # Try to load a font
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 60)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 40)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 30)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "স্বাগতম! 🎉"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 100), title, font=font_large, fill=(255, 255, 255))
            
            # Draw member name
            member_name = f"@{member.username}" if member.username else member.first_name
            name_text = f"নতুন সদস্য: {member_name}"
            name_bbox = draw.textbbox((0, 0), name_text, font=font_medium)
            name_width = name_bbox[2] - name_bbox[0]
            name_x = (width - name_width) // 2
            draw.text((name_x, 250), name_text, font=font_medium, fill=(255, 215, 0))
            
            # Draw group name
            if chat.title:
                group_text = f"গ্রুপ: {chat.title}"
                group_bbox = draw.textbbox((0, 0), group_text, font=font_medium)
                group_width = group_bbox[2] - group_bbox[0]
                group_x = (width - group_width) // 2
                draw.text((group_x, 350), group_text, font=font_medium, fill=(200, 200, 255))
            
            # Draw welcome message
            messages = [
                "রোস্টের জগতে তোমাকে স্বাগতম!",
                "প্রতিটি মেসেজ স্টাইলিশ রোস্ট পাবে!",
                "অন্যদের mention করে roast করতে পারবে!",
                "ভোট দিয়ে রেট করতে পারবে রোস্ট!",
                "লিডারবোর্ডে উঠার চেষ্টা করো!",
                "মজা নাও, রোস্ট খাও, আনন্দে থাকো! 😊"
            ]
            
            y_offset = 450
            for i, msg in enumerate(messages[:4]):
                draw.text((100, y_offset + i*60), f"• {msg}", 
                         font=font_small, fill=(220, 220, 220))
            
            # Draw bot signature
            signature = "Roastify Bot - রোস্টের রাজা 😈"
            sig_bbox = draw.textbbox((0, 0), signature, font=font_small)
            sig_width = sig_bbox[2] - sig_bbox[0]
            sig_x = (width - sig_width) // 2
            draw.text((sig_x, 750), signature, font=font_small, fill=(255, 105, 180))
            
            # Draw time
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            time_bbox = draw.textbbox((0, 0), time_str, font=font_small)
            time_width = time_bbox[2] - time_bbox[0]
            time_x = (width - time_width) // 2
            draw.text((time_x, 800), time_str, font=font_small, fill=(150, 150, 150))
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"welcome_{member.id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating welcome image: {e}")
            return None
    
    async def _generate_group_welcome_image(self, chat: Any) -> Optional[str]:
        """Generate welcome image for bot added to group"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), (30, 30, 46))  # Dark blue
            
            draw = ImageDraw.Draw(image)
            
            try:
                font_large = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 70)
                font_medium = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 45)
                font_small = ImageFont.truetype("assets/fonts/Kalpurush.ttf", 35)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw main title
            title = "রোস্টিফাই আসছে! 🔥"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 80), title, font=font_large, fill=(255, 69, 0))
            
            # Draw group name
            if chat.title:
                group_text = f"গ্রুপ: {chat.title}"
                group_bbox = draw.textbbox((0, 0), group_text, font=font_medium)
                group_width = group_bbox[2] - group_bbox[0]
                group_x = (width - group_width) // 2
                draw.text((group_x, 200), group_text, font=font_medium, fill=(255, 215, 0))
            
            # Draw features
            features = [
                "🎯 স্মার্ট টেক্সট রোস্টিং",
                "🖼️ ৩D ইমেজ জেনারেশন",
                "👥 মেম্বার mention সাপোর্ট",
                "👍 ভোটিং সিস্টেম",
                "🏆 লিডারবোর্ড",
                "😂 অটো রিঅ্যাকশন",
                "🎨 রেনডম বর্ডার & ফন্ট",
                "⏰ ২৪/৭ একটিভ"
            ]
            
            y_offset = 300
            for i in range(0, len(features), 2):
                if i < len(features):
                    draw.text((100, y_offset + (i//2)*80), features[i], 
                             font=font_small, fill=(220, 220, 255))
                if i+1 < len(features):
                    draw.text((550, y_offset + (i//2)*80), features[i+1], 
                             font=font_small, fill=(220, 220, 255))
            
            # Draw instruction
            instruction = "কিছু লিখো → রোস্ট পাবে ইমেজ সহ!"
            inst_bbox = draw.textbbox((0, 0), instruction, font=font_medium)
            inst_width = inst_bbox[2] - inst_bbox[0]
            inst_x = (width - inst_width) // 2
            draw.text((inst_x, 700), instruction, font=font_medium, fill=(50, 205, 50))
            
            # Draw bot info
            bot_info = f"{BOT_IDENTITY['name']} - {BOT_IDENTITY['tagline']}"
            bot_bbox = draw.textbbox((0, 0), bot_info, font=font_small)
            bot_width = bot_bbox[2] - bot_bbox[0]
            bot_x = (width - bot_width) // 2
            draw.text((bot_x, 780), bot_info, font=font_small, fill=(255, 105, 180))
            
            # Save image
            os.makedirs("temp", exist_ok=True)
            filename = f"group_welcome_{chat.id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join("temp", filename)
            
            image.save(filepath, 'PNG', quality=95)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating group welcome image: {e}")
            return None
    
    async def _get_chat_member_count(self, chat: Any) -> int:
        """Get chat member count (with fallback)"""
        try:
            return await chat.get_member_count()
        except:
            return 0
    
    async def send_custom_welcome(self, chat_id: int, user: Any, 
                                 welcome_type: str = "custom") -> bool:
        """Send a custom welcome message"""
        try:
            templates = {
                "birthday": "🎂 জন্মদিনের শুভেচ্ছা {name}! অনেক ভালো থেকো! ❤️",
                "anniversary": "🎉 অভিনন্দন {name}! এই বিশেষ দিনে শুভকামনা! 🌟",
                "achievement": "🏆 অভিনন্দন {name}! তোমার সাফল্যে আমরা গর্বিত! 💪",
                "returning": "👋 ফিরে আসার জন্য ধন্যবাদ {name}! তোমাকে মিস করছিলাম! 😊"
            }
            
            if welcome_type in templates:
                message = templates[welcome_type].format(name=user.first_name)
                
                # Send message
                from telegram import Bot
                bot = Bot(token=context.bot.token)
                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=ParseMode.HTML
                )
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error sending custom welcome: {e}")
            return False