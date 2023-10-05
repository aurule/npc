.. _sys_wod_vampire:

Vampire
#######

:bdg-info:`World of Darkness`

A blood-sucking creature cursed to the night




New and Changed Tags
====================

.. _tag_wod_vampire_gen:

@gen
----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The vampire's generation


.. _tag_wod_vampire_sire:

@sire
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the vampire who turned this character into another vampire

Sometimes vampiric lineage is a really big deal. Other times, it's just nice to know who's been fangin' around.

.. _tag_wod_vampire_clan:

@clan
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The vampire's clan


.. _tag_wod_vampire_sect:

@sect
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Major political body to which the vampire belongs


Allowed Values
~~~~~~~~~~~~~~
- Camarilla

- Sabbat

- Anarch

- Independent


Subtags
~~~~~~~

These tags can appear immediately after @sect and will be associated with that tag instance's value.

.. _tag_wod_vampire_sect_status:

@status
~~~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

A status held by the vampire which is recognized in this sect


.. _tag_wod_vampire_sect_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

A high-level role the vampire fulfills within the sect

Some roles are not limited to a single city, but are important to the functioning of an entire sect. Archons, Cardinals, and Prisci would be noted here.


.. _tag_wod_vampire_crew:

@crew
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the pack, gang, or coterie to which this vampire belongs

Vampires often form small social groups so they can work together toward a shared purpose. They have different names in different sects, but the outcome is the same.

Subtags
~~~~~~~

These tags can appear immediately after @crew and will be associated with that tag instance's value.

.. _tag_wod_vampire_crew_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has in their crew

Not all crews have distinct roles. This tag is primarily useful in Sabbat packs to note the ductus, abbot, and priest. It can also be used to note the less rigid roles certain vamipres play within their crew.


.. _tag_wod_vampire_city:

@city
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the domain, diocese, etc. that the vampire calls home


Subtags
~~~~~~~

These tags can appear immediately after @city and will be associated with that tag instance's value.

.. _tag_wod_vampire_city_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has in their city

This tag is best used for positions like prince, bishop, harpy, etc. that are only important within that city. If a position is recognized more universally, it's probably best represented using the title tag as well.


