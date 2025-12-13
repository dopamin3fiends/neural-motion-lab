#!/usr/bin/env python3
"""
Data preprocessing script for Neural Motion Lab.
"""

import argparse
import os
from pathlib import Path
from PIL import Image
import numpy as np


def preprocess_image(image_path: str, output_path: str, size: tuple = (512, 512)) -> None:
    """
    Preprocess an image for video generation.
    
    Args:
        image_path: Path to input image
        output_path: Path to save preprocessed image
        size: Target size (width, height)
    """
    img = Image.open(image_path)
    
    # Resize while maintaining aspect ratio
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Create new image with padding
    new_img = Image.new('RGB', size, (0, 0, 0))
    paste_pos = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
    new_img.paste(img, paste_pos)
    
    # Save
    new_img.save(output_path)
    print(f"Preprocessed: {image_path} -> {output_path}")


def batch_preprocess(input_dir: str, output_dir: str, size: tuple = (512, 512)) -> None:
    """
    Batch preprocess images in a directory.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save preprocessed images
        size: Target size (width, height)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process all images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            output_file = output_path / img_file.name
            preprocess_image(str(img_file), str(output_file), size)


def main():
    parser = argparse.ArgumentParser(description='Preprocess images for video generation')
    parser.add_argument('input', help='Input image or directory')
    parser.add_argument('output', help='Output image or directory')
    parser.add_argument('--width', type=int, default=512, help='Target width')
    parser.add_argument('--height', type=int, default=512, help='Target height')
    
    args = parser.parse_args()
    size = (args.width, args.height)
    
    if os.path.isdir(args.input):
        batch_preprocess(args.input, args.output, size)
    else:
        preprocess_image(args.input, args.output, size)


if __name__ == '__main__':
    main()
