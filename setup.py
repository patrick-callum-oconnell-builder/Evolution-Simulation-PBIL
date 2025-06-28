from setuptools import setup, find_packages

# Build the CFFI extension
from build_cffi import ffibuilder

setup(
    name="pbil_maxsat",
    version="0.1.0",
    description="PBIL (Population Based Incremental Learning) for MAXSAT problems with C backend",
    long_description="A high-performance Python implementation of Population Based Incremental Learning (PBIL) algorithm for solving MAXSAT problems, with C backend integration for computational efficiency.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "cffi>=1.16.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
    ],
    cffi_modules=["build_cffi.py:ffibuilder"],
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="pbil, maxsat, optimization, evolutionary-algorithms, satisfiability",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pbil_maxsat/issues",
        "Source": "https://github.com/yourusername/pbil_maxsat",
    },
) 