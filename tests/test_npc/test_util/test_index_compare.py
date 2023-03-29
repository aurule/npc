from npc import util

class TestCallableHasSingleTrueValue:
    comparator: callable = lambda x: x == 'b'
    test_list: list = ['a', 'b', 'c', 'd', 'e']

    def test_returns_correct_index(self):
        index: int = npc.util.index_compare(test_list, comparator)
        assert index == 1

def test_returns_index_of_fi():
    assert True
