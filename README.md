# About

I created NPC to make my life easier when running New World of Darkness tabletop RPGs. It automates and streamlines a few tedious tasks like creating new session logs and character sheets.

This project is very much a work in progress. It works well enough for me to use at my weekly game, but that's it.

## Requirements

NPC requires at least Python 3.5.0.

## Installation

First, simply clone the NPC repo into the desired install directory. Then make a symlink to somewhere in your path:

`ln -s ~/bin/npc npc.py`

# Usage

The functionality of NPC is split among a few sub-commands. Each one encompasses a single high-level task, and has its own options.

By default, NPC will open whatever files are relevant to the subcommand. To prevent this from happening, supply `--batch` or `-b` before the subcommand name.

## Set Up Directories

The `init` command creates the basic directories that NPC expects to find. Every directory under the `paths` key in the settings file is created.

## Create Session Files

The `session` command creates the files that I need at the very start of a gaming session. It looks for the last session log and plot file, named `Session Log \d+` and `Plot \d+` respectively, and extracts their sequence number. It increments that to get the number for the new files, then copies the old plot file to its new location, and copies the session log template to its new location. It will open all four files.

If anything goes wrong in this process (mismatched numbers is the most common, followed by malformatted file names) it will yell about it. Everything in a file name after "` - `" is ignored.

## Create a Character

Most subcommands involve creating a specific type of character. Character files are put into the base characters directory (`Characters/` by default), with further options based on their type, groups, and sometimes other factors.

All characters support the following options:

* `name`: The first positional argument is always the character/file name. The expected format is `character name - brief note`. During parsing, everything after "` - `" is ignored.
* `-g`, `--group`: Name of one or more groups that the character belongs to.

### Simple Characters

These character creation commands don't add any options, they just change the character's type, and potentially the path of the created character sheet.

Relevant commands:

* `human`: Create a human. Type path is `Humans/`
* `fetch`: Create a fetch. Type path is `Fetches/`
* `goblin`: Create a goblin. Type path is `Goblins/`

#### Destination Path

Simple characters all use the same rules for determining the destination path. Like all characters, they start in `Characters/`. Other directories are then appended, assuming they already exist. If these directories do not exist, they are not created.

These are the directories that are appended, in order:

1. Type path, like `Humans/`
2. First listed group name, if given (like `Police/`)
    * Other group names are also tried, in order.

Here are some examples:

> The path `Characters/Humans/Police` exists. Running `npc human "Prakash Dupene" -g Police` will start in `Characters/`, and try to find `Humans/`. Since it can, it will then look in `Characters/Humans/` for `Police/`. Finding that directory, and having no more groups to check, it will create the file `Characters/Humans/Police/Prakash Dupene.nwod` and open it.

> With the same path, running `npc human "John Doe" -g "Bulldog Barons"` will also start in `Characters/` and try to find `Humans/`. Since it can, it will then look in `Characters/Humans/` for `Bulldog Barons/`. That directory does not exist, and there are no more groups to try, so it will create `Characters/Humans/John Doe.nwod` and open it.

> With the same path, running `npc human "Hans Fritz" -g "Funkadelic" "Police"` will quickly find `Characters/Humans/`. It will look there for `Funkadelic/`, but that directory does not exist. It will then look in `Characters/Humans/` for `Police/`, and find it. There are no more groups to try, so it will create `Characters/Humans/Police/Hans Fritz.nwod`.

### Changelings

The `changeling` command has a few more arguments than the simple characters, to deal with changeling-specific attributes. New changeling caracters use the base path `Characters/Changelings/`.

Options:

* `seeming`: Name of the changeling's Seeming. This will be added to the character's stats with notes about the Seeming Blessing and Curse, if the seeming is found in `support/seeming-kith.json`.
* `kith`: Name of their Kith. Also added to the character's stats with notes about the Kith Blessing, if the kith is found in `support/seeming-kith.json`.
* `--court`: Name of the changeling's court, if they have one. This is the first "group" checked when creating the path.
* `--motley`: Name of the changeling's motley, if known. This does not affect the path, but is added to the file as a tag.

## Lint Character Files

The `lint` command checks character files for errors and inconsistencies. It's a good idea to run `npc lint` and fix all the problems it reports before you run `npc list`.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored.
* `--fix`: Automatically fix a few problems. Most require manual fixing, though.

Every character file is checked for these problems:

* A description is present
* The `@type` tag is present and has a value

Changeling character files are checked for these additional problems:

* The `@seeming` tag is present and has a recognized value. This tag is added automatically if you use the `@changeling <seeming> <kith>` tag.
* The `@kith` tag is present and has a recognized value
* The stats specify the same seeming(s) as the `@seeming` tag(s)
* The stats specify the same kith(s) as the `@kith` tag(s)
* The notes for each seeming in the stats are present and correct. If `--fix` is passed, these notes will be updated.
* The notes for each kith in the stats are present and correct. If `--fix` is passed, these notes will be updated.

## Make NPC Listing

The `list` command builds a list of parseable NPCs. It ignores everything except the tags and description.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored.
* `--format`: Specify the format of the output. One of `markdown`, `md`, or `json`. Defaults to `markdown`.
* `--metadata`: Include metadata in the output. Can optionally specify the format of this metadata, if the main format supports it. Recognized values when used with the `markdown` format are `mmd` for MultiMarkdown metadata, and `yfm` or `yaml` for YAML Front Matter metadata.
* `--outfile`: Path where the output should go. If omitted (or you pass "`-`"), the output will go to stdout for chaining to another command.

## Update Dependent Files

The `update` command isn't implemented yet. I plan to have it update motley membership based on the `@motley` tags in each character file.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored.

## Reorganize Character Files

The `reorg` command builds default paths for all the characters and then moves them. It's inspired by that time when I realized I had 20 police officers in a sea of 130 human characters, and really wanted to put them in their own folder.

Options:

* `--search`: Only look in these files and directories. Defaults to the base characters path.
* `--ignore`: Ignore these files and directories. By default, nothing is ignored.
* `--purge`: After moving the files, remove any empty directories within the root characters path
* `--verbose`: Show each change as it's made

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

User settings are loaded from `~/.config/npc/settings-user.json`. Settings in this file will overwrite the default values.

Finally, campaign settings are loaded from `.npc/settings-campaign.json` within the current directory at runtime. Settings here will overwrite the default and user values.
