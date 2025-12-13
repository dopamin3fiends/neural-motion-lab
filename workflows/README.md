# ComfyUI Workflows

This directory contains ComfyUI workflow JSON files for Neural Motion Lab.

## Available Workflows

### 1. basic_i2v_lora.json
Basic image-to-video generation with single LoRA application.

**Features:**
- Single input image
- One LoRA model
- Standard generation parameters
- Simple prompt system

**Use Case:** Quick video generation with character consistency

### 2. multi_lora_blend.json
Advanced workflow for blending multiple LoRAs.

**Features:**
- Multiple LoRA models
- Adjustable blend weights
- Style + character combination
- Advanced control

**Use Case:** Complex character and style combinations

### 3. batch_generation.json
Batch processing workflow for multiple images.

**Features:**
- Multiple input images
- Shared LoRA and settings
- Batch output
- Progress tracking

**Use Case:** Generating videos from image sequences

## How to Use

### 1. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

### 2. Setup Model Paths

Copy models to ComfyUI directories or create symlinks:

```bash
# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path "ComfyUI/models/checkpoints" -Target "models/hunyuan_video"
New-Item -ItemType SymbolicLink -Path "ComfyUI/models/loras" -Target "lora"

# Linux/Mac
ln -s models/hunyuan_video ComfyUI/models/checkpoints
ln -s lora ComfyUI/models/loras
```

### 3. Import Workflow

1. Start ComfyUI: `python main.py`
2. Open in browser (usually http://localhost:8188)
3. Click "Load" button
4. Select workflow JSON from this directory
5. Adjust parameters as needed
6. Click "Queue Prompt" to generate

## Workflow Parameters

### Common Parameters

- **Input Image**: Path or drag-and-drop image
- **Prompt**: Positive text description
- **Negative Prompt**: What to avoid
- **LoRA Path**: Path to LoRA checkpoint
- **LoRA Weight**: 0.0 to 1.5 (typically 0.8)
- **Num Frames**: 25, 49, or 73 frames
- **FPS**: 8, 12, 16, 24, or 30
- **Seed**: Random seed (-1 for random)
- **Steps**: Sampling steps (25-50 recommended)
- **CFG Scale**: Guidance scale (7-9 recommended)

### Advanced Parameters

- **Scheduler**: euler_a, ddim, pndm
- **Denoise**: Denoising strength (0.7-1.0)
- **Width/Height**: Output resolution (512, 768, 1024)

## Customizing Workflows

To customize workflows:

1. Load workflow in ComfyUI
2. Modify nodes and connections
3. Save as new JSON: Menu > Save
4. Document changes in filename

## Troubleshooting

### Models not appearing
- Check model paths in workflow nodes
- Verify models are in correct ComfyUI directories
- Restart ComfyUI after moving models

### Out of memory
- Reduce resolution
- Decrease number of frames
- Enable model offloading in ComfyUI settings

### Slow generation
- Enable xFormers
- Use fp16 precision
- Check GPU utilization

## Creating Custom Workflows

Tips for creating workflows:

1. Start from existing workflow
2. Add nodes from right-click menu
3. Connect nodes with compatible inputs/outputs
4. Test thoroughly before saving
5. Document special requirements

## Examples

### Basic Generation
```
Load: basic_i2v_lora.json
Input: portrait.png
LoRA: lora/character_v1.safetensors
Prompt: "character walking forward, smooth motion"
```

### Style + Character Blend
```
Load: multi_lora_blend.json
LoRA 1: lora/character_v1.safetensors (weight: 0.8)
LoRA 2: lora/anime_style.safetensors (weight: 0.6)
Prompt: "character in anime style, walking"
```

## Resources

- ComfyUI GitHub: https://github.com/comfyanonymous/ComfyUI
- ComfyUI Wiki: https://github.com/comfyanonymous/ComfyUI/wiki
- Community Workflows: https://comfyworkflows.com/

## Notes

- Workflows are templates and may need adjustment
- Model versions may affect compatibility
- Save custom workflows with descriptive names
- Back up working workflows
