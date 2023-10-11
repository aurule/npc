.. _cli_describe_types:

describe types
==============

Show all configured character types.

-s, --system
    *Sometimes required.* Key of the game system to use. If run within a campaign, this defaults to the campaign's configured system. Outside of a campaign, this option is required.

.. note::

    When run within a campaign, ``npc describe types`` will include any types configured within that campaign.

Example:

.. code:: sh

    npc describe types -s fate-ep

.. code:: txt

     [Character Types for Eclipse Phase: Transhumanity's Fate]
    | Name       | Key        | Description                    |
    |------------|------------|--------------------------------|
    | Nameless   | nameless   | A background character or mook |
    | Main       | main       | A full character               |
    | Supporting | supporting | A supporting character         |
