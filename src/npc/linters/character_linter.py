from npc.campaign import Campaign
from npc.characters import Character
from npc.validation import CharacterValidator, TagValidator

class CharacterLinter:
    def __init__(self, character: Character, campaign: Campaign):
        self.character = character
        self.campaign = campaign
        self.errors = []

    def lint(self) -> list:
        self.errors = []
        # character is not expected to be live
        # get error messages from the character validator
        # gather tag specs from self.campaign
        #   for each required spec
        #       run a TagValidator against the tags in that set
        #       extend our errors with those from the tag validator
        #       if the spec allows subtags, iterate those tag records
        #           run a subtag linter against the each tag record's subtags as needed
        #       note handled tag IDs
        # iterate character's unhandled tags
        #   run a validator on each set
        #   if the spec allows subtags, iterate tag records
        #       run a subtag linter on each record
        # iterate deprecated tag specs
        #   make sure we don't have any of those
        return self.errors

    @property
    def ok(self) -> bool:
        return not self.errors
