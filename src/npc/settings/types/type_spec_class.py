from pathlib import Path

import logging
logger = logging.getLogger(__name__)

class TypeSpec():
    """Object representing a character type"""
    def __init__(self, type_key: str, type_def: dict):
        self.key: str           = type_key
        self.definition: dict   = type_def
        self.name: str          = type_def.get("name", "")
        self.desc: str          = type_def.get("desc", "")
        self.doc: str          = type_def.get("doc", "")
        self.sheet_loc          = type_def.get("sheet_path", None)

    def __repr__(self):
        return f"TypeSpec(key={self.key!r}, name={self.name!r})"

    @property
    def sheet_path(self) -> Path:
        """Get the default sheet file as a Path object

        Returns:
            Path: Path to the default sheet file
        """
        try:
            return Path(self.sheet_loc)
        except:
            return None

    @property
    def default_sheet_suffix(self) -> str:
        """Get the filename suffix for this type's default sheet

        If a default sheet exists, we use its suffix. If not, we fall back on ".npc".

        Returns:
            str: Suffix of the default sheet, or ".npc" if that is not defined
        """
        if not self.sheet_path:
            return ".npc"
        return self.sheet_path.suffix

    def default_sheet_body(self) -> str:
        """Get the contents of the default sheet file

        If no file exists or can be found, a placeholder string will be provided instead

        Returns:
            str: Default sheet file
        """
        if not self.sheet_path:
            logger.debug(f"No default sheet for type {self.key}")
            return "--Notes--"
        with self.sheet_path.open('r', newline="\n") as sheet:
            return sheet.read()

class UndefinedTypeSpec(TypeSpec):
    """Represents a character type that has no definition

    This is the null object for the TypeSpec class.
    """

    def __init__(self, type_key: str):
        super().__init__(type_key, type_def={"name": type_key})
