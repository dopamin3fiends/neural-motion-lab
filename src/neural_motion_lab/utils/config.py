"""
Configuration management utilities.
"""

import json
import yaml
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from JSON or YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save configuration to JSON or YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration file
    """
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        if path.suffix in ['.yaml', '.yml']:
            yaml.dump(config, f, default_flow_style=False)
        elif path.suffix == '.json':
            json.dump(config, f, indent=2)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple configuration dictionaries.
    
    Args:
        *configs: Variable number of config dictionaries
        
    Returns:
        Merged configuration dictionary
    """
    merged = {}
    for config in configs:
        merged.update(config)
    return merged
