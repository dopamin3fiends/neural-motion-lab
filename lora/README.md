# LoRA Directory

This directory contains trained LoRA (Low-Rank Adaptation) models for character and style consistency.

## Organization

Organize your LoRA files by category:

```
lora/
├── characters/
│   ├── character_a.safetensors
│   └── character_b.safetensors
├── styles/
│   ├── anime_style.safetensors
│   └── realistic_style.safetensors
└── experimental/
    └── test_lora.safetensors
```

## Naming Conventions

Use descriptive names for your LoRA files:
- **Character LoRAs**: `character_[name]_v[version].safetensors`
- **Style LoRAs**: `style_[name]_v[version].safetensors`
- **Experimental**: `exp_[description]_[date].safetensors`

Examples:
- `character_alice_v1.safetensors`
- `style_anime_2d_v2.safetensors`
- `exp_motion_test_20250101.safetensors`

## File Formats

Supported formats:
- `.safetensors` (recommended - safer and faster)
- `.pt` or `.pth` (PyTorch format)

## Training Your Own LoRA

To train a custom LoRA:

```bash
python scripts/train_lora.py \
    --dataset data/training \
    --output lora/my_character \
    --epochs 10
```

See `docs/TRAINING_LORA.md` for detailed training guide.

## Using LoRA in Generation

Specify LoRA in generation:

```bash
python scripts/batch_generate.py \
    --input assets/examples/input_images \
    --lora lora/character_alice_v1.safetensors \
    --lora-scale 0.8
```

Multiple LoRAs can be combined:

```bash
python scripts/batch_generate.py \
    --input my_image.png \
    --lora lora/character_alice_v1.safetensors \
    --lora lora/style_anime_2d_v2.safetensors
```

## LoRA Weight Scale

- **0.0**: No effect (disabled)
- **0.5**: Subtle influence
- **0.8**: Balanced (recommended)
- **1.0**: Strong influence
- **1.2+**: Very strong (may cause artifacts)

## Validation

Validate LoRA files:

```bash
python scripts/validate_lora.py lora/
```

## Sharing LoRA

When sharing trained LoRAs:
1. Use `.safetensors` format
2. Include training parameters in filename or metadata
3. Document the training dataset (without sharing copyrighted material)
4. Specify recommended weight scale

## Notes

- LoRA files are excluded from git via `.gitignore`
- Typical LoRA size: 10-200 MB
- Store backups of important LoRAs
- Test LoRAs with validation script before use
