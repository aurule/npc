.. Basic usage guide

.. _basics:

Campaigns
============

NPC is built around using a single campaign folder to contain all of the files relevant to a given tabletop RPG game. Files for characters, sessions, plots, and other important information is organized within the campaign directory in specific folders following various (configurable) rules.

Campaign Structure
------------------

NPC is very flexible and requires only a single folder to be present in order to treat a folder as a campaign: :file:`.npc/`. That special directory holds NPC's configuration files for the campaign. All other directories can be customized (see :ref:`cust_campaign`).

Without extra customization, these are the standard directories found in a campaign:

.. code-block::
    :caption: Default campaign directory layout

    My Campaign/
    ├─ .npc/
    │  ├─ settings.yaml
    ├─ Characters/
    ├─ Plot/
    ├─ Session History/


.. tip::

    Creating a new campaign either by running :ref:`cli_init` or using the New Campaign dialog will create these folders for you, as well as help you fill out some useful fields in your campaign settings.

After a bit of use, the directory might look like this:

.. code-block::
    :caption: Default directories with some example files

    My Campaign/
    ├─ .npc/
    │  ├─ settings.yaml
    ├─ Characters/
    │  ├─ Badd Mann - bad guy.npc
    │  ├─ Caoil Mann - cool guy.npc
    ├─ Plot/
    │  ├─ planning/
    │  │  ├─ future threats.md
    │  ├─ Plot 01.md
    │  ├─ Plot 02.md
    │  ├─ Plot 03.md
    ├─ Session History/
    │  ├─ Session 01.md
    │  ├─ Session 02.md
    │  ├─ Session 03.md

Campaign Properties
-------------------

Whether created manually or through NPC, every campaign needs to know what game system it's using. NPC includes a number of :ref:`ref_systems` already, and you can add your own as needed (see :ref:`cust_systems`).


When you create a campaign using the cli :ref:`cli_init` command or the gui New Campaign dialog, this will be set automatically. If you're making a campaign by hand, or if you need to change the game system after the fact, you'll have to edit the campaign's settings file. See :ref:`cust_campaign` for how to do that.


Managed Files
-------------

As of version 2.0.0, NPC manages the following campaign files:

- everything within :file:`Characters/`
- :file:`Plot/Plot NN.md`
- :file:`Session History/Session NN.md`

Other directories, and other files or folders within the Plot and Session History subdirectories, are not touched by NPC. Use them however you want!
