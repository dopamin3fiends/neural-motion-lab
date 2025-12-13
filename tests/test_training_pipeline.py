"""Tests for training pipeline integration."""

import pytest
from pathlib import Path
import tempfile
import yaml

from scripts.train_lora import LoRATrainer


@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        # Create subdirectories
        (base_dir / 'data' / 'training').mkdir(parents=True)
        (base_dir / 'output').mkdir(parents=True)
        
        yield base_dir


@pytest.fixture
def test_config():
    """Create test training configuration."""
    return {
        'model': {
            'base_model': 'test_model',
            'precision': 'fp16',
            'gradient_checkpointing': True
        },
        'lora': {
            'rank': 32,
            'alpha': 32,
            'dropout': 0.0,
            'target_modules': ['to_q', 'to_k', 'to_v'],
            'bias': 'none'
        },
        'training': {
            'output_dir': 'output',
            'num_epochs': 5,
            'batch_size': 1,
            'learning_rate': 1e-4,
            'save_steps': 100
        },
        'data': {
            'dataset_dir': 'data/training',
            'resolution': 512
        },
        'validation': {
            'enabled': False
        }
    }


def test_lora_trainer_init(test_config):
    """Test LoRATrainer initialization."""
    trainer = LoRATrainer(test_config)
    
    assert trainer.config == test_config
    assert trainer.model_config == test_config['model']
    assert trainer.lora_config == test_config['lora']
    assert trainer.training_config == test_config['training']


def test_lora_trainer_prepare_model(test_config):
    """Test model preparation."""
    trainer = LoRATrainer(test_config)
    
    # Should not raise errors
    trainer.prepare_model()


def test_lora_trainer_prepare_dataset_empty(test_config, temp_dirs):
    """Test dataset preparation with empty directory."""
    test_config['data']['dataset_dir'] = str(temp_dirs / 'data' / 'training')
    
    trainer = LoRATrainer(test_config)
    num_images = trainer.prepare_dataset()
    
    assert num_images == 0


def test_lora_trainer_prepare_dataset_nonexistent(test_config):
    """Test dataset preparation with nonexistent directory."""
    test_config['data']['dataset_dir'] = '/nonexistent/path'
    
    trainer = LoRATrainer(test_config)
    
    with pytest.raises(FileNotFoundError):
        trainer.prepare_dataset()


def test_lora_trainer_train(test_config, temp_dirs):
    """Test training initialization."""
    test_config['training']['output_dir'] = str(temp_dirs / 'output')
    
    trainer = LoRATrainer(test_config)
    
    # Should not raise errors
    trainer.train()
    
    # Check output directory was created
    assert Path(test_config['training']['output_dir']).exists()


def test_lora_trainer_validate_disabled(test_config):
    """Test validation when disabled."""
    test_config['validation']['enabled'] = False
    
    trainer = LoRATrainer(test_config)
    
    # Should not raise errors
    trainer.validate()


def test_lora_trainer_validate_enabled(test_config):
    """Test validation when enabled."""
    test_config['validation'] = {
        'enabled': True,
        'validation_prompt': 'test prompt',
        'num_validation_images': 2
    }
    
    trainer = LoRATrainer(test_config)
    
    # Should not raise errors
    trainer.validate()
