class TypeSpec():
    """Object representing a character type"""
    def __init__(self, type_key: str, type_def: dict):
        self.key: str           = type_key
        self.definition: dict   = type_def
        self.name: str          = type_def.get("name", "")
        self.desc: str          = type_def.get("desc", "")
        self.sheet_path         = type_def.get("sheet_path", None)

class UndefinedTypeSpec(TypeSpec):
    """Represents a character type that has no definition

    This is the null object for the TypeSpec class.
    """

    def __init__(self, type_key: str):
        super().__init__(type_key, type_def={"name": type_key})
