# ComfyUI Workflows Guide

Complete guide to using ComfyUI workflows with Neural Motion Lab.

## Overview

ComfyUI provides a node-based interface for AI video generation. Neural Motion Lab includes pre-configured workflows for common tasks.

## Quick Start

1. **Install ComfyUI**
2. **Link models to ComfyUI**
3. **Load workflow**
4. **Adjust parameters**
5. **Generate**

See [QUICKSTART.md](QUICKSTART.md) for detailed setup.

## Available Workflows

### 1. Basic I2V + LoRA (`basic_i2v_lora.json`)

**Purpose:** Simple image-to-video generation with single LoRA

**Nodes:**
- Load Image
- Load Checkpoint (HunyuanVideo)
- LoRA Loader
- Text Encode (Positive/Negative)
- Video Generation
- VAE Decode
- Save Video

**Parameters:**
| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| LoRA Path | character_v1.safetensors | - | Path to LoRA file |
| LoRA Weight | 0.8 | 0.0-1.5 | LoRA influence strength |
| Width | 512 | 256-1024 | Video width (multiple of 8) |
| Height | 512 | 256-1024 | Video height (multiple of 8) |
| Num Frames | 49 | 25-73 | Number of frames |
| Steps | 50 | 20-100 | Sampling steps |
| CFG Scale | 7.5 | 1.0-20.0 | Guidance scale |
| Seed | 42 | -1 to ∞ | Random seed (-1 = random) |
| Scheduler | euler_a | - | Sampling scheduler |

**Usage:**
```
1. Load workflow in ComfyUI
2. Set input image path
3. Adjust LoRA path and weight
4. Set prompt
5. Adjust generation parameters
6. Queue Prompt
```

**Tips:**
- Use 512x512 for fastest results
- CFG 7-9 for balanced output
- LoRA weight 0.6-0.9 typical
- Fix seed for reproducibility

### 2. Multi-LoRA Blend (`multi_lora_blend.json`)

**Purpose:** Combine multiple LoRAs (character + style)

**Nodes:**
- Load Image
- Load Checkpoint
- LoRA Loader 1 (Character)
- LoRA Loader 2 (Style)
- Text Encode
- Video Generation
- VAE Decode
- Save Video

**Parameters:**

**LoRA 1 (Character):**
- Path: character_v1.safetensors
- Weight: 0.8 (typically higher)

**LoRA 2 (Style):**
- Path: style_anime.safetensors
- Weight: 0.6 (typically lower)

**Other:** Same as basic workflow

**Usage:**
```
1. Load workflow
2. Set first LoRA (character)
3. Set second LoRA (style)
4. Adjust individual weights
5. Set prompts
6. Generate
```

**Blending Guidelines:**
| Combination | LoRA 1 Weight | LoRA 2 Weight | Result |
|-------------|---------------|---------------|---------|
| Char + Style | 0.8 | 0.6 | Balanced |
| Char dominant | 0.9 | 0.4 | Strong character |
| Style dominant | 0.5 | 0.8 | Strong style |
| Experimental | 1.0 | 1.0 | May overfit |

**Tips:**
- Character LoRA typically stronger
- Total combined weight 1.0-1.4
- Test different combinations
- Adjust prompts to reinforce

### 3. Batch Generation (`batch_generation.json`)

**Purpose:** Process multiple images sequentially

**Nodes:**
- Load Image Batch
- Batch Iterator
- Load Checkpoint
- LoRA Loader
- Text Encode
- Video Generation
- VAE Decode
- Save Video Batch

**Parameters:**
- Input Directory: Folder with images
- Batch Mode: Batch processing
- Auto-increment: Automatic output naming
- Other: Same as basic workflow

**Usage:**
```
1. Load workflow
2. Set input directory
3. Configure batch settings
4. Set shared LoRA and prompts
5. Queue Prompt
6. Monitor progress
```

**Tips:**
- Place all images in one folder
- Use consistent naming
- Monitor VRAM during batch
- Use fixed seed for consistency

## Node Reference

### Input Nodes

**LoadImage:**
- Loads single image
- Supports: PNG, JPG, WebP
- Can drag-and-drop in ComfyUI

**LoadImageBatch:**
- Loads multiple images
- Specify folder path
- Supports filtering

### Model Nodes

**CheckpointLoaderSimple:**
- Loads base model
- Returns: MODEL, CLIP, VAE
- Path: models/checkpoints/

**LoraLoader:**
- Applies LoRA to model
- Inputs: MODEL, CLIP
- Outputs: Modified MODEL, CLIP
- Parameters:
  - lora_name: Filename
  - strength_model: 0.0-1.5
  - strength_clip: 0.0-1.5

### Conditioning Nodes

**CLIPTextEncode:**
- Encodes text prompts
- Input: CLIP, text
- Output: CONDITIONING
- Supports: Short and long prompts

### Generation Nodes

**HunyuanVideoI2V:**
- Main generation node
- Inputs:
  - MODEL
  - CONDITIONING (positive)
  - CONDITIONING (negative)
  - IMAGE
  - VAE
- Outputs: LATENT
- Parameters: See table above

### Decode/Save Nodes

**VAEDecode:**
- Decodes latents to images
- Input: LATENT, VAE
- Output: IMAGE

**SaveVideo:**
- Saves frames as video
- Input: IMAGE
- Parameters:
  - filename_prefix
  - fps: 8-60
  - format: mp4, avi, webm
  - codec: h264, h265

## Creating Custom Workflows

### Basic Workflow Structure

```
Input → Model Loading → LoRA → Conditioning → Generation → Decode → Save
```

### Adding Nodes

1. Right-click in ComfyUI
2. Select node category
3. Choose node type
4. Connect inputs/outputs

### Node Connections

**Valid connections:**
- MODEL → MODEL
- CLIP → CLIP
- IMAGE → IMAGE
- LATENT → LATENT
- CONDITIONING → CONDITIONING

**Type matching required!**

### Example: Add Image Preprocessing

```
LoadImage → ImageResize → ImageSharpen → [existing workflow]
```

### Example: Add Post-Processing

```
[existing workflow] → ColorCorrection → Upscale → SaveVideo
```

## Parameter Guidelines

### Resolution Settings

**512x512:**
- Fastest generation
- Lowest VRAM
- Good quality
- Recommended for testing

**768x768:**
- Medium speed
- Medium VRAM (14-16 GB)
- Better quality
- Good for final output

**1024x1024:**
- Slowest
- High VRAM (20+ GB)
- Best quality
- Use for showcase

### Frame Count

**25 frames:**
- ~1 second at 24fps
- Quick tests
- Low VRAM

**49 frames:**
- ~2 seconds at 24fps
- Standard output
- Balanced

**73 frames:**
- ~3 seconds at 24fps
- Longer videos
- High VRAM

### CFG Scale

| Value | Effect | Use Case |
|-------|--------|----------|
| 1-3 | Minimal guidance | Experimental |
| 5-7 | Balanced | Creative freedom |
| 7-9 | Standard | Recommended |
| 10-15 | Strong | Specific results |
| 15+ | Very strong | May cause artifacts |

### Sampling Steps

| Steps | Quality | Speed | Use Case |
|-------|---------|-------|----------|
| 20-30 | Low | Fast | Testing |
| 40-50 | Good | Medium | Standard |
| 60-75 | Better | Slow | Quality output |
| 75+ | Best | Very slow | Final render |

## Advanced Techniques

### Prompt Engineering

**Good prompts:**
```
"character walking forward, smooth motion, natural movement, high quality, detailed"
```

**Negative prompts:**
```
"blurry, distorted, low quality, artifacts, jittery motion, static"
```

**Structured:**
```
"[character description], [action], [style], [quality terms]"
```

### LoRA Stacking Order

Order matters when stacking LoRAs:

```
Base Model → Character LoRA → Style LoRA → Detail LoRA
```

General to specific works best.

### Seed Management

**Fixed seed:**
- Use same seed for reproducibility
- Compare different parameters
- Fine-tune settings

**Random seed (-1):**
- Explore variations
- Generate diverse outputs
- Production use

### Batch Optimization

**For batch processing:**
1. Use fixed prompts across batch
2. Set consistent seed (or sequential)
3. Monitor VRAM usage
4. Save checkpoints periodically

## Troubleshooting Workflows

### Workflow Won't Load

**Check:**
- JSON syntax valid
- ComfyUI version compatible
- Required custom nodes installed

### Node Connection Errors

**Solutions:**
- Verify type compatibility
- Check node inputs/outputs
- Reload workflow

### Missing Models

**Solutions:**
- Verify model paths
- Check symlinks
- Copy models to ComfyUI/models/

### Slow Generation

**Optimize:**
- Enable xFormers in ComfyUI settings
- Reduce resolution/frames
- Close other applications
- Check GPU utilization

## Workflow Sharing

### Export Workflow

1. File → Save
2. Choose filename
3. Share JSON file

### Import Workflow

1. File → Load
2. Select JSON
3. Adjust paths if needed

### Documentation

When sharing workflows:
- Document required models
- List custom nodes needed
- Provide parameter recommendations
- Include example outputs

## Resources

- ComfyUI GitHub: https://github.com/comfyanonymous/ComfyUI
- ComfyUI Wiki: https://github.com/comfyanonymous/ComfyUI/wiki
- Community Workflows: https://comfyworkflows.com/
- Custom Nodes: https://github.com/ltdrdata/ComfyUI-Manager

## Next Steps

- Experiment with parameters
- Create custom workflows
- Combine multiple techniques
- Share your workflows

## Getting Help

- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check ComfyUI documentation
- Ask in ComfyUI Discord
- Open GitHub issue
