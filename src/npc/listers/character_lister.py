from npc.campaign import CharacterCollection

class CharacterLister:
    def __init__(
        self,
        collection: CharacterCollection,
        *,
        lang: str = "html"):
        self.collection = collection
        self.campaign = self.collection.campaign
        self.lang = lang

        # for character in collection.all()
        #   find and cache the correct template based on system and type
        #   make a CharacterView
        #   pass the view through the template
        # open questions:
        # * how to handle grouping?
