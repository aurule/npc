.. _characters:

Character Files
===============

While the contents of plot and session files are largely up to you, character files are more structured. Their file names carry important information, and their contents always begin with a set of tags.

File Name
---------

.. include:: /reference/snippets/character_file_names.rst

File Contents
-------------

Character files are broken into sections. The first section is always the tag section, which has no header. Other sections are denoted by a header line, which looks like ``--Notes--`` or ``--Stats--``.

.. note::

    In NPC 2.0.0, everything outside of the tag section can be formatted as you like. This may change in the future.

Tag Section
~~~~~~~~~~~

Character files start with their tag section. The most important tag is :ref:`tag_type`, which is also the only tag that is *always* required. Its value is based on whichever of the :ref:`ref_systems` the campaign is using. The character type can change which other tags are available, which is why the type is so important.

Plain text in the tag section is stored as the character description and usually talks about who they are, their history, what they want in the story, etc.

The tag section ends with the first header line, which is usually ``--Notes--``.

.. code-block::
    :caption: Example file contents for ``Badd Mann - bad guy.npc``

    An evil man from a family rife with conflict. Badd hates his
    brother, Caoil, for being too damn cool.

    @org Evil League of Evil
    @role Member

    @location Hartsford, CT

    --Notes--

    Badd is the evil member of the Mann family. Hates his brother Caoil.

