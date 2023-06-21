from jinja2 import Environment

from npc.campaign import Campaign, CharacterCollection
from npc.templates import CharacterFallbackLoader

class CharacterLister:
    def __init__(self, campaign: Campaign, *, characters: CharacterCollection = None, lang: str = "html"):
        self.campaign = campaign
        self.lang = lang

        if characters:
            self.characters = characters
        else:
            self.characters = campaign.characters

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
