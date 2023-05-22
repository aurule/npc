class MetatagSpec():
    def __init__(self, name: str, tag_def: dict):
        self.name: str          = name
        self.definition: dict   = tag_def
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.static: dict       = tag_def.get("static", {})
        self.match: list        = tag_def.get("match", [])
        self.separator          = tag_def.get("separator", " ")
        self.greedy             = tag_def.get("greedy", False)
