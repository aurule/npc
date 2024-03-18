.. Custom systems documentation

.. _cust_systems:

Game System Anatomy
===============================

NPC supports custom game systems in addition to its built-in systems. Custom systems can be defined within your user settings directory, or within a campaign's settings directory. See :ref:`cust_file_locations` for how to find these.

System Files
------------

System files are written in `yaml`_ and found within the :file:`systems/` directory inside a settings directory. The name of the file **must** match the name of the file's primary key.

For example, a custom system definition for Savage Worlds in a campaign would be found in :file:`.npc/systems/savage_worlds.yaml`.

.. caution::

    Systems are defined in their own files for portability and maintanability. Technically, they can also be defined in a subkey within ``npc.systems`` in :file:`settings.yaml`, but this is generally a bad idea. Doing so prevents inheritence and ties the system to that specific settings file. Still, it can sometimes be useful for prototyping.

System Format
-------------

Each system file must begin with a single top-level key. This key is the System Key and is used by NPC to look up the system. Within this key, there are a few required and optional properties:

:name: :octicon:`note` :bdg-warning:`required` The full name of the game system
:desc: :octicon:`note` :bdg-warning:`required` A single line of text that gives an overview of the game system
:doc: :octicon:`book` A multiline block of text describing the details of the game system
:extends: :octicon:`note` The key of a different system. When present, the configuration for that system will be imported into the current system before being altered by the current configuration.
:links: :octicon:`code-square` Labelled URLs that are relevant to this system, like its SRD and homepage
:tags: :octicon:`code-square` Tag objects unique to this game system. See :ref:`cust_tags` for how to format these.
:metatags: :octicon:`code-square` Tags which set one or more other tags when found. They do not appear as separate tags in the parsed character data, but may be used as shorthand to set multiple tags at once.

You are also free to add additional data. This data will not be used by NPC, but may be useful for other custom tools or just to keep track of certain bits of data.

Here is one example of a truly minimal game system, in :file:`bikes.yaml`:

.. code:: yaml

    bikes:
        name: Kids on Bikes
        desc: Rules-light, storytelling system set in a small town with big mysteries.

Adding Links
~~~~~~~~~~~~~~

Links are simple URLs that can take the user to relevant documentation, licensing, or other information for the game system. They're defined as a list of objects with these properties:

:label: :octicon:`note` Text to display that identify the purpose of this URL
:url: :octicon:`note` The URL to go to

Here's an example of Kids on Bikes with a link added:

.. code:: yaml

    bikes:
        name: Kids on Bikes
        desc: Rules-light, storytelling system set in a small town with big mysteries.
        links:
            - label: Homepage
              url: https://www.huntersentertainment.com/kidsonbikesrpg

.. _cust_system_metatags:

Working with Metatags
~~~~~~~~~~~~~~~~~~~~~

Campaigns allow you to define special metatags which NPC will expand into multiple real tags when loading the file. When saving, those real tags will be compressed into the corresponding metatag format.

Metatags are most useful when a particular character type has a set of tags which almost always appear together, or which are all required. In these cases, it can be much easier to read a single line of text with a metatag than it is to read three or four lines each with a single tag.

The best example of this is the Changeling character type for the New World of Darkness system. Characters of this type almost always have a ``@seeming`` and ``@kith`` tag. Normally, this would be written as:

.. code::

    @type changeling
    @seeming beast
    @kith hunterheart

This works fine and is very clear. However, using a metatag can give us a nice shorthand:

.. code::

    @changeling beast hunterheart

On this line, ``@changeling`` is the name of the metatag. It sets the character's :ref:`tag_type` to ``changeling``, then splits the next two words into the character's ``@seeming`` and ``@kith``.

The metatag definition for ``@changeling`` is as follows:

.. code:: yaml

    metatags:
        changeling:
            desc: Shorthand for setting type, seeming, and kith for changelings
            static:
                type: changeling
            match:
                - seeming
                - kith

Metatag Format
^^^^^^^^^^^^^^

Each entry within the ``metatags`` key of the game system is an object describing how the metatag works.

:desc: :octicon:`note` :bdg-warning:`required` A single line of text describing the basic purpose of this metatag
:doc: :octicon:`book` A multiline block of text describing the details and nuances of this metatag
:static: :octicon:`code-square` Static values to assign to tags when this metatag is present
:match: :octicon:`list-ordered` List of tags whose values are derived by parsing the metatag's value
:separator: :octicon:`note` The string used to break the metatag value into multiple tag values to fill the tags in the ``match`` property
:greedy: :octicon:`tasklist` Whether this metatag should be emitted as many times as possible, i.e. as long as there are enough sets of static and match tags in the character object. No effect on reading in the character.

.. note::

    When a matched tag has specific ``values`` configured, the metatag will match against those values before blindly splitting the string on ``separator``.

Configuring Character Types
---------------------------

Character types are closely tied to their systems, as the types available often relate directly to the assumptions of the game system.

Type Files
~~~~~~~~~~

Each type is defined in its own `yaml`_ file. For types defined in the user settings, the file is located within :file:`types/system_key/`, where ``system_key`` matches the System Key of the game system the character type is for.

Types defined within a campaign's settings are in :file:`types/`, as the system is assumed from the campaign's :file:`settings.yaml`.

Type Format
~~~~~~~~~~~

Each character type file must begin with a single top-level key. This key is the Type Key and is used by NPC to look up the character type. Within this key, there are a few required and optional properties:

:name: :octicon:`note` :bdg-warning:`required` The full name of this character type
:desc: :octicon:`note` :bdg-warning:`required` A single line of text describing the gist of the character type's purpose
:doc: :octicon:`book` A multiline block of text describing the details and nuances of the character type
:tags: :octicon:`code-square` Tag objects unique to this character type. See :ref:`cust_tags` for how to format these.

Here is an example of a simple character type for the FATE system, which could be in the user settings in :file:`types/fate/supporting.yaml`:

.. code:: yaml

    supporting:
        name: Supporting
        desc: A supporting character
        doc: >
            Usually the face of a location or group, or someone else who plays an
            important role in the story or the players' lives.

Type Templates
~~~~~~~~~~~~~~

Custom type templates can be used along with custom character types to change the file body for new characters using that type. They're found in the same directory as the type definition file and share its name. The file extension for a sheet template must be either ``.npc``, or the name of the System Key.

The contents of the template are added to a new character file after all of its tags. For this reason, the template should start with a header like ``--Notes--``.

.. _`yaml`: https://www.tutorialspoint.com/yaml/yaml_basics.htm
