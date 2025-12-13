# Neural Motion Lab

[![CI](https://github.com/dopamin3fiends/neural-motion-lab/workflows/CI/badge.svg)](https://github.com/dopamin3fiends/neural-motion-lab/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Modular pipeline integrating LoRA with HunyuanVideo-I2V for character-consistent AI video generation via ComfyUI.

## 🎯 Features

- **Character-Consistent Video Generation**: Maintain character consistency across generated videos using LoRA
- **HunyuanVideo-I2V Integration**: Leverage powerful image-to-video generation
- **ComfyUI Compatible**: Seamless integration with ComfyUI workflows
- **Modular Architecture**: Easy to extend and customize
- **Batch Processing**: Generate multiple videos efficiently
- **Comprehensive Documentation**: Detailed guides and examples

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Quick Setup

```bash
git clone https://github.com/dopamin3fiends/neural-motion-lab.git
cd neural-motion-lab
bash scripts/install/quick_setup.sh
```

This will create a virtual environment and install all dependencies.

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Docker Installation

```bash
# Build and run with docker-compose
docker-compose up -d neural-motion-lab

# Or build manually
docker build -t neural-motion-lab .
docker run --gpus all -it neural-motion-lab
```

For detailed installation instructions, see [Installation Guide](docs/installation/installation.md).

## ⚡ Quick Start

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
pipeline.setup()

# Load input image
image = np.array(Image.open("input.jpg"))

# Generate video
video = pipeline.generate_video(
    input_image=image,
    prompt="A person walking in a park, cinematic",
    num_frames=16,
    fps=8
)

# Save video
import imageio
imageio.mimsave("output.mp4", video, fps=8)
```

## 📖 Usage

### Command Line

```bash
# Generate a single video
python -m neural_motion_lab.cli generate \
    --image input.jpg \
    --prompt "A person walking" \
    --output output.mp4

# Batch processing
python -m neural_motion_lab.cli batch \
    --input-dir images/ \
    --prompts-file prompts.txt \
    --output-dir videos/
```

### Configuration File

Create `config.yaml`:

```yaml
pipeline:
  hunyuan_model_path: "models/hunyuan"
  lora_model_path: "models/lora/character1"
  device: "cuda"

generation:
  num_frames: 16
  fps: 8
  guidance_scale: 7.5
```

Use it in your code:

```python
from neural_motion_lab.utils import load_config
config = load_config("config.yaml")
pipeline = VideoPipeline(**config['pipeline'])
```

### ComfyUI Integration

```bash
# Setup ComfyUI
bash scripts/setup/setup_comfyui.sh

# Start ComfyUI
cd comfyui
python main.py
```

Access at http://127.0.0.1:8188

## 📚 Documentation

- [Installation Guide](docs/installation/installation.md)
- [Model Setup](docs/installation/models.md)
- [Basic Usage](docs/usage/basic.md)
- [API Reference](docs/api/overview.md)

## 💡 Examples

Check out the [examples](examples/) directory for:

- [Basic Generation](examples/basic_generation.py)
- [Batch Processing](examples/batch_generation.py)
- [Using Config Files](examples/with_config.py)
- [ComfyUI Integration](examples/comfyui_integration.py)

## 🏗️ Project Structure

```
neural-motion-lab/
├── src/neural_motion_lab/    # Main package
│   ├── models/                # Model implementations
│   ├── pipelines/             # Pipeline implementations
│   └── utils/                 # Utility functions
├── scripts/                   # Installation and setup scripts
│   ├── install/               # Installation scripts
│   ├── setup/                 # Setup scripts
│   └── data/                  # Data processing scripts
├── configs/                   # Configuration files
│   ├── pipeline.yaml          # Pipeline configuration
│   └── comfyui/               # ComfyUI workflows
├── docs/                      # Documentation
│   ├── installation/          # Installation guides
│   ├── usage/                 # Usage guides
│   └── api/                   # API documentation
├── examples/                  # Example scripts
├── tests/                     # Tests
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
└── .github/workflows/         # CI/CD workflows
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=neural_motion_lab --cov-report=html
```

### Linting

```bash
# Format code
black src/ tests/

# Run linters
flake8 src/ tests/
mypy src/
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [HunyuanVideo](https://github.com/Tencent/HunyuanVideo) for the base video generation model
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) for the UI framework
- The open-source AI community

## 📧 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/dopamin3fiends/neural-motion-lab/issues)
- Discussions: [Ask questions and share ideas](https://github.com/dopamin3fiends/neural-motion-lab/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ by the Neural Motion Lab Team
