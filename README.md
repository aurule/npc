# NPC - A GM Campaign Management Tool

[![GitHub version](https://badge.fury.io/gh/aurule%2Fnpc.svg)](https://badge.fury.io/gh/aurule%2Fnpc)

<!-- MarkdownTOC autolink="true" bracket="round" depth=2 -->

- [About](#about)
    - [Requirements](#requirements)
    - [Installation](#installation)
- [Usage](#usage)
    - [Set Up Directories](#set-up-directories)
    - [Create Session Files](#create-session-files)
    - [Open Latest Plot and Session Files](#open-latest-plot-and-session-files)
    - [Create a Character](#create-a-character)
    - [Lint Character Files](#lint-character-files)
    - [Find Characters](#find-characters)
    - [Make an NPC Listing](#make-an-npc-listing)
    - [Dump Raw NPC Data](#dump-raw-npc-data)
    - [Reorganize Character Files](#reorganize-character-files)
    - [Edit Settings](#edit-settings)
    - [Make Character Tag Reports](#make-character-tag-reports)
- [Gotchas](#gotchas)
    - [Using both `search` and `ignore`](#using-both-search-and-ignore)
- [Configuration](#configuration)
    - [Type-Specific Settings](#type-specific-settings)
- [Testing](#testing)
    - [Requirements](#requirements-1)
    - [Running Tests](#running-tests)

<!-- /MarkdownTOC -->

# About

I created NPC to make my life easier when running New World of Darkness tabletop RPGs. It automates and streamlines a few tedious tasks like creating new session logs and character sheets.

NPC is very much a personal project. It works well enough for me to use at my weekly game, but that's it. That said, if you use it and come up with suggestions or bugs, open an issue! I'll at least take a look :smiley:

This readme and the [project's wiki](https://github.com/aurule/npc/wiki) are the main documentation for the project. The source code is pretty thoroughly documented, too.

All code is [hosted on github](https://github.com/aurule/npc).

## Requirements

NPC requires at least:

* Python 3.5.0
* [Mako](http://www.makotemplates.org/) 1.0.0
* [Python Markdown](http://pythonhosted.org/Markdown/index.html) 2.6.0
* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) 5.7.1

All packages can be installed with `pip -r requirements.txt`.

## Installation

NPC can be installed in a few ways.

The recommended way is to download the debian package for the latest release and install it as normal.

If you're using a different system, download the latest release tarball and unpack it (or clone the repo). Install the required packages above in the most appropriate way for your system, then run `make install` to symlink the launcher scripts. To uninstall the binaries, run `make uninstall`. If you'd rather handle the symlinks yourself, link the scripts `npc.py` and `npc-gui.py` to somewhere in your path, like `~/bin`.

Finally, you can download or clone, then run `pip install .`. This installs npc like any other python package, including launcher scripts.

# Usage

The functionality of NPC is split among a few sub-commands. Each one encompasses a single high-level task, and has its own options.

These global options must be passed *before* the name of the subcommand. They affect the overall behavior of NPC:

* `--campaign`: By default, NPC derives the campaign path from the current directory when it is run. It does this by walking backward until it finds the `.npc/` campaign config directory, or hits root. In the latter case, it just uses the current directory. The `--campaign` argument overrides this behavior and explicitly sets the campaign directory.
* `--version`: Show the version string and exit immediately. When this option is present, everything else is ignored.

These common options are available for every command:

* `--debug`: Forces NPC to show every error that occurs, even when those errors are harmless. Useful for figuring out settings problems.
* `--batch`: By default, NPC will open whatever files are relevant to the subcommand. The `--batch` switch prevents that from happening.

## Set Up Directories

The `init` command creates the basic directories that NPC expects to find. Every directory under the `paths` key in the settings file is created, along with the special `.npc` directory.

Init creates a new campaign settings file inside of `.npc` with the campaign name. This defaults to the name of the current directory, so change it as needed.

Options:

* `--types`: Within `paths.characters`, create every directory in the `type_paths` key.
* `--all`: Create all optional directories

## Create Session Files

The `session` command creates the files that I need at the very start of a gaming session. It looks for the last session log and plot file, named `Session Log \d+` and `Plot \d+` respectively, and extracts their sequence number. It increments that to get the number for the new files, then copies the old plot file to its new location, and copies the session log template to its new location. It will open all four files.

If anything goes wrong in this process (like malformatted file names) it will yell about it. Everything in a file name after "` - `" is ignored.

## Open Latest Plot and Session Files

The `latest` command opens the most recent plot and/or session file, so that I can easily find it without digging through a crowded folder.

The only option is what kind of file to open. Passing `session` opens the latest session; `plot` opens the latest plot; and `both` opens the latest plot and session together.

## Create a Character

Most subcommands involve creating a specific type of character. Character files are put into the base characters directory (`Characters/` by default), with further options based on their type, groups, and sometimes other factors.

Character templates are plain text files containing the body of the character sheet. When NPC creates a character for you, it copies this template and adds its tags to the top, above everything else.

All characters support the following options:

* `name`: The first positional argument is always the character/file name. The expected format is `character name - brief note`. During parsing, everything after "` - `" is ignored.
* `-g`, `--group`: Name of one or more groups that the character belongs to.
* `--dead`: Indicates that the character is dead, with optional notes about it.
* `--foreign`: Indicates that the character is foreign to the main campaign setting, with notes about where they are.
* `--location`: Describes where the character lives within the main campaign setting.

### Simple Characters

Simple characters have no unique options, they just change the character's type. They are created using a few commands:

The `new` command creates a new simple character using the named type. As long as that type has a defined template and type path, it'll work. There are a few accelerators for common simple types as well:

* `human`: Create a human. Type path is `Humans/`
* `fetch`: Create a fetch. Type path is `Fetches/`
* `goblin`: Create a goblin. Type path is `Goblins/`

### Changelings

The `changeling` command has a few more arguments than the simple characters, to deal with changeling-specific attributes. New changeling caracters use the base path `Characters/Changelings/`.

Options:

* `seeming`: Name of the changeling's Seeming. This will be added to the character's stats with notes about the Seeming Blessing and Curse, if the seeming is found in `support/seeming-kith.json`.
* `kith`: Name of their Kith. Also added to the character's stats with notes about the Kith Blessing, if the kith is found in `support/seeming-kith.json`.
* `--court`: Name of the changeling's court, if they have one. This is the first "group" checked when creating the path.
* `--motley`: Name of the changeling's motley, if known. This does not affect the path, but is added to the file as a tag.

Note: The `changeling` command is not the only way to create a changeling character. If you just want to make a new sheet without specifying the seeming or kith, and without using the changeling-specific options, you can do so by running `npc new changeling [name]`.

### Destination Path

All characters are put into a path based on the `hierarchy` key under `paths` in your settings. This hierarchy uses some simple rules to determine where a character will end up, both during creation and during reorganization:

1. Every slash (`/`) character denotes a new directory
2. Text inside of curly braces (`{}`) is treated as the name of a tag. The *first* value for that tag is fetched from the character and used as the directory name.
    * There's a special syntax that looks like `{tag?name}` which checks whether the character has that tag and if they do, it looks for a folder with the provided name.
3. Other text is used as the folder name without being changed

If a folder isn't found, it is skipped.

#### Meta Tags

There are a few "meta-tags" that can be used in place of a tag name. When one of these is found, it gets replaced by a real tag name before being looked up. The replacement is done based on your settings. These are the meta-tags and what they do:

* `type`: This looks up the value for `type_path` in your settings, based on the character's type. So a character with `@type human` will look in `types.human.type_path`.
* `type-unit`: This is replaced with the tag name for a small grouping appropriate for the character's type. Changelings use the value of `@motley`, werewolves use `@pack`, etc.
* `type-social`: Replaced with the tag for intermediate groupings of the character's type. Changelings use `@court`.
* `type-political`: Replaced with the tag for high-level groupings of the character's type. Changelings use `@freehold`.
* `type-groups`: Replaced with the tag for type-specific prestige groups. Changelings use `@entitlement`.

You can add your own substitutions by adding new keys within `tag_names` for one or more character types.

#### Special Words

There are some special words that can be used instead of a tag name. Each of them gives a certain more complex behavior:

* `rank` or `ranks`: Check each `@rank` value for the first `@group` in order.
* `groups`: Check all `@group` values in order.
* `groups+ranks`: Check each `@group` value along with all of its `@rank` values.
* `locations`: Check the first value of `@location` and then `@foreign`.

## Lint Character Files

The `lint` command checks character files for errors and inconsistencies. It's a good idea to run `npc lint` and fix all the problems it reports before you run `npc list`.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--fix`: Automatically fix a few problems. Most require manual fixing, though.
* `--report`: Only list the problems found and do not open the problematic files.
* `--strict`: Include optional checks.

Every character file is checked for these problems:

* A description is present
* The `@type` tag is present and has a value

Changeling character files are checked for these additional problems:

* The `@court` tag is either not present, or appears only once
* The `@motley` tag is either not present, or appears only once
* The `@seeming` tag is present and has a recognized value. This tag is added automatically if you use the `@changeling <seeming> <kith>` tag.
* The `@kith` tag is present and has a recognized value
* The stats specify the same seeming(s) as the `@seeming` tag(s)
* The stats specify the same kith(s) as the `@kith` tag(s)
* The notes for each seeming in the stats are present and correct. If `--fix` is passed, these notes will be updated.
* The notes for each kith in the stats are present and correct. If `--fix` is passed, these notes will be updated.
* The mantle merit appears at most once.
* The court of the Mantle merit (if present) matches the value of the `@court` tag.
* The court of the Court Goodwill merit (if present) does not match the value of the `@court` tag or the Mantle merit.

If `strict` is true, Changelings are also checked for the following:

* The Mantle merit is present for the same court as the `@court` tag.
* The Unseen Sense merit must not be present.

## Find Characters

The `find` command locates and opens characters by searching for text in their tags. The search is not case sensitive, so `npc find type:animal` will open every character with `@type Animal` and `@type animal`. You can search multiple tags by specifying multiple rules, like `npc find type:changeling "group: some gang"` to find changeling characters in the group Some Gang. Only characters that match all rules will be opened. To find characters who do *not* have certain text in a tag, use `~:`, like `npc find type~:human` to find all non-humans.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--dryrun`: Display the paths to the character files, but do not open them.

## Make an NPC Listing

The `list` command creates a page of character information. It ignores everything except the tags and description in each character file.

See the wiki page on [NPC Listings](https://github.com/aurule/npc/wiki/NPC-Listings) for details on how the different formats work.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--format`: Specify the format of the output. One of `markdown`, `md`, `json`, 'htm', or 'html'. Defaults to the value configured for `list_format` in settings.
* `--metadata`: Include metadata in the output. Can optionally specify the format of this metadata, if the main format supports it. Pass `default` to use the metadata type from your settings. Recognized values depend on the output format:
    - Markdown supports `mmd` for MultiMarkdown metadata, and `yfm` or `yaml` for YAML Front Matter metadata
    - HTML supports `meta` to put metadata in `<meta>` elements in the document `<head>`
* `--outfile`: Path where the output should go. If omitted (or you pass `-`), the output will go to stdout for chaining to another command.

## Dump Raw NPC Data

The `dump` command builds a list of parseable NPCs in json format. It ignores everything except the tags and description.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--sort`: Sort NPCs by name before dumping the output
* `--metadata`: Include metadata in the output. Uses the json default metadata from the settings and includes a few special fields.
* `--outfile`: Path where the output should go. If omitted (or you pass "`-`"), the output will go to stdout for chaining to another command.

## Reorganize Character Files

The `reorg` command builds default paths for all the characters and then moves them. It's inspired by that time when I realized I had 20 police officers in a sea of 130 human characters, and really wanted to put them in their own folder.

For an explanation of the default paths, see [Create a Character](#create-a-character).

Characters are always placed within the default characters path, regardless of the `search` argument.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--purge`: After moving the files, remove any empty directories within the root characters path
* `--verbose`: Show each change as it's made

## Edit Settings

While you can edit settings files manually (see [Configuration](#configuration) below), you can also use the `settings` command to easily open the desired settings file.

Options:

* `location`: The settings file to open. Use `user` to open your user settings, or `campaign` to open the current campaign's settings.
* `--type`: The type of settings to open. Leave it off to open the main settings file, or specify `changeling` to open the changeling-specific settings.

## Make Character Tag Reports

The `report` command lets you see how many characters there are for each unique value of a tag. It can make multiple tables at a time, one for each tag. See the wiki page on [Tag Reports](https://github.com/aurule/npc/wiki/Tag-Reports) for more information on how they work.

Options:

* `tags`: Name of one or more tags to analyze.
* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored. Added to the default ignore paths from settings
* `--format`: Specify the format of the output. One of `markdown`, `md`, `json`, `htm`, or `html`. Defaults to the value configured for `report_format` in settings.
* `--outfile`: Path where the output should go. If omitted (or you pass "`-`"), the output will go to stdout for chaining to another command.

# Gotchas

## Using both `search` and `ignore`

The `--search` and `--ignore` options interact in the following ways:

1. When the same directory is passed to `search` and `ignore`, `ignore` wins out and the directory is not scanned.
2. When a directory is passed to `search` and one of its child directories is passed to `ignore`, the child directory is not scanned.
3. When a directory is passed to `search` and a file within that directory is passed to `ignore`, the file is not scanned.
4. When a file is passed to `search` and `ignore`, `search` wins and the file is *always scanned*.

# Configuration

NPC reads config values from three separate files. These settings files use the json syntax and allow comments.

Default values are loaded from `support/settings-default.json` within the install directory. This file has extensive documentation of the available settings.

User settings are loaded from `~/.config/npc/settings.json`. Settings in this file will overwrite the default values.

Finally, campaign settings are loaded from `.npc/settings.json` within the current directory at runtime. Settings here will overwrite the default and user values.

To open these settings files easily, you can use the `settings` command.

## Type-Specific Settings

Additional settings files are loaded for each special character type. Their files are loaded from the same directories as above, but are named `settings-[type].json`. So, the Changeling settings for a campaign would be found in `.npc/settings-changeling.json`.

Each type-specific settings file starts with a single key that matches the name of the character type. This means that if you really want to, you can override type-specific settings within the normal `settings.json` file by putting the new values under the appropriate key. It's much better to keep the type-specific stuff separate, though.

### Changeling Settings

The keys inside `settings-changeling.json` specify what seemings and kiths are allowed, and what their blessings and curses are. The default list includes all seemings and kiths published by White Wolf for *Changeling: the Lost* as part of *New World of Darkness* first edition. To use a different list, you have to specify the entire new list of seemings or kiths that you want to use, even if only a few entries change.

Changing the blessing and curse text is less arduous. To add a new blessing or curse, just add a new entry to the appropriate dict. Its key must be the name of the seeming or kith to which it applies. To change an existing blessing or curse, just add a new entry using the same key. The old entry will be overwritten.

#### Validity

Every seeming *must* have a corresponding entry in both the `blessings` and `curses` dicts. Every kith *must* have a corresponding entry in the `blessings` dict. Kith curses are not supported by NPC and will be ignored.

Since both seemings and kiths share the same blessings and curses dictionaries, all seeming and kith names *should* be unique. If a seeming and kith have the same name, then both will have the same blessing. That's probably not what you want.

# Testing

## Requirements

* [pytest](http://doc.pytest.org/en/latest/) 2.8.5
* [pytest-qt](https://pytest-qt.readthedocs.io/en/latest/) 2.1.0
* [stdeb](https://pypi.python.org/pypi/stdeb) 0.8.5 - optional: only for building debian packages
* [coverage](https://coverage.readthedocs.io/en/coverage-4.4.1/) 4.4.1

These can all be installed with `pip -r requirements-dev.txt`.

## Running Tests

Go to the root project directory and run `python -m pytest` or `make test`.
