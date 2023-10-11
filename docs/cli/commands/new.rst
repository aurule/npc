.. _cli_new:

new
=============

Create a new character.

type_key:
    **Required.** Type of the character.
-n, --name
    **Required.** Character name.
-m, --mnemonic
    **Required.** One or two words about the character. This becomes part of the character's filename, so make sure only to use safe characters.
-d, --description
    Bio, background, etc. of the character.
-t, --tag
    Tags to add to the new character, as ``tagname value`` pairs. This option can be given multiple times, with each instance added in order to the new character.

.. important::
    This command only works within an existing campaign.

Example:

.. code:: sh

    npc new supporting -n "Jack Goosington" -m "submariner thief" --tag org "Rumblers" -d "A very wet thief."

.. code:: txt

    Jack Goosington - submariner thief.fate

.. code::

    A very wet thief.

    @type supporting
    @org Rumblers
