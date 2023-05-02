from npc.characters.tag_class import RawTag
from npc.settings.tag_definer_interface import TagDefiner
from npc.settings.tags import UndefinedTagSpec, SubTagSpec

class Metatag():
    def __init__(self, name: str, tag_def: dict):
        self.name: str          = name
        self.definition: dict   = tag_def
        self.desc: str          = tag_def.get("desc", "")
        self.doc: str           = tag_def.get("doc", "")
        self.static: dict       = tag_def.get("static", {})
        self.match: list        = tag_def.get("match", [])
        self.separator          = tag_def.get("separator", " ")

    def expand(self, meta_value: str, definer: TagDefiner) -> list[RawTag]:
        def try_contexts(spec):
            for rawtag in reversed(tags):
                if spec.in_context(rawtag.name):
                    return spec.in_context(rawtag.name)
            return UndefinedTagSpec(spec.name)

        working_value: str = meta_value
        tags = [RawTag(name, value) for name, value in self.static.items()]
        spec_stack = []

        for tag_name in self.match:
            spec = definer.get_tag(tag_name)
            if isinstance(spec, SubTagSpec):
                spec = try_contexts(spec)

            for value in spec.values:
                print(f'"{tag_name}:{value} in {working_value}"')
                if working_value.startswith(value):
                    print(f"found {value} in {working_value}")
                    tags.append(RawTag(tag_name, value))
                    working_value = working_value.removeprefix(value).lstrip(self.separator)

            value_parts = working_value.partition(self.separator)
            tags.append(RawTag(tag_name, value_parts[0]))
            working_value = value_parts[2]

        return tags

    def condense(self, tags: list):
        raise NotImplementedError
