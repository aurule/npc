from npc.characters import Character
from npc.validation.errors.character_errors import *
from .tag_validator import TagValidator

class CharacterValidator:
    def __init__(self, character: Character):
        self.character = character
        self.errors = []

    def validate(self) -> list:
        # check for attribute problems
        # gather tag specs
        #   for each required spec, run a TagValidator against our values
        # for all non-required tags which we possess, run a TagValidator against that tag's values
        # for all deprecated tags, make sure we don't have any values
        # add tag validation results to our errors list
        return self.errors
