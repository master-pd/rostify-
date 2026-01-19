"""
Master loader for all bot features
"""

import importlib
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def load_all_features() -> Dict[str, Any]:
    """Load all bot features"""
    features = {}
    
    feature_modules = [
        'welcome_system',
        'roast_engine', 
        'voting_system',
        'reaction_system',
        'mention_roast',
        'admin_protection',
        'leaderboard',
        'festival_mode',
        'auto_daily_quote',
        'custom_template_unlocks',
        'auto_mood_recognition',
        'safe_forward_share'
    ]
    
    for module_name in feature_modules:
        try:
            module = importlib.import_module(f'features.{module_name}')
            features[module_name] = module
            logger.info(f"Loaded feature: {module_name}")
        except ImportError as e:
            logger.warning(f"Could not load feature {module_name}: {e}")
            features[module_name] = None
    
    return features
