# NPC - A GM Campaign Management Tool

[![GitHub version](https://badge.fury.io/gh/aurule%2Fnpc.svg)](https://badge.fury.io/gh/aurule%2Fnpc)

# About

NPC is a tool to make my life easier when I'm running tabletop RPG games. It automates and streamlines a few tedious tasks like managing plot and session notes, and managing character sheets. 

NPC is very much a personal project. It works well enough for me to use at my weekly game, but that's it. That said, if you use it and come up with suggestions or bugs, open an issue! I'll at least take a look :smiley:

This readme and the [project's ReadTheDocs](https://npc.readthedocs.io/) are the main documentation for the project. The source code is pretty thoroughly documented, too.

All code is [hosted on github](https://github.com/aurule/npc).

## Installation

Each release of NPC has pre-built binaries for Linux and Windows. These can be used directly by putting them in a directory in the system's PATH. I have plans to improve this experience in the future.

Alternately, you can run npc from its source. To do so, clone or download the source and install the system libraries corresponding to the packages in `requirements.txt`. Symlink the `npc_cli` file to somewhere in your PATH and it *should* work.

# Usage

Right now, NPC is used primarily through its command line. See ReadTheDocs for details of the available comands and what they do.

NPC uses plain text files for all of its configuration and data. You can use whatever text editor you like to update characters, etc.

# Testing and Development

Development is pretty straightforward. Clone the repo and create a standard venv using Python 3.11 or later. Install packages from `requirements-dev.txt` and you should be all set.Development is pretty straightforward. Clone the repo and create a standard venv using Python 3.11 or later. Install packages from `requirements-dev.txt` and you should be all set.

## Running Tests

Go to the root project directory and run `python -m pytest` or `make test`.

To generate a coverage report, run `make coverage`.

## Building Documentation

The docs are built using Sphinx. From the root dir, you can run `make docs` to quickly generate them.

When actively working on the docs, use `scripts/live-docs.sh` to automatically rebuild the docs on change, using sphinx-autobuild.

To update the reference documentation for tags and systems, run `python scripts/build_reference_docs.py`.
