"""Model download script for Neural Motion Lab."""

import sys
import argparse
from pathlib import Path
import logging
from typing import Optional
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.utils.config_loader import load_config
from scripts.utils.model_manager import ModelManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_hunyuan_video(
    manager: ModelManager,
    config: dict,
    force: bool = False
) -> None:
    """Download HunyuanVideo model."""
    model_config = config.get('base_model', {}).get('hunyuan_video', {})
    model_id = model_config.get('huggingface_id')
    local_path = model_config.get('local_path')
    
    if not model_id:
        logger.error("HunyuanVideo model ID not found in config")
        return
    
    logger.info(f"Downloading HunyuanVideo model: {model_id}")
    
    try:
        model_path = manager.download_model(
            model_id=model_id,
            local_dir=local_path,
            force_download=force
        )
        logger.info(f"✓ HunyuanVideo model downloaded to {model_path}")
    except Exception as e:
        logger.error(f"Failed to download HunyuanVideo model: {e}")


def download_vae(
    manager: ModelManager,
    config: dict,
    force: bool = False
) -> None:
    """Download VAE model."""
    model_config = config.get('base_model', {}).get('vae', {})
    model_id = model_config.get('huggingface_id')
    local_path = model_config.get('local_path')
    
    if not model_id:
        logger.error("VAE model ID not found in config")
        return
    
    logger.info(f"Downloading VAE model: {model_id}")
    
    try:
        model_path = manager.download_model(
            model_id=model_id,
            local_dir=local_path,
            force_download=force
        )
        logger.info(f"✓ VAE model downloaded to {model_path}")
    except Exception as e:
        logger.error(f"Failed to download VAE model: {e}")


def download_text_encoder(
    manager: ModelManager,
    config: dict,
    force: bool = False
) -> None:
    """Download text encoder model."""
    model_config = config.get('base_model', {}).get('text_encoder', {})
    model_id = model_config.get('huggingface_id')
    local_path = model_config.get('local_path')
    
    if not model_id:
        logger.error("Text encoder model ID not found in config")
        return
    
    logger.info(f"Downloading text encoder: {model_id}")
    
    try:
        model_path = manager.download_model(
            model_id=model_id,
            local_dir=local_path,
            force_download=force
        )
        logger.info(f"✓ Text encoder downloaded to {model_path}")
    except Exception as e:
        logger.error(f"Failed to download text encoder: {e}")


def check_existing_models(config: dict) -> dict:
    """Check which models are already downloaded."""
    base_dir = Path(__file__).parent.parent
    status = {}
    
    # Check HunyuanVideo
    hunyuan_path = base_dir / config.get('base_model', {}).get('hunyuan_video', {}).get('local_path', 'models/hunyuan_video')
    status['hunyuan_video'] = hunyuan_path.exists() and any(hunyuan_path.iterdir())
    
    # Check VAE
    vae_path = base_dir / config.get('base_model', {}).get('vae', {}).get('local_path', 'models/vae')
    status['vae'] = vae_path.exists() and any(vae_path.iterdir())
    
    # Check text encoder
    encoder_path = base_dir / config.get('base_model', {}).get('text_encoder', {}).get('local_path', 'models/text_encoder')
    status['text_encoder'] = encoder_path.exists() and any(encoder_path.iterdir())
    
    return status


def main():
    """Main download function."""
    parser = argparse.ArgumentParser(description="Download models for Neural Motion Lab")
    parser.add_argument(
        '--model',
        choices=['all', 'hunyuan', 'vae', 'text_encoder'],
        default='all',
        help='Which model(s) to download'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if model exists'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to model_paths.yaml config file'
    )
    
    args = parser.parse_args()
    
    logger.info("=== Neural Motion Lab Model Downloader ===\n")
    
    # Load configuration
    try:
        if args.config:
            from scripts.utils.config_loader import ConfigLoader
            loader = ConfigLoader(Path(args.config).parent)
            config = loader.load(Path(args.config).name)
        else:
            config = load_config('model_paths')
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # Check existing models
    logger.info("Checking existing models...")
    existing = check_existing_models(config)
    
    for model_name, exists in existing.items():
        status = "✓ Downloaded" if exists else "✗ Not found"
        logger.info(f"  {model_name}: {status}")
    
    logger.info("")
    
    # Initialize model manager
    manager = ModelManager()
    
    # Download models based on selection
    try:
        if args.model in ['all', 'hunyuan']:
            if args.force or not existing.get('hunyuan_video'):
                download_hunyuan_video(manager, config, args.force)
            else:
                logger.info("HunyuanVideo already downloaded (use --force to re-download)")
        
        if args.model in ['all', 'vae']:
            if args.force or not existing.get('vae'):
                download_vae(manager, config, args.force)
            else:
                logger.info("VAE already downloaded (use --force to re-download)")
        
        if args.model in ['all', 'text_encoder']:
            if args.force or not existing.get('text_encoder'):
                download_text_encoder(manager, config, args.force)
            else:
                logger.info("Text encoder already downloaded (use --force to re-download)")
        
        logger.info("\n✓ Download complete!")
        logger.info("\nNext steps:")
        logger.info("1. Review model paths in config/model_paths.yaml")
        logger.info("2. See docs/QUICKSTART.md for usage guide")
        
    except KeyboardInterrupt:
        logger.warning("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
