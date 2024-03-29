import logging
logger = logging.getLogger(__name__)

class TagSpec():
    """Represents a single character tag

    TagSpec objects represent the configuration of a given tag, *not* its data.
    """

    def __init__(self, name: str, tag_def: dict):
        self.name: str          = name
        self.definition: dict   = tag_def
        self.needs_context      = False
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.replaced_by: str   = tag_def.get("replaced_by", "")
        self.required: bool     = tag_def.get("required", False)
        self.min: int           = tag_def.get("min", 0)
        self.max: int           = tag_def.get("max", 999)
        self.values: list[str]  = tag_def.get("values", [])
        self.allow_empty: bool  = tag_def.get("allow_empty", False)
        self.no_value: bool     = tag_def.get("no_value", False)
        self.locked: bool       = tag_def.get("locked", False)
        self.long: bool         = tag_def.get("long", False)
        self.subtags: list[str] = tag_def.get("subtags", {}).keys()
        self.history: list[str] = tag_def.get("history", [])

        if self.required and self.min < 1:
            logger.debug(f"Tag {self.name} is required but min is zero. Setting min to 1.")
            self.min = 1

        if self.min < 0:
            logger.warning(f"Tag {self.name} cannot have negative min. Setting min to 0.")
            self.min = 0

        if self.max < 0:
            logger.warning(f"Tag {self.name} cannot have negative max. Setting max to 0.")
            self.max = 0

        if self.min > self.max:
            logger.warning(f"Tag {self.name} has min {self.min} greater than max {self.max}. Swapping.")
            old_min = self.min
            self.min = self.max
            self.max = old_min

        if self.values and self.no_value:
            logger.warning(f"Tag {self.name} has list of accepted values, but is flagged no_value. Removing flag.")
            self.no_value = False

    def __repr__(self) -> str:
        return f"TagSpec(name={self.name!r}, subtags={self.subtags!r})"

    def add_context(self, parent_key: str, *args):
        raise TypeError(f"The tag {parent_key} is trying to use {self.name} as a subtag, but {self.name} is already defined as a regular tag")

    def in_context(self, parent_key: str, default = None):
        return self

class UndefinedTagSpec(TagSpec):
    """Represents a tag that has no definition

    This is the null object for the TagSpec class.
    """

    def __init__(self, name: str):
        super().__init__(name, tag_def={})

    def __repr__(self) -> str:
        return f"UndefinedTagSpec(name={self.name!r})"
