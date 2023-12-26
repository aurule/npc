.. Basic usage guide

.. _basics:

Basic Usage
===========

NPC is based around using plain text files to manage the characters, sessions, plots, and other important information of a tabletop RPG game. By standardizing file locations and adding just a touch of formatting, NPC is able to parse that campaign info and speed up many repetitive tasks for the GM.

Campaigns
---------

NPC assumes that every campaign is entirely contained within a single directory. Within this directory are special subdirectories where characters, plot files, session files, etc. will be stored.

While it can be customized (see :ref:`cust_campaign`), this is what a typical NPC-compatable campaign directory looks like:

.. code::

    My Campaign/
    ├─ .npc/
    │  ├─ settings.yaml
    ├─ Characters/
    ├─ Plot/
    ├─ Session History/


.. tip::

    If you're using the NPC CLI, the command :ref:`cli_init` will create this structure for you, while also filling out some useful fields in your campaign settings.

After a bit of use, the directory might look like this:

.. code::

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

One of the most important settings for a campaign is its system. See :ref:`ref_systems` for the ones built into NPC, and :ref:`cust_systems` for how to set up your own.

Managed Files
-------------

As of version 2.0.0, NPC manages the following campaign files:

- everything within :file:`Characters/`
- Plot/Plot NN.md
- Session History/Session NN.md

Other directories, and other files or folders within the Plot and Session History subdirectories, are not touched by NPC. Use them however you want!

.. note::

    The files within :file:`.npc/` are not typically written by NPC, but of course it depends strongly on their values. The one exception is when migrating between versions. Since new versions of NPC might need to tweak some configuration keys, the files might be updated in those circumstances.

Character Files
---------------

While the contents of plot and session files are largely up to you, character files have an additional constraint: tags. NPC uses the tags in each file to keep track of important data about that character.

File Name
~~~~~~~~~

.. include:: /reference/snippets/character_file_names.rst

File Contents
~~~~~~~~~~~~~

Character files start with their tag section. That section ends with the first header line, which is usually ``--Notes--``.

Here are some sample contents for ``Badd Mann - bad guy.npc``:

.. code::

    @org Evil League of Evil
    @role Member

    @location Hartsford, CT

    --Notes--

    Badd is the evil member of the Mann family. Hates his brother Caoil.

As of NPC 2.0.0, everything after the first header can be formatted as you like. This may change in the future.
