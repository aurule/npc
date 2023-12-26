from npc.settings import TagSpec

def test_has_name():
    tag_def = {"desc": "A testing tag"}

    tag = TagSpec("test", tag_def)

    assert tag.name == "test"

def test_has_desc():
    tag_def = {"desc": "A testing tag"}

    tag = TagSpec("test", tag_def)

    assert tag.desc == tag_def["desc"]

class TestCorrectness():
    def test_forces_positive_min(self):
        tag_def = {"min": -5}

        tag = TagSpec("test", tag_def)

        assert tag.min == 0

    def test_forces_positive_max(self):
        tag_def = {"max": -5}

        tag = TagSpec("test", tag_def)

        assert tag.max == 0

    def test_swaps_min_gt_max(self):
        tag_def = {
            "min": 5,
            "max": 1,
        }

        tag = TagSpec("test", tag_def)

        assert tag.min == 1
        assert tag.max == 5

    def test_forces_min_1_when_required(self):
        tag_def = {
            "required": True,
            "min": 0
        }

        tag = TagSpec("test", tag_def)

        assert tag.min == 1

    def test_allows_min_gt1_when_required(self):
        tag_def = {
            "required": True,
            "min": 5
        }

        tag = TagSpec("test", tag_def)


        assert tag.min == 5

    def test_removes_no_value_when_explicit_values_are_set(self):
        tag_def = {
            "values": ["a", "b"],
            "no_value": True,
        }

        tag = TagSpec("test", tag_def)

        assert tag.no_value == False
