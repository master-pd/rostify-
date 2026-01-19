#!/usr/bin/env python3
"""
Setup script for Roastify Premium v15.0
"""

import os
import sys
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the complete directory structure"""
    
    directories = [
        # Premium modules
        "premium",
        
        # Assets
        "assets/fonts",
        "assets/borders",
        "assets/templates",
        "assets/backgrounds",
        "assets/badges",
        "assets/icons",
        
        # Features
        "features",
        
        # Utilities
        "utils",
        
        # Storage
        "database",
        "temp/images",
        "temp/cards",
        "temp/diagrams",
        "temp/reports",
        "output/premium/images",
        "output/premium/cards",
        "output/premium/reports",
        "output/regular",
        "cache/premium",
        "cache/images",
        "cache/data",
        "backup/daily",
        "backup/weekly",
        "backup/monthly",
        "logs",
        "data/analytics",
        "data/user_stats",
        "data/system",
        "reports/pdf",
        "reports/html",
        "reports/excel",
        
        # Support
        "tests",
        "docs"
    ]
    
    print("🚀 Creating Roastify Premium v15.0 structure...")
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # Create empty __init__.py files
    init_files = ["premium", "features", "utils"]
    
    for init_file in init_files:
        (Path(init_file) / "__init__.py").touch()
        print(f"📄 Created: {init_file}/__init__.py")
    
    print("\n✅ Directory structure created successfully!")
    
    # Create basic files
    basic_files = {
        "README.md": "# Roastify Premium v15.0\n\nPremium roasting bot with advanced features.",
        ".env": "BOT_TOKEN=your_bot_token_here\nDEBUG=True",
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.db-journal

# Temp files
temp/
*.tmp
*.temp

# Logs
logs/*.log

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
""",
        "requirements.txt": """# Core Dependencies
python-telegram-bot==20.7
Pillow==10.1.0
numpy==1.24.3

# AI & Analytics
nltk==3.8.1
textblob==0.18.0
spacy==3.7.2

# Data Visualization
matplotlib==3.7.2
plotly==5.17.0

# Premium Features
qrcode==7.4.2
python-dateutil==2.8.2

# Development
colorlog==6.7.0
python-dotenv==1.0.0"""
    }
    
    for filename, content in basic_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Created: {filename}")
    
    print("\n🎉 Setup complete! Next steps:")
    print("1. Edit config.py with your bot token")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run: python bot.py")

if __name__ == "__main__":
    create_directory_structure()
