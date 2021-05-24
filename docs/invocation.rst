.. Core invocation documentation

Running NPC
===============================

NPC is mainly run as a command-line program. It also has a QT-based windowed application.

Command Line Interface
-------------------------------

The CLI is the main way to use NPC. Once installed, invoke it with ``npc [command]``.

Choosing the Campaign Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unless run with the ``--campaign`` option, NPC will assume that the current directory is part of the campaign's directory structure. It walks back through the directories until it finds the special :file:`.npc/` directory. The directory containing :file:`.npc/` is then used as the campaign's base directory.

Options
~~~~~~~~~

--campaign <directory>

    Change to the passed directory before running the command.

-h, --help

    Show a help message and exit. This is supported for each command as well.

--version

    Print the current program version and exit. Prevents any commands from running.

Graphical Interface
-------------------------------

The graphical interface is more limited than the CLI. It is invoked with ``npc-gui``.
