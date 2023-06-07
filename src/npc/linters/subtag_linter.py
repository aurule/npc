from npc.campaign import Campaign
from npc.characters import Tag
from npc.validation import TagValidator

class SubtagLinter:
    def __init__(self, parent_tag: Tag, campaign: Campaign):
        self.parent_tag = parent_tag
        self.campaign = campaign
        self.errors = []

    def lint(self) -> list:
        self.errors = []
        # assume our own tag has already been validated
        # gather specs for our subtags
        # validate subtags
        # if a subtag spec allows for more subtags, make a new subtag linter and recurse
        return self.errors

    @property
    def ok(self) -> bool:
        return not self.errors
