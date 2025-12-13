# Examples

This directory contains example scripts demonstrating various features of Neural Motion Lab.

## Available Examples

### Basic Generation
`basic_generation.py` - Simple video generation from a single image
```bash
python examples/basic_generation.py
```

### Batch Processing
`batch_generation.py` - Generate multiple videos at once
```bash
python examples/batch_generation.py
```

### Using Configuration Files
`with_config.py` - Use YAML configuration files
```bash
python examples/with_config.py
```

### ComfyUI Integration
`comfyui_integration.py` - Integrate with ComfyUI workflows
```bash
python examples/comfyui_integration.py
```

## Requirements

Before running examples, ensure you have:

1. Installed the package: `pip install -e .`
2. Downloaded model weights to `models/` directory
3. Prepared sample input images

## Input Data

Place your test images in this directory or specify custom paths in the scripts.

## Output

Generated videos will be saved to `outputs/videos/` by default.

For more examples and tutorials, see the [Usage Guide](../docs/usage/basic.md).
