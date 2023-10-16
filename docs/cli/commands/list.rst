.. _cli_list:

list
=============

Generate a public listing of characters.

.. note::

    Almost all of the options for ``npc list`` get default values from your settings. See :ref:`conf_home` for how to configure NPC and :ref:`conf_listings` for how to customize the way characters are presented.

-f, --format
    The format to use. One of ``md`` or ``html``.
-g, --group-by
    Tags to group by. Additional groups will be nested.
-s, --sort-by
    Tags to sort by. Applied in order within the final group.
-h, --header_level
    The minimum header level to use.
-o, --output
    **Required.** Where to put the listing. Use ``-`` for STDOUT.

.. important::

    This command only works within an existing campaign.

Example:

.. code:: sh

    npc list -o -

.. code:: html

    <h1>M</h1>

    <article>
        <h2>Fake Mann (Deceased)</h2>

        <p><i>AKA Mockery Mann</i></p>

        <p>The Fakest</p>

        <p>Supporting</p>
        <ul class="grid-list" style="display: inline">
            <li>High Concept: The Fake</li>
        </ul>

        <p><i>Appearance:</i> Wispy and transparent, with an ever-changing visage.</p>

        <p>The fakiest Mann alive!</p>

        <p><i>Deceased:</i> Though dead countless times, he always reappears with a new set of faces. No one ever sees a "dead" face again.</p>
    </article>

    <article>
        <h2>True Mann</h2>

        <p>The Truest</p>

        <p>Supporting</p>

        <p><b>Member of:</b></p>
        <ul>
            <li>Ultimates, Novitiate</li>
            <li>Hab Admin (Security Mook)</li>
        </ul>
        <ul class="grid-list" style="display: inline">
        </ul>
    </article>
