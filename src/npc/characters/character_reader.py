from pathlib import Path

from .tag_class import RawTag

class CharacterReader:
    NAME_SEPARATOR = " - "

    def __init__(self, character_path: Path):
        self.character_path = character_path
