#!/usr/bin/env python3
"""
Custom Template Unlock System for Roastify Bot
Users can unlock special templates through activity
"""

import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
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
    from utils.template_manager import TemplateManager
except ImportError:
    logger.error("Required modules not found")
    sys.exit(1)


class CustomTemplateUnlocks:
    """Manages template unlocking system"""
    
    def __init__(self):
        """Initialize template unlock system"""
        self.config = EXTRA_FEATURES.get("custom_template_unlocks", {})
        self.db = get_database()
        self.template_manager = TemplateManager()
        
        # Load unlockable templates
        self.unlockable_templates = self._load_unlockable_templates()
        
        # Track user progress
        self.user_progress = {}  # user_id -> progress_data
        
        logger.info("Custom Template Unlocks system initialized")
    
    def _load_unlockable_templates(self) -> Dict[str, Dict]:
        """Load unlockable templates configuration"""
        unlockable_templates = {
            "golden_roast": {
                "name": "গোল্ডেন রোস্ট",
                "description": "স্বর্ণের মতো চমকপ্রদ রোস্ট টেমপ্লেট",
                "requirement": {
                    "type": "roast_count",
                    "threshold": 50
                },
                "unlocked_by_default": False,
                "rarity": "rare",
                "colors": [(255, 215, 0), (255, 195, 0), (218, 165, 32)]
            },
            "diamond_savage": {
                "name": "ডায়মন্ড স্যাভেজ",
                "description": "হীরার মতো কঠিন এবং চকচকে রোস্ট",
                "requirement": {
                    "type": "vote_count",
                    "threshold": 100
                },
                "unlocked_by_default": False,
                "rarity": "epic",
                "colors": [(185, 242, 255), (0, 191, 255), (30, 144, 255)]
            },
            "rainbow_mock": {
                "name": "রেইনবো মক",
                "description": "রংধনুর সব রঙের সমাহার",
                "requirement": {
                    "type": "reaction_count",
                    "threshold": 200
                },
                "unlocked_by_default": False,
                "rarity": "legendary",
                "colors": [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                          (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
            },
            "phantom_sarcasm": {
                "name": "ফ্যান্টম সারকাজম",
                "description": "ভুতুড়ে স্টাইলের সাসপেন্সফুল রোস্ট",
                "requirement": {
                    "type": "days_active",
                    "threshold": 7
                },
                "unlocked_by_default": False,
                "rarity": "rare",
                "colors": [(0, 0, 0), (50, 50, 50), (100, 100, 100)]
            },
            "celestial_burn": {
                "name": "সেলেস্টিয়াল বার্ন",
                "description": "মহাজাগতিক স্টাইলের জ্বলন্ত রোস্ট",
                "requirement": {
                    "type": "streak",
                    "threshold": 5
                },
                "unlocked_by_default": False,
                "rarity": "epic",
                "colors": [(0, 0, 139), (25, 25, 112), (138, 43, 226)]
            }
        }
        
        # Load from file if exists
        import os
        unlock_file = "data/unlockable_templates.json"
        if os.path.exists(unlock_file):
            try:
                import json
                with open(unlock_file, 'r', encoding='utf-8') as f:
                    file_templates = json.load(f)
                    unlockable_templates.update(file_templates)
            except Exception as e:
                logger.error(f"Error loading unlockable templates: {e}")
        
        return unlockable_templates
    
    async def check_unlocks(self, user_id: int) -> List[Dict]:
        """Check for new template unlocks for user"""
        try:
            # Get user statistics
            user_stats = self._get_user_stats(user_id)
            
            # Check each unlockable template
            new_unlocks = []
            
            for template_id, template_data in self.unlockable_templates.items():
                # Skip if already unlocked
                if self._is_template_unlocked(user_id, template_id):
                    continue
                
                # Check if requirements met
                if self._check_requirements(user_stats, template_data["requirement"]):
                    # Unlock template
                    if self._unlock_template_for_user(user_id, template_id):
                        new_unlocks.append(template_data)
                        logger.info(f"Unlocked {template_id} for user {user_id}")
            
            return new_unlocks
            
        except Exception as e:
            logger.error(f"Error checking unlocks: {e}")
            return []
    
    def _get_user_stats(self, user_id: int) -> Dict[str, int]:
        """Get user statistics from database"""
        try:
            self.db.cursor.execute('''
                SELECT roast_count, vote_count, reaction_count,
                       julianday('now') - julianday(created_at) as days_since_join,
                       julianday('now') - julianday(last_active) as days_since_active
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            result = self.db.cursor.fetchone()
            
            if result:
                roast_count, vote_count, reaction_count, days_since_join, days_since_active = result
                
                # Calculate streak (simplified - days active in last week)
                self.db.cursor.execute('''
                    SELECT COUNT(DISTINCT DATE(last_active)) as active_days
                    FROM users
                    WHERE user_id = ? 
                    AND last_active > datetime('now', '-7 days')
                ''', (user_id,))
                
                streak_result = self.db.cursor.fetchone()
                streak = streak_result[0] if streak_result else 0
                
                return {
                    "roast_count": roast_count or 0,
                    "vote_count": vote_count or 0,
                    "reaction_count": reaction_count or 0,
                    "days_since_join": int(days_since_join or 0),
                    "days_since_active": int(days_since_active or 0),
                    "streak": streak
                }
            
            return {
                "roast_count": 0,
                "vote_count": 0,
                "reaction_count": 0,
                "days_since_join": 0,
                "days_since_active": 0,
                "streak": 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {
                "roast_count": 0,
                "vote_count": 0,
                "reaction_count": 0,
                "days_since_join": 0,
                "days_since_active": 0,
                "streak": 0
            }
    
    def _check_requirements(self, user_stats: Dict, requirement: Dict) -> bool:
        """Check if user meets template requirements"""
        req_type = requirement["type"]
        threshold = requirement["threshold"]
        
        if req_type == "roast_count":
            return user_stats["roast_count"] >= threshold
        elif req_type == "vote_count":
            return user_stats["vote_count"] >= threshold
        elif req_type == "reaction_count":
            return user_stats["reaction_count"] >= threshold
        elif req_type == "days_active":
            return user_stats["days_since_join"] >= threshold
        elif req_type == "streak":
            return user_stats["streak"] >= threshold
        elif req_type == "any":
            # Any of multiple requirements
            for sub_req in requirement.get("requirements", []):
                if self._check_requirements(user_stats, sub_req):
                    return True
            return False
        elif req_type == "all":
            # All of multiple requirements
            for sub_req in requirement.get("requirements", []):
                if not self._check_requirements(user_stats, sub_req):
                    return False
            return True
        
        return False
    
    def _is_template_unlocked(self, user_id: int, template_id: str) -> bool:
        """Check if template is unlocked for user"""
        try:
            self.db.cursor.execute('''
                SELECT COUNT(*) FROM template_unlocks
                WHERE user_id = ? AND template_id = ?
            ''', (user_id, template_id))
            
            return self.db.cursor.fetchone()[0] > 0
            
        except Exception as e:
            logger.error(f"Error checking template unlock: {e}")
            return False
    
    def _unlock_template_for_user(self, user_id: int, template_id: str) -> bool:
        """Unlock template for user"""
        try:
            self.db.cursor.execute('''
                INSERT OR IGNORE INTO template_unlocks (user_id, template_id, unlocked_at)
                VALUES (?, ?, ?)
            ''', (user_id, template_id, datetime.now().isoformat()))
            
            self.db.conn.commit()
            
            # Also add to template manager if it's a new template
            template_data = self.unlockable_templates.get(template_id)
            if template_data:
                # Create template for template manager
                template_obj = {
                    "id": template_id,
                    "name": template_data["name"],
                    "style": "premium",
                    "background_color": template_data["colors"][0],
                    "text_color": (255, 255, 255),
                    "border_color": template_data["colors"][-1],
                    "font_style": "premium",
                    "effects": ["premium", "special"],
                    "unlocked": True,
                    "rarity": template_data.get("rarity", "common"),
                    "category": "premium_unlocked"
                }
                
                # Add to template manager
                self.template_manager.add_template("premium_unlocked", template_obj)
            
            return True
            
        except Exception as e:
            logger.error(f"Error unlocking template: {e}")
            return False
    
    async def notify_unlocks(self, user_id: int, new_unlocks: List[Dict], 
                            context: ContextTypes.DEFAULT_TYPE):
        """Notify user about new unlocks"""
        try:
            if not new_unlocks:
                return
            
            for unlock in new_unlocks:
                # Create notification message
                message = f"""
🎉 <b>নতুন টেমপ্লেট আনলক!</b> 🎉

✨ <b>{unlock['name']}</b> ✨

{unlock['description']}

🎨 <b>বিশেষত্ব:</b>
• প্রিমিয়াম কালার স্কিম
• ইউনিক ডিজাইন
• এক্সক্লুসিভ স্টাইল

এখন এই টেমপ্লেট ব্যবহার করে রোস্ট দিতে পারবে!
                """
                
                # Try to send to user
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode=ParseMode.HTML
                    )
                except:
                    # User might have blocked bot or can't receive messages
                    pass
                
                logger.info(f"Notified user {user_id} about unlock: {unlock['name']}")
            
        except Exception as e:
            logger.error(f"Error notifying unlocks: {e}")
    
    async def show_unlock_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's unlock progress"""
        try:
            user = update.effective_user
            
            # Get user stats
            user_stats = self._get_user_stats(user.id)
            
            # Prepare progress message
            message = f"""
🔓 <b>টেমপ্লেট আনলক প্রোগ্রেস</b> 🔓
━━━━━━━━━━━━━━━━━━━━━━━

👤 <b>ইউজার:</b> {user.first_name}

📊 <b>স্ট্যাটিস্টিকস:</b>
• রোস্ট কাউন্ট: {user_stats['roast_count']}
• ভোট কাউন্ট: {user_stats['vote_count']}
• রিঅ্যাকশন কাউন্ট: {user_stats['reaction_count']}
• সক্রিয় দিন: {user_stats['days_since_join']}
• স্ট্রিক: {user_stats['streak']} দিন

━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>আনলকযোগ্য টেমপ্লেট:</b>
            """
            
            # Add unlockable templates with progress
            for template_id, template_data in self.unlockable_templates.items():
                unlocked = self._is_template_unlocked(user.id, template_id)
                requirement = template_data["requirement"]
                
                if unlocked:
                    status = "✅ আনলকড"
                else:
                    # Calculate progress
                    progress = self._calculate_progress(user_stats, requirement)
                    status = f"🔒 {progress}%"
                
                message += f"\n• {template_data['name']}: {status}"
            
            # Add unlocked templates count
            unlocked_count = self._get_unlocked_count(user.id)
            message += f"\n\n🏆 <b>মোট আনলকড:</b> {unlocked_count}/{len(self.unlockable_templates)}"
            
            # Send message
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error showing unlock progress: {e}")
            await update.message.reply_text(
                "প্রোগ্রেস দেখাতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    def _calculate_progress(self, user_stats: Dict, requirement: Dict) -> int:
        """Calculate progress percentage for requirement"""
        req_type = requirement["type"]
        threshold = requirement["threshold"]
        
        if req_type == "roast_count":
            current = user_stats["roast_count"]
        elif req_type == "vote_count":
            current = user_stats["vote_count"]
        elif req_type == "reaction_count":
            current = user_stats["reaction_count"]
        elif req_type == "days_active":
            current = user_stats["days_since_join"]
        elif req_type == "streak":
            current = user_stats["streak"]
        else:
            return 0
        
        if threshold == 0:
            return 100
        
        progress = min(100, int((current / threshold) * 100))
        return progress
    
    def _get_unlocked_count(self, user_id: int) -> int:
        """Get count of unlocked templates for user"""
        try:
            self.db.cursor.execute('''
                SELECT COUNT(*) FROM template_unlocks
                WHERE user_id = ?
            ''', (user_id,))
            
            return self.db.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Error getting unlocked count: {e}")
            return 0
    
    async def preview_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                              template_id: str):
        """Show preview of a template"""
        try:
            template_data = self.unlockable_templates.get(template_id)
            if not template_data:
                await update.message.reply_text(
                    "❌ টেমপ্লেট খুঁজে পাওয়া যায়নি!",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Create preview message
            message = f"""
🎨 <b>টেমপ্লেট প্রিভিউ</b> 🎨

✨ <b>{template_data['name']}</b> ✨

📝 <b>বর্ণনা:</b>
{template_data['description']}

🏷️ <b>দুর্লভতা:</b> {template_data.get('rarity', 'common')}

🎯 <b>আনলক রিকোয়ারমেন্ট:</b>
{self._format_requirement(template_data['requirement'])}

            """
            
            # Check if unlocked
            user = update.effective_user
            unlocked = self._is_template_unlocked(user.id, template_id)
            
            if unlocked:
                message += "✅ <b>স্ট্যাটাস:</b> আনলকড\n"
                message += "এই টেমপ্লেট এখন ব্যবহার করতে পারো!"
            else:
                # Show progress
                user_stats = self._get_user_stats(user.id)
                progress = self._calculate_progress(user_stats, template_data['requirement'])
                message += f"🔒 <b>স্ট্যাটাস:</b> লকড ({progress}%)\n"
                message += "রিকোয়ারমেন্ট পূরণ করলে আনলক হবে!"
            
            # Send message
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error previewing template: {e}")
            await update.message.reply_text(
                "প্রিভিউ দেখাতে সমস্যা হয়েছে! 😢",
                parse_mode=ParseMode.HTML
            )
    
    def _format_requirement(self, requirement: Dict) -> str:
        """Format requirement for display"""
        req_type = requirement["type"]
        threshold = requirement["threshold"]
        
        if req_type == "roast_count":
            return f"• {threshold}টি রোস্ট করুন"
        elif req_type == "vote_count":
            return f"• {threshold}টি ভোট দিন"
        elif req_type == "reaction_count":
            return f"• {threshold}টি রিঅ্যাকশন পান"
        elif req_type == "days_active":
            return f"• {threshold} দিন সক্রিয় থাকুন"
        elif req_type == "streak":
            return f"• {threshold} দিন স্ট্রিক রাখুন"
        
        return "• নির্দিষ্ট রিকোয়ারমেন্ট"
    
    def add_custom_unlockable(self, template_id: str, template_data: Dict) -> bool:
        """Add custom unlockable template"""
        try:
            # Validate required fields
            required_fields = ["name", "description", "requirement"]
            for field in required_fields:
                if field not in template_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Add to unlockable templates
            self.unlockable_templates[template_id] = template_data
            
            # Save to file
            import json
            unlock_file = "data/unlockable_templates.json"
            
            with open(unlock_file, 'w', encoding='utf-8') as f:
                json.dump(self.unlockable_templates, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Added custom unlockable template: {template_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding custom unlockable: {e}")
            return False
    
    def get_unlock_stats(self) -> Dict[str, Any]:
        """Get unlock system statistics"""
        # Count unlocks per template
        template_counts = {}
        for template_id in self.unlockable_templates:
            try:
                self.db.cursor.execute('''
                    SELECT COUNT(*) FROM template_unlocks
                    WHERE template_id = ?
                ''', (template_id,))
                count = self.db.cursor.fetchone()[0]
                template_counts[template_id] = count
            except:
                template_counts[template_id] = 0
        
        return {
            "total_unlockable_templates": len(self.unlockable_templates),
            "unlock_counts": template_counts,
            "rarity_distribution": {
                "common": sum(1 for t in self.unlockable_templates.values() 
                            if t.get("rarity") == "common"),
                "rare": sum(1 for t in self.unlockable_templates.values() 
                           if t.get("rarity") == "rare"),
                "epic": sum(1 for t in self.unlockable_templates.values() 
                           if t.get("rarity") == "epic"),
                "legendary": sum(1 for t in self.unlockable_templates.values() 
                               if t.get("rarity") == "legendary")
            }
        }