#!/usr/bin/env python3
"""
Template Manager for Roastify Bot
Manages roast templates and their selection
"""

import json
import random
import logging
import os
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import TEMPLATES, PATHS
except ImportError:
    logger.error("Config module not found")
    sys.exit(1)


class TemplateManager:
    """Manages roast templates and their rotation"""
    
    def __init__(self):
        """Initialize template manager"""
        self.config = TEMPLATES
        self.templates_dir = PATHS["templates"]
        
        # Load templates
        self.templates = self._load_templates()
        
        # Track template usage
        self.usage_count = defaultdict(int)
        self.recent_templates = []
        
        # Template weights for intelligent selection
        self.template_weights = self._initialize_weights()
        
        logger.info(f"Template Manager initialized with {len(self.templates)} templates")
    
    def _load_templates(self) -> Dict[str, List[Dict]]:
        """Load templates from file or create defaults"""
        templates_file = os.path.join(self.templates_dir, "templates.json")
        
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading templates: {e}")
        
        # Create default templates
        return self._create_default_templates()
    
    def _create_default_templates(self) -> Dict[str, List[Dict]]:
        """Create default templates if none exist"""
        default_templates = {
            "cartoon_roast": [
                {
                    "id": "cartoon_1",
                    "name": "বুদবুদ রোস্ট",
                    "style": "funny",
                    "background_color": [255, 240, 200],
                    "text_color": [50, 50, 50],
                    "border_color": [255, 100, 100],
                    "font_style": "rounded",
                    "effects": ["speech_bubble", "rounded_corners"],
                    "weight": 1.0,
                    "unlocked": True
                },
                {
                    "id": "cartoon_2",
                    "name": "কমিক স্টাইল",
                    "style": "sarcastic",
                    "background_color": [200, 230, 255],
                    "text_color": [30, 30, 30],
                    "border_color": [0, 150, 255],
                    "font_style": "bold",
                    "effects": ["comic_lines", "pop_art"],
                    "weight": 1.0,
                    "unlocked": True
                }
            ],
            "neon_savage": [
                {
                    "id": "neon_1",
                    "name": "নিয়ন স্যাভেজ",
                    "style": "savage",
                    "background_color": [10, 10, 30],
                    "text_color": [0, 255, 255],
                    "border_color": [255, 0, 255],
                    "font_style": "futuristic",
                    "effects": ["neon_glow", "grid_lines"],
                    "weight": 1.0,
                    "unlocked": True
                },
                {
                    "id": "neon_2",
                    "name": "ডার্ক নিয়ন",
                    "style": "bold",
                    "background_color": [20, 0, 20],
                    "text_color": [255, 105, 180],
                    "border_color": [0, 255, 0],
                    "font_style": "sharp",
                    "effects": ["glitch", "scan_lines"],
                    "weight": 1.0,
                    "unlocked": True
                }
            ],
            "dark_sarcastic": [
                {
                    "id": "dark_1",
                    "name": "ডার্ক স্যারা",
                    "style": "sarcastic",
                    "background_color": [30, 30, 30],
                    "text_color": [200, 200, 200],
                    "border_color": [100, 100, 100],
                    "font_style": "elegant",
                    "effects": ["shadow", "vignette"],
                    "weight": 1.0,
                    "unlocked": True
                }
            ],
            "minimal_mock": [
                {
                    "id": "minimal_1",
                    "name": "মিনিমাল মক",
                    "style": "minimal",
                    "background_color": [255, 255, 255],
                    "text_color": [0, 0, 0],
                    "border_color": [150, 150, 150],
                    "font_style": "clean",
                    "effects": ["simple_border", "clean_lines"],
                    "weight": 1.0,
                    "unlocked": True
                }
            ],
            "poster_style": [
                {
                    "id": "poster_1",
                    "name": "পোস্টার স্টাইল",
                    "style": "bold",
                    "background_color": [230, 230, 250],
                    "text_color": [139, 0, 0],
                    "border_color": [0, 0, 139],
                    "font_style": "poster",
                    "effects": ["gradient", "text_shadow"],
                    "weight": 1.0,
                    "unlocked": True
                }
            ]
        }
        
        # Save default templates
        self._save_templates(default_templates)
        
        return default_templates
    
    def _save_templates(self, templates: Dict):
        """Save templates to file"""
        try:
            os.makedirs(self.templates_dir, exist_ok=True)
            templates_file = os.path.join(self.templates_dir, "templates.json")
            
            with open(templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(templates)} template categories")
        except Exception as e:
            logger.error(f"Error saving templates: {e}")
    
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize template weights"""
        weights = {}
        
        for category, templates in self.templates.items():
            for template in templates:
                template_id = template.get("id", "unknown")
                weights[template_id] = template.get("weight", 1.0)
        
        return weights
    
    def get_random_template(self, category: str = None) -> Optional[Dict]:
        """Get a random template with intelligent selection"""
        try:
            # Get available templates
            available_templates = []
            
            if category and category in self.templates:
                # Get templates from specific category
                templates = self.templates[category]
                
                # Filter unlocked templates
                unlocked = [t for t in templates if t.get("unlocked", True)]
                
                if unlocked:
                    available_templates.extend(unlocked)
                else:
                    available_templates.extend(templates)
            else:
                # Get templates from all categories
                for cat_templates in self.templates.values():
                    unlocked = [t for t in cat_templates if t.get("unlocked", True)]
                    if unlocked:
                        available_templates.extend(unlocked)
                    else:
                        available_templates.extend(cat_templates)
            
            if not available_templates:
                logger.warning("No templates available")
                return None
            
            # Apply repetition avoidance
            if self.config.get("rotation_rule") == "Randomized with repetition avoidance":
                available_templates = self._filter_recent_templates(available_templates)
            
            # Apply weighted random selection
            weighted_templates = []
            
            for template in available_templates:
                template_id = template.get("id", "unknown")
                weight = self.template_weights.get(template_id, 1.0)
                
                # Adjust weight based on recent usage
                usage_factor = 1.0 / (1 + self.usage_count.get(template_id, 0))
                adjusted_weight = weight * usage_factor
                
                weighted_templates.append((template, adjusted_weight))
            
            # Select template based on weights
            total_weight = sum(weight for _, weight in weighted_templates)
            
            if total_weight == 0:
                selected_template = random.choice(available_templates)
            else:
                # Weighted random selection
                rand = random.uniform(0, total_weight)
                current = 0
                
                for template, weight in weighted_templates:
                    current += weight
                    if rand <= current:
                        selected_template = template
                        break
                else:
                    selected_template = available_templates[0]
            
            # Update usage tracking
            template_id = selected_template.get("id", "unknown")
            self.usage_count[template_id] += 1
            
            self.recent_templates.append(template_id)
            if len(self.recent_templates) > 10:
                self.recent_templates.pop(0)
            
            logger.debug(f"Selected template: {template_id}")
            return selected_template
            
        except Exception as e:
            logger.error(f"Error getting random template: {e}")
            # Return a simple default template
            return {
                "id": "default",
                "name": "Default",
                "style": "normal",
                "background_color": [255, 255, 255],
                "text_color": [0, 0, 0],
                "border_color": [100, 100, 100],
                "font_style": "normal",
                "effects": [],
                "unlocked": True
            }
    
    def _filter_recent_templates(self, templates: List[Dict]) -> List[Dict]:
        """Filter out recently used templates"""
        if not self.recent_templates:
            return templates
        
        # Get IDs of recent templates
        recent_ids = set(self.recent_templates[-5:])  # Last 5 templates
        
        # Filter out templates used recently
        filtered = [t for t in templates if t.get("id") not in recent_ids]
        
        # If all templates are recent, return all
        return filtered if filtered else templates
    
    def get_template_by_id(self, template_id: str) -> Optional[Dict]:
        """Get template by ID"""
        for category_templates in self.templates.values():
            for template in category_templates:
                if template.get("id") == template_id:
                    return template
        
        return None
    
    def get_templates_by_category(self, category: str) -> List[Dict]:
        """Get all templates in a category"""
        return self.templates.get(category, [])
    
    def unlock_template(self, template_id: str) -> bool:
        """Unlock a template"""
        for category, templates in self.templates.items():
            for i, template in enumerate(templates):
                if template.get("id") == template_id:
                    self.templates[category][i]["unlocked"] = True
                    
                    # Save changes
                    self._save_templates(self.templates)
                    
                    logger.info(f"Unlocked template: {template_id}")
                    return True
        
        return False
    
    def lock_template(self, template_id: str) -> bool:
        """Lock a template"""
        for category, templates in self.templates.items():
            for i, template in enumerate(templates):
                if template.get("id") == template_id:
                    self.templates[category][i]["unlocked"] = False
                    
                    # Save changes
                    self._save_templates(self.templates)
                    
                    logger.info(f"Locked template: {template_id}")
                    return True
        
        return False
    
    def adjust_template_weight(self, template_id: str, new_weight: float) -> bool:
        """Adjust template selection weight"""
        if template_id in self.template_weights:
            self.template_weights[template_id] = max(0.1, min(5.0, new_weight))
            
            # Also update in templates structure
            for category, templates in self.templates.items():
                for i, template in enumerate(templates):
                    if template.get("id") == template_id:
                        self.templates[category][i]["weight"] = new_weight
            
            logger.info(f"Adjusted weight for {template_id} to {new_weight}")
            return True
        
        return False
    
    def add_template(self, category: str, template_data: Dict) -> bool:
        """Add a new template"""
        try:
            # Generate unique ID if not provided
            if "id" not in template_data:
                template_data["id"] = f"{category}_{len(self.templates.get(category, [])) + 1}"
            
            # Set default values
            template_data.setdefault("unlocked", True)
            template_data.setdefault("weight", 1.0)
            template_data.setdefault("created_at", datetime.now().isoformat())
            
            # Add to templates
            if category not in self.templates:
                self.templates[category] = []
            
            self.templates[category].append(template_data)
            
            # Update weights
            self.template_weights[template_data["id"]] = template_data["weight"]
            
            # Save changes
            self._save_templates(self.templates)
            
            logger.info(f"Added new template: {template_data['id']} to {category}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding template: {e}")
            return False
    
    def remove_template(self, template_id: str) -> bool:
        """Remove a template"""
        for category, templates in self.templates.items():
            for i, template in enumerate(templates):
                if template.get("id") == template_id:
                    # Remove from templates
                    del self.templates[category][i]
                    
                    # Remove from weights
                    if template_id in self.template_weights:
                        del self.template_weights[template_id]
                    
                    # Remove from usage count
                    if template_id in self.usage_count:
                        del self.usage_count[template_id]
                    
                    # Remove from recent templates
                    if template_id in self.recent_templates:
                        self.recent_templates.remove(template_id)
                    
                    # Save changes if category becomes empty
                    if not self.templates[category]:
                        del self.templates[category]
                    
                    # Save changes
                    self._save_templates(self.templates)
                    
                    logger.info(f"Removed template: {template_id}")
                    return True
        
        return False
    
    def get_template_stats(self) -> Dict[str, Any]:
        """Get template usage statistics"""
        total_templates = 0
        unlocked_templates = 0
        usage_stats = {}
        
        for category, templates in self.templates.items():
            total_templates += len(templates)
            
            for template in templates:
                template_id = template.get("id", "unknown")
                
                if template.get("unlocked", True):
                    unlocked_templates += 1
                
                usage_count = self.usage_count.get(template_id, 0)
                usage_stats[template_id] = {
                    "name": template.get("name", "Unknown"),
                    "category": category,
                    "usage_count": usage_count,
                    "unlocked": template.get("unlocked", True),
                    "weight": self.template_weights.get(template_id, 1.0)
                }
        
        # Sort by usage
        sorted_usage = sorted(
            usage_stats.items(),
            key=lambda x: x[1]["usage_count"],
            reverse=True
        )[:10]  # Top 10
        
        return {
            "total_templates": total_templates,
            "unlocked_templates": unlocked_templates,
            "categories": list(self.templates.keys()),
            "top_used_templates": dict(sorted_usage),
            "total_usage": sum(self.usage_count.values())
        }
    
    def reset_usage_stats(self):
        """Reset usage statistics"""
        self.usage_count.clear()
        self.recent_templates.clear()
        logger.info("Reset template usage statistics")
    
    def export_templates(self, filepath: str) -> bool:
        """Export templates to a file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported templates to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting templates: {e}")
            return False
    
    def import_templates(self, filepath: str) -> bool:
        """Import templates from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_templates = json.load(f)
            
            # Merge with existing templates
            for category, templates in imported_templates.items():
                if category not in self.templates:
                    self.templates[category] = []
                
                for template in templates:
                    # Check if template already exists
                    template_id = template.get("id")
                    existing_ids = {t.get("id") for t in self.templates[category]}
                    
                    if template_id not in existing_ids:
                        self.templates[category].append(template)
                        
                        # Add to weights
                        self.template_weights[template_id] = template.get("weight", 1.0)
            
            # Save merged templates
            self._save_templates(self.templates)
            
            logger.info(f"Imported templates from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing templates: {e}")
            return False
    
    def create_template_variation(self, base_template_id: str, 
                                 variation_data: Dict) -> Optional[str]:
        """Create a variation of an existing template"""
        base_template = self.get_template_by_id(base_template_id)
        
        if not base_template:
            return None
        
        # Create variation
        variation = base_template.copy()
        
        # Update with variation data
        variation.update(variation_data)
        
        # Generate new ID
        variation_id = f"{base_template_id}_var_{int(datetime.now().timestamp()) % 10000}"
        variation["id"] = variation_id
        
        # Determine category
        category = "variations"
        for cat, templates in self.templates.items():
            if any(t.get("id") == base_template_id for t in templates):
                category = cat
                break
        
        # Add variation
        if self.add_template(category, variation):
            return variation_id
        
        return None