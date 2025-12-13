"""Setup script for Neural Motion Lab."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="neural-motion-lab",
    version="0.1.0",
    author="Neural Motion Lab",
    author_email="",
    description="Modular pipeline integrating LoRA with HunyuanVideo-I2V for character-consistent AI video generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dopamin3fiends/neural-motion-lab",
    packages=find_packages(include=["scripts", "scripts.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "transformers>=4.30.0",
        "diffusers>=0.27.0",
        "accelerate>=0.20.0",
        "peft>=0.5.0",
        "safetensors>=0.3.0",
        "pyyaml>=6.0",
        "omegaconf>=2.3.0",
        "opencv-python>=4.8.0",
        "imageio>=2.31.0",
        "imageio-ffmpeg>=0.4.9",
        "av>=10.0.0",
        "tqdm>=4.65.0",
        "requests>=2.31.0",
        "huggingface-hub>=0.16.0",
        "einops>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "monitoring": [
            "tensorboard>=2.13.0",
            "wandb>=0.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nml-setup=scripts.setup_environment:main",
            "nml-download=scripts.download_models:main",
            "nml-train=scripts.train_lora:main",
            "nml-generate=scripts.batch_generate:main",
            "nml-validate=scripts.validate_lora:main",
        ],
    },
)
