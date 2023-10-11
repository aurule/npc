.. CLI Commands documentation

Commands
===============================

The ``npc`` utility provides many commands for interacting with campaigns, game systems, and characters. While some commands have override options for flexibility, almost all customization is handled by NPC's configuration files. See :ref:`conf_home` for how to customize NPC for your games.

.. note::

	Some commands can only be executed within a campaign directory, or one of its subdirectories. When run outside of a campaign, these commands will show a warning and immediately exit.

Commands are often broken into subcommands. Invocation might look something like ``npc session`` or ``npc describe tags``.

.. toctree::
    :hidden:
    :glob:
    :maxdepth: 2

    commands/*


Tables of Commands
------------------

.. include:: components/command_table.rst
