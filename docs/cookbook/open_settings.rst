.. _cookbook_open_settings:

Open Settings Files
===================

NPC can open the directory of your user settings without an active campaign. If you want to browse to a campaign's settings, you will first need to :ref:`cookbook_open_campaign`.

.. tab-set::

    .. tab-item:: CLI

        Run the :ref:`cli_settings` command with the appropriate ``--location`` option (if needed).

        .. code:: sh

            npc settings --location user

    .. tab-item:: GUI

        To open the user settings, go to :guilabel:`Session > Browse User Settings`. To open the settings for the current campaign, go to :guilabel:`Session > Browse Campaign Settings`. Both of these options will open a file browser at the location of the settings file.
