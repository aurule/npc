.. _cli_describe_tag:

describe tag
=============

Show details for the named tag.

-s, --system
    *Sometimes required.* Key of the game system to use. If run within a campaign, this defaults to the campaign's configured system. Outside of a campaign, this option is required.
-t, --type
    Key of the character type to use for finding the tag.
-a, --tag
    **Required.** Name of the tag to show.
-c, --context
    *Sometimes required.* Name of the tag's parent, if looking for a subtag. Required when :option:`--tag` is a subtag.

Example:

.. code:: sh

    npc describe tag -s fate-ep -t main -a refresh

.. code:: text

    Tag: @refresh
    Number of fate points the character starts with

    Usually only relevant for PCs, since NPCs use a shared pool of GM fate points
    in every scene.
