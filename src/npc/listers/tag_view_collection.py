from npc.characters import Tag
from .tag_view import TagView

class TagViewCollection:
    """Stores related TagViews

    All TagView objects in a collection should have the same name.
    """
    def __init__(self, tags: list[TagView] = None):
        self.tag_views: list[TagView] = []

        if tags:
            for tag in tags:
                self.append_tag(tag)

    def __str__(self) -> str:
        """Return a printable representation of this view

        Since this object is meant to be used in templates, this default string implemntation returns the
        values of its tag views joined with commas

        Returns:
            str: Our tag view strings joined with commas
        """
        view_strings = (str(view) for view in self.tag_views)
        return ", ".join(view_strings)

    def append_tag(self, tag: Tag):
        """Add a TagView to this collection using data from the passed tag

        Args:
            tag (Tag): The tag to use for the new TagView
        """
        view = TagView(tag)
        self.tag_views.append(view)

    def all(self) -> list[TagView]:
        """Get all stored TagView objects

        Returns:
            list[TagView]: List of TagView objects
        """
        return self.tag_views

    def first(self) -> TagView:
        """Get the first TagView

        Returns:
            TagView: The first TagView object in this collection
        """
        return self.tag_views[0]

    def rest(self) -> list[TagView]:
        """Get all TagView objects after the first

        Returns:
            list[TagView]: List of TagView objects starting at index 1
        """
        return self.tag_views[1:]
