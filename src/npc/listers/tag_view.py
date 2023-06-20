from npc.characters import Tag

class TagView:
    """A static representation of a tag's values and subtags

    This class dynamically creates attributes for each subtag name during initialization. This lets templates
    easily access subtag values.
    """
    def __init__(self, tag: Tag):
        from .tag_view_collection import TagViewCollection

        self.name: str = tag.name
        self.value: str = tag.value

        for subtag in tag.subtags:
            if not hasattr(self, subtag.name):
                setattr(self, subtag.name, TagViewCollection())
            getattr(self, subtag.name).append_tag(subtag)

    def __str__(self) -> str:
        """Return a printable representation of this view

        Since this object is meant to be used in templates, this default string implemntation returns the
        value of the view's associated tag.

        Returns:
            str: Our value string
        """
        return self.value
