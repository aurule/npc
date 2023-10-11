.. _cli_report_values:

report values
=============

Show a how many times each unique value appears for the given tag.

.. important::
    This command only works within an existing campaign.

-t, --tag
    Tag to analyze
-c, --context
    Parent context if tag is a subtag. Use ``*`` to disregard parent. Only needed if :option:`--tag` is a subtag like ``role``.

Example:

.. code:: sh

    npc report values -t type

.. code:: txt

    [@type tag values report]
    | Value      | Count |
    |------------|-------|
    | supporting | 3     |
