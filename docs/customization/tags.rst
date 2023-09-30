.. Custom tags documentation

Configuring Tags
===============================

The ``npc.tags`` key defines every tag available to character files. The command :ref:`cmd-info` can show details about the configured tags for a given system or campaign. Adding a new tag is as easy as adding a new entry under ``npc.tags`` in either your user settings or the campaign's settings. You can also override and change an existing tag by adding an entry with that tag's name.

Tag Format
----------

Each entry within ``npc.tags`` is the name of a tag, followed by these attributes:

:desc: :bdg-warning:`required` A single line of text describing the basic purpose of this tag.

:doc: A multiline block of text describing the details and nuances of this tag.

:replaced_by: The name of a different tag which is used instead of this tag. The replacement should be limited to a specific scope, like a system or type. If the tag is replaced globally, deprecated the tag instead.

:required: Whether this tag must appear in the character file.

:min:
	The minimum number of times this tag must appear in the character file. A positive number implies ``required=true``.

:max: The maximum number of times this tag may appear in the character file.

:values: Explicit list of allowed values for this tag.

:allow_empty: Whether this tag can appear with no value.

:no_value: Whether this tag must not have a value.

:subtags: An object with additional tags which will be stored *within* this tag.

Examples
--------

:bdg-danger:`TODO`
