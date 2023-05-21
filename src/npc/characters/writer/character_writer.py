from npc.campaign import Campaign
from ..character_class import Character
from ..tag_class import Tag
from npc.db import DB, character_repository
from .helpers import viable_character, make_contags

class CharacterWriter:
    def __init__(self, campaign: Campaign, db=None):
        self.campaign = campaign
        self.block_defs = campaign.settings.get("npc.tag_blocks")
        self.blocks = campaign.settings.get("campaign.characters.use_blocks")

        if not db:
            self.db = DB()
        else:
            self.db = db

    def write(self, character: Character):
        contents = self.make_contents(character)

        # with the full string available, open character.file_path
        #   write out generated string
        #   write character.file_body

    def make_contents(self, character: Character) -> str:
        if not viable_character(character):
            raise AttributeError(f"Character {character!r} is missing minimal required attributes (id, realname)")

        chunks: list[str] = []
        rest_index: int = None
        handled_tag_ids: list[str] = []
        constructed_tags: dict = make_contags(character) # key is tag name, value is array of ConTag or Metatag objects

        if character.desc:
            chunks.append(character.desc)

        # generate metatags
        #   for each metatag definition in campaign.metatags
        #       for every static entry
        #           get the first tag whose name and value matches the config and ID is not in metatag_consumed
        #           if not found, abort
        #       for every match entry
        #           get the first tag whose name matches and ID is not in metatag_consumed
        #           if not found, abort
        #       store that info, including tag IDs, for later use
        #           put tag IDs into a special metatag_consumed list
        #           store in constructed_tags
        #       if the metatag is greedy, repeat this process until it fails

        for blockname in self.blocks:
            block_def = self.block_defs.get(blockname, [])
            if "*" in block_def:
                rest_index = len(chunks)

            tags: list = []

            # get constructed tags
            for key in block_def:
                if key in constructed_tags:
                    tags.append(constructed_tags.pop(key))

            # get normal tags
            tags_query = character_repository.tags_by_name(character, *block_def)
            tags_query.where(Tag.id.not_in(handled_tag_ids))
            with self.db.session() as session:
                tags.extend(session.scalars(tags_query).all())

            if len(tags):
                chunks.append("")
                chunks.extend([tag.emit() for tag in tags])
                handled_tag_ids.extend([tag.id for tag in tags if tag.id])

        # now that everything explicitly listed has been handled, insert the remaining tags at rest_index
        remainder_query = character_repository.tags(character).where(Tag.id.not_in(handled_tag_ids))
        with self.db.session() as session:
            remaining_tags = session.scalars(remainder_query).all()
        if len(remaining_tags):
            if rest_index is None:
                rest_index = len(chunks)
            chunks.insert(rest_index, "\n".join([tag.emit() for tag in remaining_tags]))

        return "\n".join(chunks)
