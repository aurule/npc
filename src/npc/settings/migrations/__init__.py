# these migrations are to handle discrepancies in how settings work between different versions of NPC
# they're supposed to run on a raw parsed settings file, NOT the final composite
# idea is to have a list of migration objects with each able to do whatever they need
# each should test against the declared npc version in the settings file to see if it should be run
#
# likely operations include
# * moving existing keys
# * renaming existing keys
# * warning about removed keys
# * warning about formatting changes
# special-case operations:
# * moving from json to yaml, just for the first migration
#
# we'll want to use a special yaml library for this, since we want to preserve comments, etc. as much as possible
#
# besides automatic fixes, there will be things we need to prompt the user about. Instead of trying to build a
# fancy interface for it, just tell them what needs to be manually changed for now.
#
# Need to be able to give a summary of the changes and apply as many automated fixes as possible.
