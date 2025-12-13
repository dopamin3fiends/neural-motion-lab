# API Reference

## Core Classes

### VideoPipeline

Main pipeline for video generation.

```python
from neural_motion_lab import VideoPipeline
```

#### Constructor

```python
VideoPipeline(
    hunyuan_model_path: str,
    lora_model_path: Optional[str] = None,
    device: str = "cuda"
)
```

**Parameters:**
- `hunyuan_model_path` (str): Path to HunyuanVideo model
- `lora_model_path` (str, optional): Path to LoRA model
- `device` (str): Device to use ("cuda" or "cpu")

#### Methods

##### setup()

Load and initialize all models.

```python
pipeline.setup()
```

##### generate_video()

Generate a video from an input image and prompt.

```python
video = pipeline.generate_video(
    input_image: np.ndarray,
    prompt: str,
    num_frames: int = 16,
    fps: int = 8,
    seed: Optional[int] = None,
    **kwargs
) -> np.ndarray
```

**Parameters:**
- `input_image`: Input image as numpy array (H, W, C)
- `prompt`: Text prompt for generation
- `num_frames`: Number of frames to generate
- `fps`: Frames per second
- `seed`: Random seed for reproducibility
- `**kwargs`: Additional generation parameters

**Returns:**
- `np.ndarray`: Generated video (num_frames, H, W, C)

##### batch_generate()

Generate multiple videos in batch.

```python
videos = pipeline.batch_generate(
    input_images: List[np.ndarray],
    prompts: List[str],
    **kwargs
) -> List[np.ndarray]
```

### LoRAModel

LoRA model wrapper for character consistency.

```python
from neural_motion_lab.models import LoRAModel
```

#### Constructor

```python
LoRAModel(
    model_path: str,
    config: Optional[Dict[str, Any]] = None
)
```

#### Methods

##### load()

Load the LoRA model from disk.

```python
model.load()
```

##### apply()

Apply LoRA weights to a base model.

```python
modified_model = lora_model.apply(base_model)
```

### HunyuanModel

HunyuanVideo-I2V model wrapper.

```python
from neural_motion_lab.models import HunyuanModel
```

#### Constructor

```python
HunyuanModel(
    model_path: str,
    device: str = "cuda"
)
```

#### Methods

##### load()

Load the HunyuanVideo model.

```python
model.load()
```

##### generate()

Generate video from input image.

```python
video = model.generate(
    input_image: np.ndarray,
    prompt: str,
    num_frames: int = 16,
    fps: int = 8,
    **kwargs
) -> np.ndarray
```

##### set_lora()

Set LoRA model for character consistency.

```python
model.set_lora(lora_model)
```

## Utility Functions

### Configuration

```python
from neural_motion_lab.utils import load_config, save_config
```

#### load_config()

Load configuration from file.

```python
config = load_config("config.yaml")
```

#### save_config()

Save configuration to file.

```python
save_config(config, "config.yaml")
```

### Logging

```python
from neural_motion_lab.utils import setup_logger
```

#### setup_logger()

Setup a logger instance.

```python
logger = setup_logger(
    name="my_logger",
    level=logging.INFO,
    log_file="logs/app.log"
)
```

### File Operations

```python
from neural_motion_lab.utils import ensure_dir, download_file
```

#### ensure_dir()

Ensure a directory exists.

```python
path = ensure_dir("outputs/videos")
```

#### download_file()

Download a file from URL.

```python
file_path = download_file(
    url="https://example.com/model.safetensors",
    destination="models/model.safetensors",
    show_progress=True
)
```

## ComfyUI Integration

### ComfyUIPipeline

Pipeline for ComfyUI integration.

```python
from neural_motion_lab.pipelines import ComfyUIPipeline
```

#### Constructor

```python
pipeline = ComfyUIPipeline(
    workflow_path: Optional[str] = None
)
```

#### Methods

##### load_workflow()

Load a ComfyUI workflow.

```python
workflow = pipeline.load_workflow("workflow.json")
```

##### save_workflow()

Save a ComfyUI workflow.

```python
pipeline.save_workflow("output.json", workflow)
```

##### execute()

Execute workflow on ComfyUI server.

```python
result = pipeline.execute(server_url="http://127.0.0.1:8188")
```

## Examples

### Basic Video Generation

```python
from neural_motion_lab import VideoPipeline
import numpy as np
from PIL import Image

# Initialize
pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan",
    lora_model_path="models/lora/character1"
)
pipeline.setup()

# Load image
image = np.array(Image.open("input.jpg"))

# Generate
video = pipeline.generate_video(
    input_image=image,
    prompt="A person smiling",
    num_frames=16,
    fps=8
)
```

### With Configuration File

```python
from neural_motion_lab import VideoPipeline
from neural_motion_lab.utils import load_config

config = load_config("config.yaml")
pipeline = VideoPipeline(**config['pipeline'])
pipeline.setup()
```

### Custom Logger

```python
from neural_motion_lab.utils import setup_logger
import logging

logger = setup_logger(
    name="video_gen",
    level=logging.DEBUG,
    log_file="logs/generation.log"
)

logger.info("Starting video generation")
```
