.. Main tags documentation

Core Tags
=========

Tags are the main way that NPC stores information about a character.

Tags (and :ref:`directives`) always start with a ``@`` character and are a single word. Everything after the tag name are its parameters::

	@tagname value

These universal tags are valid for all character files, regardless of type or system.

.. _tag-type:

@type
-------------------------------

.. _tag-faketype:

@faketype
-------------------------------

@name
-------------------------------

@realname
-------------------------------

@title
-------------------------------

@appearance
-------------------------------

@race
-------------------------------

@age
-------------------------------

.. _tag-group:

@group
-------------------------------

@rank
-------------------------------

.. _tag-location:

@location
-------------------------------

.. _tag-foreign:

@foreign
-------------------------------

@wanderer
-------------------------------

.. _tag-dead:

@dead
-------------------------------

@employer
-------------------------------

Unrecognized tags
-----------------

All other tags are classified as an unrecognized tag. They're still stored in the parsed character, but will be flagged by the :ref:`cmd-lint` command. Other character types can define their own tags which will be recognized appropriately.
