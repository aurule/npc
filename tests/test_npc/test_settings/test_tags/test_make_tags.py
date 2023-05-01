from npc.settings.tags import make_tags

class TestTopLevelTags():
    tag_defs = {
        "first": {
            "desc": "First tag"
        },
        "second": {
            "desc": "Second tag"
        }
    }

    def test_makes_all_tags(self):
        tags = make_tags(self.tag_defs)

        assert "first" in tags
        assert "second" in tags
