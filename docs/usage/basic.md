# Basic Usage Guide

## Getting Started

This guide covers basic usage of Neural Motion Lab for video generation.

## Quick Example

```python
from neural_motion_lab import VideoPipeline
from PIL import Image
import numpy as np

# Initialize pipeline
pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan",
    lora_model_path="models/lora/character1",
    device="cuda"
)

# Setup models
pipeline.setup()

# Load input image
image = Image.open("input.jpg")
image_array = np.array(image)

# Generate video
video = pipeline.generate_video(
    input_image=image_array,
    prompt="A person walking in a park, cinematic",
    num_frames=16,
    fps=8,
    seed=42
)

# Save video
import imageio
imageio.mimsave("output.mp4", video, fps=8)
```

## Command Line Usage

### Generate Video

```bash
python -m neural_motion_lab.cli generate \
    --image input.jpg \
    --prompt "A person walking in a park" \
    --output output.mp4 \
    --num-frames 16 \
    --fps 8
```

### Batch Processing

```bash
python -m neural_motion_lab.cli batch \
    --input-dir images/ \
    --prompts-file prompts.txt \
    --output-dir videos/ \
    --num-frames 16
```

## Configuration

### Using Config Files

Create a configuration file `config.yaml`:

```yaml
pipeline:
  hunyuan_model_path: "models/hunyuan"
  lora_model_path: "models/lora/character1"
  device: "cuda"

generation:
  num_frames: 16
  fps: 8
  width: 512
  height: 512
  guidance_scale: 7.5
  num_inference_steps: 50
```

Use the config:

```python
from neural_motion_lab.utils import load_config
from neural_motion_lab import VideoPipeline

config = load_config("config.yaml")
pipeline = VideoPipeline(**config['pipeline'])
```

## Input Image Preprocessing

### Resize and Prepare Images

```python
from scripts.data.preprocess import preprocess_image

preprocess_image(
    image_path="raw_image.jpg",
    output_path="processed_image.jpg",
    size=(512, 512)
)
```

### Batch Preprocessing

```bash
python scripts/data/preprocess.py \
    images/ \
    processed_images/ \
    --width 512 \
    --height 512
```

## Generation Parameters

### Key Parameters

- `prompt`: Text description of desired motion/scene
- `num_frames`: Number of video frames to generate (8-32)
- `fps`: Frames per second (4-30)
- `seed`: Random seed for reproducibility
- `guidance_scale`: How closely to follow prompt (1-20)
- `num_inference_steps`: Generation quality vs speed trade-off (20-100)

### Example with Custom Parameters

```python
video = pipeline.generate_video(
    input_image=image_array,
    prompt="Close-up of a person smiling and waving",
    num_frames=24,
    fps=12,
    guidance_scale=8.0,
    num_inference_steps=50,
    seed=12345
)
```

## Output Formats

### Save as MP4

```python
import imageio

imageio.mimsave("output.mp4", video, fps=8)
```

### Save as GIF

```python
imageio.mimsave("output.gif", video, fps=8)
```

### Extract Frames

```python
import os
from PIL import Image

output_dir = "frames/"
os.makedirs(output_dir, exist_ok=True)

for i, frame in enumerate(video):
    Image.fromarray(frame).save(f"{output_dir}/frame_{i:04d}.png")
```

## Tips for Best Results

### Prompt Engineering

1. **Be Specific**: "A woman slowly turning her head to the right" vs "movement"
2. **Add Style**: "cinematic lighting", "high quality", "smooth motion"
3. **Describe Motion**: Focus on the action/movement you want

### Image Preparation

1. **Good Lighting**: Well-lit images produce better results
2. **Clear Subject**: Subject should be prominent and clear
3. **Appropriate Resolution**: 512x512 or 768x768 works well
4. **Consistent Style**: Match image style to desired output

### Character Consistency

1. **Use LoRA**: Essential for maintaining character appearance
2. **Consistent Input**: Use similar poses/angles across videos
3. **Clear Features**: Character features should be visible

## Common Issues

### Video Quality Issues

- Increase `num_inference_steps`
- Adjust `guidance_scale`
- Use higher resolution
- Improve input image quality

### Character Inconsistency

- Verify LoRA model is loaded
- Increase LoRA scale in config
- Use clearer input images
- Train custom LoRA for your character

### Generation Too Slow

- Reduce `num_inference_steps`
- Lower resolution
- Enable optimizations (see Advanced Usage)

## Next Steps

- Explore [Advanced Features](advanced.md)
- Learn about [ComfyUI Integration](comfyui.md)
- Train [Custom LoRA Models](training.md)
