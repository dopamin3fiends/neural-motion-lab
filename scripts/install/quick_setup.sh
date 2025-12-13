#!/bin/bash
# Quick setup script for Neural Motion Lab

set -e

echo "========================================="
echo "Neural Motion Lab - Quick Setup"
echo "========================================="
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run installation script
echo ""
bash scripts/install/install.sh

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
