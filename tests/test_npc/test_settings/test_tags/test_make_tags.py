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

    def test_tags_have_no_parent(self):
        tags = make_tags(self.tag_defs)

        tag_parents = [t.parent for t in tags.values()]
        assert tag_parents == [None, None]

class TestSubtags():
    tag_defs = {
        "first": {
            "desc": "First tag",
            "subtags": {
                "primero": {
                    "desc": "First of firsts"
                },
                "segundo": {
                    "desc": "Second of firsts"
                }
            }
        }
    }

    def test_flattens_subtags(self):
        tags = make_tags(self.tag_defs)

        assert "primero" in tags

    def test_makes_all_subtags(self):
        tags = make_tags(self.tag_defs)

        assert "primero" in tags
        assert "segundo" in tags

    def test_adds_context(self):
        tags = make_tags(self.tag_defs)

        assert "first" in tags.get("primero").contexts
