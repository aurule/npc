.. Commands documentation

Commands
===============================

These are the commands available in NPC. They share a few common options.

All Commands
------------

All NPC commands share these common options.

Common Options
~~~~~~~~~~~~~~

-h, --help
	Show help information for the command.

--debug
	Forces NPC to show every error that occurs, even when those errors are harmless. Can be useful for figuring out problems with settings.

-b, --batch
	Prevents NPC from opening any files that are relevant to the command. Without this switch, each command may open files in the configured editor.

init
-------------------------------

.. code-block:: bash

	npc init --name "Cowboy Town"

Set up a folder for use by NPC. This creates a blank settings file along with a few directories. By default, ``init`` creates the following::

	.npc/
	    settings.json
	Characters/
	Plot/
	Session History/

Every directory listed under ``paths.required`` in the :ref:`settings` is created as well as the special ``.npc`` configuration directory.

Options
~~~~~~~

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

.. code-block:: bash

	npc settings --defaults

Open a settings file and optionally also its corresponding defaults. See :ref:`settings` for an overview of what each file can configure.

Options
~~~~~~~

-t <type>, --type <type>
	Open a supplementary settings file. Options are:

	* gui
	* changeling
	* werewolf

-d, --defaults
	Also open the corresponding defaults file for the settings type you're editing. The default files are well documented with explanations of each settings option.

session
-------------------------------

Create and open the files for a new game session. Each invocation creates a new copy of the previous session's plot file, and a fresh copy of the session template. It also creates a fresh copy of every template configured in the settings under ``story.templates.plot_extras`` and ``story.templates.session_extras``. See :ref:`session-templates` for what can go in these files.

Any files which already exist are left alone. This means you can manually create a new plot file for the next session and when you run ``npc session``, only the session and extras will be created. All files will still be opened in your editor.

latest
-------------------------------

.. code-block:: bash

	npc latest plot

Open the session and plot files with the highest number in their names. This cannot open files created through the ``plot_extras`` or ``session_extras`` keys.

Arguments
~~~~~~~~~

*thingtype*
	File type to open. Can be one of:

	* both (default)
	* plot
	* session

new
-------------------------------

h, human
-------------------------------

c, changeling
-------------------------------

w, werewolf
-------------------------------

lint
-------------------------------

Check character files for errors and missing tags. Prints a list of files and the detected errors to the console.

Basic validity requires that:

	* The character has a description
	* All tags have values
	* All tag values to be hidden exist

Additional validity checks are added for some character types.

Options
~~~~~~~

-f, --fix
	Automatically fix certain problems. This is most useful for Changeling characters, as it can update the curse and blessing descriptions to match the character's kith and seeming tags.

-o, --open
	Open all files with errors, in addition to printing a list. This option is turned off by default to avoid spamming the editor with potentially hundreds of files at once.

--strict
	Be more stringent about minor or inconsequential errors and warnings. With this option, more files will be flagged.

reorg
-------------------------------

Reorganize character files by moving them to their most appropriate directory. Because this command can make files hard to find, it does not move anything by default. Instead, it shows a rundown of what it would do. When you're satisfied, use the ``--commit`` option to move the files.

Character paths are chosen based on the path hierarchy defined in the settings under ``paths.hierarchy``.

Options
~~~~~~~

--commit
	Move the files. Without this option, ``reorg`` will leave the files where they are and only show a listing of what would change.

--search <paths>
	Look in these paths for character files. Individual files are loaded directly, and directories are searched recursively.

--ignore <paths>
	Skip these paths when looking for character files.

-p, --purge
	After moving the files, remove character directories which are now empty. This option will *not* add anything to the changes list, as it only works after files have been moved. Does nothing unless ``--commit`` is also passed.

-v, --verbose
	Show changes as they are made. Does nothing unless ``--commit`` is also passed.

.. _cmd-list:

list
-------------------------------

dump
-------------------------------

.. code-block:: bash

    npc dump -m -o dump.json

Export all parsed characters as a json file. This file contains all of the parsed tags, but nothing from the rest of the file contents.

Each character entry is an object with the character file's path and an object containing its tags.

.. code-block:: json

    {
    	"path": "path/to/character_file.nwod",
    	"tags": {
    		"type": "changeling",
    		"name": "Talon Bronzeheart",
    		"seeming": "Fairest",
    		"kith": "Draconic"
    	}
    }

The ``--metadata`` option adds a special metadata object to the json output. It contains various bits of information about the campaign and the file:

.. code-block:: json

    {
    	"meta": true,
    	"title": "Campaign Name",
    	"created": "Fri, May 28 08:30PM",
    	"npc": "1.4.2"
    }

Options
~~~~~~~

-s, --do_sort
	Sort the characters before exporting them. The default sort order is from the settings value ``dump.sort_by``.

--sort_by <tag[, tag2]>
	Override the default sort order. Requires a comma-separated list of tag names.

-m, --metadata
	Add metadata information to the output.

-o, --outfile <file path>
	Save the output to the given file. Besides a path, this option accepts a single hyphen (``-``) which writes the output to stdout, usable for piping into another command.

report
-------------------------------

.. code-block:: bash

	npc report location

Create a tabular report on the values of one or more tags across all character files.

Options
~~~~~~~

-t, --format
	The format for the report. Default value is in the settings as ``report.default_format``.

-o, --outfile
	File where the generated report will be output. Defaults to the special hyphen value ``-``, which prints the report to the console.

--search <paths>
	Look in these paths for character files. Individual files are loaded directly, and directories are searched recursively.

--ignore <paths>
	Skip these paths when looking for character files.

find
-------------------------------

.. code-block:: bash

	npc find "group:town council"

Open character files which have the given tag contents.

Files are found using the supplied tag rules, which take the format ``tag:value``. Files that have ``value`` anywhere in the named tag will be included in the results. To find files which do not contain a given value, use ``tag~:value``. To find files which have a tag present regardless of its contents, use ``tag:``.

For convenience, upper and lower case are ignored when matching values.

Options
~~~~~~~

--search <paths>
	Look in these paths for character files. Individual files are loaded directly, and directories are searched recursively.

--ignore <paths>
	Skip these paths when looking for character files.

-d, --dryrun
	Show the files that match the criteria, but do not open them.
