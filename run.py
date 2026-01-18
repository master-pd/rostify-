#!/usr/bin/env python3
"""
Run Script for Roastify Bot
Alternative entry point with enhanced features
"""

import os
import sys
import logging
import signal
import atexit
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def cleanup():
    """Cleanup before exit"""
    logger.info("Cleaning up before exit...")
    
    # Clean temp directory
    try:
        import shutil
        temp_dir = "temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            logger.info("Cleaned temp directory")
    except Exception as e:
        logger.error(f"Error cleaning temp directory: {e}")


def check_dependencies():
    """Check if all dependencies are installed"""
    required_packages = [
        'python-telegram-bot',
        'Pillow',
        'numpy',
        'emoji',
        'pytz',
        'aiohttp',
        'aiosqlite'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Install with: pip install -r requirements.txt")
        return False
    
    return True


def setup_directories():
    """Create necessary directories"""
    directories = [
        'assets/fonts',
        'assets/borders',
        'assets/templates',
        'assets/backgrounds',
        'data',
        'temp',
        'logs',
        'backups'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def main():
    """Main entry point"""
    logger.info("Starting Roastify Bot...")
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register cleanup function
    atexit.register(cleanup)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check bot token
    from config import BOT_TOKEN
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Please set your bot token in config.py")
        sys.exit(1)
    
    try:
        # Import and run bot
        from bot import RoastifyBot
        
        bot = RoastifyBot()
        logger.info("Bot initialized successfully")
        
        # Run bot
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        cleanup()


if __name__ == "__main__":
    main()