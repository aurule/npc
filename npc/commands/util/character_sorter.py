"""
Reusable sorter for characters
"""

from functools import cmp_to_key
from npc import util

def sort(characters, keys=None, prefs=None):
    """
    Sort a set of characters by a list of tag keys.

    This helper creates a CharacterSorter object and uses it to do the real
    work. If keys is not provided, the special 'last' key is used by default.

    Args:
        characters (list): List of character objects to sort
        keys (list): List of tag names by which to sort.
        prefs (Settings): Settings object containing type data

    Returns:
        List of characters sorted according to their keys.
    """
    if keys is None:
        keys = ['last']

    sorter = CharacterSorter(keys, prefs=prefs)
    return sorter.sort(characters)

class CharacterSorter:
    """
    Character sorting utility class.

    Designed to encapsulate a particular sort order than can be applied
    repeatedly to lists of character objects. The first call to `sort` will
    store comparer functions to speed up future calls.
    """
    def __init__(self, keys, prefs=None):
        """
        Args:
            keys (list): List of sorting keys. Use '-key' to sort descending. Keys
                can be the name of any tag, or a special value:
                * 'last': The last word of the character's name
                * 'first': The first word of the character's name
            prefs (Settings): Settings object containing type data. If provided,
                special type-dependent tags can be used for sorting, like
                'type-unit', or 'type-social'.
        """
        self.keys = keys
        self.prefs = prefs

        self.comparers = []
        self.functions = {
            'first': lambda c: c.get_first('name', '').split(' ')[0],
            'last': lambda c: c.get_first('name', '').split(' ')[-1]
        }

    def generic_get(self, tag_name):
        def _get(character, tag_name=tag_name):
            if self.prefs is not None:
                tag_name = util.translate_tag_for_character_type(character.type_key, tag_name, prefs=self.prefs)
            return character.get_first(tag_name)
        return _get

    def sort(self, characters):
        """
        Sort a list of characters

        Sorting is done in multiple steps, sorting by each key in order. If a
        character does not have a value for a certain key, that character will
        be sorted to the end of the list.

        Args:
            characters (list): List of character objects to sort

        Returns:
            A list of character objects, sorted according to self.keys
        """
        if len(self.comparers) == 0:
            for key in self.keys:
                tag_name = key[1:] if key.startswith('-') else key
                if not tag_name in self.functions:
                    self.functions[tag_name] = self.generic_get(tag_name)
                self.comparers.append((self.functions[tag_name], 1 if tag_name == key else -1))

        return sorted(characters, key=cmp_to_key(self.comparer))

    def comparer(self, left, right):
        for func, polarity in self.comparers:
            result = self.cmp(func(left), func(right))
            if result:
                return polarity * result
        else:
            return 0

    def cmp(self, a, b):
        try:
            return (a > b) - (a < b)
        except TypeError:
            return -1
