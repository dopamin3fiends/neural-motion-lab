"""
Main video generation pipeline.
"""

from typing import Dict, Any, Optional, List
import numpy as np

from neural_motion_lab.models import LoRAModel, HunyuanModel


class VideoPipeline:
    """
    Main pipeline for character-consistent video generation.
    
    This pipeline integrates LoRA and HunyuanVideo-I2V models to generate
    character-consistent videos from input images and prompts.
    """
    
    def __init__(
        self,
        hunyuan_model_path: str,
        lora_model_path: Optional[str] = None,
        device: str = "cuda"
    ):
        """
        Initialize the video generation pipeline.
        
        Args:
            hunyuan_model_path: Path to HunyuanVideo model
            lora_model_path: Optional path to LoRA model for character consistency
            device: Device to run models on (cuda/cpu)
        """
        self.hunyuan_model = HunyuanModel(hunyuan_model_path, device)
        self.lora_model = None
        
        if lora_model_path:
            self.lora_model = LoRAModel(lora_model_path)
            
        self.device = device
        
    def setup(self) -> None:
        """Load and setup all models in the pipeline."""
        print("Setting up video generation pipeline...")
        self.hunyuan_model.load()
        
        if self.lora_model:
            self.lora_model.load()
            self.hunyuan_model.set_lora(self.lora_model)
            
        print("Pipeline setup complete!")
        
    def generate_video(
        self,
        input_image: np.ndarray,
        prompt: str,
        num_frames: int = 16,
        fps: int = 8,
        seed: Optional[int] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Generate a character-consistent video.
        
        Args:
            input_image: Input image array
            prompt: Text prompt for video generation
            num_frames: Number of frames to generate
            fps: Frames per second
            seed: Random seed for reproducibility
            **kwargs: Additional generation parameters
            
        Returns:
            Generated video as numpy array
        """
        if seed is not None:
            np.random.seed(seed)
            
        print(f"Generating video with prompt: '{prompt}'")
        video = self.hunyuan_model.generate(
            input_image=input_image,
            prompt=prompt,
            num_frames=num_frames,
            fps=fps,
            **kwargs
        )
        
        return video
        
    def batch_generate(
        self,
        input_images: List[np.ndarray],
        prompts: List[str],
        **kwargs
    ) -> List[np.ndarray]:
        """
        Generate multiple videos in batch.
        
        Args:
            input_images: List of input images
            prompts: List of text prompts
            **kwargs: Additional generation parameters
            
        Returns:
            List of generated videos
        """
        videos = []
        for img, prompt in zip(input_images, prompts):
            video = self.generate_video(img, prompt, **kwargs)
            videos.append(video)
            
        return videos
