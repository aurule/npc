.. _cli_describe_systems:

describe systems
================

Show all configured game systems.

Example:

.. code:: sh

    npc describe systems

.. code:: text

                                                  [Configured Systems]
    | Name                                | Key          | Description                                              |
    |-------------------------------------|--------------|----------------------------------------------------------|
    | Generic                             | generic      | A generic system for representing normal, boring people  |
    | World of Darkness                   | wod          | The original dark urban fantasy system for modern nights |
    | Dungeons & Dragons 3.5e             | dnd3         | D&D 3.5! Just the right amount of crunch                 |
    | Fate Core                           | fate         | A rules-light storytelling system                        |
    | New World of Darkness               | nwod         | Urban fantasy in the modern era                          |
    | Eclipse Phase: Transhumanity's Fate | fate-ep      | Transhuman adventure in FATE                             |
    | Fate: Venture City                  | fate-venture | Superheroes in FATE                                      |

When run within a campaign, it will also show which system the campaign is using:

.. code:: text

    Currently using Eclipse Phase: Transhumanity's Fate
