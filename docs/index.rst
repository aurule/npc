.. NPC documentation master file, created by
   sphinx-quickstart on Fri May 21 20:13:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NPC's documentation!
===============================

NPC is a tool to make my life easier when I'm running tabletop RPG games. It automates and streamlines a few tedious tasks for me, like:

- Creating new session logs
- Creating new plot planning files
- Creating and organizing character files
- Generating a list of characters to publish
- And more!

Unlike other game management systems, NPC is designed to use plain text files to manage each game's resources, from characters to session notes. This means that even on devices which can't run NPC, you still have full access to all of your game's data. For more on how NPC organizes campaigns, see :ref:`basics`.

To get started in general, take a look at :ref:`install` and :ref:`guide_cli_quickstart`.

Disclaimer
----------

NPC is very much a personal project. It works well enough for me to use for my weekly games, and I think it might be useful for others. That said, if you use it and come up with suggestions or bugs, open an issue! I'll at least take a look!

.. toctree::
   :hidden:

   installation
   basics
   customization/index
   cli/quickstart

.. toctree::
   :caption: Customization
   :hidden:

   customization/index
   customization/campaigns
   customization/systems
   customization/tags
   customization/listings

.. toctree::
   :caption: Reference
   :hidden:

   reference/settings
   reference/tags/index
   reference/deprecated_tags/index
   reference/reserved_tags
   reference/systems/index

.. toctree::
   :caption: NPC CLI
   :hidden:

   cli/index
   cli/quickstart
   cli/commands

.. toctree::
   :caption: NPC GUI
   :hidden:

   gui/index

.. toctree::
   :caption: NPC API
   :hidden:

   source/npc
   source/npc_cli
   source/npc_gui
