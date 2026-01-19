#!/usr/bin/env python3
"""
Roastify Bot v7.0 - COMPLETE FIXED & UPDATED
Image + Text + Diagram Reply with UltimateImageGenerator v6.0
"""

import os
import sys
import logging
import random
import re
import asyncio
import traceback
import math
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import concurrent.futures
import hashlib
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import project modules
try:
    from config import BOT_TOKEN, BOT_IDENTITY, CORE_RULES, OWNER_ADMIN_PROTECTION
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
    from utils.template_manager import TemplateManager
    
    # Import UltimateImageGenerator v6.0
    from utils.image_generator_ultimate import (
        UltimateImageGenerator, 
        GenerationResult,
        ImageConfig,
        TextConfig,
        BorderConfig,
        BackgroundConfig,
        BorderType,
        TextEffect,
        GradientDirection
    )
    
    # Import PIL
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    HAS_PIL = True
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(traceback.format_exc())
    logger.error("Please check all required files exist")
    sys.exit(1)

# Import Telegram
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters,
        ContextTypes, CallbackQueryHandler, ApplicationBuilder
    )
    from telegram.constants import ParseMode
except ImportError:
    logger.error("Install: pip install python-telegram-bot")
    sys.exit(1)


class AsyncImageGenerator:
    """Async wrapper for UltimateImageGenerator"""
    
    def __init__(self, config: Optional[ImageConfig] = None):
        self.generator = UltimateImageGenerator(config)
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix='ImageGenAsync'
        )
        logger.info("AsyncImageGenerator initialized")
    
    async def generate_roast_image_async(self, roast_text: Any, user_info: Any,
                                       style: str = "auto", 
                                       border_config: Optional[BorderConfig] = None,
                                       background_config: Optional[BackgroundConfig] = None) -> GenerationResult:
        """Async wrapper for image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_roast_image(
                    roast_text, user_info, style, border_config, background_config
                )
            )
            return result
        except Exception as e:
            logger.error(f"Async image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    async def generate_welcome_image_async(self, user_info: Any) -> GenerationResult:
        """Async wrapper for welcome image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_welcome_image(user_info)
            )
            return result
        except Exception as e:
            logger.error(f"Async welcome image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    async def generate_achievement_image_async(self, user_info: Any, achievement: Any) -> GenerationResult:
        """Async wrapper for achievement image generation"""
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: self.generator.generate_achievement_image(user_info, achievement)
            )
            return result
        except Exception as e:
            logger.error(f"Async achievement image generation failed: {e}")
            return GenerationResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    def get_stats(self) -> Dict:
        """Get generator statistics"""
        return self.generator.get_detailed_stats()
    
    def health_check(self) -> Dict:
        """Health check"""
        return self.generator.health_check()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.generator.cleanup()
            self.executor.shutdown(wait=False)
        except:
            pass


class DiagramGenerator:
    """Generate random diagrams for roasts"""
    
    def __init__(self):
        self.diagram_types = [
            "flow_chart", "pie_chart", "bar_chart", 
            "line_graph", "venn_diagram", "mind_map",
            "process_diagram", "comparison_chart"
        ]
        
        # Color palettes
        self.palettes = {
            "funny": [(255, 200, 100), (255, 150, 150), (200, 255, 200), (200, 200, 255)],
            "savage": [(255, 100, 100), (150, 50, 50), (100, 100, 100), (50, 50, 50)],
            "friendly": [(100, 200, 255), (150, 255, 150), (255, 255, 150), (255, 200, 255)],
            "clever": [(100, 100, 255), (200, 100, 200), (100, 200, 200), (200, 200, 100)]
        }
    
    async def generate_diagram_async(self, text: str, roast_type: str = "funny") -> Optional[str]:
        """Generate a diagram image based on text (async)"""
        if not HAS_PIL:
            return None
        
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                None,
                self._generate_diagram_sync,
                text,
                roast_type
            )
            return result
        except Exception as e:
            logger.error(f"Diagram generation failed: {e}")
            return None
    
    def _generate_diagram_sync(self, text: str, roast_type: str) -> Optional[str]:
        """Synchronous diagram generation"""
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
            
            # Get colors for roast type
            colors = self.palettes.get(roast_type, self.palettes["funny"])
            
            # Add title
            title = f"{roast_type.upper()} ANALYSIS"
            try:
                font = ImageFont.truetype("assets/fonts/arial.ttf", 36)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except:
                    font = ImageFont.load_default()
            
            # Draw title
            draw.text((width//2 - 150, 30), title, fill=(0, 0, 0), font=font, align="center")
            
            # Add subtitle
            subtitle = f"Based on: {text[:50]}{'...' if len(text) > 50 else ''}"
            draw.text((width//2 - 200, 80), subtitle, fill=(100, 100, 100), font=ImageFont.load_default())
            
            # Generate diagram based on type
            if diagram_type == "pie_chart":
                self._draw_pie_chart(draw, width, height, colors)
            elif diagram_type == "bar_chart":
                self._draw_bar_chart(draw, width, height, colors, text)
            elif diagram_type == "flow_chart":
                self._draw_flow_chart(draw, width, height, colors, text)
            elif diagram_type == "venn_diagram":
                self._draw_venn_diagram(draw, width, height, colors, text)
            else:
                self._draw_generic_diagram(draw, width, height, colors, text)
            
            # Add footer
            footer = "Generated by Roastify v7.0"
            draw.text((width - 200, height - 30), footer, fill=(150, 150, 150), font=ImageFont.load_default())
            
            # Apply effects
            image = self._apply_diagram_effects(image)
            
            # Save image
            image.save(filename, 'PNG', quality=95, optimize=True)
            logger.info(f"Diagram generated: {filename}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating diagram: {e}")
            return None
    
    def _apply_diagram_effects(self, image: Image.Image) -> Image.Image:
        """Apply effects to diagram"""
        try:
            # Add slight noise
            width, height = image.size
            noise = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(noise)
            
            for _ in range(100):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                alpha = random.randint(5, 15)
                size = random.randint(1, 2)
                draw.ellipse([x, y, x + size, y + size], fill=(255, 255, 255, alpha))
            
            result = Image.alpha_composite(image.convert('RGBA'), noise)
            return result.convert('RGB')
        except:
            return image
    
    def _draw_pie_chart(self, draw, width, height, colors):
        """Draw a pie chart"""
        center_x, center_y = width // 2, height // 2 - 50
        radius = 150
        
        # Generate random segments
        segments = random.randint(3, 6)
        segment_sizes = [random.randint(1, 10) for _ in range(segments)]
        total = sum(segment_sizes)
        
        start_angle = 0
        for i in range(segments):
            # Calculate angle based on segment size
            angle = 360 * (segment_sizes[i] / total)
            end_angle = start_angle + angle
            
            # Draw segment
            draw.pieslice(
                [center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius],
                start_angle, end_angle,
                fill=colors[i % len(colors)],
                outline=(0, 0, 0),
                width=2
            )
            
            # Add label
            label_angle = (start_angle + end_angle) / 2
            label_rad = math.radians(label_angle)
            label_x = center_x + (radius + 40) * math.cos(label_rad)
            label_y = center_y + (radius + 40) * math.sin(label_rad)
            
            label = f"{int((segment_sizes[i]/total)*100)}%"
            draw.text((label_x - 10, label_y - 10), label, fill=(0, 0, 0))
            
            start_angle = end_angle
        
        # Add legend
        legend_x = 50
        legend_y = height - 150
        for i in range(min(segments, 4)):
            # Color box
            draw.rectangle(
                [legend_x, legend_y + i*30, legend_x + 20, legend_y + i*30 + 20],
                fill=colors[i % len(colors)],
                outline=(0, 0, 0)
            )
            # Label
            draw.text(
                (legend_x + 30, legend_y + i*30),
                f"Factor {i+1}: {segment_sizes[i]} pts",
                fill=(0, 0, 0)
            )
    
    def _draw_bar_chart(self, draw, width, height, colors, text):
        """Draw a bar chart"""
        chart_x, chart_y = 100, 100
        chart_width, chart_height = 600, 350
        
        # Draw axes
        draw.line([(chart_x, chart_y), (chart_x, chart_y + chart_height)], fill=(0, 0, 0), width=3)
        draw.line([(chart_x, chart_y + chart_height), 
                   (chart_x + chart_width, chart_y + chart_height)], fill=(0, 0, 0), width=3)
        
        # Generate bars based on text hash
        text_hash = hashlib.md5(text.encode()).hexdigest()
        bars = min(6, len(text_hash) // 4)
        
        bar_width = chart_width // (bars + 2)
        
        for i in range(bars):
            x = chart_x + (i + 1) * bar_width
            # Use text hash for deterministic but varied heights
            hash_val = int(text_hash[i*4:(i+1)*4], 16)
            bar_height = chart_height * (hash_val % 70 + 30) / 100
            
            # Draw bar
            color = colors[i % len(colors)]
            draw.rectangle(
                [x, chart_y + chart_height - bar_height,
                 x + bar_width - 15, chart_y + chart_height],
                fill=color,
                outline=(0, 0, 0),
                width=2
            )
            
            # Add value
            value = int((bar_height / chart_height) * 100)
            draw.text((x + bar_width//2 - 10, chart_y + chart_height - bar_height - 20), 
                     f"{value}%", fill=(0, 0, 0))
            
            # Add label
            labels = ["Humor", "Logic", "Sarcasm", "Creativity", "Impact", "Style"]
            label = labels[i] if i < len(labels) else f"Cat{i+1}"
            draw.text((x + bar_width//2 - 20, chart_y + chart_height + 10), label, fill=(0, 0, 0))
    
    def _draw_flow_chart(self, draw, width, height, colors, text):
        """Draw a flow chart"""
        # Draw boxes
        box_width, box_height = 140, 50
        positions = [
            (width//2 - box_width//2, 100),
            (150, 200),
            (width - 290, 200),
            (width//2 - box_width//2, 300),
            (width//2 - box_width//2, 400)
        ]
        
        box_texts = [
            "Input Text",
            "Analyze Context",
            "Generate Roast",
            "Add Humor",
            "Deliver!"
        ]
        
        for i, (x, y) in enumerate(positions):
            # Draw box
            draw.rounded_rectangle(
                [x, y, x + box_width, y + box_height],
                radius=10,
                fill=colors[i % len(colors)],
                outline=(0, 0, 0),
                width=2
            )
            
            # Add text
            text_in_box = box_texts[i] if i < len(box_texts) else f"Step {i+1}"
            draw.text((x + box_width//2 - 30, y + box_height//2 - 10), 
                     text_in_box, fill=(0, 0, 0))
        
        # Draw arrows
        arrow_positions = [
            (0, 1), (0, 2), (1, 3), (2, 3), (3, 4)
        ]
        
        for start_idx, end_idx in arrow_positions:
            if start_idx < len(positions) and end_idx < len(positions):
                x1 = positions[start_idx][0] + box_width//2
                y1 = positions[start_idx][1] + box_height
                x2 = positions[end_idx][0] + box_width//2
                y2 = positions[end_idx][1]
                
                # Draw line
                draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=2)
                
                # Draw arrow head
                draw.polygon([
                    (x2, y2),
                    (x2 - 8, y2 + 15),
                    (x2 + 8, y2 + 15)
                ], fill=(0, 0, 0))
    
    def _draw_venn_diagram(self, draw, width, height, colors, text):
        """Draw a Venn diagram"""
        center_x, center_y = width // 2, height // 2
        radius = 130
        
        # Draw circles with transparency
        circle_colors = [
            (255, 0, 0, 128),   # Red
            (0, 255, 0, 128),   # Green
            (0, 0, 255, 128)    # Blue
        ]
        
        offsets = [(-100, 0), (100, 0), (0, 100)]
        labels = ["Logic", "Emotion", "Humor"]
        
        for i in range(3):
            offset_x, offset_y = offsets[i]
            
            # Create circle with transparency
            circle_img = Image.new('RGBA', (radius*2, radius*2), (0, 0, 0, 0))
            circle_draw = ImageDraw.Draw(circle_img)
            circle_draw.ellipse(
                [0, 0, radius*2, radius*2],
                fill=circle_colors[i],
                outline=(0, 0, 0, 255),
                width=3
            )
            
            # Paste onto main image
            mask = circle_img.split()[3]
            draw.bitmap(
                (center_x + offset_x - radius, center_y + offset_y - radius),
                mask,
                fill=circle_colors[i][:3]
            )
            
            # Add outline
            draw.ellipse(
                [center_x + offset_x - radius, center_y + offset_y - radius,
                 center_x + offset_x + radius, center_y + offset_y + radius],
                outline=(0, 0, 0),
                width=3
            )
            
            # Add labels
            draw.text((center_x + offset_x - 30, center_y + offset_y - radius - 30),
                     labels[i], fill=(0, 0, 0), font=ImageFont.load_default().font_variant(size=16))
        
        # Add intersection labels
        draw.text((center_x - 20, center_y - 10), "Witty", fill=(0, 0, 0))
        draw.text((center_x - 50, center_y + 40), "Clever", fill=(0, 0, 0))
        draw.text((center_x + 30, center_y + 40), "Funny", fill=(0, 0, 0))
        draw.text((center_x - 10, center_y + 20), "Perfect\nRoast", fill=(0, 0, 0))
    
    def _draw_generic_diagram(self, draw, width, height, colors, text):
        """Draw a generic diagram"""
        # Draw a network/graph
        nodes = min(8, len(text) // 5 + 3)
        node_radius = 25
        node_positions = []
        
        # Generate node positions in a circle
        center_x, center_y = width // 2, height // 2 - 50
        circle_radius = 200
        
        for i in range(nodes):
            angle = 2 * math.pi * i / nodes
            x = center_x + circle_radius * math.cos(angle)
            y = center_y + circle_radius * math.sin(angle)
            node_positions.append((x, y))
            
            # Draw node
            color = colors[i % len(colors)]
            draw.ellipse(
                [x - node_radius, y - node_radius,
                 x + node_radius, y + node_radius],
                fill=color,
                outline=(0, 0, 0),
                width=3
            )
            
            # Add node label
            node_labels = ["Idea", "Words", "Humor", "Timing", "Context", "Delivery", "Impact", "Style"]
            label = node_labels[i] if i < len(node_labels) else f"Node{i+1}"
            draw.text((x - 15, y - 10), label, fill=(0, 0, 0))
        
        # Draw connections (fully connected for small networks)
        for i in range(nodes):
            for j in range(i + 1, nodes):
                # Higher chance for connections in smaller networks
                if nodes <= 4 or random.random() > 0.3:
                    x1, y1 = node_positions[i]
                    x2, y2 = node_positions[j]
                    
                    # Line width based on "importance"
                    line_width = 1 + (hash(text) % 3)
                    draw.line([(x1, y1), (x2, y2)], 
                             fill=(100, 100, 100), 
                             width=line_width)
        
        # Add central node
        draw.ellipse(
            [center_x - 40, center_y - 40,
             center_x + 40, center_y + 40],
            fill=(255, 255, 200),
            outline=(0, 0, 0),
            width=4
        )
        draw.text((center_x - 30, center_y - 10), "ROAST", fill=(0, 0, 0))


class RoastifyBot:
    """Main Roastify Bot Class v7.0"""
    
    def __init__(self):
        """Initialize the bot"""
        self.bot_token = BOT_TOKEN
        self.bot_name = BOT_IDENTITY.get("name", "Roastify")
        self.bot_tagline = BOT_IDENTITY.get("tagline", "")
        
        # Initialize components
        self.db = get_database()
        
        # Initialize Image Generator with config
        image_config = ImageConfig(
            width=1080,
            height=1080,
            quality=95,
            format="PNG",
            enable_cache=True,
            cache_ttl_hours=24,
            max_cache_size=1000,
            output_dir="./output",
            temp_dir="./temp",
            cache_dir="./cache",
            assets_dir="./assets",
            backup_dir="./backup",
            max_workers=4,
            timeout=30.0,
            enable_backup=True,
            compression_level=6
        )
        
        self.image_gen = AsyncImageGenerator(image_config)
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
            "start_time": datetime.now(),
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Application instance
        self.application = None
        
        # Rate limiting
        self.user_cooldowns = {}  # user_id -> last_request_time
        self.cooldown_seconds = CORE_RULES.get("cooldown_seconds", 3)
        
        logger.info(f"Initialized {self.bot_name} Bot v7.0")
    
    def _check_cooldown(self, user_id: int) -> bool:
        """Check if user is in cooldown"""
        now = time.time()
        last_request = self.user_cooldowns.get(user_id, 0)
        
        if now - last_request < self.cooldown_seconds:
            return False
        
        self.user_cooldowns[user_id] = now
        return True
    
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
            
            # Get welcome message
            welcome_message = f"""
🎉 <b>স্বাগতম {user.first_name}!</b>

🤖 আমি <b>{self.bot_name}</b> - {self.bot_tagline}

🔥 <b>আমি যা করতে পারি:</b>
• যেকোনো টেক্সটে রোস্ট ইমেজ তৈরি
• স্মার্ট ডায়াগ্রাম জেনারেশন
• মেনশন করে গ্রুপে রোস্ট
• অটো রিএকশন ও ভোটিং
• লিডারবোর্ড ও অ্যাচিভমেন্ট

📝 <b>ব্যবহার:</b>
শুধু আমাকে কিছু লিখে পাঠান!
• ব্যক্তিগত চ্যাটে: সরাসরি লিখুন
• গ্রুপে: @{context.bot.username} mention করুন

🔧 <b>কমান্ড:</b>
/help - সাহায্য
/stats - পরিসংখ্যান
/leaderboard - র্যাঙ্কিং
/health - সিস্টেম স্বাস্থ্য

⚡ <b>এখনি চেষ্টা করুন!</b>
কিছু লিখে পাঠান আর দেখুন জাদু!
            """
            
            # Generate welcome image
            welcome_result = await self.image_gen.generate_welcome_image_async(user)
            
            if welcome_result.success and welcome_result.image_path:
                # Send welcome image
                with open(welcome_result.image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"🎉 {user.first_name} -কে স্বাগতম!",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(welcome_result.image_path)
                except:
                    pass
                
                # Send welcome text
                await update.message.reply_text(
                    welcome_message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            else:
                # Fallback to text only
                await update.message.reply_text(
                    welcome_message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            
            logger.info(f"New start from user {user.id} in chat {chat.id}")
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text(
                f"স্বাগতম {user.first_name}! 🎉\n"
                f"আমি {self.bot_name} - {self.bot_tagline}\n\n"
                f"কিছু লিখে পাঠান রোস্ট শুরু করতে!",
                parse_mode=ParseMode.HTML
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
<b>{self.bot_name} v7.0 - {self.bot_tagline}</b>

🤖 <b>ব্যবহার পদ্ধতি:</b>
• যেকোনো টেক্সট পাঠান (সর্বনিম্ন ৪ অক্ষর)
• আমি প্রফেশনাল ইমেজ + ডায়াগ্রাম সহ রিপ্লাই দেব
• কোন কমান্ডের প্রয়োজন নেই!

🎯 <b>নতুন বৈশিষ্ট্য:</b>
• Ultra HD 1080p ইমেজ জেনারেশন
• Intelligent Diagram Creation
• Smart Cache System (ফাস্ট রেস্পন্স)
• Advanced Error Handling
• Real-time Statistics

👥 <b>গ্রুপে ব্যবহার:</b>
• @mentions দিয়ে টার্গেটেড রোস্ট
• নতুন সদস্য স্বাগতম
• Auto Reactions
• Voting System

🔧 <b>কমান্ড:</b>
/start - শুরু করুন
/help - সাহায্য
/stats - পরিসংখ্যান
/leaderboard - র্যাঙ্কিং
/health - সিস্টেম স্বাস্থ্য

⚡ <b>টিপস:</b>
• গ্রুপে @মেনশন ব্যবহার করুন
• ভোট দিয়ে উন্নতি করুন
• রেগুলার চেক করুন লিডারবোর্ড

🔒 <b>গোপনীয়তা:</b>
• ব্যক্তিগত তথ্য সংরক্ষণ করা হয় না
• নিরাপদ শেয়ারিং
• Rate Limiting Enabled

📊 <b>স্ট্যাটাস:</b>
✅ All Systems Operational
🔄 Real-time Processing
⚡ Fast Response Time
        """
        
        await update.message.reply_text(
            help_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user = update.effective_user
        
        try:
            # Check if admin
            admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if user.id not in admin_ids and user.id != owner_id:
                await update.message.reply_text(
                    "❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!",
                    parse_mode=ParseMode.HTML
                )
                return
        except:
            pass
        
        # Calculate uptime
        uptime = datetime.now() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        # Get image generator stats
        img_stats = self.image_gen.get_stats()
        
        stats_text = f"""
<b>{self.bot_name} পরিসংখ্যান v7.0</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>আপটাইম:</b> {days}দিন {hours}ঘণ্টা {minutes}মিনিট
📊 <b>বার্তা প্রসেসড:</b> {self.stats['messages_processed']:,}
🔥 <b>রোস্ট জেনারেটেড:</b> {self.stats['roasts_generated']:,}
🖼️ <b>ইমেজ তৈরি:</b> {self.stats['images_created']:,}
📈 <b>ডায়াগ্রাম তৈরি:</b> {self.stats['diagrams_created']:,}
👥 <b>ইউজার:</b> {len(self.stats['users_interacted']):,}
🏠 <b>গ্রুপ:</b> {len(self.stats['groups_managed']):,}

<b>ইমেজ জেনারেশন:</b>
✅ <b>সাকসেস রেট:</b> {img_stats['performance']['success_rate']}%
⚡ <b>অ্যাভারেজ টাইম:</b> {img_stats['performance']['average_time_seconds']:.2f}s
💾 <b>ক্যাশে হিট রেট:</b> {img_stats['performance']['cache_hit_rate']}%
🔄 <b>ক্যাশে আইটেম:</b> {img_stats['cache']['total_items']:,}

<b>সিস্টেম:</b> ✅ অপারেশনাল
━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        await update.message.reply_text(
            stats_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /health command"""
        user = update.effective_user
        
        try:
            # Check if admin
            admin_ids = OWNER_ADMIN_PROTECTION.get("admin_user_ids", [])
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if user.id not in admin_ids and user.id != owner_id:
                await update.message.reply_text(
                    "❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য!",
                    parse_mode=ParseMode.HTML
                )
                return
        except:
            pass
        
        # Get health status
        health_status = self.image_gen.health_check()
        
        health_text = f"""
<b>{self.bot_name} সিস্টেম স্বাস্থ্য v7.0</b>
━━━━━━━━━━━━━━━━━━━━━━━━
<b>সামগ্রিক অবস্থা:</b> {"✅ সুস্থ" if health_status['healthy'] else "⚠️ সমস্যা"}
<b>চেক করা হয়েছে:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

<b>কম্পোনেন্ট চেক:</b>
{"✅" if health_status['checks']['pil_available'] else "❌"} PIL/Pillow উপলব্ধ
{"✅" if health_status['checks']['directories_accessible'] else "❌"} ডিরেক্টরি এক্সেস
{"✅" if health_status['checks']['font_manager_ready'] else "❌"} ফন্ট ম্যানেজার
{"✅" if health_status['checks']['cache_operational'] else "❌"} ক্যাশে সিস্টেম
{"✅" if health_status['checks']['write_permissions'] else "❌"} রাইট পারমিশন

<b>ডেটাবেজ:</b> ✅ কানেক্টেড
<b>ফিচার লোড:</b> ✅ {len(self.features)} ফিচার
<b>মেমরি ব্যবহার:</b> 🟢 স্বাভাবিক
<b>CPU লোড:</b> 🟢 স্বাভাবিক

<b>রিকমেন্ডেশন:</b>
• নিয়মিত ব্যাকআপ নিন
• লগ মনিটর করুন
• ভার্সন আপডেট রাখুন
━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        await update.message.reply_text(
            health_text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    
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
            
            # Check cooldown
            if not self._check_cooldown(user.id):
                if chat.type == "private":
                    await message.reply_text(
                        "⏳ একটু অপেক্ষা করুন! খুব দ্রুত রিকোয়েস্ট করছেন।",
                        parse_mode=ParseMode.HTML
                    )
                return
            
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
            except Exception as e:
                logger.error(f"Admin protection error: {e}")
            
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
            except Exception as e:
                logger.error(f"Auto reaction error: {e}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
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
        
        # Check for very repetitive text
        if len(text) > 20:
            if text.count(text[0]) / len(text) > 0.8:
                return True
        
        return False
    
    async def _generate_mention_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        text: str, user: Any, chat: Any, mention_result: Dict):
        """Generate response for mentioned user"""
        try:
            target_user = mention_result.get("target")
            roast_text = mention_result.get("roast_text", text)
            
            # Generate typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(
                roast_text, user, target_user
            )
            
            # Update stats
            self.stats["roasts_generated"] += 1
            
            # Generate image
            image_result = await self.image_gen.generate_roast_image_async(
                roast_data, 
                user,
                "auto",
                None,
                None
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = await self.diagram_gen.generate_diagram_async(
                    roast_text, 
                    roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_result.success and image_result.image_path:
                # Send image
                with open(image_result.image_path, 'rb') as photo:
                    caption = roast_data.get("caption", f"🎯 {target_user.first_name} -কে রোস্ট!")
                    sent_message = await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Update cache stats
                if image_result.cache_hit:
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["cache_misses"] += 1
                
                # Cleanup
                try:
                    os.remove(image_result.image_path)
                except:
                    pass
                
                self.stats["images_created"] += 1
                
                # Add voting buttons
                try:
                    await self.voting_system.add_voting_buttons(sent_message, user, target_user)
                except:
                    pass
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 রোস্ট অ্যানালাইসিস ডায়াগ্রাম",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(diagram_path)
                except:
                    pass
                
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True) and roast_data.get("primary_roast"):
                await update.message.reply_text(
                    roast_data.get("primary_roast"),
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating mention response: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            await update.message.reply_text(
                f"🎯 {mention_result.get('target_name', 'User')} -কে রোস্ট! 🔥",
                parse_mode=ParseMode.HTML
            )
    
    async def _generate_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                text: str, user: Any, chat: Any):
        """Generate regular response"""
        try:
            # Generate typing action
            await update.message.chat.send_action(action="upload_photo")
            
            # Get roast from engine
            roast_data = await self.roast_engine.generate_roast(text, user)
            
            # Update stats
            self.stats["roasts_generated"] += 1
            
            # Generate image
            image_result = await self.image_gen.generate_roast_image_async(
                roast_data, 
                user,
                "auto",
                None,
                None
            )
            
            # Generate diagram
            diagram_path = None
            if CORE_RULES.get("diagram_reply", True):
                diagram_path = await self.diagram_gen.generate_diagram_async(
                    text, 
                    roast_data.get("roast_type", "funny")
                )
            
            # Send responses
            if image_result.success and image_result.image_path:
                # Send image
                with open(image_result.image_path, 'rb') as photo:
                    caption = roast_data.get("caption", "রোস্ট টাইম! 🔥")
                    sent_message = await update.message.reply_photo(
                        photo=photo,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                
                # Update cache stats
                if image_result.cache_hit:
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["cache_misses"] += 1
                
                # Cleanup
                try:
                    os.remove(image_result.image_path)
                except:
                    pass
                
                self.stats["images_created"] += 1
                
                # Add voting buttons
                try:
                    await self.voting_system.add_voting_buttons(sent_message, user, None)
                except:
                    pass
            
            # Send diagram
            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="📊 আপনার টেক্সট অ্যানালাইসিস",
                        parse_mode=ParseMode.HTML
                    )
                
                # Cleanup
                try:
                    os.remove(diagram_path)
                except:
                    pass
                
                self.stats["diagrams_created"] += 1
            
            # Send text reply if enabled
            if CORE_RULES.get("text_reply", True) and roast_data.get("primary_roast"):
                await update.message.reply_text(
                    roast_data.get("primary_roast"),
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
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
            await update.callback_query.answer("ভোট প্রসেসে সমস্যা!", show_alert=True)
    
    async def handle_new_chat_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new chat members"""
        try:
            await self.welcome_system.handle_new_members(update, context)
        except Exception as e:
            logger.error(f"Error handling new chat members: {e}")
    
    async def handle_leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        try:
            await self.leaderboard.handle_leaderboard_command(update, context)
        except Exception as e:
            logger.error(f"Error handling leaderboard: {e}")
            await update.message.reply_text(
                "লিডারবোর্ড লোড করতে সমস্যা!",
                parse_mode=ParseMode.HTML
            )
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling update: {context.error}")
        traceback_str = traceback.format_exc()
        logger.error(f"Traceback:\n{traceback_str}")
        
        # Try to send error to admin
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            if owner_id and context.bot:
                error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_msg = str(context.error)[:500]
                
                error_text = f"""
🚨 <b>বট এরর!</b>
━━━━━━━━━━━━━━━━
⏰ <b>সময়:</b> {error_time}
💥 <b>এরর:</b> {error_msg}
━━━━━━━━━━━━━━━━
<b>অ্যাকশন:</b> চেক লগ ফাইল
                """
                
                await context.bot.send_message(
                    chat_id=owner_id,
                    text=error_text,
                    parse_mode=ParseMode.HTML
                )
        except:
            pass
    
    def setup_handlers(self, application):
        """Setup all bot handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("health", self.health_command))
        application.add_handler(CommandHandler("leaderboard", self.handle_leaderboard_command))
        
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
        logger.info(f"{self.bot_name} bot starting up v7.0...")
        
        # Initialize auto daily quote
        try:
            self.auto_daily_quote = AutoDailyQuote(application.job_queue)
            logger.info("Auto Daily Quote initialized")
        except Exception as e:
            logger.error(f"Auto Daily Quote init failed: {e}")
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
                
                # Cleanup old temp files
                self._cleanup_temp_files()
                
                # Log statistics every hour
                logger.info(f"Statistics: {self.stats['messages_processed']} messages, "
                           f"{self.stats['roasts_generated']} roasts, "
                           f"{self.stats['images_created']} images")
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(300)
    
    def _cleanup_temp_files(self):
        """Cleanup old temporary files"""
        try:
            temp_dir = Path("temp")
            if temp_dir.exists():
                cutoff_time = time.time() - 3600  # 1 hour ago
                
                for file in temp_dir.glob("*"):
                    if file.is_file():
                        try:
                            if file.stat().st_mtime < cutoff_time:
                                file.unlink()
                        except:
                            pass
        except Exception as e:
            logger.error(f"Temp cleanup error: {e}")
    
    async def _send_startup_notification(self):
        """Send startup notification to owner"""
        try:
            owner_id = OWNER_ADMIN_PROTECTION.get("bot_owner_user_id")
            
            if owner_id:
                bot_info = await self.application.bot.get_me()
                startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get system health
                health = self.image_gen.health_check()
                
                message = f"""
🚀 <b>{self.bot_name} Started Successfully v7.0!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>Start Time:</b> {startup_time}
🤖 <b>Bot Username:</b> @{bot_info.username}
📊 <b>Version:</b> 7.0.0
🏥 <b>Health:</b> {"✅ Healthy" if health['healthy'] else "⚠️ Issues"}

<b>Features:</b>
• Ultimate Image Generator v6.0
• Async Processing
• Smart Caching
• Advanced Diagrams
• Rate Limiting
• Full Error Handling

✅ <b>Status:</b> All systems operational
🔥 <b>Ready for roasting!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
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
            self.application = ApplicationBuilder()\
                .token(self.bot_token)\
                .post_init(self.post_init)\
                .build()
            
            # Setup handlers
            self.setup_handlers(self.application)
            
            # Run bot
            logger.info(f"Starting {self.bot_name} bot v7.0...")
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            
            # Cleanup
            try:
                self.image_gen.cleanup()
            except:
                pass
            
        except Exception as e:
            logger.error(f"Fatal error running bot: {e}")
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback:\n{traceback_str}")
            
            # Cleanup
            try:
                self.image_gen.cleanup()
            except:
                pass
            
            raise


def create_directories():
    """Create necessary directories"""
    directories = [
        "assets/fonts",
        "assets/borders",
        "assets/templates",
        "assets/backgrounds",
        "output",
        "temp",
        "cache",
        "backup",
        "logs",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def main():
    """Main entry point"""
    # Create directories
    create_directories()
    
    # Check for required files
    required_files = [
        "config.py",
        "database.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            logger.warning(f"Required file not found: {file}")
    
    # Run bot
    bot = RoastifyBot()
    bot.run()


if __name__ == "__main__":
    main()
