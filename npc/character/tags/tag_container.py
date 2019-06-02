from collections import UserDict

from .unknown_tag import UnknownTag

class TagContainer(UserDict):
    """
    Manages a coherent group of tags

    Instances are callable
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def append(self, tag):
        if tag.name in self.data:
            return

        self.data[tag.name] = tag

    def __call__(self, tag_name):
        tag = self.data.get(tag_name)
        if tag is None:
            tag = UnknownTag(tag_name)
            self.append(tag)
        return tag

    def __iter__(self):
        iter(self.data.values())

    def names(self):
        return self.data.keys()

    def present(self):
        for tag in self.data:
            if tag.present:
                yield tag
