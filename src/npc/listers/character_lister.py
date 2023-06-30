from jinja2 import Environment

from npc.characters import Character
from npc.campaign import Campaign, CharacterCollection
from npc.templates import CharacterFallbackLoader
from npc.db.query_builders import CharacterListerQueryBuilder

class CharacterLister:
    SUPPORTED_OUTPUT_TYPES = {"html", "markdown"}
    LANG_SUFFIXES = {
        "html": "html",
        "markdown": "md",
    }

    def __init__(self, collection: CharacterCollection, *, lang: str = "html"):
        self.collection = collection
        self.campaign = collection.campaign
        self.lang = lang

        jenv = Environment(
            loader = CharacterFallbackLoader(self.campaign),
            auto_reload = False,
            autoescape = False,
        )

        # get characters!
        # for entity in settings.group_by:
        #   builder.group_by(entity)
        # for entity in settings.sort_by:
        #   builder.sort_by(entity)
        #
        # character_header_level = builder.next_group_index
        # current_group_values = [None] * builder.next_group_index
        # for row in results:
        #   for each group col:
        #       if current value [index] doesn't match
        #           update that value
        #           reset values after it
        #           ask jenv to get the header template
        #           emit a group_heading template with the new value at the index header level
        #   ask jenv to get the template <type>.<ext>
        #   make a CharacterView
        #   pass the view through the template
        #       header level is character_header_level

    @property
    def template_suffix(self) -> str:
        return LANG_SUFFIXES.get(self.lang, self.lang)

    @property
    def group_template_name(self) -> str:
        return f"group_heading.{self.template_suffix}"

    def character_template_name(self, character: Character) -> str:
        return f"{character.type_key}.{self.template_suffix}"
