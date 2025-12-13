"""Environment setup script for Neural Motion Lab."""

import sys
import platform
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_python_version() -> bool:
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        logger.error("Python 3.10 or higher is required")
        return False
    
    logger.info("✓ Python version OK")
    return True


def check_cuda() -> bool:
    """Check CUDA availability and version."""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        
        if cuda_available:
            cuda_version = torch.version.cuda
            device_count = torch.cuda.device_count()
            logger.info(f"✓ CUDA {cuda_version} detected")
            logger.info(f"✓ {device_count} CUDA device(s) available")
            
            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                props = torch.cuda.get_device_properties(i)
                memory_gb = props.total_memory / 1024**3
                logger.info(f"  Device {i}: {device_name} ({memory_gb:.2f} GB)")
            
            return True
        else:
            logger.warning("✗ CUDA not available - running on CPU")
            return False
            
    except ImportError:
        logger.warning("✗ PyTorch not installed - cannot check CUDA")
        return False


def check_gpu_memory() -> bool:
    """Check if GPU has sufficient memory."""
    try:
        import torch
        
        if not torch.cuda.is_available():
            return False
        
        props = torch.cuda.get_device_properties(0)
        memory_gb = props.total_memory / 1024**3
        
        if memory_gb < 12:
            logger.warning(f"GPU has {memory_gb:.2f} GB VRAM - 12 GB+ recommended")
            return False
        else:
            logger.info(f"✓ GPU memory sufficient: {memory_gb:.2f} GB")
            return True
            
    except Exception as e:
        logger.error(f"Error checking GPU memory: {e}")
        return False


def create_directories() -> None:
    """Create necessary project directories."""
    base_dir = Path(__file__).parent.parent
    
    directories = [
        "models",
        "lora",
        "outputs",
        "outputs/videos",
        "outputs/training",
        "outputs/validation",
        "logs",
        "data/training",
        "data/validation",
        "assets/examples/input_images",
        "assets/examples/output_videos",
        ".cache",
    ]
    
    logger.info("Creating project directories...")
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"  ✓ {dir_path}")
    
    logger.info("✓ All directories created")


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    required_packages = [
        "torch",
        "torchvision",
        "transformers",
        "diffusers",
        "accelerate",
        "peft",
        "safetensors",
        "yaml",
        "PIL",
        "cv2",
        "tqdm",
    ]
    
    logger.info("Checking dependencies...")
    all_installed = True
    
    for package in required_packages:
        try:
            if package == "yaml":
                __import__("yaml")
            elif package == "PIL":
                __import__("PIL")
            elif package == "cv2":
                __import__("cv2")
            else:
                __import__(package)
            logger.info(f"  ✓ {package}")
        except ImportError:
            logger.error(f"  ✗ {package} not installed")
            all_installed = False
    
    return all_installed


def install_requirements() -> bool:
    """Install requirements from requirements.txt."""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        logger.error("requirements.txt not found")
        return False
    
    logger.info("Installing requirements...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        logger.info("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False


def print_system_info() -> None:
    """Print system information."""
    logger.info("=== System Information ===")
    logger.info(f"OS: {platform.system()} {platform.release()}")
    logger.info(f"Architecture: {platform.machine()}")
    logger.info(f"Processor: {platform.processor()}")
    logger.info(f"Python: {sys.version}")


def print_next_steps() -> None:
    """Print next steps for the user."""
    logger.info("\n=== Setup Complete ===")
    logger.info("\nNext steps:")
    logger.info("1. Download models: python scripts/download_models.py")
    logger.info("2. Prepare training data in data/training/")
    logger.info("3. Review configuration files in config/")
    logger.info("4. See docs/QUICKSTART.md for usage guide")


def main():
    """Main setup function."""
    logger.info("=== Neural Motion Lab Environment Setup ===\n")
    
    # Print system info
    print_system_info()
    logger.info("")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        logger.info("\nSome dependencies are missing.")
        response = input("Install missing dependencies? (y/n): ")
        
        if response.lower() == 'y':
            if not install_requirements():
                logger.error("Failed to install dependencies")
                sys.exit(1)
        else:
            logger.warning("Skipping dependency installation")
            logger.info("Install manually with: pip install -r requirements.txt")
    
    # Check CUDA
    logger.info("")
    check_cuda()
    check_gpu_memory()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
