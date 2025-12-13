# Troubleshooting Guide

Common issues and solutions for Neural Motion Lab.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Model Loading Issues](#model-loading-issues)
- [Generation Issues](#generation-issues)
- [Training Issues](#training-issues)
- [Memory Issues](#memory-issues)
- [Performance Issues](#performance-issues)
- [ComfyUI Issues](#comfyui-issues)

## Installation Issues

### Python Version Error

**Error:** `Python 3.10 or higher is required`

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.11 from python.org
# Or use conda
conda create -n neural-motion python=3.11
conda activate neural-motion
```

### CUDA Not Available

**Error:** `torch.cuda.is_available() returns False`

**Diagnosis:**
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

**Solutions:**
1. **Check NVIDIA driver:**
```bash
nvidia-smi
```
If command fails, install/update NVIDIA drivers.

2. **Reinstall PyTorch with CUDA:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

3. **Verify CUDA version compatibility:**
```bash
python -c "import torch; print(torch.version.cuda)"
```

### Package Installation Fails

**Error:** `pip install` fails with build errors

**Solutions:**

**Windows:**
1. Install Visual Studio Build Tools
2. Download from: https://visualstudio.microsoft.com/downloads/
3. Select "Desktop development with C++"

**Alternative:**
```bash
pip install --only-binary :all: PACKAGE_NAME
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'scripts'`

**Solutions:**
1. **Install in development mode:**
```bash
pip install -e .
```

2. **Add to Python path:**
```bash
set PYTHONPATH=%PYTHONPATH%;C:\path\to\neural-motion-lab
```

3. **Run from project root:**
```bash
cd neural-motion-lab
python scripts/batch_generate.py ...
```

## Model Loading Issues

### Model Not Found

**Error:** `FileNotFoundError: Model not found`

**Solutions:**
1. **Download models:**
```bash
python scripts/download_models.py --model all
```

2. **Check model paths in config:**
```yaml
# config/model_paths.yaml
base_model:
  hunyuan_video:
    local_path: "models/hunyuan_video"  # Verify this path exists
```

3. **Verify model files exist:**
```bash
dir models\hunyuan_video
```

### Model Download Fails

**Error:** Download interrupted or fails

**Solutions:**
1. **Resume download:**
```bash
python scripts/download_models.py --model hunyuan
```

2. **Manual download:**
- Visit https://huggingface.co/tencent/HunyuanVideo
- Download files to `models/hunyuan_video/`

3. **Use HuggingFace CLI:**
```bash
pip install huggingface-hub
huggingface-cli download tencent/HunyuanVideo --local-dir models/hunyuan_video
```

### Checkpoint Format Error

**Error:** `Invalid checkpoint format` or `safetensors load failed`

**Solutions:**
1. **Install safetensors:**
```bash
pip install safetensors
```

2. **Verify file integrity:**
```bash
python scripts/validate_lora.py lora/your_model.safetensors
```

3. **Re-download model**

## Generation Issues

### Out of Memory During Generation

**Error:** `CUDA out of memory`

**Solutions:**
1. **Reduce settings in config:**
```yaml
generation:
  num_frames: 25  # Reduce from 49
  width: 512
  height: 512

optimization:
  enable_xformers: true
  enable_vae_tiling: true
  vae_batch_size: 4  # Reduce from 8
```

2. **Enable sequential offload:**
```yaml
model:
  sequential_offload: true
```

3. **Close other applications:**
```bash
taskkill /F /IM "chrome.exe"
```

4. **Clear CUDA cache:**
```python
import torch
torch.cuda.empty_cache()
```

### Poor Quality Output

**Problem:** Blurry or distorted videos

**Solutions:**
1. **Increase inference steps:**
```bash
python scripts/batch_generate.py \
    --input image.png \
    --num-frames 49 \
    # Edit config: num_inference_steps: 75
```

2. **Adjust guidance scale:**
```yaml
generation:
  guidance_scale: 8.5  # Try 7-10
```

3. **Use better input image:**
- Higher resolution (512x512+)
- Clear, well-lit subject
- Minimal compression

4. **Check LoRA scale:**
```bash
--lora-scale 0.8  # Try 0.6-0.9
```

### LoRA Not Applying

**Problem:** LoRA seems to have no effect

**Solutions:**
1. **Verify LoRA path:**
```bash
python scripts/validate_lora.py lora/your_lora.safetensors
```

2. **Increase LoRA scale:**
```bash
--lora-scale 1.0  # Try higher values
```

3. **Check LoRA training:**
- May need more training epochs
- Verify dataset quality

### Generation Hangs

**Problem:** Script freezes during generation

**Solutions:**
1. **Check GPU status:**
```bash
nvidia-smi
```

2. **Restart script with timeout:**
```python
# Add to script
import signal
signal.alarm(3600)  # 1 hour timeout
```

3. **Monitor progress:**
```bash
# Enable debug logging
set LOG_LEVEL=DEBUG
python scripts/batch_generate.py ...
```

## Training Issues

### Training Loss Not Decreasing

**Problem:** Loss stays constant or increases

**Solutions:**
1. **Adjust learning rate:**
```yaml
training:
  learning_rate: 5e-5  # Try different values: 1e-5 to 5e-4
```

2. **Check dataset:**
```bash
dir data\training  # Verify images exist
```

3. **Increase epochs:**
```bash
--epochs 15
```

4. **Verify model loaded:**
Check console output for model loading confirmation.

### Training Out of Memory

**Error:** `CUDA out of memory` during training

**Solutions:**
1. **Reduce batch size:**
```yaml
training:
  batch_size: 1
  gradient_accumulation_steps: 8  # Compensate with accumulation
```

2. **Enable optimizations:**
```yaml
optimization:
  gradient_checkpointing: true
  use_8bit_adam: true
```

3. **Reduce LoRA rank:**
```yaml
lora:
  rank: 16  # Reduce from 32
```

4. **Lower resolution:**
```yaml
data:
  resolution: 512  # Reduce if higher
```

### Training Too Slow

**Problem:** Training takes too long

**Solutions:**
1. **Enable xFormers:**
```yaml
optimization:
  enable_xformers: true
```

2. **Increase batch size (if VRAM allows):**
```yaml
training:
  batch_size: 2
```

3. **Reduce validation frequency:**
```yaml
validation:
  validation_steps: 1000  # Increase from 500
```

4. **Use faster storage (SSD)**

### Overfitting

**Problem:** Training loss very low but outputs look wrong

**Solutions:**
1. **Reduce epochs:**
```bash
--epochs 8  # Reduce from 15
```

2. **Add more diverse images**

3. **Enable dropout:**
```yaml
lora:
  dropout: 0.05
```

4. **Lower learning rate:**
```yaml
training:
  learning_rate: 5e-5
```

## Memory Issues

### System RAM Issues

**Error:** System runs out of RAM

**Solutions:**
1. **Close applications:**
```bash
taskkill /F /IM "chrome.exe"
taskkill /F /IM "discord.exe"
```

2. **Increase virtual memory:**
- Control Panel → System → Advanced → Performance
- Set larger page file

3. **Reduce dataloader workers:**
```yaml
data:
  num_workers: 2  # Reduce from 4
```

### VRAM Leaks

**Problem:** VRAM usage increases over time

**Solutions:**
1. **Clear cache between runs:**
```python
import torch
import gc

torch.cuda.empty_cache()
gc.collect()
```

2. **Restart script periodically**

3. **Use context managers:**
```python
with torch.no_grad():
    # Generation code
```

## Performance Issues

### Slow Generation

**Problem:** Generation takes too long

**Solutions:**
1. **Enable xFormers:**
```bash
pip install xformers
```

2. **Check GPU utilization:**
```bash
nvidia-smi -l 1
```

3. **Use SSD for I/O:**
Move models and outputs to SSD

4. **Close background apps**

5. **Update NVIDIA drivers**

### CPU Bottleneck

**Problem:** GPU not fully utilized

**Solutions:**
1. **Increase dataloader workers:**
```yaml
data:
  num_workers: 4
```

2. **Use faster storage**

3. **Check CPU usage in Task Manager**

## ComfyUI Issues

### ComfyUI Won't Start

**Error:** ComfyUI fails to launch

**Solutions:**
1. **Check dependencies:**
```bash
cd ComfyUI
pip install -r requirements.txt
```

2. **Try different port:**
```bash
python main.py --port 8189
```

3. **Check logs:**
```bash
python main.py --verbose
```

### Workflow Load Fails

**Error:** Can't load workflow JSON

**Solutions:**
1. **Verify JSON syntax:**
- Use JSON validator online
- Check for missing commas/brackets

2. **Update ComfyUI:**
```bash
cd ComfyUI
git pull
```

3. **Check custom nodes:**
Workflow may require custom nodes not installed

### Models Not Appearing

**Problem:** Models don't show in ComfyUI

**Solutions:**
1. **Verify symlinks:**
```powershell
dir ComfyUI\models\loras
# Should show linked files
```

2. **Copy models instead:**
```bash
copy lora\*.safetensors ComfyUI\models\loras\
```

3. **Restart ComfyUI**

## Getting More Help

### Collect Diagnostic Info

```bash
# System info
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
nvidia-smi

# Package versions
pip list | findstr torch
pip list | findstr transformers
```

### Create Issue

When opening GitHub issue, include:
1. **System info:**
   - Windows version
   - GPU model and VRAM
   - Python version
   - CUDA version

2. **Error details:**
   - Full error message
   - Command that failed
   - Config files used

3. **Steps to reproduce**

4. **Attempted solutions**

### Useful Commands

```bash
# Clear all CUDA memory
python -c "import torch; torch.cuda.empty_cache()"

# Test imports
python -c "from scripts.utils.config_loader import load_config; print('OK')"

# Check disk space
dir

# Monitor GPU
nvidia-smi -l 1

# View logs
type logs\training.log
```

## Common Error Messages

### "RuntimeError: CUDA error: out of memory"
→ See [Out of Memory During Generation](#out-of-memory-during-generation)

### "FileNotFoundError: [Errno 2] No such file"
→ See [Model Not Found](#model-not-found)

### "ModuleNotFoundError: No module named"
→ See [Import Errors](#import-errors)

### "RuntimeError: CUDA out of memory"
→ See [Memory Issues](#memory-issues)

### "ConnectionError: HTTPConnectionPool"
→ Check internet connection, try manual download

### "PermissionError: [Errno 13]"
→ Run as Administrator or check file permissions

## Additional Resources

- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) - Optimization tips
- [GitHub Issues](https://github.com/dopamin3fiends/neural-motion-lab/issues)
- [PyTorch Documentation](https://pytorch.org/docs/)
