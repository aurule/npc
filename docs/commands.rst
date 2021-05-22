.. Commands documentation

Commands
===============================

These are the commands available in NPC. They share a few common options.

All Commands
------------

Common Arguments
~~~~~~~~~~~~~~~~

-h, --help
	Show help information for the command.

--debug
	Forces NPC to show every error that occurs, even when those errors are harmless. Can be useful for figuring out problems with settings.

-b, --batch
	Prevents NPC from opening any files that are relevant to the command. Without this switch, each command may open files in the configured editor.

init
-------------------------------

Set up a folder for use by NPC. This creates a blank settings file along with a few directories. By default, ``init`` creates the following::

	.npc/
	    settings.json
	Characters/
	Plot/
	Session History/

Every directory listed under ``paths.required`` in the settings is created as well as the special ``.npc`` configuration directory.

Arguments
~~~~~~~~~

-n <campaign name>, --name <campaign name>
	Set the name for the campaign. This is saved in ``.npc/settings.json``. Without this option, the value ``null`` will be used instead.

-t, --types
	Create additional directories for each character type. These are created underneath the ``Characters/`` directory.

-a, --all
	Create all additional directories. Right now, this includes directories for all character types.

-v, --verbose
	List every directory and file that is created.

--dryrun
	Show the directories and files that would be created, but do not actually create them.

.. _cmd-settings:

settings
-------------------------------

Open a settings file

Arguments
~~~~~~~~~

-t <type>, --type <type>
	Open a supplementary settings file. Options are:

	* gui
	* changeling
	* werewolf

-d, --defaults
	Also open the corresponding defaults file for the settings type you're editing. The default files are well documented with explanations of each settings option.

session
-------------------------------

latest
-------------------------------

new
-------------------------------

human
-------------------------------

changeling
-------------------------------

werewolf
-------------------------------

lint
-------------------------------

reorg
-------------------------------

list
-------------------------------

dump
-------------------------------

report
-------------------------------

find
-------------------------------
