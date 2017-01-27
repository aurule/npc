# Change Log

This file documents the changes made in each release. I didn't start maintaining this until I was in the middle of developing v1.3.0, so it's more sparse than it should be.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/) (mostly).

## [Unreleased]
### Added
* UI based on PyQt5
* Makefile to automate uic builds and tests
* New `campaign_name` setting
* `npc.commands.init` now sets the `campaign_name` when creating the campaign settings file
* `npc.commands.init` has new `dryrun` and `verbose` flags
* Result class has a new `printable` variable
    - The meaning and name of this var is likely to change over time
* Better test coverage
* NPC version number is reported in all metadata output
* New `plot_ext` setting for the default file extension of the first plot file in a new campaign
* Better documentation of default settings
* New method `npc.util.Character.build_header` to create tags from a Character object

### Changed
* The CLI interface now lives in npc.cli
* Nicer formatting for results from the changeling settings linter
* Commands that used to print output now return a list of printed lines in their Result's `printable` var. The caller can decide what to do with them.
    - Very in-progress.
* `npc.commands.reorg` had its `dry` flag renamed to `dryrun` to match the flag on `npc.commands.init`
* The `path` item in Character objects now has the same special handling as `description`
* `Character.get_remaining` now accepts a `default` argument
* The changeling settings format now requires that kith names are grouped by seeming
* The `--batch` and `--debug` options in the CLI now live under each command. This means they must go after the command name instead of in front of it.
* `Character.get_remaining` no longer accepts a `default` argument. If the named tag is not present, it will always return an empty list.
* `Character.has_items` will raise an `OutOfBoundsError` if `threshold` is less than 1

### Removed
* `npc.main` has gone away

## 1.2.5 - 2017-01-27
### Added
* The readme now has a version badge
* Default settings files have some instructions about their use

### Changed
* Updated copyright date
* Serializable args to the CLI are handled more elegantly. Should have no impact on use.

### Fixed
* Result objects no longer throw an exception when testing their booliness
