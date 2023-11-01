.. Listings guide

.. _listing_home:

Character Listings
====================

One of the things NPC was created to do is to generate a public listing of characters. The listing system is a bit complex, but can output correctly formatted entries for every type of character in every system, with built-in support for hiding character attributes -- and entire characters -- from the output.

.. _conf_listings:

Configuration
-------------

Listing settings are stored within the :ref:`settings_characters` namespace in the ``listing`` key. They define defaults, but most can be overridden by arguments to the :ref:`cli_list` command.

.. note::

    There is an additional ``listing.metadata`` key which is currently ignored.

listing.format :octicon:`note`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-info:`type: string`
:bdg-info:`required: no`

Name of the default output format. Built-in formats are ``markdown`` and ``html``.

Example:

.. code:: yaml

    listing:
        format: markdown

.. _listing_group_by:

listing.group_by :octicon:`list-ordered`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-info:`type: list`
:bdg-info:`required: no`

List of tag names which are used to group characters together using shared values. Subsequent tag names define subgroups. Groups and subgroups are given a header in the output.

This list accepts any defined tag, as well as a few special keywords:

:last_name: The last word of the character's name.
:last_initial: The first letter of the last word of the character's name.
:first_name: The first word of the character's name.
:first_initial: The first letter of the first word of the character's name.
:full_name: The character's name.

Example:

.. code:: yaml

    listing:
        group_by:
            - location
            - last_initial

listing.sort_by :octicon:`list-ordered`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-info:`type: list`
:bdg-info:`required: no`

List of tag names which are used to sort characters within groups. Each tag is applied in order to resolve ties.

This list accepts any defined tag, as well as same special keywords as :ref:`listing_group_by`.

Example:

.. code:: yaml

    listing:
        sort_by:
            - last_name
            - first_name
            - full_name

listing.base_header_level :octicon:`number`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-info:`type: int`
:bdg-info:`required: no`

The first header level to use within a listing. When :ref:`listing_group_by` is used, this is the header level of the top-level group names. When groups are not used, this is the header level of the character names. Subgroups and characters are given lower numbered headers as appropriate.

The header level corresponds directly to the ``<h1>`` through ``<h6>`` tags in HTML. A value of ``1`` is most common when the listing will stand alone, while a value of ``2`` is useful when the listing will be embedded in a document that has its own top level header.

Example:

.. code:: yaml

    listing:
        base_header_level: 1

Templates
---------

NPC 2.0 uses the `Jinja <https://jinja.palletsprojects.com/en/3.1.x/templates/>`_ template engine to render character listings. Each character is rendered using a template, which is looked up based on the character's type and the campaign's game system.

Default Templates
^^^^^^^^^^^^^^^^^

The default templates display all information for the :ref:`ref_tags` in NPC. Various type-specific templates exist for the character types of the built-in :ref:`ref_systems`. If you're using these systems, you may be able to use the default templates without any changes.

File Locations
^^^^^^^^^^^^^^

Templates are named using the character type key and the output format's extension. To find the correct template to use, NPC will check these directories in order. If the expected file does not exist in that directory (or the entire directory is not found), NPC moves on to the next in the list.

#. <campaign>/.npc/templates/characters
#. <user settings>/templates/characters/<game system key>
#. <npc package>/templates/characters/<game system key>
#. <user settings>/templates/characters
#. <npc package>/templates/characters

This ensures the following order of precedence:

#. Campaign-specific template
#. System-specific user template
#. System-specific internal template
#. Generic user template
#. Generic internal template

If no file is found for the character type, then the same directories are checked again for the generic :file:`character.<ext>` template.

Custom Templates
^^^^^^^^^^^^^^^^

If you make a new system, or want to change how a type is displayed, you'll need to make a new template file. Name it using the character type key and use either ``.html`` or ``.md`` for the file extension, depending on the output format you're targeting.

Templates for a single campaign can go in the campaign's settings directory at :file:`<campaign>/.npc/templates/characters`. Shared templates should go in your user settings at :file:`<user settings>/templates/characters/<game system key>`.

For example, if you're making a new template for the :ref:`sys_nwod_changeling` type to be shared by multiple campaigns, you'd create the file :file:`<user settings>/templates/characters/nwod/changeling.html`.

If you want to generate everything from scratch, that's it! You can write Jinja code as normal. Check out the :ref:`listing_new_filters` added by NPC, as well.

If you don't want to start from scratch, you can inherit from one of the base character templates:

.. code:: jinja

    {%- extends "character-base.html" -%}

Putting this at the top of the file will give you access to various blocks which you can extend with new tags, or replace with custom content. To extend a block, declare it in your file and call ``super()`` to render the default contents, then insert your own additions.

.. code:: jinja

    {%- extends "character-base.html" -%}

    {%- block aka -%}
        {{ super() }}
        {%- if has("court") -%}
            <div>
                {{ character.court.first() | title }} {% if character.court.has("role") -%}
                    ({{ character.court.role.all() | join(", ") }})
                {%- endif -%}
            </div>
        {%- endif -%}
    {%- endblock -%}

.. tip::

    If you want your custom content to appear before the default block contents, just put your own code before the call to ``super()``. If you want to effectively hide the block, define it and don't call ``super()`` at all.

These are the available blocks:

:name: The character's name and a marker if they are dead.
:portrait: The portrait image, if :ref:`tag_portrait` is set.
:aka: Titles and other names the character has.
:vitals: Personal info, like race, age, location, and pronouns.
:orgs: Organization membership.
:location: Where the character is found.
:employment: Details about where the character works and what they do.
:links: Details about the character's relationships.
:system: Empty block for system-specific tags.
:appearance: :octicon:`markdown` The character's :ref:`tag_appearance`.
:description: :octicon:`markdown` The character's description.
:dead: :octicon:`markdown` Details about the character's death.

.. tip::

    Blocks marked with :octicon:`markdown` may be formatted in markdown. Use the :ref:`listing_filter_md` or :ref:`listing_filter_mdi` filters to convert their contents to HTML if desired.

Data and Helpers
^^^^^^^^^^^^^^^^

NPC supplies these properties to every character template:

:header_level: The current header level to use for this entry's header text.
:character: The character object whose data should be displayed.
:has: A simple helper function to test if the character has a named tag.

.. _listing_new_filters:

New Filters
^^^^^^^^^^^

NPC provides a few additional filters that can be used in character templates.

.. _listing_filter_md:

md
~~

This filter converts a string of markdown to a block of HTML.

Example:

.. code:: jinja

    {{ character.description | md }}

.. code:: html

    <p>This character, is a character.</p>

.. _listing_filter_mdi:

mdi
~~~

This filter converts a string of markdown into inline HTML. It uses :ref:`listing_filter_trim_tags` to do so and is not at all clever or safe about which tags are stripped.

Example:

.. code:: jinja

    <div>{{ character.description | mdi }}</div>

.. code:: html

    <div>This character, is a character.</div>

.. _listing_filter_trim_tags:

trim_tags
~~~~~~~~~

This filter removes the first and last tag in a string of HTML. It is very simple and does not check that the tags match.

.. code:: jinja

    {{ "<div>Something cool</div>" | trim_tags }}

.. code:: html

    Something cool

Showing and Hiding
------------------

By default, all tags in a character are available to the template. However, since listings are intended to be viewable by your players, you may want to hide certain bits of information. Depending on what you're hiding, there are a few different tags that can help.

.. _listing_delist:

Hiding a Character
^^^^^^^^^^^^^^^^^^

First is hiding an entire character. Adding :ref:`tag_delist` to a character file completely removes that character from all generated listings. This is ideal for characters whose very existence is secret: upcoming villains, sheets for the evil faceless army, etc.

.. _listing_faketype:

Hiding the Character's Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next is hiding a character's type. Putting :ref:`tag_faketype` ``type key`` in a character file causes all listings to show *that* type instead of the character's real type. It's useful for situations like when a powerful wizard is pretending to be a traveling fireworks salesman, or when a changeling's :ref:`sys_nwod_fetch` is under cover as a mundane human.

.. tip::

    Setting :ref:`tag_faketype` for a character changes the character's apparent type throughout the entire listing process. This means that a different template may be used to render the character's entry. However, it does *not* automatically hide any other tag values. Tags which are shared by the character's real type and fake type will be available to the template. If those tags reveal secret info, use :ref:`tag_hide` to conceal them separately.

.. _listing_hide:

Hiding Tags
^^^^^^^^^^^^^

Last up is hiding specific tag values. The :ref:`tag_hide` tag is flexible and can conceal every instance of a tag or a specific instance of a tag, and works on nested subtags, too. It's great for hiding that the mayor is secretly a don in the local mafia family, or that a prominent thief is actually an undercover guardsman.

.. tip::

    The :ref:`tag_hide` tag works just fine to hide the character's type. A type-specific template may still be used, though, which can inadvertantly reveal information. To avoid that, it's usually better to use :ref:`tag_faketype` instead of outright hiding the type.

The syntax of the hide tag takes this form:

.. code::

    @hide [tag name] >> [tag value] >> [subtag name] >> [subtag value] >> ...


Here are some examples to show it in action.

Hiding Every Tag Instance
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    @dead Mr. Fritz died seven years ago, under mysterious circumstances.
    @hide dead

This will cause the listing for Mr. Fritz to behave as though the :ref:`tag_dead` tag did not exist on his sheet. His entry will not mark him as deceased and the notes about his death will not appear.

.. note::

    Behind the scenes, NPC uses the special value ``all`` to represent hiding all instances of a given tag. Thus, ``@hide dead`` is identical to ``@hide dead >> all``. Be sure not to use ``all`` as the value for any tag, or you may end up with surprising results if you try to hide it.

Hiding One Tag Instance
~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    @name Eggsy
    @name Chuckles
    @hide name >> Eggsy

This will hide the :ref:`tag_name` entry ``Eggsy`` while leaving ``Chuckles`` available to the template.

.. code::

    @name Eggsy
    @with Kingsmen

    @name Chuckles
    @with Family

    @hide name >> Eggsy

This does the same thing. The subtags of a hidden tag are also unavailable to the template, so you don't need to hide them separately.

Hiding A Whole Subtag
~~~~~~~~~~~~~~~~~~~~~

.. code::

    @name Eggsy
    @with Kingsmen

    @name Chuckles
    @with Family

    @hide name >> Eggsy >> with

Instead of hiding the nickname Eggsy, this will only remove the :ref:`tag_name_with` info for ``Eggsy``.

.. note::

    Hiding :ref:`tag_name_with` for ``Eggsy`` does not hide the corresponding tag for ``Chuckles``. There is currently no way to hide all instances of a subtag for all instances of a given parent.
