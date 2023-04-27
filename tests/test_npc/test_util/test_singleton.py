from npc.util import Singleton

class FixtureSingleton(metaclass=Singleton):
    def __init__(self, value: str):
        self.value = value

def test_creates_one_object():
    obj = FixtureSingleton("test")
    obj2 = FixtureSingleton("nope")

    assert obj is obj2
    assert obj.value == "test"
    assert obj2.value == "test"

class ResetableSingleton(metaclass=Singleton):
    def __init__(self, value: str):
        self.value = value

def test_clear_singleton_allows_multiple_objects():
    obj = ResetableSingleton("test")
    obj2 = ResetableSingleton("nope", clearSingleton=True)

    assert obj is not obj2
    assert obj.value == "test"
    assert obj2.value == "nope"
