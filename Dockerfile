FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install the package
RUN pip3 install -e .

# Create necessary directories
RUN mkdir -p models/lora models/hunyuan outputs/videos outputs/images logs

# Expose ports (if needed for ComfyUI)
EXPOSE 8188

# Set default command
CMD ["/bin/bash"]
