CLI Quickstart
==============

This guide will get you up and running with a campaign managed by NPC using the CLI utility ``npc``. You'll see the most common commands used while running and planning a game, but check out :ref:`cli_commands` to see the full extent of what ``npc`` can do.

.. seealso::

    NPC is a very configurable program. This guide will link to configuration keys now and then, but there's plenty more you can change. Look through the :ref:`conf_home` section to see what's what.

Campaign Setup
--------------

First, choose or create a directory for your campaign. For this example, I'll create a new directory.

.. code:: sh

    $ cd "~/My Documents/Campaigns"
    $ mkdir "The Examplars"

Then, go into that directory and run ``npc init``. This will prompt you for the new campaign's name, description, and game system.

.. code:: sh

    $ cd "The Examplars"
    $ npc init
    Campaign name: The Examplars
    Campaign description: A group of high profile cadets, the best in their class, are sent on a dangerous diplomatic mission.
    Game system (generic, wod, dnd3, fate, nwod, fate-ep, fate-venture): fate
    Setting up /home/me/My Documents/Campaigns/The Examplars...
    Creating .npc/ config directory
    Creating required directories:
      Characters/
      Session History/
      Plot/
    Done

And just like that, your campaign is ready for you to start planning. How you organize that planning is up to you, but I like to create a ``Plot/Planning`` directory for long-term notes.

.. seealso::

    You can have ``npc`` create additional directories for new campaigns by setting the :ref:`setting_create_on_init` key.

Running a Session
-----------------

You've done some planning and you're ready to have a session. Great! NPC can help with that, too.

Two of the core assumptions that NPC makes are that:

#. You have specific plans for each session
#. You want to keep GM notes for each session

I sometimes create my session plan before game night, but more often than not, I create it right then and tinker a little while everyone is getting settled. Let's explore both methods.

Planning Ahead
~~~~~~~~~~~~~~

When I plan ahead, I create a new plot file manually, then open it up in my editor of choice.

.. code:: sh

    touch "Plot/Plot 01.md"
    subl "Plot/Plot 01.md"

When it's game time, I run ``npc session`` to create the corresponding session file and open it.

.. code:: sh

    npc session

This will create :file:`Session History/Session 01.md`, then open both :file:`Session 01.md` and :file:`Plot 01.md` in my editor.

.. seealso::

    The editor invoked by ``npc`` can be changed in the :ref:`setting_editor` key.

Planning Last Minute
~~~~~~~~~~~~~~~~~~~~

When I *don't* plan ahead, I let NPC handle a bit more of the process. This time, when I run ``npc session``, it will create both the :file:`Session 01.md` and :file:`Plot 01.md` files for me, then open them in my editor.

.. code:: sh

    npc session

:file:`Plot 01.md` will be filled with the contents of the previous plot file by default, if there is one, so I can immediately set about changing things for this session.

.. seealso::

    The contents of new plot and session files is set in their respective ``file_contents`` keys. See :ref:`cust_campaign_plot_sess` for how to change it.

Making Characters
-----------------

Whether it's during play or in the week beforehand, you're going to need to make characters. NPC is designed to make this easy enough to do during the session, and detailed enough to capture every thought during planning.

For example, in the middle of playing a session of *The Examplars*, my players decide to enter a thick bog, lured in by the unnaturally sweet smell coming from its low trees. There's a witch who lives here, I decide, and I want to make a bare-bones file I can reference later.

.. note::

    Sadly, NPC cannot help with creating character names, so that is left as an exercise for the reader.

.. code:: sh

    npc new supporting -n "Tina Watara" -m "bog witch"

This creates the new character file :file:`Tina Watara - bog witch.fate` in the :file:`Characters` directory, and opens it in my editor:

.. code::

    @type supporting

    --Notes--

    A supporting character. Usually the face of a location or group...

I add a few quick notes and a tag or two, then leave the rest for cleaning up later when I'm not in the middle of running a session.

.. code::

    @type supporting
    @location Sweet Bog

    --Notes--

    lives in the sweet-smelling bog
    very knowledgeable about magic
    looks shockingly young

    A supporting character. Usually the face of a location or group...

By the end of the session, I know the players are headed toward the realm of the Granite King. I decide they won't meet the king immediately, but he will send someone to negotiate with them. The king will be a Main npc (and probably antagonist), and his man will be another Supporting character. Let's start with the king.

.. code:: sh

    npc new main -n "Leonard Thorsson" -m "granite king" \
    -t "title" "The Granite King" \
    -t "org" "The Kingdom of Gray Rock" \
    -t "rank" "King" \
    -t "org" "The Lionsguard" \
    -t "role" "Border Knight" \
    -d "Leo is the strong, tight-fisted ruler of Gray Rock."

This is a much longer command and while I could easily add all those tags after the fact, why not put them in while the idea is fresh? This creates and opens the king's file :file:`Leonard Thorsson - granite king.fate`:

.. code::

    Leo is the strong, tight-fisted ruler of Gray Rock.

    @type main
    @title The Granite King

    @org The Kingdom of Gray Rock
    @rank King
    @org The Lionsguard
    @role Border Knight

    --Notes--

    A full character. Has skills appropriate to the current skill cap...

It's then a similar process for King Leo's speaker, Harold the Horn:

.. code:: sh

    npc new supporting -n "Harold Blackwell" -m "kings speaker" \
    -t "title" "Voice of the Lion" \
    -t "org" "The Kingdom of Gray Rock" \
    -t "role" "Diplomat" \
    -d "Harold serves King Leo as a spokesman and diplomat."

Which creates and opens :file:`Harold Blackwell - kings speaker.fate`:

.. code::

    Harold serves King Leo as a spokesman and diplomat.

    @type supporting
    @title Voice of the Lion

    @org The Kingdom of Gray Rock
    @role Diplomat

    --Notes--

    A supporting character. Usually the face...

I realize I've forgotten a tag and can easily add it to both files:

.. code::

    @location Kingdom of Gray Rock

I can add more details, change tags, and update their game stats as needed in the future.

.. seealso::

    So far, the files we've made have all gone into the main :file:`Characters` directory. In the future, we may want to add a directory specically for the Kingdom of Gray Rock. That's where character file subpaths and the :ref:`cli_reorg` command come into play. See :ref:`cust_campaign_char_subpaths` for more on how to set up automatic character organization.
