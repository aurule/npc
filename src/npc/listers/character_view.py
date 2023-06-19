from npc.characters import Character
from .tag_view_collection import TagViewCollection

class CharacterView:
    def __init__(self, character: Character):
        self.character = character

        self.type = character.type_key
        self.description = character.desc
        self.realname = character.realname
        self.mnemonic = character.mnemonic

        # ideally, character had its tags eagerly loaded
        # for every tag
        #   see if we have an attribute with the tag's name
        #   if not, create it and assign a new TagViewCollection()
        #   collection.append_tag(tag)
