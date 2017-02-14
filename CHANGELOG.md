# Change Log

This file documents the changes made in each release. I didn't start maintaining this until I was in the middle of developing v1.3.0, so it's more sparse than it should be.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/) (mostly).

## 1.3.0 [Unreleased]

### Highlights

This release features a brand new GUI based on Qt. It has character creation, character search, and basic campaign management, with more to come soon. This means that PyQt5 is now part of the installation requirements.

The CLI has a new `find` command which makes it easy to get character files based on their tags.

### Added

* New GUI based on PyQt5
    - Open campaign, with open recent menu
    - Create new character
    - Open campaign and user settings
    - Search for characters (in-progress)
* New CLI command `npc find` to find characters by their tag contents
* Makefile to automate uic builds and tests
* Settings
    - `campaign_name` stores the name of the current campaign, or the default name to use when not in campaign settings.
    - `plot_ext` sets the default file extension of the first plot file in a new campaign
    - Better documentation of default settings file
* Result class has a new `printable` variable for storing command output that could be shown to the user
* Commands
    - `init` has new `dryrun` and `verbose` flags
    - New `find` entry point for finding characters by their tag contents.
    - New `find_characters` function to search the tags of a set of characters and return matching objects
* Character class
    - New method `build_header` to create tags from a Character object
    - More validations
    - New method `tag_contains` to determine whether the entries for a tag contain a value
* Greatly improved test coverage

### Changed

* Settings
    - The changeling settings format now requires that kith names are grouped by seeming
    - Improved formatting for results from the changeling settings linter
    - Metadata blocks now contain the NPC version number
* CLI
    - Moved CLI interface to its own module: `npc.cli`
    - The `--batch` and `--debug` options now live under each command. This means they must go after the command name instead of in front of it.
* Character class
    - Moved Character class to its own module: `npc.character.Character`
    - The `path` item in Character objects now has the same special handling as `description`
    - `has_items` will raise an `OutOfBoundsError` if `threshold` is less than 1
    - `valid` is now False until `validate` is called
    - `type` is now required to have a non-whitespace value
* Commands
    - Commands now live in their own package and some have been renamed
    - `init` command sets the `campaign_name` when creating the campaign settings file
    - `reorg` command had its `dry` flag renamed to `dryrun` to match the flag on `npc.commands.init`
    - Refactored `reorg`, `lint`, and `init` commands to use `Result.printable` instead of directly printing output
    - Reorganized commands:
        + `listing` is now in its own module as `listing.make_list`
        + `create_changeling` and `create_simple` now share a module as `create_character.changeling` and `create_character.standard`
    - Courtless status is shown in html and markdown character listings

### Removed

* The `npc.main` package is no more. To start the cli, use `npc.cli.start(argv)`
* Removed unused `default` arg to `Character.get_remaining`. It will always return an empty list if the tag isn't present.

### Fixed

* `Character.validate` correctly propagates the `strict` param to type-specific validators
* Passing None to `Character.append` will add the named tag with no data, so it acts as a flag
* Methods in `Character` will no longer add empty elements when called on non-existing fields

## 1.2.5 - 2017-01-27

### Added

* The readme has a version badge
* Default settings files have some instructions about their use

### Changed

* Updated copyright date
* Serializable args to the CLI are handled more elegantly. Should have no impact on use.

### Fixed

* Result objects no longer throw an exception when testing their booliness
