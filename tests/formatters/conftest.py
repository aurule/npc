import npc
import pytest

@pytest.fixture(scope="module")
def character():
    char = npc.Character()
    char.append('description', 'Fee fie foe fum')
    char.append('type', 'human')
    return char
