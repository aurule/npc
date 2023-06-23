from jinja2 import Environment

from npc.characters import Character
from npc.campaign import Campaign, CharacterCollection
from npc.templates import CharacterFallbackLoader

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

        # settings are in campaign.settings.get("campaign.characters.listing")

        # need to group characters
        #   basically a fancy sort-by
        #   support tag value
        #   support meta and non-tag values:
        #       * realname (first letter group)
        #       * last_name (first letter group)
        #       * type

        # need to sort characters:
        #   sorting is applied after group sort

        # need to get the correct extension based on language

        jenv = Environment(
            loader = CharacterFallbackLoader(self.campaign),
            auto_reload = False,
            autoescape = False,
        )

        # apply group_by grouping and sorting to campaign.characters
        # add sort_by to that query
        # make a jenv
        # group_levels = settings.group_by
        # character_header_level = settings.base_header_level + len(group_levels)
        # current_group_values = {v: None for v in group_levels}
        # for character in result set:
        #   for each grouped value in character:
        #       if current_group_values[value] is different than ours
        #           update that value and the value of all groupings after it in group_levels
        #           emit a group_heading template with the new value
        #               header level is settings.base_header_level + index of group name in group_levels
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
