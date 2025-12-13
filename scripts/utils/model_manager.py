"""Model manager utility for Neural Motion Lab."""

import torch
from pathlib import Path
from typing import Optional, Dict, Any, Union
import logging
from huggingface_hub import snapshot_download
import gc

logger = logging.getLogger(__name__)


class ModelManager:
    """Manage model loading, caching, and device management."""
    
    def __init__(
        self,
        device: Optional[str] = None,
        cache_dir: Optional[Union[str, Path]] = None,
        offload_to_cpu: bool = False
    ):
        """
        Initialize ModelManager.
        
        Args:
            device: Device to load models on ('cuda', 'cpu', or specific device like 'cuda:0')
            cache_dir: Directory for model caching
            offload_to_cpu: Enable CPU offloading for memory management
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".cache" / "neural_motion_lab"
        self.offload_to_cpu = offload_to_cpu
        self.loaded_models: Dict[str, Any] = {}
        
        logger.info(f"ModelManager initialized with device: {self.device}")
        
        if self.device.startswith("cuda"):
            self._log_gpu_info()
    
    def _log_gpu_info(self) -> None:
        """Log GPU information."""
        if torch.cuda.is_available():
            device_idx = 0 if self.device == "cuda" else int(self.device.split(":")[-1])
            gpu_name = torch.cuda.get_device_name(device_idx)
            total_memory = torch.cuda.get_device_properties(device_idx).total_memory / 1024**3
            logger.info(f"GPU: {gpu_name} ({total_memory:.2f} GB)")
    
    def download_model(
        self,
        model_id: str,
        local_dir: Optional[Union[str, Path]] = None,
        force_download: bool = False,
        token: Optional[str] = None
    ) -> Path:
        """
        Download model from HuggingFace Hub.
        
        Args:
            model_id: HuggingFace model ID (e.g., 'tencent/HunyuanVideo')
            local_dir: Local directory to save model
            force_download: Force re-download even if cached
            token: HuggingFace API token
            
        Returns:
            Path to downloaded model directory
        """
        if local_dir is None:
            local_dir = self.cache_dir / model_id.replace("/", "_")
        else:
            local_dir = Path(local_dir)
        
        logger.info(f"Downloading model {model_id} to {local_dir}")
        
        try:
            model_path = snapshot_download(
                repo_id=model_id,
                local_dir=str(local_dir),
                local_dir_use_symlinks=False,
                force_download=force_download,
                token=token,
                resume_download=True
            )
            logger.info(f"Model downloaded successfully to {model_path}")
            return Path(model_path)
        except Exception as e:
            logger.error(f"Failed to download model {model_id}: {e}")
            raise
    
    def load_model(
        self,
        model_path: Union[str, Path],
        model_name: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Load a model from path.
        
        Args:
            model_path: Path to model checkpoint
            model_name: Optional name to cache the model
            **kwargs: Additional arguments for model loading
            
        Returns:
            Loaded model
        """
        model_path = Path(model_path)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Check if model already loaded
        if model_name and model_name in self.loaded_models:
            logger.info(f"Using cached model: {model_name}")
            return self.loaded_models[model_name]
        
        logger.info(f"Loading model from {model_path}")
        
        try:
            # Load based on file extension
            if model_path.suffix in ['.pt', '.pth']:
                model = torch.load(model_path, map_location=self.device, **kwargs)
            elif model_path.suffix == '.safetensors':
                from safetensors.torch import load_file
                model = load_file(str(model_path), device=self.device)
            else:
                raise ValueError(f"Unsupported model format: {model_path.suffix}")
            
            # Cache the model if name provided
            if model_name:
                self.loaded_models[model_name] = model
            
            logger.info(f"Model loaded successfully")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
            raise
    
    def unload_model(self, model_name: str) -> None:
        """
        Unload a cached model from memory.
        
        Args:
            model_name: Name of cached model to unload
        """
        if model_name in self.loaded_models:
            logger.info(f"Unloading model: {model_name}")
            del self.loaded_models[model_name]
            self.clear_memory()
    
    def unload_all(self) -> None:
        """Unload all cached models from memory."""
        logger.info("Unloading all cached models")
        self.loaded_models.clear()
        self.clear_memory()
    
    def clear_memory(self) -> None:
        """Clear GPU/CPU memory."""
        gc.collect()
        if self.device.startswith("cuda"):
            torch.cuda.empty_cache()
            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated() / 1024**3
                reserved = torch.cuda.memory_reserved() / 1024**3
                logger.debug(f"GPU memory - Allocated: {allocated:.2f} GB, Reserved: {reserved:.2f} GB")
    
    def get_memory_info(self) -> Dict[str, float]:
        """
        Get current memory usage information.
        
        Returns:
            Dictionary with memory statistics in GB
        """
        info = {}
        
        if self.device.startswith("cuda") and torch.cuda.is_available():
            device_idx = 0 if self.device == "cuda" else int(self.device.split(":")[-1])
            info['allocated'] = torch.cuda.memory_allocated(device_idx) / 1024**3
            info['reserved'] = torch.cuda.memory_reserved(device_idx) / 1024**3
            info['total'] = torch.cuda.get_device_properties(device_idx).total_memory / 1024**3
            info['free'] = info['total'] - info['allocated']
        
        return info
    
    def move_to_device(self, model: Any, device: Optional[str] = None) -> Any:
        """
        Move model to specified device.
        
        Args:
            model: Model to move
            device: Target device (defaults to manager's device)
            
        Returns:
            Model on target device
        """
        target_device = device or self.device
        
        if hasattr(model, 'to'):
            logger.info(f"Moving model to {target_device}")
            return model.to(target_device)
        
        return model
    
    def enable_memory_efficient_attention(self, model: Any) -> Any:
        """
        Enable memory-efficient attention (xFormers).
        
        Args:
            model: Model to optimize
            
        Returns:
            Optimized model
        """
        try:
            if hasattr(model, 'enable_xformers_memory_efficient_attention'):
                logger.info("Enabling xFormers memory efficient attention")
                model.enable_xformers_memory_efficient_attention()
            else:
                logger.warning("Model does not support xFormers")
        except Exception as e:
            logger.warning(f"Failed to enable xFormers: {e}")
        
        return model
    
    def set_precision(self, model: Any, precision: str = "fp16") -> Any:
        """
        Set model precision.
        
        Args:
            model: Model to convert
            precision: Target precision ('fp32', 'fp16', 'bf16')
            
        Returns:
            Converted model
        """
        if not hasattr(model, 'to'):
            return model
        
        logger.info(f"Converting model to {precision}")
        
        if precision == "fp16":
            return model.half()
        elif precision == "bf16":
            return model.bfloat16()
        elif precision == "fp32":
            return model.float()
        else:
            logger.warning(f"Unknown precision: {precision}")
            return model
