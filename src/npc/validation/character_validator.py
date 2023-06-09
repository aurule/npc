from npc.characters import Character
from npc.validation.errors.character_errors import *
from npc.validation.errors.tag_errors import *

class CharacterValidator:
    def __init__(self, campaign):
        self.campaign = campaign

    def validate(self, character: Character) -> list:
        errors: list = []
        char_name: str = character.realname

        char_type: str = character.type_key
        if not char_type:
            errors.append(TagEmptyError("type"))
        else:
            if char_type == Character.DEFAULT_TYPE:
                errors.append(TagRequiredError("type"))
            if char_type not in self.campaign.types.keys():
                errors.append(TagValueError("type", char_type))

        if not char_name:
            errors.append(CharacterMissingAttributeError(character.file_loc, "name"))

        if not character.desc:
            errors.append(CharacterMissingAttributeError(char_name, "description"))

        if not character.mnemonic:
            errors.append(CharacterMissingAttributeError(char_name, "mnemonic"))

        return errors
