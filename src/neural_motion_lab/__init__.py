"""
Neural Motion Lab - Modular pipeline for character-consistent AI video generation.

This package integrates LoRA with HunyuanVideo-I2V for character-consistent 
AI video generation via ComfyUI.
"""

__version__ = "0.1.0"
__author__ = "Neural Motion Lab Team"

from neural_motion_lab.pipelines import VideoPipeline
from neural_motion_lab.models import LoRAModel, HunyuanModel

__all__ = [
    "VideoPipeline",
    "LoRAModel",
    "HunyuanModel",
]
