from . import ValidationError

class CharacterValidationError(ValidationError):
    def __init__(self, message: str, name: str):
        super().__init__(f"Error in character {name}: {message}", name)

class CharacterMissingAttributeError(ValidationError):
    def __init__(self, name: str, attribute: str):
        super().__init__(f"missing {attribute}", name)
