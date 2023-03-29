import npc
import pytest

@pytest.fixture(scope="module")
def character():
    char = npc.character.Character()
    char.tags('description').append('Fee fie foe fum')
    char.tags('type').append('human')
    return char
