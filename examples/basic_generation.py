"""
Basic video generation example.
"""

from neural_motion_lab import VideoPipeline
from neural_motion_lab.utils import setup_logger
from PIL import Image
import numpy as np
import imageio

# Setup logger
logger = setup_logger("example")

# Initialize pipeline
logger.info("Initializing video generation pipeline...")
pipeline = VideoPipeline(
    hunyuan_model_path="models/hunyuan",
    lora_model_path="models/lora/character1",
    device="cuda"
)

# Setup models
logger.info("Loading models...")
pipeline.setup()

# Load input image
logger.info("Loading input image...")
image = Image.open("examples/sample_image.jpg")
image_array = np.array(image)

# Generate video
logger.info("Generating video...")
video = pipeline.generate_video(
    input_image=image_array,
    prompt="A person walking forward, smooth motion, cinematic lighting",
    num_frames=16,
    fps=8,
    seed=42
)

# Save video
output_path = "outputs/videos/example_output.mp4"
logger.info(f"Saving video to {output_path}...")
imageio.mimsave(output_path, video, fps=8)

logger.info("Done!")
