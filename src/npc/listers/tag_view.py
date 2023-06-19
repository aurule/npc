from npc.characters import Tag

class TagView:
    def __init__(self, tag: Tag):
        self.name = tag.name
        self.value = tag.value

        # for subtag in tag
        #   see if we have an attribute with the subtag's name
        #   if not, create it and assign a new TagViewCollection(name)
        #   collection.append_tag(subtag)

