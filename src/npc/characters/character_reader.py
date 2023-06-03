import re
from pathlib import Path
from functools import cache

from .tag_class import RawTag

class CharacterReader:
    """A specialized parser for character files

    This class extracts the name, mnemonic, tags, and body from various parts of a character file. The name
    and mnemonic come from the filename, where they are expected to be split by NAME_SEPARATOR. The tags are
    pulled from the file's contents, where they are required to appear first. The body begins at the first
    section header, which must start with "--".

    CharacterReader objects are intended to be short lived. They cache the result of parsing the file, so any
    changes made after the first read will not be read.
    """

    NAME_SEPARATOR = " - "
    SECTION_HEADER_RE = re.compile(r"^--")
    TAG_RE = re.compile(r"^@(?P<name>\w+)\s+(?P<value>.*)$")

    def __init__(self, character_path: Path):
        self.character_path: Path = character_path
        self._tags: list[RawTag] = []
        self._body: str = ""

    def name(self) -> str:
        """Get the character name from its filename

        The part of the filename before the NAME_SEPARATOR string is the default character name. This method
        gets that substring. If the separator is not present, the entire filename will be returned, minus the
        suffix.

        Returns:
            str: First part of the filename
        """
        parts = self.character_path.stem.partition(self.NAME_SEPARATOR)
        return parts[0]

    def mnemonic(self) -> str:
        """Get the character mnemonic from its filename

        The part of the filename after the NAME_SEPARATOR string is the mnemonic. This method gets it. If the
        separator is not present, an empty string is returned.

        Returns:
            str: The second part of the filename, or an empty string
        """
        parts = self.character_path.stem.partition(self.NAME_SEPARATOR)
        return parts[2]

    def tags(self) -> list[RawTag]:
        """Get the tags from our character file

        Tags each appear on their own line in the format "@tagname value". If the file has not yet been
        parsed, parse_file() will be called to collect the tag data.

        Returns:
            list[RawTag]: List of RawTag objects ready for further work
        """
        if not self._tags:
            self.parse_file()

        return self._tags

    def body(self) -> str:
        """Get the body of our character file

        The body is everything that isn't a tag and starts on the first line that looks like a section header.
        If the file has not yet been parsed, parse_file() will be called to collect the body data.

        Returns:
            str: File body string
        """
        if not self._body:
            self.parse_file()

        return self._body

    @cache
    def parse_file(self):
        """Parse the file into tags and body"""
        with self.character_path.open('r', newline="\n") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if self.SECTION_HEADER_RE.match(line):
                    self._body = line + file.read()
                    return

                if match := self.TAG_RE.match(line):
                    self._tags.append(RawTag(match.group("name"), match.group("value")))
                else:
                    self._tags.append(RawTag("description", line))
