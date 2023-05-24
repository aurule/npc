from npc.settings import MetatagSpec

from npc.characters.writer.metatag_class import Metatag

def make_spec() -> MetatagSpec:
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
        "separator": " :: "
    }
    return MetatagSpec("monster", metatag_def)

def test_includes_name():
    metatag = Metatag(make_spec())

    result = metatag.emit()

    assert "monster" in result

def test_includes_match_values():
    metatag = Metatag(make_spec())
    metatag.match_values = ["abby normal", "chonk"]

    result = metatag.emit()

    assert "abby normal" in result
    assert "chonk" in result

def test_uses_separator():
    metatag = Metatag(make_spec())
    metatag.match_values = ["abby normal", "chonk"]

    result = metatag.emit()

    assert "abby normal ::" in result

def test_excludes_statics():
    metatag = Metatag(make_spec())

    result = metatag.emit()

    assert "test" not in result
