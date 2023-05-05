from tests.fixtures import tmp_campaign
from npc.characters import Character, Tag

from npc.characters import CharacterFactory

class TestWithBareStack():
    def test_puts_regular_tag_in_character(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = Tag(name="race", value="elf")
        tag.spec = tmp_campaign.get_tag("race")
        stack = [character]

        factory.insert_tag_record(tag, stack)

        assert character.tags[0] == tag

    def test_puts_subtag_in_character(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = Tag(name="job", value="chef")
        tag.spec = tmp_campaign.get_tag("job").in_context(character)
        stack = [character]

        factory.insert_tag_record(tag, stack)

        assert character.tags[0] == tag

class TestWithFilledStack():
    def test_puts_regular_tag_in_character(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        parent = Tag(name="group", value="The Society")
        parent.spec = tmp_campaign.get_tag("group")
        tag = Tag(name="race", value="elf")
        tag.spec = tmp_campaign.get_tag("rank")
        stack = [character, parent]

        factory.insert_tag_record(tag, stack)

        assert character.tags[0] == tag

    def test_puts_correct_subtag_in_tag(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        parent = Tag(name="group", value="The Society")
        parent.spec = tmp_campaign.get_tag("group")
        tag = Tag(name="rank", value="Flagger")
        tag.spec = tmp_campaign.get_tag("rank")
        stack = [character, parent]

        factory.insert_tag_record(tag, stack)

        assert tag in parent.subtags
