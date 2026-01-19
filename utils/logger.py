"""
Advanced logging system for Roastify Premium
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
import colorlog

class PremiumLogger:
    """Premium logging system"""
    
    def __init__(self, name: str = "Roastify", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        
        # Create formatters
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Get logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler for general logs
        file_handler = RotatingFileHandler(
            self.log_dir / 'roastify.log',
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            self.log_dir / 'errors.log',
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setFormatter(file_formatter)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)
        
        # User actions handler
        user_handler = RotatingFileHandler(
            self.log_dir / 'user_actions.log',
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        user_handler.setFormatter(file_formatter)
        user_handler.setLevel(logging.INFO)
        logger.addHandler(user_handler)
        
        # Prevent propagation to root logger
        logger.propagate = False
    
    def get_logger(self, module_name: Optional[str] = None) -> logging.Logger:
        """Get logger instance"""
        if module_name:
            return logging.getLogger(f"{self.name}.{module_name}")
        return logging.getLogger(self.name)
    
    def log_user_action(self, user_id: int, action: str, details: str = ""):
        """Log user actions separately"""
        user_logger = logging.getLogger(f"{self.name}.user_actions")
        user_logger.info(f"User {user_id} - {action} - {details}")
    
    def log_system_event(self, event: str, level: str = "INFO"):
        """Log system events"""
        system_logger = logging.getLogger(f"{self.name}.system")
        
        log_method = getattr(system_logger, level.lower(), system_logger.info)
        log_method(f"System Event: {event}")


# Global logger instance
logger = PremiumLogger().get_logger()
