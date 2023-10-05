.. _tag_location:

@location
#########

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Broad description of where the character lives

A character's location depends greatly on the game's setting, and is usually one step smaller than the game area. For example, a game set in New England is likely to have a character's location be an individual town or city. One set in New York City is likely to have it be a borough.

Subtags
=======

These tags can appear immediately after @location and will be associated with that tag instance's value.

.. _tag_location_wanderer:

@wanderer
=========

:bdg-secondary:`Optional`
:bdg-warning:`No value allowed`

The character wanders within this location and has no single home.

Itinerant characters usually stick to a known territory. For those who don't, use a suitably broad location like a country or massive geographic region.

.. _tag_location_region:

@region
=======

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Specific area in which the character lives.

This tag starts to zoom in on where the character is. If their location is a city, their region might be a district or zone. If their location is a borough of NYC, their region might be a neighborhood.
Not all characters need this much specificity. It's most helpful when dealing with very large play areas, where the location only tells you in which massive city a character is found.

Subtags
-------

These tags can appear immediately after @region and will be associated with that tag instance's value.

.. _tag_location_region_locale:

@locale
-------

:bdg-secondary:`Optional`
:bdg-info:`Value required`

Very specific area in which the character lives.

This tag zooms all the way in on where the character is. If their location is a city, and their region is a district, then their locale might be a neighborhood. If their location is a borough and their region is a neighborhood, their locale could be a single block.
Most characters do not need this level of specificity. It can be useful if the game deals with extremely local drama, where a five minute walk can put you in another world, or if you want to put your characters on an actual map.


