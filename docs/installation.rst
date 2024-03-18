.. Core invocation documentation

.. _install:

Installing NPC
===============================

The best way to install NPC right now is to download the binaries from the `latest release <https://github.com/aurule/npc/releases/latest>`_. Once downloaded, you'll have to unpack the archive and ensure the :file:`npc_cli` and :file:`npc_gui` binaries are in your path. I like to symlink :file:`npc_cli` to :file:`npc` on my posix systems. Binaries are available for Linux and Windows.

.. note::

    I have not created bespoke packages or installers yet. These instructions will be updated if those become available.

Once installed, you'll have access to the ``npc`` cli utility and gui app. See :ref:`cli_home` and :ref:`guide_cli_quickstart` for an intro to using the command line program, and :ref:`gui_home` and :ref:`guide_gui_quickstart` for the graphical app.

Installing from Source
-----------------------

You can install the latest development version of NPC by installing it from source. This is also the only way to run NPC on MacOS right now.

To do so, follow these steps:

#. Clone the repository
#. Ensure you have Python 3.11 or later
#. Install the system packages which correspond to the packages listed in :file:`requirements.txt`
#. You will likely have to install NPC as an editable system package using ``pip install -e .`` from the repo's root
#. Create a script named :file:`npc` somewhere in your path (like :file:`~/bin`) which invokes ``python3 npc``

After that, you can update with a simple `git pull`.

Development
-----------

For working on NPC, follow these steps:

#. Clone the repository
#. Create a Python 3.11 virtualenv and activate it
#. Install the dev requirements:

.. code:: sh

   pip install -r requirements-dev.txt

4. Install npc as an editable package:

.. code:: sh

    pip install -e .

To make sure that everything works, run ``poe test``.

5. If dependencies may have updated, you can run ``pip-sync requirements-dev.txt`` to synchronize your installed packages with NPC's requirements. Just remember to run ``pip install -e .`` afterward, as pip-sync will remove the local package.
