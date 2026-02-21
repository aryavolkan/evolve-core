"""
Setup script for evolve-core
"""

from setuptools import find_packages, setup

with open("../README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evolve-core",
    version="0.1.0",
    author="Evolve Team",
    description="Shared evolutionary algorithm and neural network components for Godot AI projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/evolve-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "wandb>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
)
