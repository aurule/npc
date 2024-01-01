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

``npc new`` creates a new character file using the type, name, mnemonic, description, and tags provided. It uses the configured subpaths to pick a directory for new characters. See :ref:`cust_campaign_char_subpaths` for how to configure these.

.. tip::

    To add a tag which does not allow any values (like :ref:`tag_foreign`), supply whatever value you want. It will be removed before the character is created.

Example:

.. code:: sh

    npc new supporting -n "Jack Goosington" -m "submariner thief" --tag org Rumblers -d "A very wet thief."

Creates the file:

.. code:: text

    Jack Goosington - submariner thief.fate

With these contents:

.. code::

    A very wet thief.

    @type supporting
    @org Rumblers
