.. Custom tags documentation

.. _cust_tags:

Configuring Tags
===============================

The ``npc.tags`` key defines every tag available to character files. The command :ref:`cli_info` can show details about the configured tags for a given system or campaign. Adding a new tag is as easy as adding a new entry under ``npc.tags`` in either your user settings or the campaign's settings. You can also override and change an existing tag by adding an entry with that tag's name.

Tag Format
----------

Each entry within ``npc.tags`` is the name of a tag, followed by these attributes:

:desc: :octicon:`note` :bdg-warning:`required` A single line of text describing the basic purpose of this tag.

:doc: :octicon:`book` A multiline block of text describing the details and nuances of this tag.

:replaced_by: :octicon:`note` The name of a different tag which is used instead of this tag. The replacement should be limited to a specific scope, like a system or type.

:required: :octicon:`tasklist` Whether this tag must appear in the character file.

:min: :octicon:`number` The minimum number of times this tag must appear in the character file. A positive number implies ``required=true``.

:max: :octicon:`number` The maximum number of times this tag may appear in the character file.

:values: :octicon:`list-ordered` Explicit list of allowed values for this tag.

:allow_empty: :octicon:`tasklist` Whether this tag can appear with no value.

:no_value: :octicon:`tasklist` Whether this tag must not have a value.

:subtags: :octicon:`code-square` An object with additional tags which will be stored *within* this tag.

Examples
--------

One of the most common reasons to add a tag is to support some facet of a new system. The FATE system, for example, requires every character to have a Concept. This new ``concept`` tag can be defined as follows:

.. code:: yaml

	tags:
	    concept:
	      desc: The character's high concept
	      required: true
	      max: 1

The ``@concept`` tag will now be recognized in character files in a campaign that uses the FATE system.
