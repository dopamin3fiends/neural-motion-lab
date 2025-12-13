# Quick Start Guide

Get up and running with Neural Motion Lab in 5 minutes!

## Prerequisites

- NVIDIA RTX GPU (12+ GB VRAM)
- Python 3.10+ installed
- Git installed

## Installation (5 steps)

### 1. Clone and Setup

```bash
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab
pip install -r requirements.txt
python scripts/setup_environment.py
```

### 2. Download Models

```bash
python scripts/download_models.py --model all
```

⏱️ This takes 15-30 minutes depending on your internet speed.

### 3. Prepare Input Image

Place your input image in `assets/examples/input_images/`:

```bash
# Or use your own image
copy my_character.png assets/examples/input_images/
```

### 4. Generate Video (Without LoRA)

```bash
python scripts/batch_generate.py \
    --input assets/examples/input_images/my_character.png \
    --output outputs/my_first_video \
    --prompt "character walking forward, smooth motion" \
    --num-frames 49 \
    --fps 24
```

### 5. Check Output

Your video is saved in `outputs/my_first_video/my_character.mp4`

## Using LoRA

If you have a trained LoRA:

```bash
python scripts/batch_generate.py \
    --input assets/examples/input_images/my_character.png \
    --lora lora/my_character.safetensors \
    --lora-scale 0.8 \
    --prompt "character in specific style, walking" \
    --output outputs/with_lora
```

## Training Your First LoRA

### 1. Prepare Dataset

Create a folder with 10-50 images of your character:

```
data/training/
├── image_001.png
├── image_002.png
├── ...
└── image_050.png
```

### 2. Start Training

```bash
python scripts/train_lora.py \
    --dataset data/training \
    --output lora/my_character_v1 \
    --epochs 10 \
    --batch-size 1
```

⏱️ Training takes 30-120 minutes depending on dataset size and hardware.

### 3. Validate LoRA

```bash
python scripts/validate_lora.py lora/my_character_v1.safetensors
```

## Using ComfyUI

### 1. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

### 2. Link Models

**Windows (PowerShell as Admin):**
```powershell
cd neural-motion-lab
New-Item -ItemType SymbolicLink -Path "ComfyUI\models\loras" -Target "lora"
```

### 3. Start ComfyUI

```bash
cd ComfyUI
python main.py
```

Open http://localhost:8188

### 4. Load Workflow

1. Click "Load" button
2. Navigate to `neural-motion-lab/workflows/`
3. Select `basic_i2v_lora.json`
4. Adjust parameters
5. Click "Queue Prompt"

## Configuration

Edit `config/generation_config.yaml` for default settings:

```yaml
generation:
  num_frames: 49        # Video length
  fps: 24               # Frame rate
  width: 512            # Resolution
  height: 512
  lora_scale: 0.8       # LoRA strength
  guidance_scale: 7.5   # CFG scale
```

## Common Operations

### Batch Generate Multiple Images

```bash
python scripts/batch_generate.py \
    --input assets/examples/input_images/ \
    --output outputs/batch \
    --lora lora/my_character.safetensors
```

### Use Multiple LoRAs

```bash
python scripts/batch_generate.py \
    --input my_image.png \
    --lora lora/character.safetensors \
    --lora lora/style.safetensors \
    --output outputs/multi_lora
```

### Change Video Settings

```bash
python scripts/batch_generate.py \
    --input my_image.png \
    --num-frames 73 \
    --fps 30 \
    --output outputs/long_video
```

## Tips for Best Results

### Image Preparation
- Use high-quality input images (512x512 or higher)
- Clear, well-lit subjects
- Minimal background clutter
- Consistent character appearance for training

### Prompts
- Be specific and descriptive
- Include motion keywords: "walking", "turning", "moving"
- Add quality terms: "smooth motion", "high quality"
- Use negative prompts to avoid artifacts

### LoRA Training
- 10-50 images minimum
- Consistent subject across images
- Vary poses and angles
- Train for 8-15 epochs

### Generation Settings
- **Frames:** 25 (short), 49 (medium), 73 (long)
- **CFG Scale:** 7-9 for balanced results
- **LoRA Scale:** 0.6-0.9 for most cases
- **Seed:** Fix for reproducibility

## Troubleshooting Quick Fixes

### Out of Memory
```yaml
# Edit config/generation_config.yaml
optimization:
  enable_xformers: true
  enable_vae_tiling: true
  vae_batch_size: 4
```

### Slow Generation
- Use `fp16` precision
- Enable xFormers
- Close other GPU applications

### Poor Quality
- Increase `num_inference_steps` to 50-75
- Adjust `guidance_scale` to 8-10
- Use better input images
- Try different prompts

## Next Steps

- **Learn More:** Read [WORKFLOWS.md](WORKFLOWS.md) for ComfyUI details
- **Train LoRA:** See [TRAINING_LORA.md](TRAINING_LORA.md) for complete guide
- **Optimize:** Check [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for performance tips
- **Issues:** Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Command Reference

```bash
# Setup
python scripts/setup_environment.py

# Download models
python scripts/download_models.py --model all

# Generate video
python scripts/batch_generate.py --input IMAGE --output DIR

# Train LoRA
python scripts/train_lora.py --dataset DIR --output DIR

# Validate LoRA
python scripts/validate_lora.py LORA_PATH

# Check config
python -c "from scripts.utils.config_loader import load_config; print(load_config('generation_config'))"
```

## Getting Help

- Documentation: `docs/` directory
- Issues: GitHub Issues
- Examples: `workflows/` directory
