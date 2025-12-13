# LoRA Training Guide

Complete guide to training LoRA models for character-consistent video generation.

## Overview

LoRA (Low-Rank Adaptation) allows fine-tuning large models with minimal parameters, enabling:
- Character consistency across videos
- Style adaptation
- Concept learning
- Fast training (compared to full fine-tuning)

## Table of Contents

- [Dataset Preparation](#dataset-preparation)
- [Training Configuration](#training-configuration)
- [Training Process](#training-process)
- [Validation and Testing](#validation-and-testing)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Dataset Preparation

### Image Requirements

**Quantity:**
- Minimum: 10-15 images
- Recommended: 20-50 images
- Maximum: 100+ images (diminishing returns)

**Quality:**
- Resolution: 512x512 or higher
- Format: PNG, JPG, WebP
- Clear, well-lit subjects
- Minimal compression artifacts

**Diversity:**
- Various angles and poses
- Different lighting conditions
- Consistent subject/character
- Avoid duplicates

### Dataset Structure

```
data/training/
├── image_001.png
├── image_002.png
├── image_003.png
├── ...
└── image_050.png
```

Optional: Add captions

```
data/training/
├── image_001.png
├── image_001.txt  # "character standing, front view"
├── image_002.png
├── image_002.txt  # "character walking, side view"
└── ...
```

### Image Preprocessing

Neural Motion Lab automatically handles:
- Resizing to training resolution
- Center cropping
- Normalization

For manual preprocessing:

```python
from PIL import Image

def preprocess_image(input_path, output_path, size=512):
    img = Image.open(input_path).convert('RGB')
    
    # Resize
    img = img.resize((size, size), Image.LANCZOS)
    
    # Save
    img.save(output_path, quality=95)

# Process all images
import os
from pathlib import Path

input_dir = Path("data/raw")
output_dir = Path("data/training")
output_dir.mkdir(exist_ok=True)

for img_file in input_dir.glob("*.png"):
    preprocess_image(img_file, output_dir / img_file.name)
```

## Training Configuration

Edit `config/training_config.yaml`:

### Basic Settings

```yaml
training:
  output_dir: "lora/my_character_v1"
  num_epochs: 10
  batch_size: 1
  learning_rate: 1e-4
```

### LoRA Settings

```yaml
lora:
  rank: 32              # Higher = more capacity (4, 8, 16, 32, 64, 128)
  alpha: 32             # Typically same as rank
  dropout: 0.0          # 0.0-0.1 for regularization
  target_modules:
    - "to_q"
    - "to_k"
    - "to_v"
    - "to_out.0"
```

### Data Settings

```yaml
data:
  dataset_dir: "data/training"
  resolution: 512
  center_crop: true
  random_flip: true      # Augmentation
```

### Optimization

```yaml
optimization:
  enable_xformers: true
  gradient_checkpointing: true
  use_8bit_adam: false    # Enable for lower VRAM
```

## Training Process

### Start Training

```bash
python scripts/train_lora.py \
    --dataset data/training \
    --output lora/my_character_v1 \
    --epochs 10 \
    --batch-size 1 \
    --learning-rate 1e-4
```

### Monitor Progress

Training outputs:
- Console logs with loss values
- TensorBoard logs in `logs/tensorboard/`
- Checkpoints saved every N steps

View TensorBoard:

```bash
tensorboard --logdir logs/tensorboard
```

Open http://localhost:6006

### Training Parameters by Hardware

**RTX 3060 (12 GB):**
```bash
--batch-size 1 \
--learning-rate 1e-4 \
--epochs 10
```

**RTX 3090/4090 (24 GB):**
```bash
--batch-size 2 \
--learning-rate 1e-4 \
--epochs 15
```

**Lower VRAM (<12 GB):**
```yaml
# Edit config/training_config.yaml
optimization:
  use_8bit_adam: true
  gradient_checkpointing: true
  
training:
  batch_size: 1
  gradient_accumulation_steps: 8
```

## Validation and Testing

### Validate Checkpoint

```bash
python scripts/validate_lora.py lora/my_character_v1.safetensors
```

Output shows:
- File format and size
- LoRA rank
- Parameter count
- Load test result

### Test Generation

```bash
python scripts/batch_generate.py \
    --input test_image.png \
    --lora lora/my_character_v1.safetensors \
    --lora-scale 0.8 \
    --prompt "character walking forward" \
    --output outputs/test
```

### Compare LoRA Weights

Test different scales to find optimal strength:

```bash
for scale in 0.5 0.6 0.7 0.8 0.9 1.0; do
    python scripts/batch_generate.py \
        --input test.png \
        --lora lora/my_character_v1.safetensors \
        --lora-scale $scale \
        --output outputs/scale_$scale
done
```

## Best Practices

### Dataset Quality

✅ **Do:**
- Use consistent lighting
- Include variety of poses
- High-resolution source images
- Remove blurry/low-quality images
- Curate carefully

❌ **Don't:**
- Use watermarked images
- Mix different characters
- Include text overlays
- Use extremely similar images
- Exceed copyright boundaries

### Training Hyperparameters

**Learning Rate:**
- Too high (>5e-4): Unstable, divergence
- Sweet spot (1e-4 to 5e-5): Stable training
- Too low (<1e-5): Slow convergence

**Epochs:**
- Too few (<5): Underfitting
- Optimal (8-15): Good generalization
- Too many (>20): Overfitting

**LoRA Rank:**
- Low (4-8): Fast, low VRAM, less capacity
- Medium (16-32): Balanced
- High (64-128): High capacity, more VRAM

### Avoiding Overfitting

1. **Use validation set:**
```yaml
data:
  validation_split: 0.1
```

2. **Early stopping:**
Monitor validation loss, stop when it increases

3. **Regularization:**
```yaml
lora:
  dropout: 0.05
```

4. **Dataset size:**
Use 20-50 images minimum

### Iterative Training

Train multiple versions:

```bash
# Version 1: Conservative
python scripts/train_lora.py \
    --output lora/character_v1 \
    --epochs 8 \
    --learning-rate 1e-4

# Version 2: More epochs
python scripts/train_lora.py \
    --output lora/character_v2 \
    --epochs 12 \
    --learning-rate 1e-4

# Version 3: Higher rank
# Edit config: lora.rank = 64
python scripts/train_lora.py \
    --output lora/character_v3 \
    --epochs 10
```

Test all versions and pick the best.

## Advanced Techniques

### Resume Training

```bash
python scripts/train_lora.py \
    --config config/training_config.yaml \
    --resume lora/my_character_v1/checkpoint-500
```

### Multi-Concept Training

Train on multiple concepts:

```
data/training/
├── character_a/
│   ├── img1.png
│   └── img2.png
└── character_b/
    ├── img1.png
    └── img2.png
```

### Text Encoder Training

```yaml
advanced:
  train_text_encoder: true
  text_encoder_lr: 5e-6
```

⚠️ Requires more VRAM and training time.

## Troubleshooting

### Training Loss Not Decreasing

- Check learning rate (try 5e-5 or 2e-4)
- Verify dataset quality
- Increase epochs
- Check if model is loading correctly

### Out of Memory

- Reduce batch size to 1
- Enable gradient checkpointing
- Use 8-bit Adam optimizer
- Reduce LoRA rank
- Lower resolution

### Overfitting

Signs:
- Training loss decreases, validation increases
- Generated images too similar to training data
- Loss becomes very low (<0.01)

Solutions:
- More diverse dataset
- Fewer epochs
- Add dropout
- Increase dataset size

### Generated Videos Look Wrong

- Adjust LoRA scale (0.6-0.9)
- Train for more/fewer epochs
- Check dataset consistency
- Verify model loaded correctly

## Output Files

After training:

```
lora/my_character_v1/
├── my_character_v1.safetensors   # Final LoRA weights
├── checkpoint-500/               # Intermediate checkpoint
├── checkpoint-1000/
├── training_log.txt              # Training logs
└── config.yaml                   # Training configuration
```

## Next Steps

- Test LoRA with different scales
- Generate videos with trained LoRA
- Try combining multiple LoRAs
- Experiment with different datasets
- Share your LoRA (with permission)

## Resources

- PEFT Library: https://github.com/huggingface/peft
- LoRA Paper: https://arxiv.org/abs/2106.09685
- HunyuanVideo: https://huggingface.co/tencent/HunyuanVideo

## Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub Issue
- Review example configs
