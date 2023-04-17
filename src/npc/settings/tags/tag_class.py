class Tag():
    """Represents a single character tag

    Tag objects represent the configuration of a given tag, *not* its data.
    """

    def __init__(self, name: str, tag_def: dict):
        self.definition: dict   = tag_def
        self.name: str          = name
        self.definition         = tag_def
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.required: bool     = tag_def.get("required", False)
        self.min: int           = tag_def.get("min", 0)
        self.max: int           = tag_def.get("max", 999)
        self.allow_empty: bool  = tag_def.get("allow_empty", False)
        self.no_value: bool     = tag_def.get("no_value", False)
        self.subtags: list[str] = tag_def.get("subtags", {}).keys()
        self.parent: str        = None
