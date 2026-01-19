#!/usr/bin/env python3
"""
Roastify Bot - COMPLETE WORKING VERSION
Image + Text + Diagram Reply with All Features
"""

import os
import sys
import logging
import random
import re
import asyncio
import traceback
import math
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import project modules
try:
    from config import BOT_TOKEN, BOT_IDENTITY, CORE_RULES
    from database import get_database
    from features.master_loader import load_all_features
    from features.welcome_system import WelcomeSystem
    from features.roast_engine import RoastEngine
    from features.voting_system import VotingSystem
    from features.reaction_system import ReactionSystem
    from features.mention_roast import MentionRoast
    from features.admin_protection import AdminProtection
    from features.leaderboard import Leaderboard
    from features.festival_mode import FestivalMode
    from features.auto_daily_quote import AutoDailyQuote
    from features.custom_template_unlocks import CustomTemplateUnlocks
    from features.auto_mood_recognition import AutoMoodRecognition
    from features.safe_forward_share import SafeForwardShare
    from utils.image_generator import ImageGenerator
    from utils.template_manager import TemplateManager
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Please check all required files exist")
    sys.exit(1)

# Import Telegram
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters,
        ContextTypes, CallbackQueryHandler
    )
    from telegram.constants import ParseMode
except ImportError:
    logger.error("Install: pip install python-telegram-bot")
    sys.exit(1)

# Import PIL for image generation
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
    import numpy as np
    HAS_PIL = True
except ImportError:
    logger.warning("PIL not installed, image generation will be limited")
    HAS_PIL = False


class DiagramGenerator:
    """Generate random diagrams for roasts"""
    
    def __init__(self):
        self.diagram_types = [
            "flow_chart", "pie_chart", "bar_chart", 
            "line_graph", "venn_diagram", "mind_map",
            "process_diagram", "comparison_chart"
        ]
    
    def generate_diagram(self, text: str, roast_type: str = "funny") -> Optional[str]:
        """Generate a diagram image based on text"""
        if not HAS_PIL:
            return None
        
        try:
            # Create temp directory
            os.makedirs("temp", exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"temp/diagram_{timestamp}.png"
            
            # Choose random diagram type
            diagram_type = random.choice(self.diagram_types)
            
            # Create image
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color=(240, 240, 240))
            draw = ImageDraw.Draw(image)
            
            # Add title
            title = f"{roast_type.upper()} ANALYSIS"
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            # Draw title
            draw.text((width//2 - 100, 30), title, fill=(0, 0, 0), font=font)
            
            # Generate diagram based on type
            if diagram_type == "pie_chart":
                self._draw_pie_chart(draw, width, height, text)
            elif diagram_type == "bar_chart":
                self._draw_bar_chart(draw, width, height, text)
            elif diagram_type == "flow_chart":
                self._draw_flow_chart(draw, width, height, text)
            elif diagram_type == "venn_diagram":
                self._draw_venn_diagram(draw, width, height, text)
            else:
                self._draw_generic_diagram(draw, width, height, text)
            
            # Save image
            image.save(filename, 'PNG', quality=95)
            logger.info(f"Diagram generated: {filename}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating diagram: {e}")
            return None
    
    def _draw_pie_chart(self, draw, width, height, text):
        """Draw a pie chart"""
        center_x, center_y = width // 2, height // 2
        radius = 200
        
        # Generate random segments
        segments = random.randint(3, 6)
        colors = [
            (255, 99, 132), (54, 162, 235), (255, 205, 86),
            (75, 192, 192), (153, 102, 255), (255, 159, 64)
        ]
        
        start_angle = 0
        for i in range(segments):
            # Random angle for each segment
            angle = random.randint(30, 150)
            end_angle = start_angle + angle
            
            # Draw segment
            draw.pieslice(
                [center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius],
                start_angle, end_angle,
                fill=colors[i % len(colors)],
                outline=(0, 0, 0)
            )
            
            # Add label
            label_angle = (start_angle + end_angle) / 2
            label_rad = math.radians(label_angle)
            label_x = center_x + (radius + 30) * math.cos(label_rad)
            label_y = center_y + (radius + 30) * math.sin(label_rad)
            
            label = f"Part {i+1}"
            draw.text((label_x - 20, label_y - 10), label, fill=(0, 0, 0))
            
            start_angle = end_angle
    
    def _draw_bar_chart(self, draw, width, height, text):
        """Draw a bar chart"""
        chart_x, chart_y = 100, 100
        chart_width, chart_height = 600, 400
        
        # Draw axes
        draw.line([(chart_x, chart_y), (chart_x, chart_y + chart_height)], fill=(0, 0, 0), width=3)
        draw.line([(chart_x, chart_y + chart_height), 
                   (chart_x + chart_width, chart_y + chart_height)], fill=(0, 0, 0), width=3)
        
        # Generate random bars
        bars = random.randint(4, 8)
        bar_width = chart_width // (bars + 2)
        
        for i in range(bars):
            x = chart_x + (i + 1) * bar_width
            bar_height = random.randint(50, chart_height - 100)
            
            # Draw bar
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            draw.rectangle(
                [x, chart_y + chart_height - bar_height,
                 x + bar_width - 10, chart_y + chart_height],
                fill=color,
                outline=(0, 0, 0)
            )
            
            # Add label
            label = f"B{i+1}"
            draw.text((x + bar_width//2 - 5, chart_y + chart_height + 10), label, fill=(0, 0, 0))
    
    def _draw_flow_chart(self, draw, width, height, text):
        """Draw a flow chart"""
        # Draw boxes
        box_width, box_height = 150, 60
        positions = [
            (width//2 - box_width//2, 100),
            (200, 200),
            (width - 350, 200),
            (width//2 - box_width//2, 300),
            (width//2 - box_width//2, 400)
        ]
        
        colors = [(173, 216, 230), (144, 238, 144), (255, 228, 196), 
                  (221, 160, 221), (255, 218, 185)]
        
        for i, (x, y) in enumerate(positions):
            # Draw box
            draw.rectangle(
                [x, y, x + box_width, y + box_height],
                fill=colors[i % len(colors)],
                outline=(0, 0, 0),
                width=2
            )
            
            # Add text
            text_in_box = f"Step {i+1}"
            draw.text((x + box_width//2 - 20, y + box_height//2 - 10), 
                     text_in_box, fill=(0, 0, 0))
        
        # Draw arrows
        for i in range(len(positions) - 1):
            x1 = positions[i][0] + box_width//2
            y1 = positions[i][1] + box_height
            x2 = positions[i+1][0] + box_width//2
            y2 = positions[i+1][1]
            
            draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=2)
            
            # Draw arrow head
            draw.polygon([
                (x2, y2),
                (x2 - 10, y2 + 20),
                (x2 + 10, y2 + 20)
            ], fill=(0, 0, 0))
    
    def _draw_venn_diagram(self, draw, width, height, text):
        """Draw a Venn diagram"""
        center_x, center_y = width // 2, height // 2
        radius = 150
        
        # Draw circles
        colors = [(255, 0, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128)]
        
        for i in range(3):
            offset_x = (i - 1) * 100
            offset_y = 0 if i != 2 else 50
            
            draw.ellipse(
                [center_x + offset_x - radius, center_y + offset_y - radius,
                 center_x + offset_x + radius, center_y + offset_y + radius],
                fill=colors[i],
                outline=(0, 0, 0),
                width=2
            )
            
            # Add labels
            labels = ["Logic", "Emotion", "Humor"]
            draw.text((center_x + offset_x - 30, center_y + offset_y - radius - 30),
                     labels[i], fill=(0, 0, 0))
    
    def _draw_generic_diagram(self, draw, width, height, text):
        """Draw a generic diagram"""
        # Draw a network/graph
        nodes = 8
        node_radius = 20
        node_positions = []
        
        # Generate random node positions
        for i in range(nodes):
            x = random.randint(100, width - 100)
            y = random.randint(100, height - 100)
            node_positions.append((x, y))
            
            # Draw node
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            draw.ellipse(
                [x - node_radius, y - node_radius,
                 x + node_radius, y + node_radius],
                fill=color,
                outline=(0, 0, 0),
                width=2
            )
            
            # Add node label
            draw.text((x - 10, y - 10), f"N{i+1}", fill=(0, 0, 0))
        
        # Draw connections
        for i in range(nodes):
            for j in range(i + 1, nodes):
                if random.random() > 0.6:  # 40% chance of connection
                    x1, y1 = node_positions[i]
                    x2, y2 = node_positions[j]
                    
                    draw.line([(x1, y1), (x2, y2)], 
                             fill=(100, 100, 100), 
                             width=1)


class RoastifyBot:
    """Main Roastify Bot Class"""
    
    def __init__(self):
        """Initialize the bot"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY.get("name", "Roastify")
        self.bot_tagline = BOT_IDENTITY.get("tagline", "")
        
        # Initialize components
        self.db = get_database()
        self.image_gen = ImageGenerator()
        self.diagram_gen = DiagramGenerator()
        self.template_manager = TemplateManager()
        self.roast_engine = RoastEngine()
        self.welcome_system = WelcomeSystem()
        self.voting_system = VotingSystem()
        self.reaction_system = ReactionSystem()
        self.mention_roast = MentionRoast()
        self.admin_protection = AdminProtection()
        self.leaderboard = Leaderboard()
        self.festival_mode = FestivalMode()
        self.mood_recognition = AutoMoodRecognition()
        self.safe_forward = SafeForwardShare()
        
        # Initialize job-based features
        self.auto_daily_quote = None
        
        try:
            self.custom_unlocks = CustomTemplateUnlocks()
        except:
            self.custom_unlocks = None
        
        # Load all features
        try:
            self.features = load_all_features()
        except:
            self.features = {}
        
        # Statistics
        self.stats = {
            "messages_processed": 0,
            "roasts_generated": 0,
            "images_created": 0,
            "diagrams_created": 0,
            "users_interacted": set(),
            "groups_managed": set(),
            "start_time": datetime.now()
        }
        
        # Application instance
        self.application = None
        
        logger.info(f"Initialized {self.bot_name} Bot")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        try:
            # Add user to database
            self.db.add_or_update_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            welcome_message = await self.welcome_system.get_welcome_message(user, chat)
            
            if update.message:
                await update.message.reply_text(
                    welcome_message,
                    parse_mode=ParseMode.HTML
                )
            
            logger.info(f"New start from user {user.id} in chat {chat.id}")
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            if update.message:
                await update.message.reply_text(
                    f"স্বাগতম {user.first_name}! 🎉\n"
                    f"আমি {self.bot_name} - {self.bot_tagline}",
                    parse_mode=ParseMode.HTML
                )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
<b>{self.bot_name} - {self.bot_tagline}</b>

🤖 <b>ব্যবহার পদ্ধতি:</b>
• যেকোনো টেক্সট পাঠান (সর্বনিম্ন ৪ অক্ষর)
• আমি ইমেজ + টেক্সট + ডায়াগ্রাম সহ রিপ্লাই দেব
• কোন কমান্ডের প্রয়োজন নেই!

🎯 <b>বৈশিষ্ট্য:</b>
• 3D স্টাইলড ইমেজ জেনারেশন
• র্যান্ডম ডায়াগ্রাম তৈরি
• স্মার্ট রোস্ট ইঞ্জিন
• গ্রুপে মেনশন সাপোর্ট
• ভোটিং সিস্টেম
• অটো রিএকশন
• লিডারবোর্ড
• ফেস্টিভাল থিম

👥 <b>গ্রুপে ব্যবহার:</b>
• @mentions দিয়ে টার্গেটেড রোস্ট
• নতুন সদস্য স্বাগতম
• গ্রুপ স্ট্যাটিস্টিক্স

🔧 <b>কমান্ড:</b>
/start - শুরু করুন
/help - সাহায্য
/stats - পরিসংখ্যান
/leaderboard - র্যাঙ্কিং

⚡ <b>টিপস:</b>
• গ্রুপে @মেনশন ব্যবহার করুন
• ভোট দিয়ে উন্নতি করুন
• রেগুলার চেক করুন লিডারবোর্ড

🔒 <b>গোপনীয়তা:</b>
• ব্যক্তিগত তথ্য সংরক্ষণ করা হয় না
• নিরাপদ শেয়ারিং
        """
        
        if update.message:
            await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user = update.effective_user
        
        try:
            # Check if admin
            from config import OWNER_ADMIN_PROTECTION
            admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
            
            if user.id not in admin_ids and user.id != OWNER_ADMIN_PROTECTION.get("bot_owner_user_id"):
                await update.message.reply_text("❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!")
                return
        except:
            pass
        
        # Calculate uptime
        uptime = datetime.now() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        stats_text = f"""
<b>{self.bot_name} পরিসংখ্যান</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>আপটাইম:</b> {days}দিন {hours}ঘণ্টা {minutes}মিনিট {seconds}সেকেন্ড
📊 <b>বার্তা প্রসেসড:</b> {self.stats['messages_processed']:,}
🔥 <b>রোস্ট জেনারেটেড:</b> {self.stats['roasts_generated']:,}
🖼️ <b>ইমেজ তৈরি:</b> {self.stats['images_created']:,}
📈 <b>ডায়াগ্রাম তৈরি:</b> {self.stats['diagrams_created']:,}
👥 <b>ইউজার:</b> {len(self.stats['users_interacted']):,}
🏠 <b>গ্রুপ:</b> {len(self.stats['groups_managed']):,}
━━━━━━━━━━━━━━━━━━━━
<b>সিস্টেম:</b> ✅ অপারেশনাল
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.HTML)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages"""
        try:
            # Update statistics
            self.stats["messages_processed"] += 1
            
            user = update.effective_user
            chat = update.effective_chat
            message = update.message
            
            if not message or not message.text:
                return
            
            text = message.text.strip()
            
            # Add user to interacted set
            self.stats["users_interacted"].add(user.id)
            
            # Add group to managed set
            if chat.type in ["group", "supergroup"]:
                self.stats["groups_managed"].add(chat.id)
            
            # Check minimum length
            if len(text) < CORE_RULES.get("minimum_input_length", 4):
                if len(text) > 0:
                    await message.reply_text(
                        f"একটু লম্বা লিখুন! কমপক্ষে {CORE_RULES.get('minimum_input_length', 4)} অক্ষর প্রয়োজন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
            # Check ignore conditions
            if self._should_ignore_message(text):
                return
            
            # Check for admin protection
            try:
                if await self.admin_protection.check_protection_needed(user, text, chat):
                    await self.admin_protection.handle_protected_response(
                        update, context, user, text
                    )
                    return
            except:
                pass
            
            # Check for mentions in groups
            if chat.type in ["group", "supergroup"]:
                try:
                    mention_result = await self.mention_roast.process_mention(
                        message, text, user, chat
                    )
                    if mention_result:
                        await self._generate_mention_response(
                            update, context, text, user, chat, mention_result
                        )
                        return
                except Exception as e:
                    logger.error(f"Error processing mention: {e}")
            
            # Generate regular response
            await self._generate_response(update, context, text, user, chat)
            
            # Auto reactions
            try:
                await self.reaction_system.add_auto_reactions(message, text, user, chat)
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            
            if update.message:
                await update.message.reply_text(
                    "⚠️ সমস্যা হয়েছে! আবার চেষ্টা করুন।",
                    parse_mode=ParseMode.HTML
                )
    
    def _should_ignore_message(self, text: str) -> bool:
        """Check if message should be ignored"""
        # Check for only emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002500-\U00002BEF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"
            u"\u3030"
            "]+", flags=re.UNICODE)
        
        if emoji_pattern.sub('', text).strip() == '':
            return True
        
        # Check for only numbers
        if text.strip().isdigit():
            return True
        
        # Check for links only
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        if url_pattern.sub('', text).strip() == '':
            return True
        
        return False
    
    async def _generate_mention_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        text: str, user: Any, chat: Any, mention_result: Dict):
        """Generate response for mentioned user"""
        try:
            target_user = mention_result.get("target")
            roast_text = mention_result.get("roast_text", text)
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(
                roast_text, user, target_user
            )
            
            # Update stats
            self.stats["roasts_generated"] += 1
            
            # Generate image
            image_path = await self.image_gen.generate_roast_image(
                roast_data, user, target_user
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = self.diagram_gen.generate_diagram(
                    roast_text, roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_path and os.path.exists(image_path):
                # Send image
                with open(image_path, 'rb') as photo:
                    caption = roast_data.get("caption", f"🎯 {target_user.first_name} -কে রোস্ট!")
                    await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                os.remove(image_path)
                self.stats["images_created"] += 1
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 রোস্ট অ্যানালাইসিস ডায়াগ্রাম",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                os.remove(diagram_path)
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True):
                await update.message.reply_text(
                    roast_data.get("primary_roast", "রোস্ট টাইম! 🔥"),
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating mention response: {e}")
            await update.message.reply_text(
                f"🎯 {mention_result.get('target_name', 'User')} -কে রোস্ট! 🔥",
                parse_mode=ParseMode.HTML
            )
    
    async def _generate_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                text: str, user: Any, chat: Any):
        """Generate regular response"""
        try:
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(text, user)
            
            # Update stats
            self.stats["roasts_generated"] += 1
            
            # Generate image
            image_path = await self.image_gen.generate_roast_image(roast_data, user)
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = self.diagram_gen.generate_diagram(
                    text, roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_path and os.path.exists(image_path):
                # Send image
                with open(image_path, 'rb') as photo:
                    caption = roast_data.get("caption", "রোস্ট টাইম! 🔥")
                    await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                os.remove(image_path)
                self.stats["images_created"] += 1
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 আপনার টেক্সট অ্যানালাইসিস",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                os.remove(diagram_path)
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True):
                await update.message.reply_text(
                    roast_data.get("primary_roast", "রোস্ট টাইম! 🔥"),
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await update.message.reply_text(
                f"🔥 {text}\n\n- {user.first_name}",
                parse_mode=ParseMode.HTML
            )
    
    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle vote callback queries"""
        try:
            await self.voting_system.handle_vote_callback(update, context)
        except Exception as e:
            logger.error(f"Error handling vote callback: {e}")
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        try:
            await self.welcome_system.handle_new_members(update, context)
        except Exception as e:
            logger.error(f"Error handling new chat members: {e}")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling update: {context.error}")
        traceback_str = traceback.format_exc()
        logger.error(f"Traceback:\n{traceback_str}")
    
    def setup_handlers(self, application):
        """Setup all bot handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("leaderboard", 
            lambda u, c: self.leaderboard.handle_leaderboard_command(u, c)))
        
        # Message handlers
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
        
        # New chat members
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_chat_members
        ))
        
        # Callback queries
        application.add_handler(CallbackQueryHandler(
            self.handle_vote_callback, pattern="^vote_"
        ))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        logger.info("All handlers setup complete")
    
    async def post_init(self, application):
        """Run after bot initialization"""
        logger.info(f"{self.bot_name} bot starting up...")
        
        # Initialize auto daily quote
        try:
            self.auto_daily_quote = AutoDailyQuote(application.job_queue)
        except:
            self.auto_daily_quote = None
        
        # Start background tasks
        asyncio.create_task(self._background_tasks())
        
        # Send startup notification
        await self._send_startup_notification()
        
        logger.info("Bot startup complete")
    
    async def _background_tasks(self):
        """Run background maintenance tasks"""
        while True:
            try:
                # Cleanup old data
                self.db.cleanup_old_data(days=7)
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(300)
    
    async def _send_startup_notification(self):
        """Send startup notification to owner"""
        try:
            from config import OWNER_ADMIN_PROTECTION
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if owner_id:
                bot_info = await self.application.bot.get_me()
                startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                message = f"""
🚀 <b>{self.bot_name} Started Successfully!</b>
━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot Username:</b> @{bot_info.username}
📊 <b>Version:</b> 3.0.0
━━━━━━━━━━━━━━━━━━━━
✅ <b>Status:</b> All systems operational
🔥 <b>Ready for roasting!</b>
                """
                
                await self.application.bot.send_message(
                    chat_id=owner_id,
                    text=message,
                    parse_mode=ParseMode.HTML
                )
                
                logger.info("Startup notification sent to owner")
        except Exception as e:
            logger.error(f"Error sending startup notification: {e}")
    
    def run(self):
        """Run the bot"""
        try:
            # Create application
            self.application = Application.builder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Run bot
            logger.info(f"Starting {self.bot_name} bot...")
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error running bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            raise


def main():
    """Main entry point"""
    # Create directories
    directories = [
        "assets/fonts",
        "assets/borders",
        "assets/templates",
        "assets/backgrounds",
        "data",
        "temp",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Run bot
    bot = RoastifyBot()
    bot.run()


if __name__ == "__main__":
    main()
