#!/usr/bin/env python3
"""
Setup script for Baileyspy - Python wrapper for Baileys WhatsApp library
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = "Baileyspy - Python wrapper for Baileys WhatsApp library"

# Read requirements
def read_requirements(filename):
    """Read requirements from file."""
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="baileyspy",
    version="1.0.0",
    description="Python wrapper for Baileys WhatsApp library with comprehensive bot automation capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BF667",
    author_email="",
    url="https://github.com/terastudio-org/Baileyspy",
    project_urls={
        "Bug Reports": "https://github.com/terastudio-org/Baileyspy",
        "Source": "https://github.com/angstvorfrauen/Baileys",
        "Documentation": "https://github.com/terastudio-org/Baileyspy",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    python_requires=">=3.14.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Human Interface Device (HID)",
    ],
    keywords="whatsapp bot automation wrapper api baileys python whatsapp-web chat messaging",
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "coverage>=6.0",
        ],
        "docs": [
            "sphinx>=7.0",
            "sphinx-rtd-theme>=1.3",
            "myst-parser>=0.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "baileyspy=baileyspy.cli:main",
        ],
    },
    package_data={
        "baileyspy": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    zip_safe=False,
)
