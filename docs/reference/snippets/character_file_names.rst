Character file names have three parts: the character's name, their mnemonic, and the file extension.

.. code::

    Grete Mann - goodest boy.npc
    ^            ^           ^
    name         mnemonic    extension

The name and mnemonic *must* be separated by a space, hyphen, and then another space (``n - m``).

The default file extension is ``.npc``, but a more specific extension can be used instead based on the extension used for the character type's sheet template. This is usually the same as the key of the campaign's game system, like ``.fate`` or ``.nwod``.

If a character's name cannot be part of a valid filename, usually because of special characters, use a simplified version for the filename and add a :ref:`tag_realname` tag to the file with the correct name. This is handled automatically by NPC when it creates a new character, but is important to remember when you create or rename character files by hand.
