from . import ValidationError

class CharacterValidationError(ValidationError):
    def __init__(self, detail: str, character_name: str):
        super().__init__(detail)
        self.character_name: str = character_name
        self.preamble = f"Error in character {character_name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag_name={self.character_name!r})"

class CharacterMissingAttributeError(CharacterValidationError):
    def __init__(self, character_name: str, attribute: str):
        super().__init__(f"missing {attribute}", character_name)
        self.attribute: str = attribute
