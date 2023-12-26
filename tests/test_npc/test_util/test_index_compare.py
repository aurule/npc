from npc.util import index_compare

class TestCallableHasSingleTrueValue:

    def test_returns_correct_index(self):
        test_list: list = ['a', 'b', 'c', 'd', 'e']
        comparator: callable = lambda x: x == 'b'
        
        index: int = index_compare(test_list, comparator)
        
        assert index == 1

class TestCallableHasMultipleTrueValues:
    def test_returns_first_true_index(self):
        test_list: list = ['a', 'b', 'c', 'd', 'e']
        comparator: callable = lambda x: x in ['b', 'e']
        
        index: int = index_compare(test_list, comparator)
        
        assert index == 1

class TestCallableHasNoTrueValue:
    def test_returns_negative_index(self):
        test_list: list = ['a', 'b', 'c', 'd', 'e']
        comparator: callable = lambda x: x == 'n'
        
        index: int = index_compare(test_list, comparator)
        
        assert index == -1
