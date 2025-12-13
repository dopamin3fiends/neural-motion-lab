"""
Pytest configuration file.
"""

import pytest
import os


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "gpu: marks tests that require GPU")


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def sample_config():
    """Provide a sample configuration for tests."""
    return {
        "pipeline": {
            "hunyuan_model_path": "models/hunyuan",
            "lora_model_path": "models/lora/test",
            "device": "cpu"
        },
        "generation": {
            "num_frames": 8,
            "fps": 8,
            "width": 512,
            "height": 512
        }
    }
