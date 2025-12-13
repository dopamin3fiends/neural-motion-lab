"""
Unit tests for HunyuanVideo model.
"""

import pytest
from neural_motion_lab.models import HunyuanModel


class TestHunyuanModel:
    def test_init_default_device(self):
        """Test model initialization with default device."""
        model = HunyuanModel("models/hunyuan")
        assert model.model_path == "models/hunyuan"
        assert model.device == "cuda"
        
    def test_init_custom_device(self):
        """Test model initialization with custom device."""
        model = HunyuanModel("models/hunyuan", device="cpu")
        assert model.device == "cpu"
        
    def test_model_not_loaded_initially(self):
        """Test that model is not loaded on init."""
        model = HunyuanModel("models/hunyuan")
        assert model.model is None
