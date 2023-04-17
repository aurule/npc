class Type():
    """Object representing a character type"""
    def __init__(self, type_key: str, type_def: dict):
        self.key: str           = type_key
        self.definition: dict   = type_def
        self.name: str          = type_def.get("name", "")
        self.desc: str          = type_def.get("desc", "")

class UndefinedType():
    """Represents a character type that has no definition

    This is the null object for the Type class.
    """

    def __init__(self, *args, **kwargs):
        self.key = "undefined"
        self.definition = {}
        self.name = "Undefined"
        self.desc = "Undefined character type"
