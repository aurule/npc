"""
Reusable sorter for characters
"""

def sort(characters, keys=None):
    """
    Sort a set of characters by a list of tag keys.

    This helper creates a CharacterSorter object and uses it to do the real
    work. If keys is not provided, the special 'last' key is used by default.

    Args:
        characters (list): List of character objects to sort
        keys (list): List of tag names by which to sort.

    Returns:
        List of characters sorted according to their keys.
    """
    if keys is None:
        keys = ['last']

    sorter = CharacterSorter.new(keys)
    return sorter.sort(characters)

class CharacterSorter:
    """
    Character sorting utility class.

    Designed to encapsulate a particular sort order than can be applied
    repeatedly to lists of character objects.
    """
    def __init__(self, keys):
        """
        Args:
            keys (list): List of sorting keys. Keys can be the name of any tag, or a special value:
                'last': The last word of the character's name
                'first': The first word of the character's name
        """
        self.keys = keys

    def sort(self, characters):
        pass
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

        # use sorted
        # key needs to be (x is None, x) after getting the value of x
        # foreign and dead will need special handling, since they can be a string or a boolean

def sort_characters(characters, order=None):
    """
    Sort a list of Characters.

    Deprecated!

    Args:
        characters (list): Characters to sort.
        order (str|None): The order in which the characters should be sorted.
            Unrecognized sort orders are ignored. Supported orders are:
            * "last" - sort by last-most name (default)
            * "first" - sort by first name

    Returns:
        List of characters ordered as requested.
    """
    def last_name(character):
        """Get the character's last-most name"""
        return character.get_first('name', '').split(' ')[-1]

    def first_name(character):
        """Get the character's first name"""
        return character.get_first('name', '').split(' ')[0]

    if order is None:
        order = "last"

    if order == "last":
        return sorted(characters, key=last_name)
    elif order == "first":
        return sorted(characters, key=first_name)
    return characters
