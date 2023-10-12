.. Settings reference guide

.. _ref_settings:

Settings Keys
========================

NPCs settings are spread throughout multiple top-level keys. The settings here are all found within :file:`settings.yaml`. Configuration for systems is discussed in :ref:`cust_systems`.

:npc: Primary key. Used for settings that affect all parts of NPC.

:campaign: Used for settings that affect campaigns.

NPC Settings
############

Settings that affect all parts of NPC.

npc.version :octicon:`note`
---------------------------

:bdg-info:`type: string`
:bdg-warning:`required: yes`

The version of NPC which last used this settings file. This key is automatically set by NPC and should not be changed by hand.

Example:

.. code:: yaml

    npc:
        version: 2.0.0

.. _setting_editor:

npc.editor :octicon:`note`
---------------------------

:bdg-info:`type: string`
:bdg-info:`required: no`

The text editor to invoke for editing various campaign files. If not provided, the system default will be used.

npc.tags :octicon:`code-square`
-------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Defines tags available to all characters, regardless of system. See :ref:`cust_tags` for how each tag object works.

Example:

.. code:: yaml

    tags:
        type:
            desc: The character type of an npc
            required: true
            max: 1

npc.deprecated_tags :octicon:`code-square`
------------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Describes tags which are deprecated and no longer used. This is intended for internal use, as certain tags have unique programmatic handling.

Each key underneath ``npc.deprecated_tags`` is the name of a tag that is deprecated, and contains an object with the following attributes:

:desc: What the deprecated tag did

:replaced_by: Name of the tag that replaces the deprecated tag

:replacement_pattern: How to transform the value of the deprecated tag to a valid value for the replacement tag

:version: The version of NPC in which the deprecated tag was removed

For example:

.. code:: yaml

    deprecated_tags:
        hidegroup:
          desc: Hide a single named group
          replaced_by: hide
          replacement_pattern: "group >> $value"
          version: 1.4.1

npc.reserved_tags :octicon:`code-square`
----------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Describes tag names which are reserved for internal use. These tag names typically are not tags at all, but instead are reserved words. They *must not* appear in character files.

Each key underneath ``npc.reserved_tags`` is the name of a reserved tag, and contains an object with these properties:

:desc: Description of what the reserved tag name is used for

:doc: More detail about the data associated with the name

Example:

.. code:: yaml

    reserved_tags:
        description:
          desc: Generated automatically for bare text in the tag area
          doc: >
            Public text about this character, like who they are, their history, what
            they want, etc. This is an internal tag used to store bare text that
            appears in the tags area of npc sheets. It should not be used
            explicitly.

.. _setting_tag_blocks:

npc.tag_blocks :octicon:`code-square`
-------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Defines blocks of tags which are related to each other, and are grouped together in newly created files. Each key is the name of a group and contains a list of tag names which are a member of that group. Tags in a group are added to character files in the same order they appear in the group. Empty tags are omitted.

The special group ``rest`` has the tag identifier ``"*"``, which matches all tags which have not yet been omitted. It's a catch-all so that system-specific tags are not left out of character files.

These tag groups are used in :ref:`cust_campaign_char_management`.

.. code:: yaml

    tag_blocks:
        flags:
            - sticky
            - nolint
            - delist

npc.metatags :octicon:`code-square`
-----------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Like in campaigns, it's possible to define special metatags at the global level. Metatags here will be available within every game system. For a full description of how metatags works, see :ref:`cust_system_metatags`.

.. warning::

    Top-level metatags are generally discouraged. Since they are available to *every* game system, they need to work correctly regardless of changes that any system or character type might make to the available tags. Thus, it's almost always a better idea to define metatags at the game system level than at the global level.

Campaign Settings
#################

Settings which affect campaigns. See :ref:`cust_campaign` for more detail on how to set up a campaign.

campaign.name :octicon:`note`
-----------------------------

:bdg-info:`type: string`
:bdg-info:`required: no`

Name of the campaign.

Example:

.. code:: yaml

    campaign:
        name: The Depths of Moria

campaign.desc :octicon:`book`
-----------------------------

:bdg-info:`type: text`
:bdg-info:`required: no`

A long-form description of the campaign.

Example:

.. code:: yaml

    campaign:
        desc: A harrowing journey into the depths of the forgotten Dwarven city of Moria.

campaign.system :octicon:`note`
-------------------------------

:bdg-info:`type: string`
:bdg-info:`required: no`

The key of the game system the campaign uses. If not provided, NPC falls back on :ref:`sys_generic`.

Example:

.. code:: yaml

    campaign:
        system: dnd35

.. _setting_create_on_init:

campaign.create_on_init :octicon:`list-ordered`
-----------------------------------------------

:bdg-info:`type: list`
:bdg-info:`required: no`

List of directory names to create in new campaigns. See :ref:`cust_campaign_new` for more.

Example:

.. code:: yaml

    create_on_init:
        - Setting
        - House Rules

.. _settings_characters:

campaign.characters :octicon:`code-square`
------------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Defines how characters are organized and managed. See :ref:`cust_campaign_char_management` for more.

Example:

.. code:: yaml

    characters:
        path: Characters
        ignore_subpaths: []
        subpath_components:
          - selector: first_value
            tags: [location]
          - selector: first_value
            tags: [org, employer]
        listing:
          format: markdown
          group_by:
            - last_initial
          sort_by:
            - full_name
          base_header_level: 1
          metadata:
            title: NPC Listing
            timestamp: '%a, %b %d %I:%M%p'
        use_blocks:
          - flags
          - bio
          - geo
          - assoc
          - rest

campaign.plot :octicon:`code-square`
------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Defines how plot files are stored and named. See :ref:`cust_campaign_plot_sess` for more.

Example:

.. code:: yaml

    plot:
        path: Plot
        latest_index: 0
        filename_pattern: Plot ((NN)).md
        file_contents: ((COPY))

campaign.session :octicon:`code-square`
---------------------------------------

:bdg-info:`type: object`
:bdg-info:`required: no`

Defines how session files are stored and named. See :ref:`cust_campaign_plot_sess` for more.

Example:

.. code:: yaml

    session:
        path: Session History
        latest_index: 0
        filename_pattern: Session ((NN)).md
        file_contents: |
            Played:

            # (in-game date and time)
