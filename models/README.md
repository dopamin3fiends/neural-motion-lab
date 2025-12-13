# Models Directory

This directory contains the base models required for Neural Motion Lab.

## Required Models

### 1. HunyuanVideo-I2V
- **Model ID**: `tencent/HunyuanVideo`
- **Size**: ~20 GB
- **Purpose**: Base video generation model
- **Download**: Run `python scripts/download_models.py --model hunyuan`

### 2. VAE (Variational Autoencoder)
- **Model ID**: `stabilityai/sd-vae-ft-mse`
- **Size**: ~1 GB
- **Purpose**: Encoding/decoding images and video frames
- **Download**: Run `python scripts/download_models.py --model vae`

### 3. Text Encoder
- **Model ID**: `openai/clip-vit-large-patch14`
- **Size**: ~1 GB
- **Purpose**: Text prompt encoding
- **Download**: Run `python scripts/download_models.py --model text_encoder`

## Directory Structure

After downloading, your directory should look like:

```
models/
├── hunyuan_video/
│   ├── config.json
│   ├── model_index.json
│   └── ... (model files)
├── vae/
│   └── ... (VAE files)
└── text_encoder/
    └── ... (encoder files)
```

## Automatic Download

To download all models at once:

```bash
python scripts/download_models.py --model all
```

## Manual Download

You can also manually download models from HuggingFace:
- Visit https://huggingface.co/
- Search for the model ID
- Download and extract to appropriate subdirectory

## Storage Requirements

- Minimum: ~25 GB for all models
- Recommended: 30 GB+ with extra space for checkpoints

## Notes

- Models are cached in `.cache/` by default
- Large files are excluded from git via `.gitignore`
- See `config/model_paths.yaml` to customize paths
