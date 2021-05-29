.. Character file format documentation

Character Files
===============

Character files are specially formatted text files which NPC can parse to pull out tagged information and certain data blocks.

Each sheet has multiple sections separated by headers::

	--Header Name--

Only two sections are parsed by NPC: the tags section (which has no header) and the Stats section.

.. _sheet-tags:

Tags Section
------------

The tags section starts at the top of the file and goes until the first section header is encountered. This is the only section where tags are recognized and parsed. All untagged text is treated as implicit values for the hidden description tag.

.. _sheet-stats:

Stats Section
-------------



Other Sections
--------------

All other sections are treated as plain text blobs and do not get parsed by NPC. Their contents are not available for commands.
