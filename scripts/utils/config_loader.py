"""Configuration loader utility for Neural Motion Lab."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage YAML configuration files."""
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        Initialize ConfigLoader.
        
        Args:
            config_dir: Directory containing config files. Defaults to './config'
        """
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_dir = Path(config_dir)
        
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")
    
    def load(self, config_name: str) -> Dict[str, Any]:
        """
        Load a configuration file.
        
        Args:
            config_name: Name of config file (with or without .yaml extension)
            
        Returns:
            Dictionary containing configuration
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not config_name.endswith('.yaml') and not config_name.endswith('.yml'):
            config_name = f"{config_name}.yaml"
        
        config_path = self.config_dir / config_name
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        logger.info(f"Loading configuration from {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config if config is not None else {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {config_path}: {e}")
            raise
    
    def load_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all configuration files from config directory.
        
        Returns:
            Dictionary mapping config names to their contents
        """
        configs = {}
        for config_file in self.config_dir.glob("*.yaml"):
            config_name = config_file.stem
            try:
                configs[config_name] = self.load(config_file.name)
            except Exception as e:
                logger.warning(f"Failed to load {config_file.name}: {e}")
        
        return configs
    
    def merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge multiple configuration dictionaries.
        Later configs override earlier ones.
        
        Args:
            *configs: Variable number of config dictionaries
            
        Returns:
            Merged configuration dictionary
        """
        merged = {}
        
        for config in configs:
            merged = self._deep_merge(merged, config)
        
        return merged
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries.
        
        Args:
            base: Base dictionary
            update: Dictionary with updates
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def save(self, config: Dict[str, Any], config_name: str) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config: Configuration dictionary to save
            config_name: Name of config file (with or without .yaml extension)
        """
        if not config_name.endswith('.yaml') and not config_name.endswith('.yml'):
            config_name = f"{config_name}.yaml"
        
        config_path = self.config_dir / config_name
        
        logger.info(f"Saving configuration to {config_path}")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    def validate_config(self, config: Dict[str, Any], required_keys: list) -> bool:
        """
        Validate that required keys exist in configuration.
        
        Args:
            config: Configuration dictionary
            required_keys: List of required key paths (e.g., ['model.name', 'training.batch_size'])
            
        Returns:
            True if all required keys exist, False otherwise
        """
        for key_path in required_keys:
            keys = key_path.split('.')
            current = config
            
            for key in keys:
                if not isinstance(current, dict) or key not in current:
                    logger.error(f"Missing required configuration key: {key_path}")
                    return False
                current = current[key]
        
        return True
    
    def get_nested(self, config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
        """
        Get nested configuration value using dot notation.
        
        Args:
            config: Configuration dictionary
            key_path: Dot-separated key path (e.g., 'model.precision')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        current = config
        
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        
        return current


def load_config(config_name: str, config_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Convenience function to load a single configuration file.
    
    Args:
        config_name: Name of config file
        config_dir: Optional config directory path
        
    Returns:
        Configuration dictionary
    """
    loader = ConfigLoader(config_dir)
    return loader.load(config_name)
