.. Changeling tags documentation

Changeling Tags
===============

The changeling type is designed around :t:`Changeling: The Lost`. It has many special tags to describe the supernatural aspects of these characters, as well as their unique social groups. Settings for changeling characters are in :file:`settings-changeling.yaml`.

@changeling
-------------------------------

*meta, can appear only once*

This special compound tag marks the character's :ref:`tag-type` as ``changeling``, their seeming as the first value, and their kith as the second value. That is::

	@changeling elemental fireheart

replaces::

	@type changeling
	@seeming elemental
	@kith fireheart

Multi-word kiths like ``Bright One`` do not need to be quoted and do not need the space to be replaced or escaped.

This meta tag is not exported verbatim, as it is broken into its component parts when the file is parsed.

@seeming
-------------------------------

*required*

Name of the character's seeming. The value must appear under ``changeling.seemings``. This value is used to set the seeming blessing and curse descriptions within the character's :ref:`sheet-stats` using the values under ``changeling.blessings.<seeming>`` and ``changeling.curses.<seeming``.

@kith
-------------------------------

*required*

Name of the character's kith. The value must appear under ``changeling.kiths.<seeming>``. This value is used to set the kith blessing within the character's :ref:`sheet-stats` using the value under ``changeling.blessings.<kith>``.

@mask
-------------------------------

*markdown*

Description of the character's human-facing appearance.

@mien
-------------------------------

*markdown*

Description of the character's fae-facing appearance.

.. _tag-freehold:

@freehold
-------------------------------

Name of the freehold that the character belongs to.

.. _tag-court:

@court
-------------------------------

Name of the character's court.

.. _tag-motley:

@motley
-------------------------------

Name of the character's motley.

.. _tag-entitlement:

@entitlement
-------------------------------

Name of the character's entitlement.
