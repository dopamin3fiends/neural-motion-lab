"""LoRA validation script for Neural Motion Lab."""

import sys
import argparse
from pathlib import Path
import logging
import torch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.utils.config_loader import load_config, ConfigLoader
from scripts.utils.model_manager import ModelManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LoRAValidator:
    """LoRA validation and testing."""
    
    def __init__(self, lora_path: Path):
        """
        Initialize LoRA validator.
        
        Args:
            lora_path: Path to LoRA checkpoint
        """
        self.lora_path = lora_path
        self.model_manager = ModelManager()
        
        if not lora_path.exists():
            raise FileNotFoundError(f"LoRA checkpoint not found: {lora_path}")
        
        logger.info(f"Initialized LoRA validator for: {lora_path}")
    
    def check_file_format(self) -> bool:
        """Check if LoRA file format is valid."""
        logger.info("Checking file format...")
        
        valid_extensions = ['.pt', '.pth', '.safetensors']
        
        if self.lora_path.suffix not in valid_extensions:
            logger.error(f"Invalid file format: {self.lora_path.suffix}")
            logger.info(f"Supported formats: {', '.join(valid_extensions)}")
            return False
        
        logger.info(f"  ✓ Format: {self.lora_path.suffix}")
        return True
    
    def check_file_size(self) -> bool:
        """Check LoRA file size."""
        size_mb = self.lora_path.stat().st_size / (1024 * 1024)
        logger.info(f"  File size: {size_mb:.2f} MB")
        
        # Typical LoRA sizes range from a few MB to a few hundred MB
        if size_mb < 0.1:
            logger.warning("File size is very small - may be corrupted")
            return False
        
        if size_mb > 1000:
            logger.warning("File size is very large - may not be a LoRA")
        
        return True
    
    def load_checkpoint(self) -> dict:
        """
        Load and inspect LoRA checkpoint.
        
        Returns:
            Checkpoint dictionary
        """
        logger.info("Loading checkpoint...")
        
        try:
            if self.lora_path.suffix == '.safetensors':
                from safetensors.torch import load_file
                checkpoint = load_file(str(self.lora_path), device='cpu')
            else:
                checkpoint = torch.load(self.lora_path, map_location='cpu')
            
            logger.info(f"  ✓ Checkpoint loaded successfully")
            return checkpoint
            
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            raise
    
    def inspect_checkpoint(self, checkpoint: dict) -> None:
        """
        Inspect checkpoint contents.
        
        Args:
            checkpoint: Checkpoint dictionary
        """
        logger.info("\nCheckpoint inspection:")
        
        # Check if it's a state dict or wrapped checkpoint
        if isinstance(checkpoint, dict):
            # Count parameters
            num_params = len(checkpoint)
            logger.info(f"  Number of parameters: {num_params}")
            
            # Show first few keys
            keys = list(checkpoint.keys())[:10]
            logger.info(f"  Sample keys:")
            for key in keys:
                tensor = checkpoint[key]
                if isinstance(tensor, torch.Tensor):
                    logger.info(f"    {key}: shape {tuple(tensor.shape)}, dtype {tensor.dtype}")
                else:
                    logger.info(f"    {key}: {type(tensor)}")
            
            if num_params > 10:
                logger.info(f"    ... and {num_params - 10} more")
            
            # Check for LoRA-specific patterns
            lora_keys = [k for k in checkpoint.keys() if 'lora' in k.lower()]
            if lora_keys:
                logger.info(f"\n  LoRA parameters found: {len(lora_keys)}")
            else:
                logger.warning("  No 'lora' in parameter names - may not be a LoRA checkpoint")
            
        else:
            logger.warning(f"  Unexpected checkpoint type: {type(checkpoint)}")
    
    def validate_rank(self, checkpoint: dict) -> None:
        """
        Validate LoRA rank from checkpoint.
        
        Args:
            checkpoint: Checkpoint dictionary
        """
        logger.info("\nValidating LoRA rank...")
        
        # Look for lora_down parameters to infer rank
        lora_down_keys = [k for k in checkpoint.keys() if 'lora_down' in k.lower() or 'lora_a' in k.lower()]
        
        if lora_down_keys:
            first_key = lora_down_keys[0]
            tensor = checkpoint[first_key]
            
            if isinstance(tensor, torch.Tensor) and tensor.ndim >= 2:
                rank = tensor.shape[0]
                logger.info(f"  ✓ Detected LoRA rank: {rank}")
            else:
                logger.warning("  Could not determine LoRA rank")
        else:
            logger.warning("  No LoRA down parameters found")
    
    def test_loading(self) -> bool:
        """
        Test if LoRA can be loaded properly.
        
        Returns:
            True if loading successful
        """
        logger.info("\nTesting LoRA loading...")
        
        try:
            checkpoint = self.load_checkpoint()
            self.inspect_checkpoint(checkpoint)
            self.validate_rank(checkpoint)
            
            logger.info("\n✓ LoRA validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False


def validate_lora(lora_path: Path) -> bool:
    """
    Validate a LoRA checkpoint.
    
    Args:
        lora_path: Path to LoRA checkpoint
        
    Returns:
        True if valid, False otherwise
    """
    try:
        validator = LoRAValidator(lora_path)
        
        # Check file format
        if not validator.check_file_format():
            return False
        
        # Check file size
        if not validator.check_file_size():
            return False
        
        # Test loading
        return validator.test_loading()
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description="Validate LoRA checkpoints for Neural Motion Lab")
    parser.add_argument(
        'lora_path',
        type=str,
        help='Path to LoRA checkpoint file or directory'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Recursively validate all LoRA files in directory'
    )
    
    args = parser.parse_args()
    
    logger.info("=== Neural Motion Lab LoRA Validator ===\n")
    
    lora_path = Path(args.lora_path)
    
    if not lora_path.exists():
        logger.error(f"Path does not exist: {lora_path}")
        sys.exit(1)
    
    # Validate single file or directory
    if lora_path.is_file():
        success = validate_lora(lora_path)
        sys.exit(0 if success else 1)
    
    elif lora_path.is_dir():
        # Find all LoRA files
        lora_extensions = ['.pt', '.pth', '.safetensors']
        
        if args.recursive:
            lora_files = []
            for ext in lora_extensions:
                lora_files.extend(list(lora_path.rglob(f"*{ext}")))
        else:
            lora_files = []
            for ext in lora_extensions:
                lora_files.extend(list(lora_path.glob(f"*{ext}")))
        
        if not lora_files:
            logger.warning(f"No LoRA files found in {lora_path}")
            sys.exit(1)
        
        logger.info(f"Found {len(lora_files)} LoRA file(s)\n")
        
        # Validate each file
        results = {}
        for lora_file in lora_files:
            logger.info(f"\n{'='*60}")
            logger.info(f"Validating: {lora_file.name}")
            logger.info('='*60)
            
            success = validate_lora(lora_file)
            results[lora_file.name] = success
        
        # Print summary
        logger.info(f"\n{'='*60}")
        logger.info("Validation Summary")
        logger.info('='*60)
        
        success_count = sum(results.values())
        total_count = len(results)
        
        for filename, success in results.items():
            status = "✓ PASS" if success else "✗ FAIL"
            logger.info(f"  {status}: {filename}")
        
        logger.info(f"\nTotal: {success_count}/{total_count} passed")
        
        sys.exit(0 if success_count == total_count else 1)
    
    else:
        logger.error(f"Invalid path: {lora_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
