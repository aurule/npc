from . import ValidationError

class CharacterValidationError(ValidationError):
    """Base character validation error object

    Alters the preamble of the ValidationError class and stores the character name.
    """
    def __init__(self, detail: str, character_name: str):
        super().__init__(detail)
        self.character_name: str = character_name
        self.preamble = f"Error in character {character_name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(character={self.character_name!r})"

class CharacterMissingAttributeError(CharacterValidationError):
    def __init__(self, character_name: str, attribute: str):
        super().__init__(f"missing {attribute}", character_name)
        self.preamble = f"Attribute error"
        self.attribute: str = attribute

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(character_name={self.character_name!r}, attribute={self.attribute!r})"
