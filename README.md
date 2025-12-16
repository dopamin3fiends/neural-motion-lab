# Neural Motion Lab

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen)

A fully functional modular pipeline integrating LoRA with HunyuanVideo-I2V for character-consistent AI video generation via ComfyUI.

## 🎬 Overview

Neural Motion Lab transforms static images into dynamic videos using state-of-the-art AI models. Built on HunyuanVideo and enhanced with LoRA support, it enables:

- **Character-Consistent Animation**: Maintain character identity across all frames
- **Style Transfer**: Apply anime, realistic, cinematic, or artistic styles
- **Flexible Workflows**: Pre-built ComfyUI workflows for various use cases
- **Easy Configuration**: YAML-based settings for quick customization
- **Batch Processing**: Generate multiple variations efficiently

### Key Features

✨ **Multiple Workflow Presets**
- Basic image-to-video conversion
- LoRA-enhanced generation
- Character consistency workflows
- Advanced multi-LoRA combinations

🎨 **Style Flexibility**
- Anime/manga aesthetics
- Photorealistic rendering
- Cinematic film looks
- Artistic/painterly styles
- Fantasy and custom styles

🔧 **Developer-Friendly**
- Modular Python scripts
- Comprehensive configuration files
- Automated setup and model downloading
- Extensive documentation

🚀 **Production-Ready**
- Memory optimization profiles
- Quality presets (preview to production)
- Batch processing capabilities
- API-compatible workflows

## 📋 Prerequisites

### Required Software

- **ComfyUI**: Latest version from [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- **Python**: 3.8 or higher
- **CUDA**: 11.8+ (for GPU acceleration)

### Hardware Requirements

| Resolution | VRAM    | RAM   | Recommended GPU          |
|------------|---------|-------|--------------------------|
| 480p       | 8GB+    | 16GB  | RTX 3060, RTX 4060       |
| 720p       | 12GB+   | 32GB  | RTX 3080, RTX 4070       |
| 1080p      | 24GB+   | 64GB  | RTX 4090, A5000          |

**Minimum**: 8GB VRAM, 16GB RAM, CUDA-capable GPU  
**Recommended**: 12GB+ VRAM, 32GB+ RAM, RTX 3080 or better

### Required ComfyUI Custom Nodes

- **VideoHelperSuite**: For video output functionality
- **ComfyUI-Manager**: For easy node management (optional but recommended)
- **ControlNet**: For pose-guided generation (optional)
- **IP-Adapter**: For image conditioning (optional)

Install via ComfyUI Manager or manually from their repositories.

## 🚀 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab

# Run automated setup
python scripts/setup.py

# Download required models
python scripts/download_models.py
```

The setup script will:
- ✅ Check Python version
- ✅ Verify ComfyUI installation
- ✅ Create necessary directories
- ✅ Install Python dependencies
- ✅ Check GPU availability
- ✅ Create .gitignore

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

#### 1. Clone Repository

```bash
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Create Directory Structure

```bash
mkdir -p models/checkpoints models/loras models/vae models/clip
mkdir -p models/controlnet models/ipadapter
mkdir -p outputs
```

#### 4. Download Models

Download the following models and place in respective directories:

**HunyuanVideo Model** (~14GB)
```
URL: https://huggingface.co/tencent/HunyuanVideo
File: hunyuan_video_720_cfgdistill.safetensors
Location: models/checkpoints/
```

**VAE Model** (~1GB)
```
URL: https://huggingface.co/tencent/HunyuanVideo
File: hunyuan_video_vae_fp16.safetensors
Location: models/vae/
```

**CLIP Text Encoder** (~8GB)
```
URL: https://huggingface.co/llava/LLaVA-v1.6-Llama-3-8B
File: llava_llama3_fp16.safetensors
Location: models/clip/
```

**LoRAs** (Optional, community-provided)
- Character consistency LoRAs
- Style LoRAs (anime, realistic, cinematic)
- Motion enhancement LoRAs

Place LoRAs in: `models/loras/`

#### 5. Configure ComfyUI

Update model paths in ComfyUI's `extra_model_paths.yaml` or place models in ComfyUI's default directories.

</details>

## 🎯 Quick Start

### Your First Video Generation

1. **Prepare an image**
   - Place in `ComfyUI/input/` directory
   - Recommended: 1280x720 resolution
   - Format: PNG, JPG, or WebP

2. **Launch ComfyUI**
   ```bash
   cd /path/to/ComfyUI
   python main.py
   ```
   Open browser to `http://127.0.0.1:8188`

3. **Load workflow**
   - In ComfyUI, click **Load**
   - Navigate to `neural-motion-lab/workflows/`
   - Select `basic_i2v.json`

4. **Configure settings**
   - **LoadImage**: Select your input image
   - **Positive Prompt**: Describe desired motion
   - **Negative Prompt**: Things to avoid
   - **KSampler**: Adjust steps/CFG if needed

5. **Generate**
   - Click **Queue Prompt** (or Ctrl+Enter)
   - Wait 2-5 minutes
   - Find output in `ComfyUI/output/`

📖 **Detailed guide**: See [examples/basic_usage.md](examples/basic_usage.md)

## 📚 Usage Guide

### Basic Image-to-Video

Transform static images into animated videos.

**Workflow**: `workflows/basic_i2v.json`

```
Input Image → HunyuanVideo → Motion Generation → Video Output
```

**Key Parameters**:
- **Steps**: 25 (balanced), 30-35 (high quality)
- **CFG Scale**: 6.0 (balanced), 7-8 (more faithful)
- **Prompt**: Describe the motion you want

**Example**:
```
Positive: "A person walking forward, natural movement, smooth motion"
Negative: "blurry, low quality, distorted, artifacts"
```

📖 **Full guide**: [examples/basic_usage.md](examples/basic_usage.md)

### LoRA-Enhanced Generation

Add style and enhancement LoRAs to your generation.

**Workflow**: `workflows/lora_i2v.json`

```
Input Image → Model + LoRA → Enhanced Generation → Video Output
```

**Use Cases**:
- Apply artistic styles (anime, realistic, cinematic)
- Enhance motion smoothness
- Improve detail and clarity

**Configuration**:
```yaml
# In LoraLoader node
LoRA File: style_anime_lora.safetensors
Strength (Model): 0.7
Strength (CLIP): 0.7
```

📖 **Style guide**: [examples/style_transfer.md](examples/style_transfer.md)

### Character-Consistent Animation

Maintain character identity throughout the video.

**Workflow**: `workflows/character_consistent.json`

```
Character Reference → IPAdapter + ControlNet + LoRA → Consistent Animation
```

**Features**:
- Face consistency across frames
- Stable clothing and accessories
- Maintained body proportions
- Identity preservation

**Best Practices**:
- Use high-quality reference images
- Increase LoRA strength (0.85-0.95)
- Describe character details in prompt
- Use higher step count (30-35)

📖 **Character guide**: [examples/character_animation.md](examples/character_animation.md)

### Advanced Multi-LoRA Variations

Combine multiple LoRAs for complex styles.

**Workflow**: `workflows/advanced_variations.json`

```
Input → LoRA Stack (Style + Motion + Detail) → Complex Generation
```

**Example Combinations**:
- Anime Style + Character Consistency
- Cinematic Style + Smooth Motion
- Realistic + Detail Enhancer
- Fantasy + Character + Motion

**Configuration**:
```yaml
LoRA 1: style_anime (0.7)
LoRA 2: character_consistency (0.85)
LoRA 3: motion_smooth (0.6)
```

## ⚙️ Configuration

### Directory Structure

```
configs/
├── default_config.yaml      # Main configuration
├── lora_presets.yaml         # LoRA combinations
└── model_settings.yaml       # Model-specific settings
```

### default_config.yaml

Global settings for video generation:

```yaml
video:
  resolution:
    width: 1280
    height: 720
  frame_rate: 24
  duration_seconds: 4

sampling:
  steps: 25
  cfg_scale: 6.0
  sampler: "dpmpp_2m"
  scheduler: "karras"

memory:
  enable_attention_slicing: true
  enable_vae_slicing: true
  use_fp16: true
```

### lora_presets.yaml

Pre-configured LoRA settings:

```yaml
styles:
  anime:
    lora: "style_anime_lora.safetensors"
    strength_model: 0.7
    strength_clip: 0.7
  
  realistic:
    lora: "style_realistic_lora.safetensors"
    strength_model: 0.8
    strength_clip: 0.8
```

### model_settings.yaml

Memory profiles and quality presets:

```yaml
memory_profiles:
  low_vram_8gb:
    resolution: "sd_480p"
    max_frames: 48
    enable_cpu_offload: true
  
  medium_vram_12gb:
    resolution: "hd_720p"
    max_frames: 96
  
  high_vram_24gb:
    resolution: "fhd_1080p"
    max_frames: 120
```

## 🔧 Workflow Variations

### 1. Simple Animation
**Use**: Basic motion from static image  
**Workflow**: `basic_i2v.json`  
**Time**: 2-3 minutes  
**Complexity**: ⭐

### 2. Character Animation
**Use**: Consistent character across frames  
**Workflow**: `character_consistent.json`  
**Time**: 4-6 minutes  
**Complexity**: ⭐⭐⭐

### 3. Style Transfer Video
**Use**: Apply artistic styles to motion  
**Workflow**: `lora_i2v.json`  
**Time**: 3-4 minutes  
**Complexity**: ⭐⭐

### 4. Multi-LoRA Combinations
**Use**: Complex style mixing  
**Workflow**: `advanced_variations.json`  
**Time**: 5-7 minutes  
**Complexity**: ⭐⭐⭐⭐

### 5. Long-form Video
**Use**: Extended sequences  
**Method**: Chain multiple generations  
**Time**: 10-20 minutes  
**Complexity**: ⭐⭐⭐⭐

### 6. Batch Processing
**Use**: Process multiple images  
**Method**: Script automation  
**Time**: Varies  
**Complexity**: ⭐⭐⭐

## 🛠️ Troubleshooting

### Common Issues

<details>
<summary><b>CUDA Out of Memory</b></summary>

**Solutions**:
- Reduce resolution to 480p or 720p
- Enable CPU offload in config
- Lower frame count
- Enable attention slicing
- Close other GPU applications
- Use lower precision (fp16)

```yaml
# In default_config.yaml
memory:
  enable_attention_slicing: true
  enable_vae_slicing: true
  enable_cpu_offload: true
```
</details>

<details>
<summary><b>Workflow Loading Errors</b></summary>

**Solutions**:
- Verify JSON syntax is valid
- Check all required nodes are installed
- Update ComfyUI to latest version
- Install missing custom nodes
- Check ComfyUI console for specific errors

```bash
# Validate workflow
python scripts/workflow_loader.py --validate basic_i2v.json
```
</details>

<details>
<summary><b>Model Download Issues</b></summary>

**Solutions**:
- Check internet connection
- Use VPN if region-blocked
- Download manually from HuggingFace
- Verify disk space available
- Check file permissions

```bash
# Manual download with wget
wget -c https://huggingface.co/.../model.safetensors
```
</details>

<details>
<summary><b>Quality Problems</b></summary>

**Blurry output**:
- Increase steps to 30-35
- Raise CFG scale to 7-8
- Use higher quality input image
- Check model versions

**Inconsistent motion**:
- Increase steps
- Use karras scheduler
- Adjust CFG scale
- Simplify prompt

**Character morphing**:
- Increase character LoRA strength
- Use character_consistent.json workflow
- Add IPAdapter for better consistency
- Increase CFG scale
</details>

<details>
<summary><b>Speed Optimization</b></summary>

**Fast preview**:
```yaml
steps: 15
resolution: 480p
frames: 48
```

**Balanced**:
```yaml
steps: 25
resolution: 720p
frames: 96
```

**Use TensorRT** (if available):
- Compile models for faster inference
- 2-3x speed improvement
- Requires initial compilation time
</details>

## 🚀 Advanced Usage

### Custom Workflow Creation

Create your own workflows by:
1. Opening ComfyUI workflow editor
2. Adding/connecting nodes
3. Saving as JSON
4. Testing with `workflow_loader.py`

### API Integration

Use workflows programmatically:

```python
import json
import requests

# Load workflow
with open('workflows/basic_i2v.json') as f:
    workflow = json.load(f)

# Modify parameters
workflow['nodes'][6]['widgets_values'][0] = 12345  # seed

# Submit to ComfyUI API
response = requests.post(
    'http://localhost:8188/prompt',
    json={'prompt': workflow}
)
```

### Batch Processing Scripts

Process multiple images:

```python
# Example batch script
from pathlib import Path

input_dir = Path('inputs/')
for image in input_dir.glob('*.png'):
    # Load workflow
    # Set image path
    # Generate video
    # Save with unique name
```

### Parameter Optimization

Find optimal settings for your use case:

```python
# Grid search example
for steps in [20, 25, 30, 35]:
    for cfg in [5.5, 6.0, 6.5, 7.0]:
        generate(steps=steps, cfg=cfg)
        evaluate_quality()
```

## 📊 Examples

### Example Outputs

*Note: Add your generated examples here*

| Input | Style | Output | Description |
|-------|-------|--------|-------------|
| Portrait | Anime | video.mp4 | Character walk cycle |
| Landscape | Cinematic | video.mp4 | Camera pan |
| Character | Realistic | video.mp4 | Natural motion |

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Workflow Submissions

1. Create and test your workflow
2. Document parameters and use cases
3. Submit via pull request
4. Include example outputs

### Code Contributions

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

### Bug Reports

Use GitHub Issues with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- System specifications
- Relevant logs

### LoRA Sharing

Share your trained LoRAs:
- Include training parameters
- Provide example outputs
- Document recommended strength values
- License information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits & References

### Core Technologies

- **[HunyuanVideo](https://github.com/Tencent/HunyuanVideo)**: Tencent's video generation model
- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)**: Node-based interface by comfyanonymous
- **[LoRA](https://github.com/microsoft/LoRA)**: Low-Rank Adaptation by Microsoft

### Inspiration & Related Projects

- Stable Diffusion video generation techniques
- AnimateDiff for video diffusion
- ControlNet for conditional generation
- IP-Adapter for image conditioning

### Community

- ComfyUI Discord community
- HunyuanVideo developers
- Open-source AI art community

## 📞 Support

- **Documentation**: Check [examples/](examples/) directory
- **Issues**: [GitHub Issues](https://github.com/dopamin3fiends/neural-motion-lab/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dopamin3fiends/neural-motion-lab/discussions)

## 🗺️ Roadmap

- [ ] Additional workflow templates
- [ ] Web UI for easy configuration
- [ ] More LoRA presets
- [ ] Video-to-video workflows
- [ ] Long video generation pipelines
- [ ] Real-time preview
- [ ] Cloud deployment guides
- [ ] Mobile device support

## ⚡ Quick Links

- [Installation Guide](#-installation)
- [Quick Start](#-quick-start)
- [Basic Usage Tutorial](examples/basic_usage.md)
- [Character Animation Guide](examples/character_animation.md)
- [Style Transfer Guide](examples/style_transfer.md)
- [Configuration Reference](#-configuration)
- [Troubleshooting](#-troubleshooting)

---

**Made with ❤️ by the Neural Motion Lab community**

*Transform your images into dynamic stories*
