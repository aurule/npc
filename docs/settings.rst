.. Settings documentation

.. _settings:

Settings
===============================

The settings for NPC allow you to customize its behavior at the user level and the campaign level. The various options are spread over a few files.

See the command :ref:`cmd-settings` for editing these files.

File Locations
--------------

User settings are stored under :file:`.config/npc/` in the user home directory. Campaign settings are stored in :file:`.npc/` within the campaign's directory. User settings override default settings, and campaign settings override user and default settings.

Settings Files
--------------

All of the settings files can either be in `yaml`_ or `json`_ syntax. You should not use two files for the same settings, but if you do, the yaml file takes precedence. When using JSON, comments starting with a double slash ``//`` are supported, even though these are not part of the json syntax. The examples here show yaml for brevity.

:file:`settings.yaml`
	The core settings file

:file:`settings-changeling.yaml`
	Supplemental settings for the changeling character type

:file:`settings-werewolf.yaml`
	Supplemental settings for the werewolf character type

Core Settings
-------------

These settings apply to the entirety of NPC. You can set all kinds of options in this file:

* The paths used for character, session, and other campaign files
* Define character types
* Set up session and plot file :ref:`templates`
* Set properties for reports and listings

Changeling Settings
-------------------

These settings only affect the creation and linting of changeling type characters. It is designed around :t:`Changeling: The Lost`. You can set the allowed seemings and their kiths, as well as written descriptions of the blessings for both seemings and kiths, and the curses for seemings.

Validity
~~~~~~~~

Changeling settings have a few additional checks to make sure that they're usable. Any errors will show up when NPC is run and must be fixed before it will do anything.

* All seemings must have an entry under ``blessings``
* All seemings must have an entry under ``curses``
* All kiths must have an entry under ``blessings``
* Each kith must appear under exactly one seeming

Werewolf Settings
-----------------

These settings only affect the creation and linting of werewolf type characters. It is designed around :t:`Werewolf: The Forsaken`. You can set the allowed auspices, tribes of the moon, and pure tribes.

Validity
~~~~~~~~

Werewolf settings have a few additional checks to make sure that they're usable. Any errors will show up when NPC is run and must be fixed before it will do anything.

* Each tribe name must appear under exactly one of ``moon`` or ``pure``

.. _`yaml`: https://www.tutorialspoint.com/yaml/yaml_basics.htm
.. _`json`: https://www.tutorialspoint.com/json/json_syntax.htm
