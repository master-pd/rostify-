#!/bin/bash

# Roastify Bot Setup Script
# Run this script to setup the bot

set -e

echo "🔧 Roastify Bot Setup Script 🔧"
echo "==============================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p assets/{fonts,borders,templates,backgrounds}
mkdir -p data temp logs backups

# Download sample Bangla font
echo "Downloading sample Bangla font..."
if ! [ -f "assets/fonts/Kalpurush.ttf" ]; then
    echo "Please download a Bangla font (like Kalpurush.ttf) and place it in assets/fonts/"
    echo "You can download from: https://www.omicronlab.com/bangla-fonts.html"
fi

# Create sample borders if none exist
echo "Creating sample borders..."
if [ -z "$(ls -A assets/borders/)" ]; then
    echo "No borders found. Default borders will be created on first run."
fi

# Create config from template if not exists
if ! [ -f "config.py" ]; then
    echo "Creating config.py from template..."
    cp config_template.py config.py
    echo "Please edit config.py and add your bot token!"
fi

# Make run script executable
chmod +x run.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.py and add your bot token"
echo "2. Add Bangla fonts to assets/fonts/"
echo "3. Add border images to assets/borders/"
echo "4. Run the bot: ./run.py or python bot.py"
echo ""
echo "For help, see README.md"