.. _cli_lint:

lint
=============

Check character files for errors.

--edit, --no-edit
    Whether to open all character files with errors (default False).

.. important::

    This command only works within an existing campaign.

Example:

.. code:: sh

    npc lint

.. code:: text

    Fake Mann has 4 errors:
    * Error in tag @trouble: required, but not present
    * Error in tag @trouble: too few. 1 required, found 0
    * Error in tag @description: no definition found
    * Error in tag @wanderer: no definition found
