#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'npc'
DESCRIPTION = "Game master's tool to manage characters and game files"
URL = 'https://github.com/aurule/npc'
EMAIL = 'pmandrews@gmail.com'
AUTHOR = 'Peter Andrews'

# What packages are required for this module to be executed?
REQUIRED = [
    'mako', 'markdown', 'pyqt5'
]

# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with io.open('npc/__version__.py') as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="npc tabletop gaming gm campaign",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "Mako>=1.0.0",
        "Markdown>=2.6.0"
    ],
    extras_requires={
        "test": [
            "pytest>=2.8.5",
            "pytest-qt>=2.1.0"
        ]
    },
    package_data={
        'npc': [
            'settings/*.json',
            'templates/*.nwod',
            'templates/*.mako',
            'templates/*.md',
            'templates/listing/*.mako'
        ]
    },
    entry_points={
        'console_scripts': [
            'npc=npc.cli:start',
        ],
        'gui_scripts': [
            'npc-gui=npc.gui:start',
        ]
    }
)
