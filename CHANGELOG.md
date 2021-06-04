# Change Log

This file documents the changes made in each release. I didn't start maintaining this until I was in the middle of developing v1.3.0, so it's more sparse than it should be.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/) (mostly).

## 1.4.2 [unreleased]

### Added

* The `race`, `age`, and `employer` tags will no longer give an "unrecognized tag" error when linting
* Now recognizes `.fate` and `.npc` file extensions

### Changed

* Improved documentation
* The `faketype` tag can now only appear once
* The YAML format is now the default for settings files and takes precedence over JSON

### Removed

* No longer recognizes `.dfrpg` file extension. Use `.fate` instead.

## 1.4.1

### Added

* The `session` command can now create additional files alongside the plot and session log
* New `employer` group-like tag
* Internal caching in the template formatter should speed up generating large character lists
* YAML is now supported for configuration files alongside JSON. If a JSON file and a YAML file are both present with the same name other than the file extension, the JSON file will take precedence. This is due to the massively slower parsing speed of YAML files. All configuration files are present in both formats for reference.
* Discrete classes for more involved character types: Changeling, Werewolf, and Spirit
* New `@keep` directive flag to prevent a character from being moved by the reorg command
* The `changeling` command accepts two new arguments: `--freehold` and `--entitlement`. These set the new character's freehold name and entitlement name, respectively.
* It's now possible to hide a single tag value
* New `@nolint` directive flag to exclude a character from linting

### Changed

* The `session` command got rewritten
    - Now reports which path was missing if either the plot path or session path are not accessible
    - Its settings structure is different: see the "story" section in "settings-default.json"
    - Template names are now used to locate existing files as well as generate new file names. They must contain NNN in the filename.
    - Character case in template names are now duplicated in generated files
    - Templates can have special "NNN" and "((COPY))" keywords that get replaced on file creation
* The `latest` command now reports which path was missing if either the plot path or session path are not accessible
* The `latest` command no longer requires the input "both" to return all the latest files. Instead, all files are returned by default and using a keyword limits what is returned. The function argument is now optional.
* Files are opened by the system default editor for that type, or the "editor" value from settings.
* The `settings` command now detects which format is in use
* Character objects now store their tags in `self.tags` instead of directly on the object
    - Tag getting and setting has been moved from Character objects to their TagContainer and stored Tag objects
* Strict character validation now flags the class type if there's a mismatch
* Character path is now accessed through the `path` attribute, not through `tags['path']`
    - The `has_path` property has been removed. Test path presence by testing `character.path` directly
* Each character type can have its own list of supported tags
    - This improves the support for oddball or unique tags, like auspice and ban, and allows more accurate linting
* The `list` command no longer automatically opens all files. Instead, there's a new `--open` option to do that. The old `--report` option has been removed.
* The `@hide` directive can now hide a tag, a single tag value, all the subvalues for a group value, or a single subvalue for a single group value. The syntax is straightforward: `@hide tagname >> tag value >> subvalue`.
    - The special `subtags` element hides the subtag entirely, so `@hide group >> Orchestra >> subtags` will hide all `rank` elements for the `Orchestra` group.

### Fixed

* New character objects won't choke on a non-list attribute value

### Removed

* The `@hidegroup` and `@hideranks` directives are deprecated and should be replaced using the new syntax

## 1.4.0

Werewolves are supported! Along with the tags, character sheet, and templates for that, there are a few other neat features.

* Werewolf characters
* Spirit characters
* Default tag values for new characters
* Separate ignored paths for each command (requires settings change)
* Better character sorting (requires settings change)

### Added

* New `@werewolf` tag for specifying werewolf type and auspice on one line
* Settings now has a `tag_defaults` key that sets default tag values for newly created characters.
* Settings files now ignore trailing commas
* Sort character listings and dumps by any tag or set of tags, each in ascending or descending order. You'll have to update your settings files to use the new `sort_by` format.
* Sort by type-dependent tags
* Configurable list headings for character tags.
* Set the base heading level in settings.
* Turn off sorting for character listings altogether using `--no_sort`
* Force listing to contain only body content using `--partial`
* New setting for default character type in GUI
* Settings for allowed werewolf auspices and tribes
* Customizable sectioners to support complex sorting of character listings

### Changed

* Ignored paths can now be specified for each command separately, in addition to universal ignored paths. You'll have to change your settings files to use the new `ignore` section format.
* The `list` command's `--sort` argument is renamed `--sort_by`.
* The `include_metadata` argument to formatters is now `metadata_format`.
* Refactored the listing renderers into objects

### Fixed

### Removed

* The `fetch` and `goblin` character creation commands are gone. Use `new fetch` or `new goblin` instead.

## 1.3.1

The path hierarchy is here! This new setting allows you to configure exactly where your character files are placed based on their tags. See the readme for more details.

This release comes with a few enhancements, including a new way to configure character organization, and a big change to the settings file format. You will need to update your user and campaign settings; the old versions will not work!

### Added

* New `hierarchy` setting for configuring where character files are placed
* New `campaign` option to the GUI that allows it to start in a given campaign directory
* New `location` tag for specifying a non-foreign character location
* List command and helpers now support a progress bar callback
* CLI list output now shows a fancy progress bar
    - Supports integration with other progress bars for the gui
* Explicit result objects for success state
* New `latest` command to open the latest plot file, session file, or both
* The `init` command can now create user-specified directories during campaign setup from the `additional_paths` key.
* Markdown listings now accept "multimarkdown" as a metadata format. It works the same as passing "mmd".
* New `report` option to the lint command that allows the reported problems to be shown without opening all of the affected files.
* Can now clear recent campaign menu in the GUI
* The `find` command now accepts the asterisk (`*`) character when searching on a field. It returns all characters that have any value for that field.
* New `Open Latest` menu in the GUI to open the most recent plot or session file.
* Character names are no longer limited to word-like characters and can include any letters or typographical marks you want

### Changed

* Change cli file layout
* Added more explicit result classes and removed old error codes
* Refactor session command into story module
* Change main settings file to use a different layout. User and campaign settings will need to be updated.
* Added features to the markdown lister to bring it closer to the html lister's feature set
    - Section headings are now supported, though not used by default
    - Footers are supported
* Clarified what the `--batch` option actually does
* The `reorg` command is now safe by default. When run with no options, it will just display the actions that it would take. To actually move files (and optionally delete directories), use the new `--commit` option.

### Fixed

* Changeling linter thought every kith was unrecognized
* Fix extra `p` tags in parsed markdown in html listings
* Fix listing output for characters with a bare `foreign` tag
* Parser no longer chokes on special characters in character name from file name

### Removed

* The `reorg` command no longer has a `dryrun` option.

## 1.3.0

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
* New `@freehold` tag for changeling characters
* Freehold is shown in listings, if provided

### Changed

* Settings
    - The changeling settings format now requires that kith names are grouped by seeming
    - Improved formatting for results from the changeling settings linter
    - Metadata blocks now contain the NPC version number
    - Changeling kiths can only appear under one seeming
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
    - First freehold is used when creating a character path
    - Character paths will try to add a directory matching the first `@foreign` tag, if present

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
