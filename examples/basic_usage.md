# Basic Usage Guide

Welcome to Neural Motion Lab! This guide will walk you through creating your first AI-generated video from a static image.

## Prerequisites

Before starting, ensure you have:
- Installed ComfyUI
- Run `python scripts/setup.py`
- Downloaded required models with `python scripts/download_models.py`
- A source image to animate

## Quick Start

### Step 1: Prepare Your Image

1. Place your input image in ComfyUI's `input/` directory
2. Recommended image specifications:
   - Format: PNG, JPG, or WebP
   - Resolution: 1280x720 (or 720p aspect ratio)
   - Clear subject with good lighting
   - Avoid overly complex backgrounds for first attempts

### Step 2: Launch ComfyUI

```bash
cd /path/to/ComfyUI
python main.py
```

Open your browser to `http://127.0.0.1:8188`

### Step 3: Load the Basic Workflow

1. In ComfyUI, click the **Load** button (or drag and drop)
2. Navigate to `neural-motion-lab/workflows/`
3. Select `basic_i2v.json`
4. The workflow will load with all nodes connected

### Step 4: Configure the Workflow

#### A. Load Image Node
- Click on the **LoadImage** node
- Select your input image from the dropdown
- Preview should show your image

#### B. Text Prompt (Positive)
- Click on the **CLIPTextEncode** node (positive prompt)
- Enter your motion description, for example:
  ```
  A person walking forward, natural movement, smooth motion, high quality
  ```
- Be specific about the motion you want

#### C. Text Prompt (Negative)
- Click on the negative **CLIPTextEncode** node
- Keep or modify the negative prompt:
  ```
  blurry, low quality, distorted, artifacts
  ```

#### D. Sampling Settings
- Click on the **KSampler** node
- Adjust parameters:
  - **Seed**: Change for different results (or use -1 for random)
  - **Steps**: 25 is good for testing (higher = better quality but slower)
  - **CFG Scale**: 6.0 is recommended (controls prompt adherence)

#### E. Output Settings
- Click on the **VHS_VideoCombine** node
- Set frame rate (default: 24 fps)
- Choose output filename

### Step 5: Generate Video

1. Click **Queue Prompt** in the sidebar (or press Ctrl+Enter)
2. Watch the progress in the console/UI
3. Generation typically takes 2-5 minutes depending on GPU
4. Find your video in `ComfyUI/output/`

## Understanding the Parameters

### Seed
- **Fixed value**: Same image + prompt = same result
- **-1 (random)**: Different result each time
- **Incremental**: Slightly vary results between runs

### Steps
- **15-20**: Fast preview (lower quality)
- **25-30**: Good balance (recommended)
- **35-50**: High quality (slower)

### CFG Scale
- **Low (3-5)**: More creative, less prompt adherence
- **Medium (6-8)**: Balanced (recommended)
- **High (9-15)**: Strong prompt adherence, may be rigid

### Sampler
- **dpmpp_2m**: Balanced quality and speed (default)
- **euler_a**: Faster, more creative
- **ddim**: Slower, more stable

### Scheduler
- **karras**: Recommended for most cases
- **normal**: Standard schedule
- **exponential**: Sometimes smoother results

## Tips for Better Results

### Prompt Writing
- **Be specific**: "A woman walking towards camera with confident stride" vs "person moving"
- **Include motion**: Specify the type and speed of movement
- **Add quality terms**: "smooth motion", "high quality", "detailed"
- **Avoid contradictions**: Don't ask for both "fast" and "slow" motion

### Image Selection
- **Clear subjects**: Well-defined characters or objects work best
- **Good lighting**: Avoid overly dark or blown-out images
- **Simple backgrounds**: Complex backgrounds may distort
- **Centered composition**: Subject in center frame works better

### Common Issues

**Video is blurry**
- Increase steps to 30-35
- Increase CFG scale to 7-8
- Check input image quality

**Motion is too fast/slow**
- Adjust frame duration in video settings
- Modify prompt with "slow motion" or "quick movement"

**Character/object distorts**
- Lower CFG scale to 5-6
- Try fewer steps initially
- Check if input image is too complex

**Out of memory error**
- Reduce resolution to 854x480
- Enable CPU offload in config
- Close other GPU applications

## Next Steps

Once comfortable with basic generation:

1. **Try different prompts**: Experiment with various motions
2. **Use LoRAs**: Check out [character_animation.md](character_animation.md)
3. **Apply styles**: See [style_transfer.md](style_transfer.md)
4. **Batch processing**: Generate multiple variations

## Example Prompts

### Natural Motion
```
A person walking forward naturally, casual pace, smooth movement, realistic motion
```

### Camera Movement
```
Static subject, camera slowly zooming in, cinematic movement
```

### Environmental Motion
```
Person standing still, hair and clothes gently blowing in wind, subtle movement
```

### Action
```
Character running forward energetically, dynamic motion, action pose
```

## Troubleshooting

### Workflow won't load
- Verify JSON file isn't corrupted
- Check ComfyUI console for errors
- Ensure all required custom nodes are installed

### Missing nodes error
- Install required ComfyUI custom nodes
- Check dependencies in requirements.txt

### Generation fails
- Verify all models are downloaded
- Check file paths in config files
- Ensure sufficient VRAM (8GB minimum)

## Getting Help

- Check the main [README.md](../README.md) for detailed information
- Review [model_settings.yaml](../configs/model_settings.yaml) for optimization
- Join the community for support and examples

Happy animating! 🎬
