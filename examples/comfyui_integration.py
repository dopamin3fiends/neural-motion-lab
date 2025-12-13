"""
ComfyUI integration example.
"""

from neural_motion_lab.pipelines import ComfyUIPipeline
from neural_motion_lab.utils import setup_logger

# Setup logger
logger = setup_logger("comfyui_example")

# Initialize ComfyUI pipeline
logger.info("Initializing ComfyUI pipeline...")
pipeline = ComfyUIPipeline()

# Load workflow
logger.info("Loading workflow...")
workflow = pipeline.load_workflow("configs/comfyui/i2v_workflow.json")

# Update workflow parameters
logger.info("Updating workflow parameters...")
pipeline.update_workflow_params({
    "nodes": {
        "1": {
            "inputs": {
                "image_path": "examples/sample_image.jpg"
            }
        },
        "5": {
            "inputs": {
                "text": "A person walking in a beautiful garden"
            }
        },
        "7": {
            "inputs": {
                "output_path": "outputs/videos/comfyui_output.mp4"
            }
        }
    }
})

# Save modified workflow
logger.info("Saving modified workflow...")
pipeline.save_workflow("outputs/modified_workflow.json")

# Execute on ComfyUI server
logger.info("Executing workflow on ComfyUI server...")
result = pipeline.execute(server_url="http://127.0.0.1:8188")

logger.info(f"Workflow execution result: {result}")
