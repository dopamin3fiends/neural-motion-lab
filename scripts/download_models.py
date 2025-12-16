#!/usr/bin/env python3
"""
Neural Motion Lab - Model Download Script
Automates downloading of HunyuanVideo models and recommended LoRAs
"""

import os
import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}")
    print(f"{message}")
    print(f"{'=' * 60}{Colors.END}\n")


def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")


# Model definitions with download information
MODELS = {
    "hunyuan_video": {
        "name": "HunyuanVideo 720p",
        "filename": "hunyuan_video_720_cfgdistill.safetensors",
        "path": "models/checkpoints/",
        "url": "https://huggingface.co/tencent/HunyuanVideo/resolve/main/hunyuan_video_720_cfgdistill.safetensors",
        "size": "~14GB",
        "required": True,
        "description": "Main HunyuanVideo model for 720p generation"
    },
    "vae": {
        "name": "HunyuanVideo VAE",
        "filename": "hunyuan_video_vae_fp16.safetensors",
        "path": "models/vae/",
        "url": "https://huggingface.co/tencent/HunyuanVideo/resolve/main/hunyuan_video_vae_fp16.safetensors",
        "size": "~1GB",
        "required": True,
        "description": "VAE model for encoding/decoding"
    },
    "clip": {
        "name": "CLIP Text Encoder",
        "filename": "llava_llama3_fp16.safetensors",
        "path": "models/clip/",
        "url": "https://huggingface.co/llava/LLaVA-v1.6-Llama-3-8B/resolve/main/llava_llama3_fp16.safetensors",
        "size": "~8GB",
        "required": True,
        "description": "Text encoder for prompt conditioning"
    }
}


OPTIONAL_LORAS = {
    "character_consistency": {
        "name": "Character Consistency LoRA",
        "filename": "character_consistency_lora.safetensors",
        "path": "models/loras/",
        "url": "# URL would be provided by community/custom training",
        "size": "~150MB",
        "description": "Maintains character consistency across frames"
    },
    "style_anime": {
        "name": "Anime Style LoRA",
        "filename": "style_anime_lora.safetensors",
        "path": "models/loras/",
        "url": "# URL would be provided by community",
        "size": "~150MB",
        "description": "Anime/manga art style"
    },
    "motion_smooth": {
        "name": "Smooth Motion LoRA",
        "filename": "motion_smooth_lora.safetensors",
        "path": "models/loras/",
        "url": "# URL would be provided by community",
        "size": "~150MB",
        "description": "Enhances motion smoothness"
    }
}


def check_file_exists(filepath):
    """Check if a model file already exists"""
    return Path(filepath).exists()


def download_file_wget(url, output_path):
    """Download file using wget"""
    import subprocess
    try:
        subprocess.check_call(['wget', '-c', url, '-O', output_path])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_file_curl(url, output_path):
    """Download file using curl"""
    import subprocess
    try:
        subprocess.check_call(['curl', '-L', '-C', '-', url, '-o', output_path])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_file_huggingface(url, output_path):
    """Download file using huggingface_hub"""
    try:
        from huggingface_hub import hf_hub_download
        
        # Parse HuggingFace URL
        # Format: https://huggingface.co/{repo_id}/resolve/main/{filename}
        parts = url.split('/')
        if 'huggingface.co' in url:
            repo_id = f"{parts[3]}/{parts[4]}"
            filename = parts[-1]
            
            print_info(f"Downloading from HuggingFace: {repo_id}/{filename}")
            
            downloaded_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                cache_dir=None,
                force_download=False
            )
            
            # Copy to destination
            import shutil
            shutil.copy(downloaded_path, output_path)
            return True
    except ImportError:
        print_warning("huggingface_hub not installed, trying alternative methods")
        return False
    except Exception as e:
        print_error(f"HuggingFace download failed: {e}")
        return False


def download_file(url, output_path):
    """Download file using available method"""
    print_info(f"Downloading to: {output_path}")
    
    # Create directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Try huggingface_hub first for HF URLs
    if 'huggingface.co' in url:
        if download_file_huggingface(url, output_path):
            return True
    
    # Try wget
    if download_file_wget(url, output_path):
        return True
    
    # Try curl
    if download_file_curl(url, output_path):
        return True
    
    return False


def download_models(base_dir, skip_existing=True, models_only=False):
    """Download required models"""
    print_header("Downloading Models")
    
    # Download main models
    for key, model in MODELS.items():
        print(f"\n{Colors.BOLD}Model: {model['name']}{Colors.END}")
        print(f"Size: {model['size']}")
        print(f"Description: {model['description']}")
        
        filepath = base_dir / model['path'] / model['filename']
        
        if check_file_exists(filepath) and skip_existing:
            print_success(f"Already exists: {filepath}")
            continue
        
        if model['url'].startswith('#'):
            print_warning(f"No download URL available - manual download required")
            print_info(f"Place file at: {filepath}")
            continue
        
        print_info(f"Downloading {model['filename']}...")
        if download_file(model['url'], filepath):
            print_success(f"Downloaded successfully")
        else:
            print_error(f"Download failed - please download manually from:")
            print(f"  {model['url']}")
            print(f"  Save to: {filepath}")
    
    # Download optional LoRAs if requested
    if not models_only:
        print_header("Optional LoRAs")
        print_info("LoRAs are optional and can be downloaded from the community")
        
        for key, lora in OPTIONAL_LORAS.items():
            print(f"\n{Colors.BOLD}LoRA: {lora['name']}{Colors.END}")
            print(f"Description: {lora['description']}")
            print(f"File: {lora['filename']}")
            
            filepath = base_dir / lora['path'] / lora['filename']
            
            if check_file_exists(filepath):
                print_success(f"Already exists: {filepath}")
            else:
                print_info(f"Not downloaded - place at: {filepath}")


def print_manual_instructions():
    """Print manual download instructions"""
    print_header("Manual Download Instructions")
    
    print(f"{Colors.BOLD}Required Models:{Colors.END}\n")
    
    for key, model in MODELS.items():
        if model['required']:
            print(f"{Colors.CYAN}{model['name']}{Colors.END}")
            print(f"  URL: {model['url']}")
            print(f"  Save to: {model['path']}{model['filename']}")
            print(f"  Size: {model['size']}\n")
    
    print(f"\n{Colors.BOLD}Optional LoRAs:{Colors.END}\n")
    print("LoRAs can be downloaded from:")
    print("  - CivitAI: https://civitai.com/")
    print("  - HuggingFace: https://huggingface.co/")
    print("  - Custom trained models\n")


def create_download_script():
    """Create a download script for manual use"""
    base_dir = Path(__file__).parent.parent
    script_path = base_dir / "download_models.sh"
    
    script_content = """#!/bin/bash
# Neural Motion Lab - Model Download Script (Generated)

# Create directories
mkdir -p models/checkpoints
mkdir -p models/vae
mkdir -p models/clip
mkdir -p models/loras

# Download models using wget or curl
"""
    
    for key, model in MODELS.items():
        if not model['url'].startswith('#'):
            script_content += f"\n# {model['name']}\n"
            script_content += f"wget -c {model['url']} -O {model['path']}{model['filename']}\n"
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print_success(f"Created download script: {script_path}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Download models for Neural Motion Lab"
    )
    parser.add_argument(
        '--no-skip',
        action='store_true',
        help="Download even if files exist"
    )
    parser.add_argument(
        '--models-only',
        action='store_true',
        help="Only download required models, skip optional LoRAs"
    )
    parser.add_argument(
        '--manual',
        action='store_true',
        help="Print manual download instructions only"
    )
    parser.add_argument(
        '--create-script',
        action='store_true',
        help="Create a download script for manual use"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    
    print_header("Neural Motion Lab - Model Downloader")
    
    if args.manual:
        print_manual_instructions()
        return
    
    if args.create_script:
        create_download_script()
        return
    
    download_models(
        base_dir,
        skip_existing=not args.no_skip,
        models_only=args.models_only
    )
    
    print_header("Download Complete")
    print_info("Verify all required models are in place before using workflows")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Download interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Download failed with error: {e}")
        sys.exit(1)
