#!/usr/bin/env python3
"""
Neural Motion Lab - Setup Script
Automated setup and installation for the Neural Motion Lab project
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


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
    """Print a formatted header message"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}")
    print(f"{message}")
    print(f"{'=' * 60}{Colors.END}\n")


def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    """Print an info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")


def check_python_version():
    """Check if Python version is compatible"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8 or higher required. Current version: {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_comfyui_installation():
    """Check if ComfyUI is installed"""
    print_info("Checking for ComfyUI installation...")
    
    # Common ComfyUI installation paths
    possible_paths = [
        Path.home() / "ComfyUI",
        Path.cwd().parent / "ComfyUI",
        Path("/opt/ComfyUI"),
        Path("C:/ComfyUI") if platform.system() == "Windows" else None
    ]
    
    for path in possible_paths:
        if path and path.exists() and (path / "main.py").exists():
            print_success(f"ComfyUI found at: {path}")
            return path
    
    print_warning("ComfyUI installation not found automatically")
    print_info("Please ensure ComfyUI is installed before proceeding")
    print_info("Visit: https://github.com/comfyanonymous/ComfyUI")
    
    custom_path = input("\nEnter ComfyUI installation path (or press Enter to skip): ").strip()
    if custom_path and Path(custom_path).exists():
        return Path(custom_path)
    
    return None


def create_directories():
    """Create necessary project directories"""
    print_info("Creating project directories...")
    
    base_dir = Path(__file__).parent.parent
    directories = [
        base_dir / "outputs",
        base_dir / "models" / "checkpoints",
        base_dir / "models" / "loras",
        base_dir / "models" / "vae",
        base_dir / "models" / "clip",
        base_dir / "models" / "controlnet",
        base_dir / "models" / "ipadapter",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {directory.relative_to(base_dir)}")


def install_dependencies():
    """Install required Python dependencies"""
    print_info("Installing Python dependencies...")
    
    base_dir = Path(__file__).parent.parent
    requirements_file = base_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print_warning("requirements.txt not found, skipping dependency installation")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def check_gpu():
    """Check for GPU availability"""
    print_info("Checking GPU availability...")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print_success(f"GPU detected: {gpu_name}")
            print_success(f"GPU Memory: {gpu_memory:.1f} GB")
            
            if gpu_memory < 8:
                print_warning("GPU has less than 8GB VRAM - may need to use lower resolution settings")
            
            return True
        else:
            print_warning("No CUDA-capable GPU detected")
            print_info("CPU mode will be very slow - GPU strongly recommended")
            return False
    except ImportError:
        print_warning("PyTorch not installed, unable to check GPU")
        return None


def verify_workflows():
    """Verify workflow files exist"""
    print_info("Verifying workflow files...")
    
    base_dir = Path(__file__).parent.parent
    workflow_dir = base_dir / "workflows"
    
    required_workflows = [
        "basic_i2v.json",
        "lora_i2v.json",
        "character_consistent.json",
        "advanced_variations.json"
    ]
    
    all_exist = True
    for workflow in required_workflows:
        workflow_path = workflow_dir / workflow
        if workflow_path.exists():
            print_success(f"Found: {workflow}")
        else:
            print_error(f"Missing: {workflow}")
            all_exist = False
    
    return all_exist


def create_gitignore():
    """Create or update .gitignore file"""
    print_info("Creating .gitignore...")
    
    base_dir = Path(__file__).parent.parent
    gitignore_path = base_dir / ".gitignore"
    
    gitignore_content = """# Models (large files)
models/
*.safetensors
*.ckpt
*.pth
*.pt

# Outputs
outputs/
output/
*.mp4
*.avi
*.mov
*.gif

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
tmp/
temp/
*.tmp
*.log

# ComfyUI specific
input/
output/
temp/
"""
    
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)
    
    print_success(".gitignore created")


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.END}\n")
    print(f"1. Download required models:")
    print(f"   {Colors.CYAN}python scripts/download_models.py{Colors.END}\n")
    
    print(f"2. Place your input images in:")
    print(f"   {Colors.CYAN}ComfyUI/input/{Colors.END}\n")
    
    print(f"3. Load a workflow in ComfyUI:")
    print(f"   - Start ComfyUI")
    print(f"   - Load workflows/basic_i2v.json\n")
    
    print(f"4. Configure settings in:")
    print(f"   {Colors.CYAN}configs/default_config.yaml{Colors.END}\n")
    
    print(f"5. Read the documentation:")
    print(f"   {Colors.CYAN}examples/basic_usage.md{Colors.END}\n")
    
    print(f"{Colors.BOLD}For more information, see README.md{Colors.END}\n")


def main():
    """Main setup function"""
    print_header("Neural Motion Lab - Setup Script")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check for ComfyUI
    comfyui_path = check_comfyui_installation()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Check GPU
    check_gpu()
    
    # Verify workflows
    verify_workflows()
    
    # Create .gitignore
    create_gitignore()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed with error: {e}")
        sys.exit(1)
