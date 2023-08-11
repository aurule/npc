from npc.characters.character_class import Character
from npc.characters.tag_class import Tag
from npc.db import DB, character_repository
from .helpers import *

class CharacterWriter:
    def __init__(self, campaign, *, db = None):
        self.campaign = campaign
        self.block_defs = campaign.settings.get("npc.tag_blocks")
        self.blocks = campaign.settings.get("campaign.characters.use_blocks")
        self.db = db if db else DB()

    def write(self, character: Character):
        """Write the contents of a character file

        Opens the file at character.file_path, creating it if necessary, and writes the output of
        tag_strings along with the character.file_body string.

        Args:
            character (Character): [description]
        """
        contents = self.tag_strings(character)
        dest = character.file_path

        dest.touch(exist_ok=True)

        with dest.open('w', newline="\n") as char_file:
            char_file.write(contents)
            char_file.write("\n\n")
            char_file.write(character.file_body)

    def tag_strings(self, character: Character) -> str:
        """Create the contents of the tag section for a character file

        Constructed tags are generated, followed by metatags. Any tag records that appear in a metatag are
        excluded from future output. Then, the character's tag records, contags, and metatags are emitted
        using the block definitions and order in the campaign settings.

        Args:
            character (Character): Character we're generating for

        Returns:
            str: Big string of the character's tag text

        Raises:
            AttributeError: If the character does not meet the conditions in helpers.viable_character (id and
            realname present).
        """
        if not viable_character(character):
            raise AttributeError(f"Character {character!r} is missing minimal required attributes (id, realname)")

        chunks: list[str] = []
        rest_index: int = None

        handled_tag_ids: list[int] = []
        constructed_tags: dict[str, list] = make_contags(character)

        if character.desc:
            chunks.append(character.desc)

        for metatag_def in self.campaign.metatags.values():
            metatags = make_metatags(metatag_def, character, handled_tag_ids)
            for metatag in metatags:
                if metatag.name not in constructed_tags:
                    constructed_tags[metatag.name] = []
                constructed_tags[metatag.name].append(metatag)
                handled_tag_ids.extend(metatag.tag_ids)
                for tag_name in metatag.required_tag_names:
                    if tag_name in constructed_tags:
                        del constructed_tags[tag_name]

        for blockname in self.blocks:
            block_def = self.block_defs.get(blockname, [])
            if "*" in block_def:
                rest_index = len(chunks)

            tags: list = []

            # get constructed tags
            for key in block_def:
                if key in constructed_tags:
                    tags.extend(constructed_tags.pop(key))

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
            remainder_result = session.scalars(remainder_query).all()

        if len(constructed_tags) or len(remainder_result):
            if rest_index is None:
                rest_index = len(chunks)
            remaining_contags = constructed_tags.values()
            chunks.insert(rest_index, "\n".join([tag.emit() for tag in remainder_result]))
            chunks.insert(rest_index, "\n".join([tag[0].emit() for tag in remaining_contags]))

        return "\n".join(chunks)
