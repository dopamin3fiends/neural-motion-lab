# Neural Motion Lab - Project Overview

## Purpose

Neural Motion Lab is a modular pipeline for generating character-consistent AI videos by integrating LoRA (Low-Rank Adaptation) with HunyuanVideo-I2V (Image-to-Video). The project provides both programmatic and UI-based (ComfyUI) interfaces for video generation.

## Key Components

### 1. Core Pipeline (`src/neural_motion_lab/`)

#### Models
- **LoRAModel**: Handles LoRA model loading and application for character consistency
- **HunyuanModel**: Wrapper for HunyuanVideo-I2V model
- Integration between LoRA and base model for consistent character generation

#### Pipelines
- **VideoPipeline**: Main pipeline for video generation
- **ComfyUIPipeline**: ComfyUI workflow integration
- Batch processing capabilities
- Configuration-based setup

#### Utils
- **config.py**: YAML/JSON configuration management
- **logger.py**: Logging utilities
- **file_ops.py**: File operations and downloads

### 2. Scripts (`scripts/`)

#### Installation Scripts
- `install.sh`: Full installation with dependencies
- `quick_setup.sh`: Quick setup with virtual environment

#### Setup Scripts
- `setup_models.sh`: Model directory setup
- `setup_comfyui.sh`: ComfyUI integration setup

#### Data Processing
- `preprocess.py`: Image preprocessing
- `postprocess.py`: Video postprocessing

### 3. Configuration (`configs/`)

- `pipeline.yaml`: Main pipeline configuration
- `comfyui/`: ComfyUI workflow templates
  - `i2v_workflow.json`: Single video generation
  - `batch_workflow.json`: Batch processing

### 4. Documentation (`docs/`)

- Installation guides
- Usage tutorials
- API reference
- Model setup instructions

### 5. Examples (`examples/`)

- Basic generation example
- Batch processing example
- Configuration-based example
- ComfyUI integration example

## Workflow

1. **Setup**: Install dependencies and download models
2. **Initialize**: Create pipeline with model paths
3. **Load**: Load models into memory
4. **Generate**: Create videos from images and prompts
5. **Output**: Save generated videos

## Architecture

```
Input Image + Prompt
       ↓
   LoRA Model (optional)
       ↓
   HunyuanVideo-I2V
       ↓
  Generated Video
```

## Key Features

- **Modular Design**: Easy to extend and customize
- **Multiple Interfaces**: CLI, Python API, and ComfyUI
- **Batch Processing**: Process multiple videos efficiently
- **Configuration System**: Flexible YAML/JSON configs
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and linting

## Technologies

- **Python 3.8+**
- **PyTorch**: Deep learning framework
- **HunyuanVideo**: Base video generation model
- **LoRA**: Character consistency
- **ComfyUI**: Visual workflow interface
- **GitHub Actions**: CI/CD

## Development Workflow

1. **Code Changes**: Make changes to source files
2. **Testing**: Run unit and integration tests
3. **Linting**: Check code style with Black/Flake8
4. **Documentation**: Update relevant docs
5. **Commit**: Use conventional commit messages
6. **CI/CD**: Automated checks run on push

## Future Enhancements

- Support for more video generation models
- Advanced LoRA training pipeline
- Web UI for easier access
- Cloud deployment options
- Model optimization techniques
- Advanced video editing features

## Directory Structure Reference

```
neural-motion-lab/
├── src/neural_motion_lab/    # Main package source
├── scripts/                   # Installation & utility scripts
├── configs/                   # Configuration files
├── docs/                      # Documentation
├── examples/                  # Example scripts
├── tests/                     # Test suite
├── models/                    # Model storage (gitignored)
├── outputs/                   # Generated videos (gitignored)
└── .github/workflows/         # CI/CD workflows
```

## Getting Help

- Check documentation in `docs/`
- Review examples in `examples/`
- Read API reference
- Open GitHub issue for bugs
- Use discussions for questions

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.
