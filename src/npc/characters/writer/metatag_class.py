from npc.settings import MetatagSpec
from npc.characters.tag_class import Tag

class Metatag:
    def __init__(self, spec: MetatagSpec):
        self.spec: MetatagSpec = spec
        self.open_names: list[str] = spec.required_tag_names.copy()
        self.tag_ids: list[int] = []
        self.match_values: list[str] = []

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def required_tag_names(self) -> list:
        return self.spec.required_tag_names

    def consider(self, tag: Tag):
        """See if a tag fits this metatag

        To fit, a tag must:
        * appear in our spec's required_tag_names
        * match a name that has not been used yet
        * if it matches a static tag, its value must match the stated value in the spec

        Matching tags have their id added to our tag_ids and their name removed from the open_names list. Tags
        in the spec's match list also have their values added to our match_values. After this, consider() is
        called on each subtag of that tag.

        This method does not enforce the order of tags, even though that's pretty critical to the parsing
        process. Call consider() in the correct order or you may generate metatags that cannot be read.

        The tag object is never modified by this method.

        Args:
            tag (Tag): The tag to try to fit in this metatag
        """
        if tag.name not in self.open_names:
            return

        if tag.name in self.spec.static and tag.value != self.spec.static[tag.name]:
            return

        self.tag_ids.append(tag.id)
        self.open_names.remove(tag.name)
        if tag.name in self.spec.match:
            self.match_values.append(tag.value)

        for subtag in tag.subtags:
            self.consider(subtag)

    def satisfied(self) -> bool:
        """Get whether this metatag has received all required tags

        If our open_names is empty, then all required tags have been filled. The open_names list is supposed
        to be manipulated by the consider() method, to make sure that other attributes are set appropriately.

        Returns:
            bool: True if all required names are filled, false if not
        """
        return not self.open_names

    def emit(self) -> str:
        """Generate a parseable representation of this metatag

        Matched values are added in order, with the spec's separator
            @changeling seeming kith

        Returns:
            str: Parseable version of the metatag
        """
        values: str = self.spec.separator.join(self.match_values)
        return f"@{self.spec.name} {values}"
