"""
Setup configuration for Neural Motion Lab package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open('requirements.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="neural-motion-lab",
    version="0.1.0",
    author="Neural Motion Lab Team",
    description="Modular pipeline integrating LoRA with HunyuanVideo-I2V for character-consistent AI video generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dopamin3fiends/neural-motion-lab",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pytest>=7.3.0",
            "pytest-cov>=4.1.0",
            "sphinx>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neural-motion-lab=neural_motion_lab.cli:main",
        ],
    },
)
