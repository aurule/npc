.. Settings documentation

.. _settings:

Configuration
===============================

You can change NPC's settings for your user and for each individual campaign. User settings override the built-in defaults, and campaign settings override user settings and defaults.

The command :ref:`cmd-settings` can be used to open the user settings file or current campaign settings file, but it's useful to open the entire settings directory too.

File Locations
--------------

User settings are stored in a different directory based on the current operating system. On Mac OSX, it's :file:`~/Library/Application Support/NPC`. On Unix systems, it's :file:`~/.config/NPC`. On Windows, it's :file:`C:\\Users\\<user>\\AppData\\Roaming\\`.
[#app_dir]_

Campaign settings are stored under :file:`.npc/` within the campaign's directory.

In either location, the settings file itself is :file:`settings.yaml`. Other files can be put in the settings directory (or certain subdirectories) to configure the game system or its character types, or to provide templates for character listings.

The Settings File
-----------------

All settings files are written in `yaml`_ syntax. The main settings file, :file:`settings.yaml`, has two main sections. The ``npc`` section holds core info like the tags available to character files. The ``campaign`` section holds campaign-specific info, like where to find different files.

Version
-------

The ``npc.version`` key is **always** required and **must not** be changed manually. It defines the version of NPC which last touched the file.

Tags
----

the ``npc.tags`` key defines every tag available to character files. The command :ref:`cmd-info` can show details about the configured tags for a given system or campaign. Adding a new tag is as easy as adding a new entry under ``npc.tags`` in either your user settings or the campaign's settings. You can also override and change an existing tag by adding an entry with that tag's name.

Tag Format
~~~~~~~~~~

Each entry within ``npc.tags`` is the name of a tag, followed by these attributes:

:desc: :bdg-warning:`required` A single line of text describing the basic purpose of this tag.

:doc: A multiline block of text describing the details and nuances of this tag.

:replaced_by: The name of a different tag which is used instead of this tag. The replacement should be limited to a specific scope, like a system or type. If the tag is replaced globally, deprecated the tag instead.

:required: Whether this tag must appear in the character file.

:min:
	The minimum number of times this tag must appear in the character file. A positive number implies ``required=true``.

:max: The maximum number of times this tag may appear in the character file.

:values: Explicit list of allowed values for this tag.

:allow_empty: Whether this tag can appear with no value.

:no_value: Whether this tag must not have a value.

:subtags: An object with additional tags which will be stored *within* this tag.

.. _`yaml`: https://www.tutorialspoint.com/yaml/yaml_basics.htm
.. _`json`: https://www.tutorialspoint.com/json/json_syntax.htm

.. [#app_dir] This location is determined using `Click <https://click.palletsprojects.com/en/8.1.x/api/#click.get_app_dir>`_
