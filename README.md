# Neural Motion Lab

<div align="center">

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/pytorch-2.0%2B-orange)
![CUDA](https://img.shields.io/badge/CUDA-11.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

**Modular pipeline integrating LoRA with HunyuanVideo-I2V for character-consistent AI video generation**

[Quick Start](#quick-start) • [Documentation](#documentation) • [Features](#features) • [Installation](#installation) • [Usage](#usage)

</div>

---

## 🎯 Overview

Neural Motion Lab is a production-ready framework for AI-powered video generation with **character consistency** across frames. Built on HunyuanVideo-I2V and enhanced with LoRA (Low-Rank Adaptation), it enables:

- **Character-consistent video generation** from single images
- **Style transfer** via trained LoRA models
- **Modular Python scripts** for training, generation, and validation
- **ComfyUI workflows** for visual node-based control
- **Windows + RTX GPU optimization** out of the box

Perfect for creators, researchers, and enthusiasts working with AI video generation on consumer hardware.

## ✨ Features

### Core Capabilities

- 🎬 **Image-to-Video Generation**: Transform static images into smooth, animated videos
- 🎨 **LoRA Training**: Fine-tune models for specific characters, styles, or concepts
- 🔄 **Multi-LoRA Blending**: Combine character and style LoRAs for complex outputs
- 📦 **Batch Processing**: Generate videos from multiple images efficiently
- ⚙️ **ComfyUI Integration**: Visual workflow editor with pre-built templates
- 🔍 **LoRA Validation**: Test and verify LoRA checkpoints before use

### Technical Features

- **Modular Architecture**: Reusable utilities for config, models, and video processing
- **Configuration-Driven**: YAML configs for all parameters
- **Memory Optimized**: xFormers, VAE tiling, gradient checkpointing
- **Progress Tracking**: TensorBoard logging and real-time monitoring
- **Type-Safe**: Python type hints throughout
- **Tested**: Unit tests for core utilities

## 🚀 Quick Start

### Prerequisites

- **Hardware**: NVIDIA RTX GPU (12+ GB VRAM recommended)
- **OS**: Windows 10/11 64-bit
- **Software**: Python 3.10+, CUDA 11.8+

### Installation (3 commands)

```bash
# 1. Clone repository
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
python scripts/setup_environment.py
```

### Download Models

```bash
python scripts/download_models.py --model all
```

⏱️ *Takes ~15-30 minutes*

### Generate Your First Video

```bash
python scripts/batch_generate.py \
    --input your_image.png \
    --output outputs/first_video \
    --prompt "character walking forward, smooth motion" \
    --num-frames 49
```

**Done!** Check `outputs/first_video/your_image.mp4`

See [Quick Start Guide](docs/QUICKSTART.md) for detailed walkthrough.

## 📁 Project Structure

```
neural-motion-lab/
├── config/                   # Configuration files
│   ├── generation_config.yaml   # Video generation settings
│   ├── training_config.yaml     # LoRA training settings
│   └── model_paths.yaml         # Model locations
├── scripts/                  # Python scripts
│   ├── setup_environment.py     # Environment setup
│   ├── download_models.py       # Model downloader
│   ├── train_lora.py           # LoRA training
│   ├── batch_generate.py       # Video generation
│   ├── validate_lora.py        # LoRA validation
│   └── utils/                  # Utility modules
│       ├── config_loader.py       # Configuration management
│       ├── model_manager.py       # Model loading
│       └── video_processor.py     # Video processing
├── workflows/                # ComfyUI workflows
│   ├── basic_i2v_lora.json     # Basic generation
│   ├── multi_lora_blend.json   # Multi-LoRA blending
│   └── batch_generation.json   # Batch processing
├── docs/                     # Documentation
│   ├── INSTALLATION.md         # Setup guide
│   ├── QUICKSTART.md          # Getting started
│   ├── WORKFLOWS.md           # ComfyUI workflows
│   ├── TRAINING_LORA.md       # LoRA training guide
│   ├── HARDWARE_GUIDE.md      # Optimization tips
│   ├── TROUBLESHOOTING.md     # Common issues
│   └── API_REFERENCE.md       # API documentation
├── models/                   # Model storage (gitignored)
├── lora/                     # LoRA checkpoints (gitignored)
├── tests/                    # Unit tests
└── outputs/                  # Generated videos (gitignored)
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/INSTALLATION.md) | Complete setup instructions for Windows |
| [Quick Start](docs/QUICKSTART.md) | Get up and running in 5 minutes |
| [Workflows Guide](docs/WORKFLOWS.md) | ComfyUI workflow documentation |
| [Training LoRA](docs/TRAINING_LORA.md) | Complete LoRA training guide |
| [Hardware Guide](docs/HARDWARE_GUIDE.md) | Windows/RTX optimization tips |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [API Reference](docs/API_REFERENCE.md) | Script and utility API docs |

## 💻 Usage Examples

### Basic Video Generation

```bash
python scripts/batch_generate.py \
    --input character.png \
    --output outputs/basic \
    --prompt "character walking, natural motion" \
    --num-frames 49 \
    --fps 24
```

### With LoRA

```bash
python scripts/batch_generate.py \
    --input character.png \
    --lora lora/my_character.safetensors \
    --lora-scale 0.8 \
    --prompt "character in specific style" \
    --output outputs/with_lora
```

### Train Custom LoRA

```bash
python scripts/train_lora.py \
    --dataset data/training \
    --output lora/my_character_v1 \
    --epochs 10 \
    --batch-size 1 \
    --learning-rate 1e-4
```

### Batch Processing

```bash
python scripts/batch_generate.py \
    --input input_images/ \
    --output outputs/batch \
    --lora lora/style.safetensors
```

### Validate LoRA

```bash
python scripts/validate_lora.py lora/my_character.safetensors
```

## ⚙️ Configuration

Edit `config/generation_config.yaml` for default settings:

```yaml
generation:
  num_frames: 49          # Video length
  fps: 24                 # Frame rate
  width: 512              # Resolution
  height: 512
  lora_scale: 0.8         # LoRA strength
  guidance_scale: 7.5     # CFG scale
  num_inference_steps: 50 # Quality vs speed

optimization:
  enable_xformers: true   # Memory optimization
  enable_vae_tiling: false
  vae_batch_size: 8
```

See [Configuration Guide](docs/INSTALLATION.md#configuration) for all options.

## 🔧 Requirements

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | RTX 3060 (12 GB) | RTX 3090/4090 (24 GB) |
| RAM | 16 GB | 32 GB |
| Storage | 50 GB | 100 GB (SSD) |
| OS | Windows 10 | Windows 11 |

### Software

- Python 3.10 or 3.11
- CUDA 11.8 or 12.1
- PyTorch 2.0+
- See [requirements.txt](requirements.txt) for full list

## 🎓 Learning Path

1. **Start**: [Quick Start Guide](docs/QUICKSTART.md) - Basic generation
2. **Learn**: [Workflows Guide](docs/WORKFLOWS.md) - ComfyUI usage
3. **Train**: [Training LoRA](docs/TRAINING_LORA.md) - Custom models
4. **Optimize**: [Hardware Guide](docs/HARDWARE_GUIDE.md) - Performance tuning
5. **Troubleshoot**: [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## 🛠️ Technology Stack

- **Base Model**: [HunyuanVideo-I2V](https://huggingface.co/tencent/HunyuanVideo) by Tencent
- **Framework**: PyTorch 2.0+
- **Fine-tuning**: PEFT (Parameter-Efficient Fine-Tuning) with LoRA
- **Orchestration**: ComfyUI (optional)
- **Acceleration**: xFormers for memory efficiency
- **Video Processing**: OpenCV, imageio, PIL

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **HunyuanVideo**: Check [model license](https://huggingface.co/tencent/HunyuanVideo)
- **PyTorch**: BSD-style license
- **ComfyUI**: GPL-3.0 license

## 🙏 Acknowledgments

- **Tencent** for HunyuanVideo-I2V model
- **HuggingFace** for PEFT and model hosting
- **ComfyUI** team for the excellent UI framework
- **PyTorch** and **xFormers** teams
- Open-source AI community

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/dopamin3fiends/neural-motion-lab/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dopamin3fiends/neural-motion-lab/discussions)
- **Documentation**: [docs/](docs/)

## 🗺️ Roadmap

- [ ] Additional video models support
- [ ] Enhanced LoRA merging strategies
- [ ] Web UI interface
- [ ] Cloud deployment guides
- [ ] More example workflows
- [ ] Video upscaling integration

## 📊 Performance

**Generation Speed (RTX 4090):**
- 512x512, 25 frames: ~2 minutes
- 512x512, 49 frames: ~4 minutes
- 768x768, 49 frames: ~8 minutes

**Training Speed (RTX 4090):**
- 20 images, 10 epochs: ~30 minutes
- 50 images, 10 epochs: ~60 minutes

See [Hardware Guide](docs/HARDWARE_GUIDE.md) for detailed benchmarks.

## ⚠️ Disclaimer

This tool is for research and creative purposes. Users are responsible for:
- Complying with model licenses
- Respecting intellectual property rights
- Ethical use of AI-generated content
- Not generating harmful or illegal content

---

<div align="center">

**Star ⭐ this repository if you find it useful!**

Made with ❤️ for the AI video generation community

[Report Bug](https://github.com/dopamin3fiends/neural-motion-lab/issues) • [Request Feature](https://github.com/dopamin3fiends/neural-motion-lab/issues)

</div>
