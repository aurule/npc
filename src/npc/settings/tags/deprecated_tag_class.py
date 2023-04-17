class DeprecatedTag():
    """Represents a single, deprecated character tag

    This object exists mostly for linting and validation purposes, as deprecated tags should not be used in
    character data.
    """

    def __init__(self, name: str, tag_def: dict):
        self.name: str          = name
        self.definition: dict   = tag_def
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.replaced_by: str   = tag_def.get("replaced_by", None)
        self.deprecation_version: str = tag_def.get("deprecated", "")
