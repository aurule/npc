class MetatagSpec():
    """Represents a metatag definition"""

    def __init__(self, name: str, tag_def: dict):
        self.name: str              = name
        self.definition: dict       = tag_def
        self.desc: str              = tag_def.get("desc", "")
        self.doc: str               = tag_def.get("doc", "")
        self.static: dict[str, str] = tag_def.get("static", {})
        self.match: list[str]       = tag_def.get("match", [])
        self.separator: str         = tag_def.get("separator", " ")
        self.greedy: bool           = tag_def.get("greedy", False)

    @property
    def required_tag_names(self) -> list[str]:
        """Get a list of required tags

        These tag names must be present in a character for this spec to be used

        Returns:
            list[str]: List of tag names required for this spec
        """
        return list(self.static) + self.match
