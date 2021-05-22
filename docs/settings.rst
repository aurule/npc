.. Settings documentation

Settings
===============================

The settings for NPC allow you to customize its behavior at the user level and the campaign level. The various options are spread over a few files.

See the command :ref:`cmd-settings` for editing these files.

File Locations
--------------

User settings are stored under :file:`.config/npc/` in the user home directory. Campaign settings are stored in :file:`.npc/` within the campaign's directory. User settings override default settings, and campaign settings override user and default settings.

Settings Files
--------------

All of the settings files can either be in yaml or json. You should not use both formats for a given file, but if you do, the json file takes precedence. The examples here show yaml for brevity.

:file:`settings.yaml`
	The core settings file

:file:`settings-gui.yaml`
	Supplemental settings for the GUI

:file:`settings-changeling.yaml`
	Supplemental settings for the changeling character type

:file:`settings-werewolf.yaml`
	Supplemental settings for the werewolf character type

Core Settings
-------------

These settings apply to the entirety of NPC. You can set all kinds of options in this file:

* The paths used for character, session, and other campaign files
* Define character types
* Set up session and plot file templates
* Set properties for reports and listings

GUI Settings
------------

These settings only affect the graphical interface. It only has a single setting which sets the default type for the new character window.

Changeling Settings
-------------------

These settings only affect the creation and linting of changeling type characters. It is designed around :t:`Changeling: The Lost`. You can set the allowed seemings and their kiths, as well as written descriptions of the blessings for both seemings and kiths, and the curses for seemings.

Werewolf Settings
-----------------

These settings only affect the creation and linting of werewolf type characters. It is designed around :t:`Werewolf: The Forsaken`. You can set the allowed auspices, tribes of the moon, and pure tribes.
