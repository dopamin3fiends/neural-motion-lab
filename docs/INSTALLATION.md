# Installation Guide

Complete installation instructions for Neural Motion Lab on Windows with RTX GPU.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Python Installation](#python-installation)
- [CUDA and PyTorch Setup](#cuda-and-pytorch-setup)
- [Neural Motion Lab Installation](#neural-motion-lab-installation)
- [ComfyUI Setup](#comfyui-setup)
- [Model Downloads](#model-downloads)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements

**Minimum:**
- NVIDIA RTX GPU with 12 GB VRAM
- 16 GB System RAM
- 50 GB Free Storage
- Windows 10/11 64-bit

**Recommended:**
- NVIDIA RTX 3090/4090 or better (24 GB VRAM)
- 32 GB System RAM
- 100 GB Free Storage (SSD recommended)
- Windows 11 64-bit

### Software Requirements

- Python 3.10 or 3.11
- CUDA 11.8 or 12.1
- Git for Windows
- Visual Studio 2019/2022 Build Tools (optional, for some packages)

## Python Installation

### Option 1: Official Python (Recommended)

1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Run installer with these options:
   - ☑ Add Python to PATH
   - ☑ Install for all users
3. Verify installation:

```bash
python --version
# Should show: Python 3.11.x
```

### Option 2: Anaconda/Miniconda

1. Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Install and create environment:

```bash
conda create -n neural-motion python=3.11
conda activate neural-motion
```

## CUDA and PyTorch Setup

### Check CUDA Version

```bash
nvidia-smi
```

Note the CUDA version shown (e.g., "CUDA Version: 12.1").

### Install PyTorch

Visit [PyTorch Get Started](https://pytorch.org/get-started/locally/) for exact command.

**For CUDA 11.8:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Verify PyTorch Installation

```python
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}')"
```

Expected output:
```
PyTorch: 2.1.0+cu118
CUDA Available: True
CUDA Version: 11.8
```

## Neural Motion Lab Installation

### 1. Clone Repository

```bash
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### 3. Run Setup Script

```bash
python scripts/setup_environment.py
```

This will:
- Check Python and CUDA versions
- Create necessary directories
- Verify dependencies
- Display system information

## ComfyUI Setup

### 1. Clone ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### 2. Install ComfyUI Dependencies

```bash
pip install -r requirements.txt
```

### 3. Link Models

Create symbolic links to share models between Neural Motion Lab and ComfyUI:

**PowerShell (Run as Administrator):**
```powershell
# From neural-motion-lab directory
New-Item -ItemType SymbolicLink -Path "ComfyUI\models\checkpoints" -Target "models\hunyuan_video"
New-Item -ItemType SymbolicLink -Path "ComfyUI\models\loras" -Target "lora"
New-Item -ItemType SymbolicLink -Path "ComfyUI\models\vae" -Target "models\vae"
```

**Alternative: Copy Config**

Edit `config/model_paths.yaml` to point to ComfyUI directories.

### 4. Test ComfyUI

```bash
cd ComfyUI
python main.py
```

Open browser to http://localhost:8188

## Model Downloads

### Automatic Download

```bash
python scripts/download_models.py --model all
```

This downloads:
- HunyuanVideo-I2V model (~20 GB)
- VAE model (~1 GB)
- Text encoder (~1 GB)

### Download Individual Models

```bash
# HunyuanVideo only
python scripts/download_models.py --model hunyuan

# VAE only
python scripts/download_models.py --model vae

# Text encoder only
python scripts/download_models.py --model text_encoder
```

### Manual Download

If automatic download fails:

1. Visit [HuggingFace](https://huggingface.co/)
2. Download models manually:
   - [tencent/HunyuanVideo](https://huggingface.co/tencent/HunyuanVideo)
   - [stabilityai/sd-vae-ft-mse](https://huggingface.co/stabilityai/sd-vae-ft-mse)
   - [openai/clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)
3. Extract to appropriate directories in `models/`

## Verification

### Check Installation

```bash
python -c "import scripts; print('Neural Motion Lab installed successfully')"
```

### Test Scripts

```bash
# Test configuration loading
python -c "from scripts.utils.config_loader import load_config; print(load_config('generation_config'))"

# Test model manager
python -c "from scripts.utils.model_manager import ModelManager; m = ModelManager(); print(f'Device: {m.device}')"
```

### Run Tests

```bash
pip install pytest
pytest tests/
```

## Troubleshooting

### PyTorch Not Finding CUDA

**Problem:** `torch.cuda.is_available()` returns `False`

**Solutions:**
1. Verify NVIDIA drivers are installed: `nvidia-smi`
2. Check PyTorch CUDA version matches your CUDA
3. Reinstall PyTorch with correct CUDA version

### Out of Memory Errors

**Solutions:**
1. Close other GPU applications
2. Reduce batch size in config
3. Enable model offloading
4. Lower resolution settings

### Import Errors

**Problem:** `ModuleNotFoundError` when importing packages

**Solutions:**
1. Verify virtual environment is activated
2. Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
3. Check Python version: `python --version`

### Download Fails

**Solutions:**
1. Check internet connection
2. Try manual download from HuggingFace
3. Use HuggingFace CLI: `huggingface-cli download MODEL_ID`
4. Check disk space

### Permission Errors (Windows)

**Solutions:**
1. Run PowerShell/CMD as Administrator
2. Disable antivirus temporarily
3. Check folder permissions

## Next Steps

After successful installation:

1. **Quick Start:** See [QUICKSTART.md](QUICKSTART.md)
2. **Workflows:** Review [WORKFLOWS.md](WORKFLOWS.md)
3. **Training:** Read [TRAINING_LORA.md](TRAINING_LORA.md)
4. **Optimization:** Check [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)

## Getting Help

- **Issues:** Open an issue on GitHub
- **Documentation:** See `docs/` directory
- **Troubleshooting:** Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
