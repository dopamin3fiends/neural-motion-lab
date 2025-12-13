# Installation Guide

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended)
- Git
- 20GB+ free disk space for models

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab
```

### 2. Quick Setup (Recommended)

Run the quick setup script to create a virtual environment and install dependencies:

```bash
bash scripts/install/quick_setup.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies
- Set up the package in development mode
- Create necessary directories

### 3. Activate the Environment

```bash
source venv/bin/activate
```

## Manual Installation

If you prefer to install manually:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Package

```bash
pip install -e .
```

### 4. Create Directories

```bash
mkdir -p models/lora models/hunyuan outputs/videos outputs/images logs
```

## Model Setup

### Download Models

1. **HunyuanVideo-I2V Model**
   - Download from [HunyuanVideo repository](https://github.com/Tencent/HunyuanVideo)
   - Place model files in `models/hunyuan/`

2. **LoRA Models (Optional)**
   - Download character-specific LoRA models
   - Place in `models/lora/`

### Configure Model Paths

Edit `configs/pipeline.yaml` to point to your model locations:

```yaml
hunyuan_model_path: "models/hunyuan/model.safetensors"
lora_model_path: "models/lora/character.safetensors"
```

## ComfyUI Integration (Optional)

To use the ComfyUI interface:

```bash
bash scripts/setup/setup_comfyui.sh
```

This will:
- Clone and install ComfyUI
- Copy workflow templates
- Set up integration

Start ComfyUI:

```bash
cd comfyui
python main.py
```

Access at: http://127.0.0.1:8188

## Verification

Verify your installation:

```bash
python -c "import neural_motion_lab; print(neural_motion_lab.__version__)"
```

## Troubleshooting

### CUDA Not Available

If you get CUDA errors:
1. Verify CUDA installation: `nvidia-smi`
2. Check PyTorch CUDA support: `python -c "import torch; print(torch.cuda.is_available())"`
3. Reinstall PyTorch with CUDA support

### Import Errors

If you get import errors:
1. Ensure virtual environment is activated
2. Reinstall package: `pip install -e .`
3. Check Python version: `python --version`

### Memory Issues

If you run out of memory:
1. Use smaller batch sizes
2. Enable gradient checkpointing
3. Use CPU offloading in configuration

## Next Steps

- Read the [Usage Guide](../usage/basic.md)
- Check out [Examples](../../examples/)
- Review [API Documentation](../api/overview.md)
