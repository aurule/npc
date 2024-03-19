.. Campaign settings

.. _cust_campaign:

Customizing Campaigns
=====================

Campaigns are configured using the :file:`settings.yaml` file in the campaign's :file:`.npc/` directory. All of the campaign settings are under the ``campaign`` key.

:name: :octicon:`note` The campaign's name
:system: :octicon:`note` The game system the campaign uses
:desc: :octicon:`book` A long-form description of the campaign
:characters: :octicon:`code-square` An object that defines where characters are stored and displayed
:plot: :octicon:`code-square` An object that defines how plot files are stored
:session: :octicon:`code-square` Object that defines how session files are stored
:create_on_init: :octicon:`list-ordered` List of additional folder names to create for every new campaign

.. code-block:: yaml
    :caption: A basic campaign's settings.yaml file

    campaign:
        name: The First or the Last
        desc: My First Campaign
        plot:
            latest_index: 1
        session:
            latest_index: 1
        system: dnd5
    npc:
        version: 2.0.1


.. _cust_campaign_new:

New Campaigns
-------------

Newly created campaigns are given a few directories by default:

- :file:`.npc/`
- :file:`Characters/` (from ``campaign.characters.path``)
- :file:`Plot/` (from ``campaign.plot.path``)
- :file:`Session History/` (from ``campaign.session.path``)

An empty directy is also created for each entry in ``campaign.create_on_init``.

The new campaign's :file:`.npc/settings.yaml` file is populated with the chosen ``name`` and ``system``, as well as the current ``npc.version``.

See :ref:`cli_init` for how to set up a new campaign using the CLI.

.. _cust_campaign_plot_sess:

Plot and Session Management
---------------------------

Plot and session files are configured in the ``campaign.plot`` and ``campaign.session`` objects, respectively. Both config objects share the same keys:

:path: :octicon:`note` Directory where the files should be placed
:latest_index: :octicon:`number` Numerical index of the most recent file
:filename_pattern: :octicon:`note` How to name the file
:filename_contents: :octicon:`book` What to put in the file
:additional_files: :octicon:`list-ordered` Other files to create alongside the plot or session file

.. code-block:: yaml
    :caption: Fully qualified plot and session blocks

    campaign:
        plot:
            path: Plot
            latest_index: 0
            filename_pattern: Plot ((NN)).md
            file_contents: ((COPY))
            additional_files: []
        session:
            path: Session History
            latest_index: 0
            filename_pattern: Session ((NN)).md
            file_contents: |
                Played:

                # (in-game date and time)
            additional_files: []

Naming and Indexes
~~~~~~~~~~~~~~~~~~

When a new plot or session file is created through NPC, it's named using its ``filename_pattern``, replacing the text ``((NN))`` with the index number that comes next. The new file's index is derived from existing files, if they're in ``path``, so you can do things like manually create a plot file for next session, then use :ref:`cli_session` to generate the corresponding session file. If neither file exists, then NPC falls back on the saved ``latest_index`` to generate the new file's index.

File Contents
~~~~~~~~~~~~~

New files created through NPC are filled with the value in ``file_contents``. Plot files may use the special ``((COPY))`` placeholder string, which is replaced with the *entire* contents of the previous plot file, if it exists. This is a great way to keep running planning notes.

Additional Files
~~~~~~~~~~~~~~~~

Each entry in the ``additional_files`` list is an object with a ``filename_pattern`` and ``file_contents`` property. These properties act just like the ones for the main plot and session files.

.. code-block:: yaml
    :caption: An example of additional session files

    campaign:
        session:
            additional_files:
                - filename_pattern: Session ((NN)) Recap.md
                  file_contents: "# Recap for Session NN"
                - filename_pattern: Session ((NN)) Journals.md
                  file_contents: |
                    # Character Journals for Session NN

                    ## Tybalt

                    ## Jolene

*Added in 2.0.1*

.. _cust_campaign_char_management:

Character Management
--------------------

Character organization and handling is configured in the ``campaign.characters`` object.

:path: :octicon:`note` Directory where characters should be put
:ignore_subpaths: :octicon:`list-ordered` List of directories under ``path`` that should be ignored when loading characters. Good for archiving.
:subpath_components: :octicon:`list-ordered` List of objects that describe how to build the "ideal path" for a character based on its tags.
:listing: :octicon:`code-square` Object configuring how to generate :ref:`listing_home`
:use_blocks: :octicon:`list-ordered` Which :ref:`setting_tag_blocks` to use for new files, and in what order

Basic Organization
~~~~~~~~~~~~~~~~~~~~~~

All character files are stored within the directory in ``campaign.characters.path``, default :file:`Characters/`.

Any character files within a directory found in ``ignore_subpaths`` is skipped entirely and will not be available within NPC. This is most useful for archiving old files or cordoning off generic sheets.

.. _cust_campaign_char_subpaths:

Guide to Subpaths
~~~~~~~~~~~~~~~~~

When creating a new character, or reorganizing existing characters, the list of objects within ``subpath_components`` are used to build out the character's path. Each of these objects is applied in order and can add a directory to the character's path.

If a directory would be added that doesn't already exist, it will be skipped entirely and the next subpath component will be evaluated. This can be very useful for creating branching paths.

.. hint::

    Some cli commands (like :ref:`cmd_reorg`) have an option to create these missing directories instead.

.. important::

    Subpaths can only examine top-level tags. Nested tags, like the character's ``role`` within an ``org``, cannot be accessed.

*The* ``fallback`` *properties were added in NEW_VERSION*

These are the available subpath components:

Conditional Value
^^^^^^^^^^^^^^^^^

Add the directory from ``value`` if at least one of the ``tags`` is present in the character.

Properties:

:selector: :octicon:`note` :bdg-warning:`required` Must be ``conditional_value``
:value: :octicon:`note` :bdg-warning:`required` The directory name to return
:tags: :octicon:`list-ordered` :bdg-warning:`required` The tags whose presence will be checked, in order
:fallback: :octicon:`note` A directory name to use if none of the tags are present

Example:

.. code:: yaml

    subpath_components:
        - selector: conditional_value
          value: Deceased
          tags: [dead]

First Value
^^^^^^^^^^^

Add a directory from the first value found for any of the specified tags. Tags are checked in order.

Properties:

:selector: :octicon:`note` :bdg-warning:`required` Must be ``first_value``
:tags: :octicon:`list-ordered` :bdg-warning:`required` The tags to read, in order
:fallback: :octicon:`note` A directory name to use if none of the tags are present

Example:

.. code:: yaml

    subpath_components:
        - selector: first_value
          tags: [org, location]

Static Value
^^^^^^^^^^^^

Add the directory from ``value``.

Properties:

:selector: :octicon:`note` :bdg-warning:`required` Must be ``static_value``
:value: :octicon:`note` :bdg-warning:`required` The directory name to return

Example:

.. code:: yaml

    subpath_components:
        - selector: static_value
          value: Unaligned

Match Value
^^^^^^^^^^^

Add the directory from ``value`` if at least one of the ``tags`` contains the value in ``equals``.

Properties:

:selector: :octicon:`note` :bdg-warning:`required` Must be ``match_value``
:value: :octicon:`note` :bdg-warning:`required` The directory name to return
:equals: :octicon:`note` :bdg-warning:`required` The tag value to test against
:tags: :octicon:`list-ordered` :bdg-warning:`required` The tags to examine
:fallback: :octicon:`note` A directory name to use if none of the tags match the value in ``equals``

Example:

.. code:: yaml

    subpath_components:
        - selector: match_value
          tags: [class]
          equals: Cleric
          value: Blessed

*Added in 2.0.2*

File Names
~~~~~~~~~~

.. include:: /reference/snippets/character_file_names.rst
