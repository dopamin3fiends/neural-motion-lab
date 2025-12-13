"""
Example using configuration file.
"""

from neural_motion_lab import VideoPipeline
from neural_motion_lab.utils import load_config, setup_logger
from PIL import Image
import numpy as np
import imageio

# Setup logger
logger = setup_logger("config_example")

# Load configuration
logger.info("Loading configuration...")
config = load_config("configs/pipeline.yaml")

# Initialize pipeline from config
logger.info("Initializing pipeline...")
pipeline = VideoPipeline(
    hunyuan_model_path=config['pipeline']['hunyuan_model_path'],
    lora_model_path=config['pipeline']['lora_model_path'],
    device=config['pipeline']['device']
)
pipeline.setup()

# Load input image
image = Image.open("examples/sample_image.jpg")
image_array = np.array(image)

# Generate using config parameters
logger.info("Generating video with config parameters...")
gen_config = config['generation']
video = pipeline.generate_video(
    input_image=image_array,
    prompt="A person smiling and nodding",
    num_frames=gen_config['num_frames'],
    fps=gen_config['fps'],
    guidance_scale=gen_config['guidance_scale'],
    num_inference_steps=gen_config['num_inference_steps']
)

# Save video
output_path = f"{config['output']['output_dir']}/config_example.mp4"
imageio.mimsave(output_path, video, fps=gen_config['fps'])

logger.info(f"Video saved to {output_path}")
