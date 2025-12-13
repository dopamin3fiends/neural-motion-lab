# LoRA Models

Place your LoRA model files in this directory.

## Directory Structure

```
lora/
├── character1/
│   ├── lora_weights.safetensors
│   └── config.json
├── character2/
│   └── lora_weights.safetensors
└── ...
```

## Supported Formats

- `.safetensors` (recommended)
- `.ckpt`
- `.pth`

## Usage

Specify the LoRA model path in your configuration:

```yaml
pipeline:
  lora_model_path: "models/lora/character1"
```

Or in code:

```python
from neural_motion_lab import VideoPipeline

pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan",
    lora_model_path="models/lora/character1"
)
```

For more information, see the [Model Setup Guide](../../docs/installation/models.md).
