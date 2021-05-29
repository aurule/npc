.. Main tags documentation

Core Tags
=========

Tags are the main way that NPC stores information about a character.

Tags (and :ref:`directives`) always start with a ``@`` character and are a single word. Everything after the tag name are its parameters::

	@tagname value

Each tag can appear more than once, with each additional value being stored alongside the first. :ref:`listing-templates` may or may not use the additional values for each tag, but they can be customized if you want those values to appear.

All tags that accept an arbitrary description support Markdown formatting. They are marked here for clarity.

These universal tags are valid for all character files, regardless of type or system.

.. _tag-type:

@type
-------------------------------

*required, must appear only once*

The character's type. Must be one of the values defined under ``types`` in the settings. The value changes how the character is treated for validation and which templates are used when rendering it for a :ref:`cmd-list`.

.. _tag-faketype:

@faketype
-------------------------------

*can appear at most once*

A fake type designation for the character. Must be one of the values defined under ``types`` in the settings. When :ref:`cmd-list` runs, it replaces the real :ref:`tag-type` with this value.

@name
-------------------------------

An additional name for this character, like a nickname or alternate identity. The primary value is populated from the filename, not the tags. To change that, use :ref:`tag-realname`.

.. _tag-realname:

@realname
-------------------------------

Explicitly define the primary name for the character. This is useful for characters that have non-latin names which might not be able to be used for a filename.

@title
-------------------------------

An honorific for the character. It's for things like "Blessed of Chireus" or "The Kingslayer". For titles that are bestowed as part of a hierarchy, it may be more appropriate to use :ref:`tag-rank` after a :ref:`tag-group`.

@appearance
-------------------------------

*markdown*

Description of the character's appearance.

@race
-------------------------------

Name of the character's race. This is primarily for classic fantasy settings with races like dwarf, elf, human, etc. In other games, this could be used for more modern racial demographics.

@age
-------------------------------

The age of the character. Intended to be a number like 42, but can be a description if preferred.

.. _tag-group:

@group
-------------------------------

The name of a group to which the character belongs.

.. _tag-rank:

@rank
-------------------------------

The name of a rank that the character holds within a group. This tag is automatically associated with the group tag immediately preceeding it.

.. _tag-location:

@location
-------------------------------

The place where the character is found. This is meant to be used for characters who live outside of the main location of the game. It's also handy for game's which are spread out and have characters in many locations by default.

.. _tag-foreign:

@foreign
-------------------------------

*does not need a value*

Designate the character as foreign to the game's setting. This might mean that they're from another country, another city, etc. It can also serve to indicate characters who are so remote that they effectively cannot be contacted.

@wanderer
-------------------------------

*does not need a value*

Indicates that the character is itinerant or otherwise has no permanent home. If a value is supplied, it's probably the region where the character wanders.

.. _tag-dead:

@dead
-------------------------------

*markdown, does not need a value*

Indicates that the character is dead. Optionally, a description can be given for how they died.

@employer
-------------------------------

Names the character's place of work.

.. _tag-desc:

Description Tag
-------------------------------

*markdown*

The description tag does not appear explicitly within character files. Instead, it serves as a hidden tag which accepts all of the untagged text within the file's :ref:`sheet-tags`. It can still be hidden with ``@hide description`` if desired.

Unrecognized tags
-----------------

All other tags are classified as an unrecognized tag. They're still stored in the parsed character, but will be flagged by the :ref:`cmd-lint` command. Other character types can define their own tags which will be recognized appropriately.
