.. _sys_dnd5:

Dungeons & Dragons 5e
#####################

:bdg-info:`key: dnd5`

D&D Fifth Edition. Modern, streamlined, and popular.

Released in 2014, Dungeons & Dragons 5e became more and more popular over the next ten years. It features a streamlined system for playing action combat in a fantasy setting, and can be tweaked (both officially and unofficially) to work with all kinds of other themes.


Related Links
=============

.. button-link:: https://dnd.wizards.com/products?category=tabletop-rpg
    :color: primary
    :shadow:

    Books

.. button-link:: https://dnd.wizards.com/resources/systems-reference-document
    :color: primary
    :shadow:

    Official SRD

.. button-link:: https://5e.d20srd.org/
    :color: primary
    :shadow:

    Online SRD



New and Changed Tags
====================

.. _tag_dnd5_class:

@class
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of a class in which the character has levels


Subtags
~~~~~~~

These tags can appear immediately after @class and will be associated with that tag instance's value.

.. _tag_dnd5_class_level:

@level
~~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Number of levels the character has in this class



.. _tag_dnd5_faith:

@faith
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the deity the character worships

With whole classes built around worship, it can be very important to keep track of which god(s) a character prays to.


.. _tag_dnd5_monster:

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

    dnd5/*

.. include:: components/types/dnd5_table.rst