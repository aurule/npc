from tests.fixtures import tmp_campaign
from npc.campaign import Campaign
from npc.characters import Character, Tag
from npc.db import DB

from npc.campaign import Pathfinder

class TestWithExistingDirsOnly:
    pass
    # character has named tag, value exists: adds to path
    # character has named tag, value not exist: does not add
    # character has two values for named tag, values both exist: adds first value
    # character does not have named tag: does not add
    # character only has second named tag, value exists: adds to path
    # character has first and second tag, values both exist: adds first tag value

class TestWithNonExistingDirs:
    def test_has_tag_adds_tag(self, tmp_campaign):
        patch = {
            "characters": {
                "subpath_components": [
                    {
                        "selector": "first_value",
                        "tags": ["test"]
                    }
                ]
            }
        }
        tmp_campaign.patch_campaign_settings(patch)
        db = DB()
        character = Character(realname="Test Mann", type_key="person", delist=False, nolint=False, sticky=False)
        tag1 = Tag(name="test", value="blep")
        character.add_tag(tag1)
        with db.session() as session:
            session.add(character)
            session.add(tag1)
            session.commit()
        finder = Pathfinder(tmp_campaign)

        result = finder.build_character_path(character, exists=False)

        assert result == tmp_campaign.characters_dir / "blep"

    # character has named tag: adds to path
    # character does not have named tag: does not add
    # character only has second named tag: adds to path

class TestWithBadSelector:
    pass
    # throws an error
