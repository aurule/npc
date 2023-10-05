.. _sys_nwod_changeling:

Changeling
##########

:bdg-info:`New World of Darkness`

A human who was captured by the fae and returned to the mundane world




New and Changed Tags
====================

.. _tag_nwod_changeling_seeming:

@seeming
--------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The broad grouping of the changeling's fae kin.


Allowed Values
~~~~~~~~~~~~~~
- beast

- darkling

- elemental

- fairest

- ogre

- wizened


.. _tag_nwod_changeling_kith:

@kith
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The more specific grouping of the changeling's fae kin. A subset of their seeming.


.. _tag_nwod_changeling_mask:

@mask
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

How the changeling appears to humans and other non-fae.


.. _tag_nwod_changeling_mien:

@mien
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

How the changeling appears to other changelings, as well as goblins and other fae creatures.


.. _tag_nwod_changeling_appearance:

@appearance
-----------

:bdg-danger:`Replaced by @mask`
:bdg-secondary:`Optional`
:bdg-info:`Value required`

Not specific enough for changeling appearances

Changeling appearance is broken into the mask ane mien. Use those tags instead.

.. _tag_nwod_changeling_motley:

@motley
-------

:bdg-secondary:`Optional`
:bdg-info:`Value required`
:bdg-info:`Max 1`

Tight-knit group the changeling belongs to, like a family

This is a magically-bound group of changelings which often lives together. Changelings socialize all the time outside of their motley, but it's these people the changeling comes home to.

.. _tag_nwod_changeling_freehold:

@freehold
---------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the main political group to which the changeling belongs

Usually tied to a human city. Freeholds almost always have multiple courts within them.

Subtags
~~~~~~~

These tags can appear immediately after @freehold and will be associated with that tag instance's value.

.. _tag_nwod_changeling_freehold_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Official position the changeling has in their freehold

This is a position outside of their court. Freehold-wide roles are not common, but some freeholds use them to help unify the disparate courts.


.. _tag_nwod_changeling_court:

@court
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`
:bdg-info:`Max 1`

Court the changeling belongs to

Usually one of the seasonal courts: Winter, Spring, Summer, or Autumn.

Subtags
~~~~~~~

These tags can appear immediately after @court and will be associated with that tag instance's value.

.. _tag_nwod_changeling_court_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of an official position the changeling holds within their court

Most courts have a seasonal king or queen, and many courts have optional positions. Changelings in these roles help run the court or forward its goals within their freehold.


.. _tag_nwod_changeling_entitlement:

@entitlement
------------

:bdg-secondary:`Optional`
:bdg-info:`Value required`
:bdg-info:`Max 1`

Magical, prestigious group the changeling belongs to.

These elite groups have specific criteria for changelings who wish to join. Some require a certain seeming, membership in a court, or displays of skill.

Subtags
~~~~~~~

These tags can appear immediately after @entitlement and will be associated with that tag instance's value.

.. _tag_nwod_changeling_entitlement_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Official position the changeling holds within their entitlement.

Not all entitlements have specific roles. For those that do, achieving a certain role can be a major motivation for members.


.. _tag_nwod_changeling_other:

@other
------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The changeling's fetch


