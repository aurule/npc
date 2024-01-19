from jinja2 import ChainableUndefined

class UndefinedView(ChainableUndefined):
    """Special Undefined object for jinja templates

    In addition to the standard properties (see https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.ChainableUndefined),
    this object adds the has method. This makes it safe to write code like character.org.has("role") regardless
    of whether the character has the org tag.
    """
    def has(self, _tag_name: str) -> bool:
        """Get whether this undefined view has a named property

        Always false.

        Args:
            _tag_name (str): Tag to look up (not used)

        Returns:
            bool: False
        """
        return False

    def first(self, _tag_name: str = None):
        """Make the first() method chainable

        Returns:
            UndefinedView: Always returns self
        """
        return self

    def all(self):
        """Make the all() method chainable

        Returns:
            UndefinedView: Always returns self
        """
        return self

    def rest(self):
        """Make the rest() method chainable

        Returns:
            UndefinedView: Always returns self
        """
        return self
