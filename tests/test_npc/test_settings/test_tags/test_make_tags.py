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

        tag_names = [t.name for t in tags]
        assert tag_names == ["first", "second"]

    def test_tags_have_no_parent(self):
        tags = make_tags(self.tag_defs)

        tag_parents = [t.parent for t in tags]
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

        tag_names = [t.name for t in tags]
        assert "primero" in tag_names

    def test_makes_all_subtags(self):
        tags = make_tags(self.tag_defs)

        tag_names = [t.name for t in tags]
        assert "primero" in tag_names
        assert "segundo" in tag_names

    def test_assigns_parent(self):
        tags = make_tags(self.tag_defs)

        tag_parents = [t.parent for t in tags]
        assert "first" in tag_parents
