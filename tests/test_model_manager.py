"""Tests for model_manager module."""

import pytest
import torch
from pathlib import Path
import tempfile

from scripts.utils.model_manager import ModelManager


@pytest.fixture
def temp_cache_dir():
    """Create temporary cache directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_model_manager_init(temp_cache_dir):
    """Test ModelManager initialization."""
    manager = ModelManager(cache_dir=temp_cache_dir)
    
    assert manager.cache_dir == temp_cache_dir
    assert manager.device in ['cuda', 'cpu']


def test_model_manager_device_selection():
    """Test device selection."""
    # Auto device
    manager = ModelManager()
    expected = 'cuda' if torch.cuda.is_available() else 'cpu'
    assert manager.device == expected
    
    # Force CPU
    manager = ModelManager(device='cpu')
    assert manager.device == 'cpu'


def test_get_memory_info():
    """Test getting memory info."""
    manager = ModelManager()
    info = manager.get_memory_info()
    
    if torch.cuda.is_available():
        assert 'allocated' in info
        assert 'reserved' in info
        assert 'total' in info
        assert 'free' in info


def test_clear_memory():
    """Test memory clearing."""
    manager = ModelManager()
    
    # Should not raise any errors
    manager.clear_memory()


def test_unload_all():
    """Test unloading all models."""
    manager = ModelManager()
    
    # Add a fake model
    manager.loaded_models['test_model'] = {'fake': 'model'}
    
    assert 'test_model' in manager.loaded_models
    
    manager.unload_all()
    
    assert len(manager.loaded_models) == 0


def test_set_precision():
    """Test setting model precision."""
    manager = ModelManager()
    
    # Create a simple tensor
    tensor = torch.randn(2, 2)
    
    # Test fp16
    result = manager.set_precision(tensor, 'fp16')
    assert result.dtype == torch.float16
    
    # Test fp32
    result = manager.set_precision(tensor, 'fp32')
    assert result.dtype == torch.float32
    
    # Test bf16 (if supported)
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        result = manager.set_precision(tensor, 'bf16')
        assert result.dtype == torch.bfloat16


def test_load_model_nonexistent(temp_cache_dir):
    """Test loading nonexistent model raises error."""
    manager = ModelManager(cache_dir=temp_cache_dir)
    
    with pytest.raises(FileNotFoundError):
        manager.load_model(temp_cache_dir / 'nonexistent.pt')


def test_move_to_device():
    """Test moving model to device."""
    manager = ModelManager()
    
    tensor = torch.randn(2, 2)
    result = manager.move_to_device(tensor, 'cpu')
    
    assert result.device.type == 'cpu'
