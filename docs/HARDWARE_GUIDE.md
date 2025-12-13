# Hardware Guide - Windows & RTX Optimization

Complete guide for optimizing Neural Motion Lab on Windows with NVIDIA RTX GPUs.

## GPU Compatibility

### Supported GPUs

| GPU | VRAM | Performance | Recommended Resolution |
|-----|------|------------|----------------------|
| RTX 3060 | 12 GB | Good | 512x512, 25-49 frames |
| RTX 3060 Ti | 8 GB* | Limited | 512x512, 25 frames |
| RTX 3070 | 8 GB* | Limited | 512x512, 25 frames |
| RTX 3080 | 10 GB | Good | 512x512, 49 frames |
| RTX 3090 | 24 GB | Excellent | 768x768, 49-73 frames |
| RTX 4070 Ti | 12 GB | Good | 512x512, 49 frames |
| RTX 4080 | 16 GB | Excellent | 768x768, 49 frames |
| RTX 4090 | 24 GB | Excellent | 1024x1024, 73 frames |

\* May require optimizations for larger models

### Minimum Requirements

- **VRAM:** 12 GB (8 GB with optimizations)
- **CUDA Compute:** 7.5+ (RTX 2000 series or newer)
- **Drivers:** Latest NVIDIA drivers
- **CUDA:** 11.8 or 12.1

## Windows Optimization

### NVIDIA Driver Setup

1. **Update to latest drivers:**
   - Visit [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)
   - Download and install latest Game Ready or Studio drivers
   - Restart computer

2. **Verify installation:**
```bash
nvidia-smi
```

3. **Enable GPU scheduling (Windows 10/11):**
   - Settings → System → Display → Graphics settings
   - Enable "Hardware-accelerated GPU scheduling"
   - Restart

### Windows Power Settings

**High Performance Mode:**
1. Control Panel → Power Options
2. Select "High performance"
3. Edit plan settings → Advanced → PCI Express → Link State Power Management → Off

**Windows 11 Game Mode:**
1. Settings → Gaming → Game Mode
2. Enable Game Mode (can improve GPU performance)

### PyTorch Optimization

**Install PyTorch with CUDA:**
```bash
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Enable TF32 (Ampere+ GPUs):**
```python
# Automatic in config, or manually:
import torch
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

### Memory Management

**Windows Memory Settings:**
1. System Properties → Advanced → Performance Settings
2. Advanced tab → Virtual memory → Change
3. Set page file to "System managed size"

**Free Up VRAM:**
```bash
# Close unnecessary applications
taskkill /F /IM "chrome.exe"
taskkill /F /IM "discord.exe"

# Monitor GPU usage
nvidia-smi -l 1
```

## Configuration Optimization

### Generation Config

Edit `config/generation_config.yaml`:

**For 12 GB VRAM:**
```yaml
generation:
  num_frames: 49
  width: 512
  height: 512
  
optimization:
  enable_xformers: true
  enable_vae_tiling: false
  vae_batch_size: 8
```

**For 24 GB VRAM:**
```yaml
generation:
  num_frames: 73
  width: 768
  height: 768
  
optimization:
  enable_xformers: true
  enable_vae_tiling: false
  vae_batch_size: 16
```

**For 8 GB VRAM (Aggressive):**
```yaml
generation:
  num_frames: 25
  width: 512
  height: 512
  
optimization:
  enable_xformers: true
  enable_vae_tiling: true
  enable_slicing: true
  vae_batch_size: 4

model:
  sequential_offload: true
```

### Training Config

**For 12 GB VRAM:**
```yaml
training:
  batch_size: 1
  gradient_accumulation_steps: 4
  
lora:
  rank: 32
  
optimization:
  enable_xformers: true
  gradient_checkpointing: true
  use_8bit_adam: false
```

**For 24 GB VRAM:**
```yaml
training:
  batch_size: 2
  gradient_accumulation_steps: 2
  
lora:
  rank: 64
  
optimization:
  enable_xformers: true
  gradient_checkpointing: true
```

## Performance Benchmarks

### Generation Speed (RTX 4090)

| Resolution | Frames | Steps | Time |
|------------|--------|-------|------|
| 512x512 | 25 | 50 | ~2 min |
| 512x512 | 49 | 50 | ~4 min |
| 768x768 | 49 | 50 | ~8 min |
| 1024x1024 | 49 | 50 | ~15 min |

### Training Speed (RTX 4090)

| Dataset Size | Epochs | Batch Size | Time |
|-------------|--------|------------|------|
| 20 images | 10 | 2 | ~30 min |
| 50 images | 10 | 2 | ~60 min |
| 100 images | 10 | 2 | ~120 min |

### VRAM Usage

| Task | 512x512 | 768x768 | 1024x1024 |
|------|---------|---------|-----------|
| Generation (49f) | ~10 GB | ~16 GB | ~22 GB |
| Training (rank 32) | ~11 GB | ~18 GB | N/A |
| Training (rank 64) | ~14 GB | ~22 GB | N/A |

## Advanced Optimizations

### xFormers

**Install:**
```bash
pip install xformers
```

**Enable in config:**
```yaml
optimization:
  enable_xformers: true
```

**Benefits:**
- 20-30% speed increase
- 10-20% VRAM reduction
- Better quality (sometimes)

### Compilation (PyTorch 2.0+)

```python
import torch

# In your script
model = torch.compile(model, mode="reduce-overhead")
```

**Benefits:**
- 5-15% speed increase
- No VRAM impact

**Tradeoffs:**
- First run slower (compilation)
- May not work with all models

### CPU Offloading

For limited VRAM:

```yaml
model:
  offload_to_cpu: true
  sequential_offload: true
```

**Benefits:**
- Run on lower VRAM GPUs
- Enables larger models

**Tradeoffs:**
- Significantly slower
- Requires fast CPU and RAM

### Batch Processing

Generate multiple videos efficiently:

```bash
python scripts/batch_generate.py \
    --input input_dir/ \
    --output outputs/ \
    --batch-size 1
```

Process images sequentially but reuse loaded model.

## Monitoring and Diagnostics

### GPU Monitoring

**NVIDIA SMI:**
```bash
# Watch GPU usage
nvidia-smi -l 1

# Detailed info
nvidia-smi -q -d MEMORY,UTILIZATION
```

**Windows Task Manager:**
- Ctrl+Shift+Esc → Performance → GPU
- Shows GPU utilization, VRAM, temperature

**MSI Afterburner (Recommended):**
- Real-time overlay
- Temperature monitoring
- Fan curve control

### Performance Profiling

```python
# Add to scripts
import torch.profiler as profiler

with profiler.profile(
    activities=[profiler.ProfilerActivity.CPU, profiler.ProfilerActivity.CUDA]
) as prof:
    # Your generation code
    
print(prof.key_averages().table(sort_by="cuda_time_total"))
```

### TensorBoard Monitoring

```bash
tensorboard --logdir logs/tensorboard
```

Monitor:
- Training loss
- GPU utilization
- Memory usage
- Training speed

## Cooling and Thermal Management

### Temperature Monitoring

```bash
nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader -l 1
```

**Safe ranges:**
- **Idle:** 30-50°C
- **Load:** 60-80°C
- **Max:** <85°C (thermal throttling starts)

### Cooling Improvements

1. **Case airflow:**
   - Ensure good case ventilation
   - Clean dust filters
   - Add case fans if needed

2. **Custom fan curve:**
   - Use MSI Afterburner
   - Increase fan speed at 65°C+
   - Balance noise vs. cooling

3. **Undervolting:**
   - Reduce voltage for same performance
   - Lower temperatures
   - Less power consumption

## Multi-GPU Setup

For multiple GPUs:

```yaml
platform:
  cuda_device: 0  # Use first GPU
```

Or specify via environment:

```bash
set CUDA_VISIBLE_DEVICES=0
python scripts/batch_generate.py ...
```

**Load balancing:**
```bash
# Terminal 1
set CUDA_VISIBLE_DEVICES=0
python scripts/batch_generate.py --input batch1/ --output out1/

# Terminal 2
set CUDA_VISIBLE_DEVICES=1
python scripts/batch_generate.py --input batch2/ --output out2/
```

## Troubleshooting Performance

### Slow Generation

**Check:**
1. GPU utilization with nvidia-smi
2. If <90%, likely CPU bottleneck
3. Close background applications
4. Check disk I/O (use SSD)

**Solutions:**
- Enable xFormers
- Increase batch size (if VRAM allows)
- Use faster storage
- Update drivers

### Out of Memory

**Solutions:**
1. Reduce resolution
2. Reduce number of frames
3. Enable VAE tiling
4. Enable sequential offload
5. Lower batch size
6. Restart script (clear cache)

### Thermal Throttling

Signs:
- GPU usage drops during generation
- Clock speeds decrease
- Temperature at 83°C+

**Solutions:**
- Improve case cooling
- Increase fan speeds
- Lower ambient temperature
- Undervolt GPU

## Best Practices

### For Best Performance

1. Use latest NVIDIA drivers
2. Enable xFormers
3. Close unnecessary applications
4. Use SSD for models and outputs
5. Monitor temperatures
6. Keep GPU drivers updated
7. Use appropriate resolution for your GPU

### For Best Quality

1. Use maximum steps your patience allows
2. Use higher CFG scale (8-10)
3. Don't sacrifice resolution for speed (within VRAM limits)
4. Use fp16 precision
5. Quality input images

### For Development

1. Start with small settings for testing
2. Use fixed seed for reproducibility
3. Profile performance regularly
4. Monitor VRAM usage
5. Use TensorBoard for training

## Hardware Upgrade Path

**Current: RTX 3060 (12 GB)**
→ **Upgrade:** RTX 4080 (16 GB) for better speed and larger models

**Current: RTX 3090 (24 GB)**
→ **Upgrade:** RTX 4090 (24 GB) for 2x speed improvement

**Current: RTX 4070 Ti (12 GB)**
→ **Upgrade:** RTX 4080 (16 GB) or wait for next gen

## Resources

- NVIDIA Documentation: https://docs.nvidia.com/
- PyTorch Performance: https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
- xFormers: https://github.com/facebookresearch/xformers

## Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Monitor GPU with nvidia-smi
- Review config files
- Open GitHub Issue with system specs
