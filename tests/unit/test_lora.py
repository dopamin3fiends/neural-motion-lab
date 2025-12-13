"""
Unit tests for LoRA model.
"""

import pytest
import os
from neural_motion_lab.models import LoRAModel


class TestLoRAModel:
    def test_init(self):
        """Test LoRA model initialization."""
        model = LoRAModel("models/lora/test.safetensors")
        assert model.model_path == "models/lora/test.safetensors"
        assert model.model is None
        
    def test_init_with_config(self):
        """Test LoRA model initialization with config."""
        config = {"scale": 0.8}
        model = LoRAModel("models/lora/test.safetensors", config)
        assert model.config == config
        
    def test_get_config(self):
        """Test getting model config."""
        config = {"scale": 0.8, "rank": 4}
        model = LoRAModel("models/lora/test.safetensors", config)
        assert model.get_config() == config
