Character file names have three parts: the character's name, their mnemonic, and the file extension.

.. code::

    Grete Mann - good boy.npc
    ^            ^        ^
    name         mnemonic extension

The name and mnemonic *must* be separated by a space, hyphen, and then another space (`` - ``). The file extension can either be ``.npc``, or the key of the campaign's game system, like ``.fate`` or ``.nwod``.

If a character's name cannot be part of a valid filename, usually because of special characters, use a dumbed-down version for the filename and add a :ref:`tag_realname` tag to the file with the correct name.
