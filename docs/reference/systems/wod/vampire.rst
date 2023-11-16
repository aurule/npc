.. _sys_wod_vampire:

Vampire
#######

:bdg-info:`World of Darkness`

A blood-sucking creature cursed to the night

Vampires are immortal denizens of the night. Once human, they were cursed with an unquenchable thirst for blood and forever bound to their inner beast.




New and Changed Tags
====================

.. _tag_wod_vampire_gen:

@gen
----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The vampire's generation

A vampire's power is measured in part by how many steps removed they are from the mythical first vampire. Who that might be doesn't really matter. A vampire with a high generation of 12 or 11 is pretty typical, while a vampire with a low generation of 8 or 9 is able to wield significantly more blood powers.


.. _tag_wod_vampire_sire:

@sire
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the vampire who turned this character into another vampire

Creating another vampire is called the Embrace. Sometimes vampiric lineage is a really big deal. Other times, it's just nice to know who's been fangin' around.


.. _tag_wod_vampire_clan:

@clan
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The vampire's clan

Almost every vampire is associated with a clan, a group of vampires who share a common heritage and set of powers. The clan also tends to come with certain social expectations and responsibilities, but those vary dramatically from the laissez faire Gangrel to the hierarchical Ventrue.


Subtags
~~~~~~~

These tags can appear immediately after @clan and will be associated with that tag instance's value.

.. _tag_wod_vampire_clan_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has within their clan

Some clans, like the Assamites, have an internal hierarchy of power. While the role may not matter outside of the clan, a vampire's role within it may give them access to unique resources in exchange for extra responsibility.



.. _tag_wod_vampire_sect:

@sect
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Major political body to which the vampire belongs

Vampires are social creatures and whether they like it or not, have a habit of organizing themselves. In modern games, this tends to mean Anarchs, Camarilla, or Sabbat.


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



.. _tag_wod_vampire_pack:

@pack
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the pack to which this vampire belongs (Sabbat only)

Vampires often form small social groups so they can work together toward a shared purpose. In the Sabbat, these are called packs, and they are truly the cornerstone of the sect. Each pack is made official through repeated use of the Vaulderie ritus.


Subtags
~~~~~~~

These tags can appear immediately after @pack and will be associated with that tag instance's value.

.. _tag_wod_vampire_pack_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has in their pack

Every pack needs three key roles filled: Ductus, Priest, and Abbot. The ductus guides the pack's actions, the priest sees to the members' spiritual needs, and the abbot provides shelter and worldly goods.



.. _tag_wod_vampire_gang:

@gang
-----

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the gang to which this vampire belongs (Anarch only)

Vampires often form small social groups so they can work together toward a shared purpose. Among the Anarchs, these are called gangs.


Subtags
~~~~~~~

These tags can appear immediately after @gang and will be associated with that tag instance's value.

.. _tag_wod_vampire_gang_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has in their gang

Gangs have no formal roles or positions. Still, it can be useful to note the ad-hoc roles that emerge based on the gang's needs and actions.



.. _tag_wod_vampire_coterie:

@coterie
--------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of the coterie to which this vampire belongs (Camarilla, primarily)

Vampires often form small social groups so they can work together toward a shared purpose. In the Camarilla, these are called coteries.


Subtags
~~~~~~~

These tags can appear immediately after @coterie and will be associated with that tag instance's value.

.. _tag_wod_vampire_coterie_role:

@role
~~~~~

:bdg-secondary:`Optional`
:bdg-info:`Value required`

The role the vampire has in their coterie

Coteries have no formal roles or positions. Still, it can be useful to note the ad-hoc roles that emerge based on the coterie's needs and actions.



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



