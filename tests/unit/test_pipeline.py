"""
Unit tests for video pipeline.
"""

import pytest
from neural_motion_lab.pipelines import VideoPipeline


class TestVideoPipeline:
    def test_init_without_lora(self):
        """Test pipeline initialization without LoRA."""
        pipeline = VideoPipeline(
            hunyuan_model_path="models/hunyuan",
            device="cuda"
        )
        assert pipeline.lora_model is None
        assert pipeline.device == "cuda"
        
    def test_init_with_lora(self):
        """Test pipeline initialization with LoRA."""
        pipeline = VideoPipeline(
            hunyuan_model_path="models/hunyuan",
            lora_model_path="models/lora/character1",
            device="cuda"
        )
        assert pipeline.lora_model is not None
        
    def test_init_with_cpu(self):
        """Test pipeline initialization with CPU."""
        pipeline = VideoPipeline(
            hunyuan_model_path="models/hunyuan",
            device="cpu"
        )
        assert pipeline.device == "cpu"
