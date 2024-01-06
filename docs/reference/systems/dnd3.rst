.. _sys_dnd3:

Dungeons & Dragons 3.5e
#######################

:bdg-info:`key: dnd3`

D&D 3.5! Just the right amount of crunch

Released in 2003, Dungeons & Dragons v3.5 is a refined version of the D&D 3rd Edition rules available under the Open Game License. Classic sword and sorcery fantasy.


Related Links
=============

.. button-link:: https://www.drivethrurpg.com/browse/pub/44/Wizards-of-the-Coast?filters=0_0_44833_0_0
    :color: primary
    :shadow:

    Books

.. button-link:: https://www.d20srd.org/index.htm
    :color: primary
    :shadow:

    SRD



New and Changed Tags
====================

.. _tag_dnd3_class:

@class
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of a class in which the character has levels


Subtags
~~~~~~~

These tags can appear immediately after @class and will be associated with that tag instance's value.

.. _tag_dnd3_class_level:

@level
~~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Number of levels the character has in this class



.. _tag_dnd3_faith:

@faith
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the deity the character worships

With whole classes built around worship, it can be very important to keep track of which god(s) a character prays to.


.. _tag_dnd3_monster:

@monster
--------

:bdg-secondary:`Optional`
:bdg-info:`Value required`
:bdg-info:`Max 1`

Designate this as a generic sheet for a given type of monster

It is very handy to have a way to represent the many monsters PCs fight in D&D, but these monsters are not necessarily real characters. More, they are often reused over and over again. This tag makes it clear that the given npc is more of a template than an individual creature with goals and motives.

The value of this tag should be the "creature type" as listed in the monster manual, or other original source.




Character Types
===============

.. toctree::
    :hidden:
    :glob:

    dnd3/*

.. include:: components/types/dnd3_table.rst