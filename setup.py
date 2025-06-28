#!/usr/bin/env python3
"""
Sonify - Spotify Data Visualizer
Setup script for package installation
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='sonify',
    version='1.0.0',
    description='A beautiful Spotify data visualizer that creates shareable insights from your listening habits',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Sonify Team',
    author_email='contact@sonify.app',
    url='https://github.com/makalin/Sonify',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Flask',
    ],
    keywords='spotify music visualization data analysis charts graphs',
    project_urls={
        'Bug Reports': 'https://github.com/makalin/Sonify/issues',
        'Source': 'https://github.com/makalin/Sonify',
        'Documentation': 'https://github.com/makalin/Sonify#readme',
    },
    entry_points={
        'console_scripts': [
            'sonify=run:main',
        ],
    },
    zip_safe=False,
) 