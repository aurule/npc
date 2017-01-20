import npc

class TestCreation:
    """Test different instantiation behaviors"""

    def test_dict(self):
        char = npc.Character({"name": ["hello"]})
        assert char["name"] == ["hello"]

    def test_kwargs(self):
        char = npc.Character(name=["hello"])
        assert char["name"] == ["hello"]

    def test_both(self):
        char = npc.Character(attributes={"name": ["hello"], "profession": ["tailor"]}, name=["nope"])
        assert char["name"] == ["nope"]
        assert char["profession"] == ["tailor"]

class TestGetFirst:
    def test_normal(self):
        char = npc.Character(name=["hello", "goodbye"])
        assert char.get_first("name") == "hello"

    def test_desc(self):
        char = npc.Character(description="Fee Fie Foe Fum")
        assert char.get_first("description") == "Fee Fie Foe Fum"

    def test_not_present(self):
        char = npc.Character()
        assert char.get_first("nope") == None

class TestGetRemaining:
    def test_normal(self):
        char = npc.Character(name=["hello", "goodbye"])
        assert char.get_remaining("name") == ["goodbye"]

    def test_desc(self):
        char = npc.Character(description="Fee Fie Foe Fum")
        assert char.get_remaining("description") == "Fee Fie Foe Fum"

    def test_not_present(self):
        char = npc.Character()
        assert char.get_remaining("nope") == []

class TestAppend:
    def test_normal(self):
        char = npc.Character()
        char.append("title", "The Stern")
        assert char["title"] == ["The Stern"]

    def test_desc(self):
        char = npc.Character()
        char.append("description", "Hello hello")
        char.append("description", " baby, you called")
        assert char["description"] == "Hello hello baby, you called"

def test_append_rank():
    char = npc.Character()
    char.append_rank("Knights of the Round Table", "Dancer")
    assert char["rank"]["Knights of the Round Table"] == ["Dancer"]

# tests to do:
# valid
# typekey
# get first, and with string tags
# get remaining, and with string tags
# validation
# changeling validation
# has items
# copy and alter
# build header
