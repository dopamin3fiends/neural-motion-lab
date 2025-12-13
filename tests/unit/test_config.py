"""
Unit tests for configuration utilities.
"""

import pytest
import tempfile
import os
from neural_motion_lab.utils.config import load_config, save_config, merge_configs


class TestConfigUtils:
    def test_save_and_load_yaml(self):
        """Test saving and loading YAML config."""
        config = {"key1": "value1", "key2": 42}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
            
        try:
            save_config(config, temp_path)
            loaded = load_config(temp_path)
            assert loaded == config
        finally:
            os.unlink(temp_path)
            
    def test_save_and_load_json(self):
        """Test saving and loading JSON config."""
        config = {"key1": "value1", "key2": 42}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            
        try:
            save_config(config, temp_path)
            loaded = load_config(temp_path)
            assert loaded == config
        finally:
            os.unlink(temp_path)
            
    def test_merge_configs(self):
        """Test merging multiple configs."""
        config1 = {"a": 1, "b": 2}
        config2 = {"b": 3, "c": 4}
        
        merged = merge_configs(config1, config2)
        assert merged == {"a": 1, "b": 3, "c": 4}
        
    def test_load_nonexistent_file(self):
        """Test loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")
