class GroupView:
    """Static representation of a list grouping

    This holds the data used by group heading templates. Right now it's very bare-bones, but is here so that
    more data can be added in the future in an easily testable way.
    """
    def __init__(self, title: str, grouping: str = None):
        self.title = title
        self.grouping = grouping

    def __str__(self) -> str:
        """Return a printable representation of this view

        Since this object is meant to be used in templates, this default string implementation returns the
        title.

        Returns:
            str: Our title string
        """
        return self.title
