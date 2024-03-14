.. Settings documentation

.. _conf_home:

Core Configuration
===============================

You can change NPC's settings for your user and for each individual campaign. User settings override the built-in defaults, and campaign settings override user settings and defaults.

The CLI command :ref:`cli_settings` can be used to open the user settings file or current campaign settings file, but it's useful to check out the entire settings directory too.

.. _cust_file_locations:

File Locations
--------------

User settings are stored in a different directory based on the current operating system. On Mac OSX, it's :file:`~/Library/Application Support/NPC`. On Unix systems, it's :file:`~/.config/NPC`. On Windows, it's :file:`C:\\Users\\<user>\\AppData\\Roaming\\`.
[#app_dir]_

Campaign settings are stored under :file:`.npc/` within the campaign's directory.

In either location, the settings file itself is :file:`settings.yaml`. Other files can be put in the settings directory (or certain subdirectories) to configure the game system or its character types, or to provide templates for character listings.

The Settings File
-----------------

All settings files are written in `yaml`_ syntax. The main settings file, :file:`settings.yaml`, has two main sections. The ``npc`` section holds core info like the tags available to character files. The ``campaign`` section holds campaign-specific info, like where to find different files.

See :ref:`ref_settings` for an explanation of all of the available settings keys.

Global Campaign Settings
------------------------

While any key can appear in your user settings, there is one campaign key that is most useful to configure there: ``campaign.create_on_init``. This key is a list of folder names that will be created for every new campaign.

.. _`yaml`: https://www.tutorialspoint.com/yaml/yaml_basics.htm

.. [#app_dir] This location is determined using `Click <https://click.palletsprojects.com/en/8.1.x/api/#click.get_app_dir>`_
