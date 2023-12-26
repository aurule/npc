.. _cli_describe_type:

describe type
=============

Show details about a single character type.

-s, --system
    *Sometimes required.* Key of the game system to use. If run within a campaign, this defaults to the campaign's configured system. Outside of a campaign, this option is required.
-t, --type
    **Required.** Key of the character type to show.

Example:

.. code:: sh

    npc describe type -s fate-ep -t main

.. code:: text

    Character Type: Main
    ID: main
    File suffix: .fate
    Sheet template: /home/me/config/npc/types/fate-ep/main.fate

    A full character
