# Changelog for NPC v2.0.2

Another small release with some bug fixes and convenience tags.

## Added

* New `@monster` tag for generic dnd3 creatures
* New `@async` tag for fate-ep system
* Match Value subpath component to add a static named directory when a tag matches a value
* New `history` attribute for all tags to track changes to the definition by version
* [api] Added first(...) helper to character_view to simplify some template logic

## Changed

* Campaign info command shows full system name

## Fixed

* Crash when parsing a subtag that did not exist for a given parent
* Tags that cannot accept a value are assigned one during creation
* Migrations run on legacy user settings
* [api] All subpath components now respect the only_existing flag independently
* Crash when loading a character with utf-8 symbols

For changes in previous versions, see the files in `changelog/`.
