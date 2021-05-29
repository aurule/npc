.. Directive documentation

.. _directives:

Directives
==========

Directives change the way that NPC treats a character file for certain commands.

.. _tag-hide:

@hide
-------------------------------

Remove a tag or one of its values from the character when running the :ref:`cmd-list` command. The format for ``@hide`` is more complex than other tags:

To completely remove a tag from the character, use::

	@hide tagname

To remove a single value for a tag, use::

	@hide tagname >> valuename

To remove all of the ranks for a named group, but leave the group visible, use::

	@hide group >> group name >> subtags

Finally, to remove a single rank from a named group, use::

	@hide group >> group name >> rank name

@hidegroup
-------------------------------

Hide a single named group.

.. deprecated:: 1.4.1
	Use ``@hide group >> group name`` instead

@hideranks
-------------------------------

Hide all the ranks for a particular named group.

.. deprecated:: 1.4.1
	Use ``@hide group >> group name >> subtags`` instead


.. _tag-skip:

@skip
-------------------------------

Ignore this character when running the :ref:`cmd-list` command.

.. _tag-nolint:

@nolint
-------------------------------

Do not lint this character when running :ref:`cmd-lint`.

.. _tag-keep:

@keep
-------------------------------

Do not move this character when running :ref:`cmd-reorg`.
