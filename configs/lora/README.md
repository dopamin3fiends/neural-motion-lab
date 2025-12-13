# LoRA Configuration

This directory contains configuration files for LoRA models.

## Configuration Files

Place your LoRA configuration files (*.yaml, *.json) in this directory.

## Example Configuration

```yaml
# lora_config.yaml
lora:
  enabled: true
  model_path: "models/lora/character1"
  scale: 0.8
  rank: 4
  alpha: 8
```

Or in JSON format:

```json
{
  "lora": {
    "enabled": true,
    "model_path": "models/lora/character1",
    "scale": 0.8,
    "rank": 4,
    "alpha": 8
  }
}
```

## Parameters

- **enabled**: Whether to use LoRA
- **model_path**: Path to LoRA model weights
- **scale**: LoRA weight scale (0.0-1.0)
- **rank**: LoRA rank
- **alpha**: LoRA alpha value

## Usage

These configs can be loaded using the pipeline configuration system.

For more information, see the [Model Setup Guide](../../docs/installation/models.md).

