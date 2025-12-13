"""Tests for config_loader module."""

import pytest
from pathlib import Path
import tempfile
import yaml

from scripts.utils.config_loader import ConfigLoader, load_config


@pytest.fixture
def temp_config_dir():
    """Create temporary config directory with test configs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        
        # Create test config files
        test_config = {
            'model': {
                'name': 'test_model',
                'precision': 'fp16'
            },
            'training': {
                'batch_size': 4,
                'learning_rate': 0.001
            }
        }
        
        with open(config_dir / 'test_config.yaml', 'w') as f:
            yaml.dump(test_config, f)
        
        yield config_dir


def test_config_loader_init(temp_config_dir):
    """Test ConfigLoader initialization."""
    loader = ConfigLoader(temp_config_dir)
    assert loader.config_dir == temp_config_dir


def test_config_loader_load(temp_config_dir):
    """Test loading a config file."""
    loader = ConfigLoader(temp_config_dir)
    config = loader.load('test_config.yaml')
    
    assert config['model']['name'] == 'test_model'
    assert config['model']['precision'] == 'fp16'
    assert config['training']['batch_size'] == 4


def test_config_loader_load_without_extension(temp_config_dir):
    """Test loading config without .yaml extension."""
    loader = ConfigLoader(temp_config_dir)
    config = loader.load('test_config')
    
    assert config['model']['name'] == 'test_model'


def test_config_loader_load_nonexistent(temp_config_dir):
    """Test loading nonexistent config raises error."""
    loader = ConfigLoader(temp_config_dir)
    
    with pytest.raises(FileNotFoundError):
        loader.load('nonexistent.yaml')


def test_merge_configs(temp_config_dir):
    """Test merging multiple configs."""
    loader = ConfigLoader(temp_config_dir)
    
    base = {
        'model': {'name': 'base', 'precision': 'fp32'},
        'training': {'batch_size': 2}
    }
    
    override = {
        'model': {'precision': 'fp16'},
        'training': {'learning_rate': 0.01}
    }
    
    merged = loader.merge_configs(base, override)
    
    assert merged['model']['name'] == 'base'
    assert merged['model']['precision'] == 'fp16'
    assert merged['training']['batch_size'] == 2
    assert merged['training']['learning_rate'] == 0.01


def test_get_nested(temp_config_dir):
    """Test getting nested config values."""
    loader = ConfigLoader(temp_config_dir)
    config = loader.load('test_config')
    
    value = loader.get_nested(config, 'model.precision')
    assert value == 'fp16'
    
    value = loader.get_nested(config, 'model.nonexistent', default='default')
    assert value == 'default'


def test_validate_config(temp_config_dir):
    """Test config validation."""
    loader = ConfigLoader(temp_config_dir)
    config = loader.load('test_config')
    
    # Valid keys
    assert loader.validate_config(config, ['model.name', 'training.batch_size']) is True
    
    # Invalid keys
    assert loader.validate_config(config, ['nonexistent.key']) is False


def test_save_config(temp_config_dir):
    """Test saving config."""
    loader = ConfigLoader(temp_config_dir)
    
    new_config = {
        'test': {
            'value': 123
        }
    }
    
    loader.save(new_config, 'new_config.yaml')
    
    # Load and verify
    loaded = loader.load('new_config.yaml')
    assert loaded['test']['value'] == 123


def test_load_all(temp_config_dir):
    """Test loading all configs."""
    loader = ConfigLoader(temp_config_dir)
    configs = loader.load_all()
    
    assert 'test_config' in configs
    assert configs['test_config']['model']['name'] == 'test_model'
