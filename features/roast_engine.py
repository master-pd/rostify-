"""
Roast Engine for generating roasts
"""

import random
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class RoastEngine:
    """Engine for generating roasts"""
    
    def __init__(self):
        self.roast_templates = {
            "funny": [
                "তোমার আইডিয়াটা {name} এর মতই - একদম ফাঁকা! 😂",
                "{name} দেখছি তুমি গুগলকে হার মানিয়েছ! কীভাবে সব উত্তর ভুল হতে পারে! 🤣",
                "তোমার লজিক {name} এর চেয়েও দুর্বল! 🥴",
                "তুমি যদি {name} হও, তাহলে কমেডির প্রয়োজন নেই! 😄",
                "তোমার বুদ্ধি {name} দেখে লজ্জা পেয়ে গেল! 🤪"
            ],
            "savage": [
                "তোমার মত {name} কে দেখলে রাগ আসে! 🔥",
                "{name} তোমার থেকে ভাল রোস্ট দিতে গুগলও পারবে না! 💀",
                "তুমি যদি ইন্টারনেট হতো {name}, তাহলে ডায়াল আপ থাকত! 😈",
                "তোমার মত {name} এর জন্য রোস্ট লিখতে আমার সময় নষ্ট হচ্ছে! ⚡",
                "তোমার আইকিউ {name} দেখে পালাতে চায়! 🧠💨"
            ],
            "clever": [
                "তোমার যুক্তি {name} এর মতই অনন্য - কেউ বুঝতে পারে না! 🧐",
                "{name} দেখছি তুমি প্যারাডক্সের নতুন সংজ্ঞা দিয়েছ! 🤔",
                "তোমার চিন্তা প্রক্রিয়া {name} - এককথায় অসাধারণ! 🎯",
                "তুমি যদি {name} হও, তাহলে ফিলোসফি নতুন অর্থ পায়! 💭",
                "তোমার লজিক {name} দেখে সায়েন্টিস্টরা অবাক! 🔬"
            ],
            "friendly": [
                "ভাই {name}, তুমি একটু অন্যরকম! 😊",
                "{name} তোমার মতো বন্ধু চাইলে কমেডি শো যেতে হয় না! 🤗",
                "তুমি যদি {name} হও, তাহলে দিন ভালো যায়! 🌟",
                "{name} তোমার উপস্থিতি পার্টি জমিয়ে দেয়! 🎉",
                "তোমার মত {name} থাকলে মজা করতে অন্য কোথাও যেতে হয় না! 😁"
            ]
        }
        
        self.roast_types = list(self.roast_templates.keys())
        logger.info("RoastEngine initialized")
    
    async def generate_roast(self, text: str, user: Any, 
                           target_user: Optional[Any] = None) -> Dict[str, Any]:
        """Generate a roast based on input text"""
        try:
            # Analyze text to determine roast type
            roast_type = self._determine_roast_type(text)
            
            # Get appropriate template
            templates = self.roast_templates.get(roast_type, self.roast_templates["funny"])
            roast_template = random.choice(templates)
            
            # Fill template with user info
            roast_text = self._fill_template(roast_template, user, target_user)
            
            # Generate caption
            caption = self._generate_caption(roast_type, user, target_user)
            
            # Calculate roast score
            score = self._calculate_roast_score(text, roast_type)
            
            return {
                "primary_roast": roast_text,
                "roast_type": roast_type,
                "roast_score": score,
                "caption": caption,
                "user_id": user.id,
                "target_id": target_user.id if target_user else None,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "input_text": text[:100],
                    "length": len(text),
                    "style": roast_type
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating roast: {e}")
            return self._generate_fallback_roast(user, target_user)
    
    def _determine_roast_type(self, text: str) -> str:
        """Determine roast type based on text"""
        text_lower = text.lower()
        
        # Simple keyword matching
        funny_keywords = ["হাসি", "মজা", "কমেডি", "লোল", "হাহা"]
        savage_keywords = ["কটু", "তীক্ষ্ণ", "তীব্র", "আগুন", "ব্লাস্ট"]
        clever_keywords = ["বুদ্ধি", "জ্ঞান", "লজিক", "যুক্তি", "ফিলোসফি"]
        
        for keyword in savage_keywords:
            if keyword in text_lower:
                return "savage"
        
        for keyword in clever_keywords:
            if keyword in text_lower:
                return "clever"
        
        for keyword in funny_keywords:
            if keyword in text_lower:
                return "funny"
        
        # Default to random type
        return random.choice(self.roast_types)
    
    def _fill_template(self, template: str, user: Any, target_user: Optional[Any]) -> str:
        """Fill template with user information"""
        name = target_user.first_name if target_user else user.first_name
        
        replacements = {
            "{name}": name,
            "{username}": target_user.username if target_user else user.username,
            "{user}": user.first_name
        }
        
        result = template
        for key, value in replacements.items():
            if value:
                result = result.replace(key, value)
        
        return result
    
    def _generate_caption(self, roast_type: str, user: Any, target_user: Optional[Any]) -> str:
        """Generate image caption"""
        captions = {
            "funny": "😂 মজার রোস্ট টাইম!",
            "savage": "🔥 স্যাভেজ রোস্ট এলার্ট!",
            "clever": "🧠 ক্লেভার রিপ্লাই!",
            "friendly": "🤗 ফ্রেন্ডলি রোস্ট!"
        }
        
        base_caption = captions.get(roast_type, "🎯 রোস্ট টাইম!")
        
        if target_user:
            return f"{base_caption} {target_user.first_name} -কে!"
        
        return f"{base_caption} {user.first_name}!"
    
    def _calculate_roast_score(self, text: str, roast_type: str) -> int:
        """Calculate roast score (1-100)"""
        base_score = len(text) % 100
        
        # Adjust based on roast type
        type_multipliers = {
            "savage": 1.3,
            "clever": 1.2,
            "funny": 1.1,
            "friendly": 1.0
        }
        
        multiplier = type_multipliers.get(roast_type, 1.0)
        score = int(base_score * multiplier)
        
        return min(max(score, 1), 100)
    
    def _generate_fallback_roast(self, user: Any, target_user: Optional[Any]) -> Dict:
        """Generate fallback roast in case of error"""
        name = target_user.first_name if target_user else user.first_name
        
        fallback_roasts = [
            f"{name}, তোমাকে রোস্ট দিতে গিয়ে আমার ব্রেইন ফ্রিজ হয়ে গেল! 😅",
            f"ওহো {name}, আজ রোস্ট জেনারেটরে সমস্যা! 😬",
            f"{name}, আজকের রোস্ট তোমার জন্য বিশেষ! (তবে নয়) 😉"
        ]
        
        return {
            "primary_roast": random.choice(fallback_roasts),
            "roast_type": "funny",
            "roast_score": 50,
            "caption": "🎯 স্পেশাল রোস্ট!",
            "user_id": user.id,
            "target_id": target_user.id if target_user else None,
            "timestamp": datetime.now().isoformat()
        }
