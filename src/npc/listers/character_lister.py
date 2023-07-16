from jinja2 import Environment
from typing import TextIO
from functools import cached_property, cache
import mistletoe

from npc.characters import Character
from npc.campaign import Campaign, CharacterCollection
from npc.templates import CharacterFallbackLoader
from npc.db.query_builders import CharacterListerQueryBuilder
from npc.util import arg_or_default
from .character_view import CharacterView
from .group_view import GroupView

class CharacterLister:
    """Class to create character listings from a character collection

    This uses Jinja to create formatted listings of a collection of character objects. See the documentation
    for CharacterFallbackLoader for details about search paths and loading order for templates.

    Attributes:
        SUPPORTED_LANGUAGES: These strings are the names of listing languages that NPC ships with. It is not
            necessarily an exhaustive list, since users can add their own templates using whatever ext suits
            their fancy.
        LANG_SUFFIXES: Mapping of language names to template suffixes. Only works for the built-in languages.
    """
    SUPPORTED_LANGUAGES = {"html", "markdown"}
    LANG_SUFFIXES = {
        "html": "html",
        "markdown": "md",
    }

    def __init__(self,
        collection: CharacterCollection,
        *,
        lang: str = None,
        group_by: list[str] = None,
        sort_by: list[str] = None,
        base_header_level: int = None):
        """Create a character lister

        Args:
            collection (CharacterCollection): Character collection we'll be operating on
            lang (str): Output language to use. Defaults to the value in the settings key
                "campaign.characters.listing.format". If this language is not in SUPPORTED_LANGUAGES, it will
                be treated as the template file suffix.
        """
        self.collection: CharacterCollection = collection
        self.campaign: Campaign = collection.campaign

        settings = self.campaign.settings
        self.lang: str = arg_or_default(lang, settings.get("campaign.characters.listing.format"))
        self.group_by: list[str] = arg_or_default(group_by, settings.get("campaign.characters.listing.group_by"))
        self.sort_by: list[str] = arg_or_default(sort_by, settings.get("campaign.characters.listing.sort_by"))
        self.base_header_level: int = arg_or_default(base_header_level, settings.get("campaign.characters.listing.base_header_level"))

    def list(self, target: TextIO):
        """Generate a complete listing of all characters

        This gets the characters and generates a listing entry for each one, emitting it to the given target.

        Grouping headers are created automatically for each level of group criteria. Whenever that criterion
        changes, a new header is emitted.

        Args:
            target (TextIO): Target to receive the emitted listings
        """
        jenv = Environment(
            loader = CharacterFallbackLoader(self.campaign),
            auto_reload = False,
            autoescape = False,
        )
        jenv.filters["md"] = mistletoe.markdown
        gt = jenv.get_template
        write = target.write

        builder = CharacterListerQueryBuilder()
        builder.group_by(*self.group_by)
        builder.sort_by(*self.sort_by)

        num_groups: int = builder.next_group_index
        character_header_level: int = self.base_header_level + num_groups
        current_group_values: list[str] = []
        results = self.collection.apply_query(builder.query)

        group_template = gt(self.group_template_name)
        for row in results:
            for group_index in range(num_groups):
                row_value = row[group_index + 1]
                if group_index >= len(current_group_values) or current_group_values[group_index] != row_value:
                    current_group_values[group_index::] = [row_value]
                    write(
                        group_template.render(
                            {
                                "header_level": self.base_header_level + group_index,
                                "group": GroupView(
                                    title=row_value,
                                    grouping=builder.grouped_by[group_index]),
                            }
                        )
                    )
                    write("\n\n")

            character = row[0]
            character_template = gt(self.character_template_name(character.type_key))
            character_view = CharacterView(character)
            write(
                character_template.render(
                    {
                        "header_level": character_header_level,
                        "character": character_view,
                        "has": character_view.has,
                    }
                )
            )
            write("\n\n")

    @cached_property
    def template_suffix(self) -> str:
        """Get the template suffix to use when searching for templates

        When our lang is one of the SUPPORTED_LANGUAGES, this will look up the correct suffixe in the
        LANG_SUFFIXES table. Otherwise, our language is returned as the suffix string.

        Returns:
            str: File suffix string
        """
        return self.LANG_SUFFIXES.get(self.lang, self.lang)

    @property
    def group_template_name(self) -> str:
        """Get the name of our group template

        Returns:
            str: Name of the group template to load
        """
        return f"group_heading.{self.template_suffix}"

    @cache
    def character_template_name(self, type_key: str) -> str:
        """Get the name of a template for a character type

        The character template names are based on the charcter's type_key and use our language suffix. Jinja's
        internal template caching has a limit of 500 templates, which NPC is exceedingly unlikely to reach.

        Args:
            type_key (str): The character type we need a template for

        Returns:
            str: Charcter template name
        """
        return f"{type_key}.{self.template_suffix}"
