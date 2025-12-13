# API Reference

Complete API documentation for Neural Motion Lab scripts and utilities.

## Scripts

### setup_environment.py

Environment setup and validation script.

**Usage:**
```bash
python scripts/setup_environment.py
```

**Functions:**

#### `check_python_version() -> bool`
Checks if Python version is 3.10+.

**Returns:** `True` if version is compatible

#### `check_cuda() -> bool`
Checks CUDA availability and displays GPU information.

**Returns:** `True` if CUDA is available

#### `create_directories() -> None`
Creates all required project directories.

#### `check_dependencies() -> bool`
Verifies all required packages are installed.

**Returns:** `True` if all dependencies are installed

#### `install_requirements() -> bool`
Installs packages from requirements.txt.

**Returns:** `True` if installation successful

---

### download_models.py

Automated model download script.

**Usage:**
```bash
python scripts/download_models.py [--model MODEL] [--force] [--config CONFIG]
```

**Arguments:**
- `--model`: Which model to download (all, hunyuan, vae, text_encoder)
- `--force`: Force re-download even if exists
- `--config`: Path to custom config file

**Functions:**

#### `download_hunyuan_video(manager, config, force=False) -> None`
Downloads HunyuanVideo model.

**Args:**
- `manager`: ModelManager instance
- `config`: Configuration dictionary
- `force`: Force re-download

#### `download_vae(manager, config, force=False) -> None`
Downloads VAE model.

#### `download_text_encoder(manager, config, force=False) -> None`
Downloads text encoder model.

#### `check_existing_models(config) -> dict`
Checks which models are already downloaded.

**Returns:** Dictionary with model status

---

### train_lora.py

LoRA training script.

**Usage:**
```bash
python scripts/train_lora.py \
    --dataset DIR \
    --output DIR \
    [--epochs N] \
    [--batch-size N] \
    [--learning-rate F]
```

**Arguments:**
- `--dataset`: Training dataset directory
- `--output`: Output directory for trained LoRA
- `--epochs`: Number of training epochs
- `--batch-size`: Batch size per device
- `--learning-rate`: Learning rate

**Classes:**

#### `LoRATrainer`

##### `__init__(config: dict)`
Initialize LoRA trainer.

**Args:**
- `config`: Training configuration dictionary

##### `prepare_model() -> None`
Prepares base model for LoRA training.

##### `prepare_dataset() -> int`
Prepares training dataset.

**Returns:** Number of images in dataset

##### `train() -> None`
Executes training loop.

##### `validate() -> None`
Runs validation if enabled.

---

### batch_generate.py

Batch video generation script.

**Usage:**
```bash
python scripts/batch_generate.py \
    --input PATH \
    --output DIR \
    [--lora PATH] \
    [--lora-scale FLOAT] \
    [--prompt TEXT] \
    [--num-frames N]
```

**Arguments:**
- `--input`: Input image or directory
- `--output`: Output directory
- `--lora`: Path to LoRA file(s) (can specify multiple)
- `--lora-scale`: LoRA weight scale (0.0-1.5)
- `--prompt`: Positive prompt
- `--negative-prompt`: Negative prompt
- `--num-frames`: Number of frames
- `--fps`: Output FPS

**Classes:**

#### `BatchGenerator`

##### `__init__(config: dict)`
Initialize batch generator.

**Args:**
- `config`: Generation configuration

##### `load_models() -> None`
Loads required models.

##### `get_input_images(input_dir: Path) -> List[Path]`
Gets list of input images from directory.

**Returns:** List of image paths

##### `generate_video(input_image: Path, output_path: Path) -> bool`
Generates video from input image.

**Returns:** `True` if successful

##### `batch_generate(input_dir: Path, output_dir: Path) -> None`
Generates videos for all images in directory.

---

### validate_lora.py

LoRA validation script.

**Usage:**
```bash
python scripts/validate_lora.py PATH [--recursive]
```

**Arguments:**
- `PATH`: Path to LoRA file or directory
- `--recursive`: Recursively validate all LoRA files

**Classes:**

#### `LoRAValidator`

##### `__init__(lora_path: Path)`
Initialize LoRA validator.

**Args:**
- `lora_path`: Path to LoRA checkpoint

##### `check_file_format() -> bool`
Checks if LoRA file format is valid.

**Returns:** `True` if format is valid

##### `check_file_size() -> bool`
Checks LoRA file size.

**Returns:** `True` if size is reasonable

##### `load_checkpoint() -> dict`
Loads and inspects LoRA checkpoint.

**Returns:** Checkpoint dictionary

##### `inspect_checkpoint(checkpoint: dict) -> None`
Inspects checkpoint contents.

##### `validate_rank(checkpoint: dict) -> None`
Validates LoRA rank from checkpoint.

##### `test_loading() -> bool`
Tests if LoRA can be loaded properly.

**Returns:** `True` if validation passes

**Functions:**

#### `validate_lora(lora_path: Path) -> bool`
Validates a LoRA checkpoint.

**Returns:** `True` if valid

---

## Utilities

### config_loader.py

Configuration management utilities.

**Classes:**

#### `ConfigLoader`

##### `__init__(config_dir: Optional[Path] = None)`
Initialize ConfigLoader.

**Args:**
- `config_dir`: Directory containing config files

##### `load(config_name: str) -> Dict[str, Any]`
Loads a configuration file.

**Args:**
- `config_name`: Name of config file

**Returns:** Configuration dictionary

**Raises:** `FileNotFoundError` if config doesn't exist

##### `load_all() -> Dict[str, Dict[str, Any]]`
Loads all configuration files.

**Returns:** Dictionary mapping config names to contents

##### `merge_configs(*configs) -> Dict[str, Any]`
Merges multiple configuration dictionaries.

**Args:**
- `*configs`: Variable number of config dictionaries

**Returns:** Merged configuration

##### `save(config: dict, config_name: str) -> None`
Saves configuration to YAML file.

**Args:**
- `config`: Configuration to save
- `config_name`: Output filename

##### `validate_config(config: dict, required_keys: list) -> bool`
Validates required keys exist.

**Args:**
- `config`: Configuration dictionary
- `required_keys`: List of required key paths

**Returns:** `True` if all keys exist

##### `get_nested(config: dict, key_path: str, default: Any = None) -> Any`
Gets nested value using dot notation.

**Args:**
- `config`: Configuration dictionary
- `key_path`: Dot-separated key path
- `default`: Default value if not found

**Returns:** Configuration value or default

**Example:**
```python
from scripts.utils.config_loader import ConfigLoader

loader = ConfigLoader()
config = loader.load('generation_config')

# Get nested value
fps = loader.get_nested(config, 'generation.fps', default=24)

# Merge configs
base = loader.load('generation_config')
override = {'generation': {'fps': 30}}
merged = loader.merge_configs(base, override)

# Validate
required = ['generation.fps', 'model.device']
valid = loader.validate_config(merged, required)
```

**Functions:**

#### `load_config(config_name: str, config_dir: Optional[Path] = None) -> dict`
Convenience function to load a configuration.

**Args:**
- `config_name`: Name of config file
- `config_dir`: Optional config directory

**Returns:** Configuration dictionary

---

### model_manager.py

Model loading and management utilities.

**Classes:**

#### `ModelManager`

##### `__init__(device: Optional[str] = None, cache_dir: Optional[Path] = None, offload_to_cpu: bool = False)`
Initialize ModelManager.

**Args:**
- `device`: Device for models ('cuda', 'cpu')
- `cache_dir`: Model cache directory
- `offload_to_cpu`: Enable CPU offloading

##### `download_model(model_id: str, local_dir: Optional[Path] = None, force_download: bool = False, token: Optional[str] = None) -> Path`
Downloads model from HuggingFace Hub.

**Args:**
- `model_id`: HuggingFace model ID
- `local_dir`: Local directory to save
- `force_download`: Force re-download
- `token`: HuggingFace API token

**Returns:** Path to downloaded model

##### `load_model(model_path: Path, model_name: Optional[str] = None, **kwargs) -> Any`
Loads a model from path.

**Args:**
- `model_path`: Path to model checkpoint
- `model_name`: Optional name to cache
- `**kwargs`: Additional loading arguments

**Returns:** Loaded model

##### `unload_model(model_name: str) -> None`
Unloads a cached model from memory.

##### `unload_all() -> None`
Unloads all cached models.

##### `clear_memory() -> None`
Clears GPU/CPU memory.

##### `get_memory_info() -> Dict[str, float]`
Gets current memory usage.

**Returns:** Dictionary with memory statistics (GB)

##### `move_to_device(model: Any, device: Optional[str] = None) -> Any`
Moves model to specified device.

**Args:**
- `model`: Model to move
- `device`: Target device

**Returns:** Model on target device

##### `enable_memory_efficient_attention(model: Any) -> Any`
Enables xFormers memory efficient attention.

**Args:**
- `model`: Model to optimize

**Returns:** Optimized model

##### `set_precision(model: Any, precision: str = "fp16") -> Any`
Sets model precision.

**Args:**
- `model`: Model to convert
- `precision`: Target precision ('fp32', 'fp16', 'bf16')

**Returns:** Converted model

**Example:**
```python
from scripts.utils.model_manager import ModelManager

# Initialize
manager = ModelManager(device='cuda')

# Download model
model_path = manager.download_model('tencent/HunyuanVideo')

# Load model
model = manager.load_model(model_path, model_name='hunyuan')

# Optimize
model = manager.enable_memory_efficient_attention(model)
model = manager.set_precision(model, 'fp16')

# Check memory
info = manager.get_memory_info()
print(f"VRAM used: {info['allocated']:.2f} GB")

# Cleanup
manager.unload_all()
manager.clear_memory()
```

---

### video_processor.py

Video processing utilities.

**Classes:**

#### `VideoProcessor`

##### `__init__(output_dir: Optional[Path] = None)`
Initialize VideoProcessor.

**Args:**
- `output_dir`: Default output directory

##### `save_video(frames: Union[List[np.ndarray], np.ndarray], output_path: Path, fps: int = 24, codec: str = 'mp4v', quality: int = 9) -> Path`
Saves frames as video file.

**Args:**
- `frames`: List of frames or 4D array
- `output_path`: Output video path
- `fps`: Frames per second
- `codec`: Video codec
- `quality`: Quality level (0-10)

**Returns:** Path to saved video

##### `save_frames(frames: Union[List, np.ndarray], output_dir: Path, prefix: str = "frame", format: str = "png") -> List[Path]`
Saves individual frames as images.

**Args:**
- `frames`: List of frames
- `output_dir`: Output directory
- `prefix`: Filename prefix
- `format`: Image format

**Returns:** List of saved frame paths

##### `load_video(video_path: Path, max_frames: Optional[int] = None) -> Tuple[List[np.ndarray], int]`
Loads video file as frames.

**Args:**
- `video_path`: Path to video file
- `max_frames`: Maximum frames to load

**Returns:** Tuple of (frames list, fps)

##### `load_image(image_path: Path) -> np.ndarray`
Loads image file.

**Args:**
- `image_path`: Path to image

**Returns:** Image as numpy array (RGB)

##### `resize_frames(frames: List[np.ndarray], size: Tuple[int, int], interpolation: int = cv2.INTER_LANCZOS4) -> List[np.ndarray]`
Resizes frames to target size.

**Args:**
- `frames`: List of frames
- `size`: Target size (width, height)
- `interpolation`: Interpolation method

**Returns:** List of resized frames

##### `concatenate_videos(video_paths: List[Path], output_path: Path, fps: Optional[int] = None) -> Path`
Concatenates multiple videos.

**Args:**
- `video_paths`: List of video paths
- `output_path`: Output path
- `fps`: Output FPS

**Returns:** Path to concatenated video

##### `apply_color_correction(frames: List[np.ndarray], brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0) -> List[np.ndarray]`
Applies color correction to frames.

**Args:**
- `frames`: List of frames
- `brightness`: Brightness multiplier
- `contrast`: Contrast multiplier
- `saturation`: Saturation multiplier

**Returns:** List of corrected frames

**Example:**
```python
from scripts.utils.video_processor import VideoProcessor
import numpy as np

# Initialize
processor = VideoProcessor(output_dir='outputs')

# Load image
image = processor.load_image('input.png')

# Generate frames (dummy example)
frames = [image] * 49

# Save video
output_path = processor.save_video(
    frames,
    'outputs/video.mp4',
    fps=24,
    codec='mp4v'
)

# Save individual frames
frame_paths = processor.save_frames(
    frames,
    'outputs/frames',
    prefix='frame',
    format='png'
)

# Load and process video
loaded_frames, fps = processor.load_video('outputs/video.mp4')
resized = processor.resize_frames(loaded_frames, (768, 768))
corrected = processor.apply_color_correction(
    resized,
    brightness=1.1,
    contrast=1.05
)
```

---

## Configuration Schema

### generation_config.yaml

```yaml
model:
  name: str              # Model name
  precision: str         # fp32, fp16, bf16
  device: str           # cuda, cpu

generation:
  num_frames: int       # Number of frames
  fps: int              # Frames per second
  width: int            # Video width
  height: int           # Video height
  num_inference_steps: int
  guidance_scale: float
  scheduler: str
  lora_scale: float
  lora_paths: list

optimization:
  enable_xformers: bool
  enable_vae_tiling: bool
  vae_batch_size: int
```

### training_config.yaml

```yaml
lora:
  rank: int
  alpha: int
  dropout: float
  target_modules: list

training:
  output_dir: str
  num_epochs: int
  batch_size: int
  learning_rate: float
  
data:
  dataset_dir: str
  resolution: int
```

### model_paths.yaml

```yaml
base_model:
  hunyuan_video:
    huggingface_id: str
    local_path: str
  
lora:
  custom_dir: str
  
outputs:
  generated_videos: str
```

---

## Error Handling

All scripts raise appropriate exceptions:

- `FileNotFoundError`: File/directory not found
- `ValueError`: Invalid parameter value
- `RuntimeError`: CUDA/model errors
- `yaml.YAMLError`: Configuration parse errors

Use try-except blocks when calling scripts programmatically.

---

## Type Hints

All utilities use Python type hints:

```python
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import numpy as np
```

---

## Logging

All scripts use Python logging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Log levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages

---

## Examples

See individual script docstrings and `docs/QUICKSTART.md` for usage examples.

---

## Contributing

When adding new functions:
1. Add type hints
2. Write docstrings
3. Add to this reference
4. Write tests
5. Update examples

---

## Version

API Version: 0.1.0

Changes may occur in future versions.
