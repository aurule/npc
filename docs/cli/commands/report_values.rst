.. _cli_report_values:

report values
=============

Show a how many times each unique value appears for the given tag.

-t, --tag
    Tag to analyze
-c, --context
    Parent context if tag is a subtag. Use ``*`` to disregard parent. Only needed if :option:`--tag` is a subtag like ``role``.

.. important::

    This command only works within an existing campaign.

Example:

.. code:: sh

    npc report values -t type

.. code:: text

    [@type tag values report]
    | Value      | Count |
    |------------|-------|
    | supporting | 3     |
