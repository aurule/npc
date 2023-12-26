.. _cli_reorg:

reorg
=============

Reorganize character files.

--interactive, --batch
    Whether to prompt before making changes, or make them automatically. Default ``--interactive``.
--keep-empty, --del-empty
    Whether to keep empty directories after all files are moved. Default ``--keep-empty``.
--use-existing, --add-folders
    Whether to only use existing ones or allow making new folders. Default ``--use-existing``.

.. important::

    This command only works within an existing campaign.

As moving around a bunch of files can be disruptive, this command by default
uses "interactive" mode, where the changes which would be made are displayed
and you are prompted whether to apply them. In batch mode, the changes are
applied automatically.

If two or more characters would try to claim the same file, errors are
shown.

``npc reorg`` uses the same subpaths that :ref:`cli_new` uses to pick a directory for new characters. See :ref:`cust_campaign_char_subpaths` for how to configure these.

Example:

.. code:: sh

    npc reorg

.. code:: text

    These characters will be moved:

    | Character          | Destination                  |
    |--------------------|------------------------------|
    | Fake Mann - tester | Dead/Fake Mann - tester.fate |

    Do you want to apply these changes? [y/N]:
