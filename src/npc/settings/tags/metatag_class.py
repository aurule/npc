class Metatag():
    def __init__(self, name: str, tag_def: dict):
        self.name: str          = name
        self.definition: dict   = tag_def
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.set: dict          = tag_def.get("set", {})
        self.match: list        = tag_def.get("match", [])

    def expand(self, value: str) -> list:
        pass

    def condense(self, tags: list):
        pass
