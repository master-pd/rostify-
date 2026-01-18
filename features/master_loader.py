#!/usr/bin/env python3
"""
Master Loader - Auto-loads all features dynamically
Add new features by just creating files in features/ directory
"""

import os
import importlib
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MasterLoader:
    """Dynamically loads all feature modules"""
    
    def __init__(self, features_dir: str = "features"):
        """Initialize master loader"""
        self.features_dir = features_dir
        self.loaded_features = {}
        self.feature_instances = {}
        
        # Ensure features directory exists
        os.makedirs(features_dir, exist_ok=True)
        
        # Create __init__.py if not exists
        init_file = os.path.join(features_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Features package\n")
        
        logger.info("Master Loader initialized")
    
    def discover_features(self) -> List[str]:
        """Discover all feature modules in features directory"""
        feature_modules = []
        
        for filename in os.listdir(self.features_dir):
            # Look for Python files (excluding __init__.py and .pyc files)
            if filename.endswith('.py') and filename != '__init__.py' and not filename.endswith('.pyc'):
                module_name = filename[:-3]  # Remove .py extension
                feature_modules.append(module_name)
        
        logger.info(f"Discovered {len(feature_modules)} feature modules: {feature_modules}")
        return feature_modules
    
    def load_feature(self, module_name: str) -> Any:
        """Load a single feature module"""
        try:
            # Import the module
            module = importlib.import_module(f'.{module_name}', package='features')
            
            # Look for a class with the same name (convention)
            # e.g., WelcomeSystem in welcome_system.py
            class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            
            if hasattr(module, class_name):
                feature_class = getattr(module, class_name)
                
                # Create instance if the class has a no-args constructor
                try:
                    instance = feature_class()
                    self.feature_instances[module_name] = instance
                    logger.info(f"Loaded feature: {module_name} -> {class_name}")
                    return instance
                except Exception as e:
                    logger.warning(f"Could not instantiate {class_name}: {e}")
                    self.feature_instances[module_name] = module
                    return module
            else:
                # No class found, return the module itself
                self.feature_instances[module_name] = module
                logger.info(f"Loaded module: {module_name}")
                return module
                
        except ImportError as e:
            logger.error(f"Error importing {module_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error loading {module_name}: {e}")
            return None
    
    def load_all_features(self) -> Dict[str, Any]:
        """Load all discovered features"""
        feature_modules = self.discover_features()
        
        for module_name in feature_modules:
            feature = self.load_feature(module_name)
            if feature:
                self.loaded_features[module_name] = feature
        
        logger.info(f"Successfully loaded {len(self.loaded_features)} features")
        return self.loaded_features
    
    def get_feature(self, feature_name: str) -> Any:
        """Get a loaded feature by name"""
        return self.loaded_features.get(feature_name)
    
    def get_all_features(self) -> Dict[str, Any]:
        """Get all loaded features"""
        return self.loaded_features.copy()
    
    def reload_feature(self, module_name: str) -> bool:
        """Reload a feature module (for hot reloading)"""
        try:
            if module_name in self.loaded_features:
                # Remove from loaded features
                del self.loaded_features[module_name]
                
                if module_name in self.feature_instances:
                    del self.feature_instances[module_name]
                
                # Reload the module
                module_spec = importlib.util.find_spec(f'.{module_name}', package='features')
                if module_spec and module_spec.loader:
                    importlib.invalidate_caches()
                    module = importlib.import_module(f'.{module_name}', package='features')
                    module = importlib.reload(module)
                    
                    # Try to create instance again
                    class_name = ''.join(word.capitalize() for word in module_name.split('_'))
                    if hasattr(module, class_name):
                        feature_class = getattr(module, class_name)
                        try:
                            instance = feature_class()
                            self.feature_instances[module_name] = instance
                            self.loaded_features[module_name] = instance
                        except:
                            self.loaded_features[module_name] = module
                    else:
                        self.loaded_features[module_name] = module
                    
                    logger.info(f"Reloaded feature: {module_name}")
                    return True
        except Exception as e:
            logger.error(f"Error reloading feature {module_name}: {e}")
        
        return False
    
    def auto_discover_new_features(self) -> List[str]:
        """Check for new feature files and load them"""
        current_features = set(self.loaded_features.keys())
        available_features = set(self.discover_features())
        
        new_features = available_features - current_features
        
        if new_features:
            logger.info(f"Found {len(new_features)} new features: {list(new_features)}")
            
            for feature_name in new_features:
                self.load_feature(feature_name)
        
        return list(new_features)


def load_all_features(features_dir: str = "features") -> Dict[str, Any]:
    """Convenience function to load all features"""
    loader = MasterLoader(features_dir)
    return loader.load_all_features()


# Test the loader
if __name__ == "__main__":
    loader = MasterLoader()
    features = loader.load_all_features()
    
    print(f"Loaded {len(features)} features:")
    for name, feature in features.items():
        print(f"  - {name}: {type(feature)}")