.. _cli_describe_tags:

describe tags
=============

Show all configured tags for a game system.

-s, --system
    *Sometimes required.* Key of the game system to use. If run within a campaign, this defaults to the campaign's configured system. Outside of a campaign, this option is required.
-t, --type
    Only show valid tags for this character type

``npc describe tags`` can show all of the tags for a given game system, or just the tags available to a single character type.

.. note::

    When run within a campaign, ``npc describe tags`` will include any tags configured within that campaign.

Example:

.. code:: sh

    npc describe tags -s fate-ep -t main

.. code:: text

                    [Tags for Main in Eclipse Phase: Transhumanity's Fate]
    | Name       | Description                                                           |
    |------------|-----------------------------------------------------------------------|
    | type       | The character type of an npc                                          |
    | faketype   | A false character type that will be shown in listings                 |
    | name       | An additional name the character uses                                 |
    | └ with     | Where or with whom this name is used                                  |
    | realname   | The true primary name for the character                               |
    | title      | Honorific title for the character, like The Kingslayer                |
    | pronouns   | Pronouns the character uses                                           |
    | gender     | Gender role this character has                                        |
    | appearance | What the character looks like to other people                         |
    | race       | Observable ancestry of the character                                  |
    | age        | How old the character is                                              |
    | portrait   | Path to an image file to use for the character                        |
    | location   | Broad description of where the character lives                        |
    | └ wanderer | The character wanders within this location and has no single home.    |
    | └ region   | Specific area in which the character lives.                           |
    | foreign    | The character lives somewhere outside the main play area              |
    | group      | Name of a group that the character belongs to                         |
    | └ rank     | The character's rank or role within this group                        |
    | org        | Official organization to which the character belongs                  |
    | └ role     | The role or position the character holds within this organization     |
    | └ rank     | A formal rank the character holds within this organization            |
    | employer   | Name of a person or organization that pays the character for work     |
    | └ job      | Name of the character's job at their employer                         |
    | lineage    | Brief listing of the character's ancestors                            |
    | dead       | Indicates that the character is deceased                              |
    | sticky     | Prevent this file from being moved by the reorg command               |
    | nolint     | Do not show linting errors for this character                         |
    | delist     | Do not show this character in listings                                |
    | hide       | Conceal the named tag from listings                                   |
    | concept    | The character's high concept                                          |
    | └ trouble  | The character's main trouble in life                                  |
    | └ aspect   | An aspect of the character's ego                                      |
    | morph      | Special aspect for the body the character is wearing                  |
    | └ aspect   | An aspect of the character's morph                                    |
    | muse       | Name of the character's muse                                          |
    | refresh    | Number of fate points the character starts with                       |
    | stunt      | Name of a special power the character possesses                       |
