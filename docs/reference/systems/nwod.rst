.. _sys_nwod:

New World of Darkness
#####################

:bdg-info:`key: nwod`

Urban fantasy in the modern era

Building on the success of the World of Darkness setting, White Wolf released New World of Darkness to unify the various monsters and allow shared play. It was rebranded later as Chronicles of Darkness and got a 2nd edition release.

The New World of Darkness system defined here tries to capture the unique quirks of each character type by using lots of type-specific tags. It is only compatible with NWoD / CWoD 1st edition. CWoD 2nd edition uses different tags and different meanings for shared tags, so it does not work with the NWoD character types.


Metatags
========

These metatags will be expanded into their ``static`` and ``match`` tags when a character file is loaded. Groups of those tags will be condensed into a metatag when a character is saved. For an explanation of how metatags work, see :ref:`cust_system_metatags`.

@changeling
-----------

Shorthand for setting type, seeming, and kith for changelings


Static Tags:

- @type: ``changeling``

Matches Tags:

- @seeming
- @kith

separator: " "

greedy: no


Character Types
===============

.. toctree::
    :hidden:
    :glob:

    nwod/*

.. include:: components/types/nwod_table.rst