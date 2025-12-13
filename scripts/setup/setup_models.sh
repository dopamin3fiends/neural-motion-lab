#!/bin/bash
# Model setup script for Neural Motion Lab

set -e

echo "========================================="
echo "Neural Motion Lab - Model Setup"
echo "========================================="
echo ""

MODELS_DIR="models"
HUNYUAN_DIR="$MODELS_DIR/hunyuan"
LORA_DIR="$MODELS_DIR/lora"

# Create model directories
mkdir -p "$HUNYUAN_DIR"
mkdir -p "$LORA_DIR"

echo "Model directories created:"
echo "  - $HUNYUAN_DIR"
echo "  - $LORA_DIR"
echo ""

echo "========================================="
echo "Model Setup Information"
echo "========================================="
echo ""
echo "To complete the setup, you need to:"
echo ""
echo "1. Download HunyuanVideo-I2V model weights:"
echo "   Place model files in: $HUNYUAN_DIR/"
echo ""
echo "2. (Optional) Download LoRA model weights:"
echo "   Place LoRA files in: $LORA_DIR/"
echo ""
echo "3. Update configuration files in configs/ to point to your models"
echo ""
echo "Refer to docs/installation/models.md for detailed instructions."
echo ""
