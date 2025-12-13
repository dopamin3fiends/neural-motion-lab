# Model Setup Guide

## Overview

Neural Motion Lab requires two main types of models:
1. HunyuanVideo-I2V base model
2. LoRA models for character consistency (optional)

## HunyuanVideo-I2V Model

### Download

```bash
# Using git-lfs (if available through official repository)
cd models/hunyuan
# Follow instructions from HunyuanVideo repository
```

### Alternative: Manual Download

1. Visit the HunyuanVideo model repository
2. Download the model weights
3. Place files in `models/hunyuan/`

Expected files:
```
models/hunyuan/
├── model.safetensors
├── config.json
└── tokenizer/
```

### Verify Installation

```python
from neural_motion_lab.models import HunyuanModel

model = HunyuanModel("models/hunyuan")
model.load()
print("Model loaded successfully!")
```

## LoRA Models

### Character-Specific LoRA

LoRA models enable character-consistent generation across videos.

#### Download Pre-trained LoRA

```bash
# Example: Download from Hugging Face
cd models/lora
# wget or git clone your LoRA model
```

#### Train Custom LoRA

See [Training Guide](../usage/training.md) for details on training custom LoRA models.

### LoRA Directory Structure

```
models/lora/
├── character1/
│   ├── lora_weights.safetensors
│   └── config.json
├── character2/
│   └── lora_weights.safetensors
└── ...
```

## Model Configuration

### Pipeline Configuration

Edit `configs/pipeline.yaml`:

```yaml
models:
  hunyuan:
    path: "models/hunyuan"
    device: "cuda"
    precision: "fp16"
  
  lora:
    enabled: true
    path: "models/lora/character1"
    scale: 0.8
```

### Advanced Settings

```yaml
generation:
  num_frames: 16
  fps: 8
  width: 512
  height: 512
  guidance_scale: 7.5
  num_inference_steps: 50
```

## Model Requirements

### Disk Space

- HunyuanVideo-I2V: ~10-15 GB
- Each LoRA model: ~50-500 MB
- Total recommended: 20+ GB

### GPU Memory

| Resolution | Frames | Minimum VRAM |
|-----------|--------|--------------|
| 512x512   | 16     | 8 GB         |
| 768x768   | 16     | 12 GB        |
| 1024x1024 | 16     | 16+ GB       |

## Optimization Tips

### Reduce Memory Usage

1. **Use Lower Precision**
   ```yaml
   precision: "fp16"  # or "int8" for even lower memory
   ```

2. **Enable CPU Offloading**
   ```yaml
   offload:
     enabled: true
     offload_to: "cpu"
   ```

3. **Reduce Resolution**
   ```yaml
   width: 512
   height: 512
   ```

### Improve Speed

1. **Use xFormers** (if available)
   ```bash
   pip install xformers
   ```

2. **Enable Flash Attention**
   ```yaml
   attention:
     type: "flash"
   ```

3. **Compile Model** (PyTorch 2.0+)
   ```python
   model = torch.compile(model)
   ```

## Troubleshooting

### Model Not Loading

- Check file paths in config
- Verify model files exist
- Ensure sufficient disk space

### Out of Memory

- Reduce batch size
- Lower resolution
- Enable CPU offloading
- Use gradient checkpointing

### Slow Generation

- Check GPU utilization
- Enable optimizations (xFormers, Flash Attention)
- Use lower precision (fp16)

## Next Steps

- Try [Basic Usage](../usage/basic.md)
- Explore [Advanced Features](../usage/advanced.md)
- Train [Custom LoRA](../usage/training.md)
