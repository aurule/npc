.. _cookbook_new_campaign:

Create a Campaign
=================

To make a new campaign, first create the folder you want to use for the campaign.

.. code:: sh

    mkdir "My Campaign"

Then, NPC can set up the basic folders and files for you.

.. tab-set::

    .. tab-item:: CLI

        Run the :ref:`cli_init` command. It will prompt you for all the important campaign info.

        .. code:: sh

            npc init "My Campaign"

    .. tab-item:: GUI

        Go to :guilabel:`&File > New Campaign`. You'll be prompted to open the new campaign's directory, then shown a popup which asks you to fill in all the important campaign info.

The folders for a new campaign can be changed by editing the values in your user settings file. See :ref:`cookbook_open_settings` for how to edit that file.
