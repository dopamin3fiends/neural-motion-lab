#!/bin/bash
# Installation script for Neural Motion Lab

set -e

echo "========================================="
echo "Neural Motion Lab - Installation Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if we're in a virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo ""
    echo "WARNING: No virtual environment detected!"
    echo "It's recommended to use a virtual environment."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install package in development mode
echo ""
echo "Installing neural-motion-lab package..."
pip install -e .

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p models/lora
mkdir -p models/hunyuan
mkdir -p outputs/videos
mkdir -p outputs/images
mkdir -p logs

echo ""
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Download model weights to models/ directory"
echo "2. Configure your settings in configs/"
echo "3. Run setup script: bash scripts/setup/setup_models.sh"
echo ""
