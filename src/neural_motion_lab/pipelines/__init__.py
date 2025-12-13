"""
Pipeline implementations for video generation.

This module contains the core pipeline logic for integrating models
and generating character-consistent videos.
"""

from neural_motion_lab.pipelines.video_pipeline import VideoPipeline
from neural_motion_lab.pipelines.comfyui_pipeline import ComfyUIPipeline

__all__ = [
    "VideoPipeline",
    "ComfyUIPipeline",
]
