#!/bin/bash
# ComfyUI setup script for Neural Motion Lab

set -e

echo "========================================="
echo "Neural Motion Lab - ComfyUI Setup"
echo "========================================="
echo ""

COMFYUI_DIR="comfyui"

# Check if ComfyUI is already installed
if [ -d "$COMFYUI_DIR" ]; then
    echo "ComfyUI directory already exists at: $COMFYUI_DIR"
    read -p "Remove and reinstall? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$COMFYUI_DIR"
    else
        echo "Setup cancelled."
        exit 0
    fi
fi

# Clone ComfyUI
echo "Cloning ComfyUI repository..."
git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFYUI_DIR"

# Install ComfyUI dependencies
echo ""
echo "Installing ComfyUI dependencies..."
cd "$COMFYUI_DIR"
pip install -r requirements.txt
cd ..

# Copy workflow templates
echo ""
echo "Copying workflow templates..."
cp -r configs/comfyui/*.json "$COMFYUI_DIR/workflows/" 2>/dev/null || true

echo ""
echo "========================================="
echo "ComfyUI Setup Complete!"
echo "========================================="
echo ""
echo "To start ComfyUI, run:"
echo "  cd $COMFYUI_DIR"
echo "  python main.py"
echo ""
echo "Then access the UI at: http://127.0.0.1:8188"
echo ""
