# NPC - A GM Campaign Management Tool

[![GitHub version](https://badge.fury.io/gh/aurule%2Fnpc.svg)](https://badge.fury.io/gh/aurule%2Fnpc)

# About

NPC is a tool to make my life easier when I'm running tabletop RPG games. It automates and streamlines a few tedious tasks like managing plot and session notes, and managing character sheets. 

NPC is very much a personal project. It works well enough for me to use at my weekly game, but that's it. That said, if you use it and come up with suggestions or bugs, open an issue! I'll at least take a look :smiley:

This readme and the [project's ReadTheDocs](https://npc.readthedocs.io/) are the main documentation for the project. The source code is pretty thoroughly documented, too.

All code is [hosted on github](https://github.com/aurule/npc).

## Requirements

NPC requires at least:

* Python 3.5.0
* [Mako](http://www.makotemplates.org/) 1.0.0
* [Python Markdown](https://github.com/Python-Markdown/markdown) 3.0.0
* [PyYAML](https://github.com/yaml/pyyaml) 5.0.0

All packages can be installed with `pip -r requirements.txt`.

## Installation

NPC can be installed in a few ways.

The recommended way is to download the debian package for the latest release and install it as normal.

If you're using a different system, download the latest release tarball and unpack it (or clone the repo). Install the required packages above in the most appropriate way for your system, then run `make install` to symlink the launcher scripts. To uninstall the binaries, run `make uninstall`. If you'd rather handle the symlinks yourself, link the script `npc.py` to somewhere in your path, like `~/bin`.

Finally, you can download or clone, then run `pip install .`. This installs npc like any other python package, including launcher scripts.

# Usage

NPC is used through the command line. It has several commands which do different operations on the current folder, called a campaign. See ReadTheDocs for [the basics](https://npc.readthedocs.io/en/latest/invocation.html) and a rundown of [available commands](https://npc.readthedocs.io/en/latest/commands.html), along with configuration and other docs.

# Testing and Development

To set up the development environment, create and activate a venv and run `bin/setup`. It'll ensure everything is installed and ready to go.

## Requirements

* [pytest](http://doc.pytest.org/en/latest/) 3.3.0
* [pytest-cov](https://pypi.python.org/pypi/pytest-cov) 2.5.1
* [coverage](https://coverage.readthedocs.io/en/coverage-4.4.1/) 4.4.1
* [stdeb](https://pypi.python.org/pypi/stdeb) 0.8.5 - optional: only for building debian packages

These can all be installed with `pip install -r requirements-dev.txt`.

After cloning, I like using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) to manage the venv:

`mkvirtualenv -p /usr/bin/python3 -a ~/Workspace/npc -r requirements-dev.txt npc`

Then call `workon npc` to launch into the venv.

## Running Tests

Go to the root project directory and run `python -m pytest` or `make test`.

To generate a coverage report, run `make coverage`.

## Release Process

Releases are handled through [GitHub Releases](https://github.com/aurule/npc/releases).

1. Update the version number in [npc/__version__.py](https://github.com/aurule/npc/blob/develop/npc/__version__.py)
2. Update the [Changelog](https://github.com/aurule/npc/blob/develop/CHANGELOG.md) and remove the `[unreleased]` text from the to-be-released version number
3. Checkout `master` and merge in `develop`.
4. *(optional)* Create a tag on `master` containing the version number, like `1.4.2`.
5. Go to the [GitHub Releases](https://github.com/aurule/npc/releases) page and draft a new release
6. Use the version number as the tag name, and use the master branch
7. Add a title and description
8. *(optional)* If releasing premade packages for this release, add them now
9. Publish the release
