# HunyuanVideo Models

Place your HunyuanVideo model files in this directory.

## Directory Structure

```
hunyuan/
├── model.safetensors
├── config.json
└── tokenizer/
    ├── vocab.json
    └── merges.txt
```

## Download

Download the HunyuanVideo-I2V model from the official repository:

https://github.com/Tencent/HunyuanVideo

## Usage

Specify the model path in your configuration:

```yaml
pipeline:
  hunyuan_model_path: "models/hunyuan"
```

Or in code:

```python
from neural_motion_lab import VideoPipeline

pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan"
)
```

For more information, see the [Model Setup Guide](../../docs/installation/models.md).
