.. Werewolf tags documentation

Werewolf Tags
=============

The werewolf type is designed around :t:`Werewolf: The Forsaken`. It has a few special tags to describe the supernatural and social aspects of werewolf life. Settings for werewolf characters are in :file:`settings-werewolf.yaml`.

@werewolf
-------------------------------

*meta, can appear only once*

This special compound tag marks the character's :ref:`tag-type` as ``werewolf`` and their auspice as the given value. That is::

	@werewolf Cahalith

replaces::

	@type Werewolf
	@auspice Cahalith

This meta tag is not exported verbatim, as it is broken into its component parts when the file is parsed.

@auspice
-------------------------------

*can appear only once*


Name of the character's auspice. The value must appear under the key ``werewolf.auspices``.

@tribe
-------------------------------

*can appear only once*

Name of the character's tribe. The value must appear under ``werewolf.tribes.moon`` or ``werewolf.tribes.pure``.

@pack
-------------------------------

*can appear only once*

Name of the werewolf's pack.

@lodge
-------------------------------

*can appear only once*

Name of the werewolf's lodge. Lodge membership is fairly rare compared to the other tags.

Spirit Tags
===========

Spirits are a less commoncharacter type most often used alongside werewolves. They are patterned after the spirits found in :t:`Werewolf: The Forsaken`.

@ban
-------------------------------

*required*

Description of the spirit's ban.
