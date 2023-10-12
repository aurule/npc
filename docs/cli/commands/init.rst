.. _cli_init:

init
=============

Create the basic folders to set up an npc campaign.

*campaign_dir*
    The directory to initialize as a campaign. Defaults to the current directory.

-n, --name
    Name for the new campaign. You will be prompted if you don't provide this argument.
-d, --desc
    Description of the new campaign. You will be prompted if you don't provide this argument.
-s, --system
    Game system the campaign will use. You will be prompted to pick one of the available systems if you don't provide this argument.

.. note::

    The arguments to ``npc init`` are all optional, as this command is designed to be used interactively. The options are there so that it can still be used in non-interactive shells, like from another program.

The directories created are derived from your settings. See :ref:`cust_campaign_new` for how to customize these directories.

Example:

.. code:: sh

    npc init

.. code:: text

    Campaign name: Test Campaign
    Campaign description: A campaign to test with
    Game system (generic, wod, dnd3, fate, nwod, fate-ep, fate-venture): fate
    Setting up /home/me/campaigns/test_campaign...
    Creating .npc/ config directory
    Creating required directories:
      Characters/
      Session History/
      Plot/
    Done
