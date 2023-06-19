from npc.characters import Tag
from .tag_view import TagView

class TagViewCollection:
    def __init__(self):
        self.tag_views = []

    def append_tag(tag: Tag):
        view = TagView(tag)
        self.tag_views.append(view)

    def first(self) -> TagView:
        return tag_views[0]

    def remainder(self) -> list[TagView]:
        return tag_views[1:]
