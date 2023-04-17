class Type():
    def __init__(self, type_key: str, type_def: dict):
        self.key: str           = type_key
        self.definition: dict   = type_def
        self.name: str          = type_def.get("name", "")
        self.desc: str          = type_def.get("desc", "")
