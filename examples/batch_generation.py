"""
Batch video generation example.
"""

from neural_motion_lab import VideoPipeline
from neural_motion_lab.utils import setup_logger, ensure_dir
from pathlib import Path
from PIL import Image
import numpy as np
import imageio

# Setup logger
logger = setup_logger("batch_example")

# Initialize pipeline
logger.info("Initializing pipeline...")
pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan",
    lora_model_path="models/lora/character1",
    device="cuda"
)
pipeline.setup()

# Load images and prompts
input_dir = Path("examples/batch_inputs")
prompts = [
    "A person walking forward",
    "A person turning around",
    "A person waving hello",
]

images = []
for img_file in input_dir.glob("*.jpg"):
    img = Image.open(img_file)
    images.append(np.array(img))

# Generate videos
logger.info(f"Generating {len(images)} videos...")
videos = pipeline.batch_generate(
    input_images=images,
    prompts=prompts,
    num_frames=16,
    fps=8
)

# Save videos
output_dir = ensure_dir("outputs/videos/batch")
for i, video in enumerate(videos):
    output_path = output_dir / f"video_{i:03d}.mp4"
    logger.info(f"Saving video {i+1}/{len(videos)} to {output_path}...")
    imageio.mimsave(str(output_path), video, fps=8)

logger.info("Batch generation complete!")
