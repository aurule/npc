from .character import Character

class Werewolf(Character):
    """
    Special handling for werewolf-type characters
    """

    def type_validations(self, strict=False):
        """
        Validate the basics of a werewolf character

        Validations:
            * Zero or one auspice
            * Zero or one tribe
            * Zero or one pack
            * Zero or one lodge

        Any errors are added to the problems list.

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            None
        """
        self.validate_tag_appears_once('auspice')
        self.validate_tag_appears_once('tribe')
        self.validate_tag_appears_once('pack')
        self.validate_tag_appears_once('lodge')

    def type_header(self):
        """
        Create werewolf-specific header lines

        If auspice is present, adds a compound `@werewolf` line. Otherwise, it
        adds a simple `@type` line.

        Returns:
            List of strings describing the werewolf-specific tags for this
            character.
        """
        lines = []
        if 'auspice' in self.tags:
            lines.append("@werewolf {}".format(self.get_first('auspice')))
        else:
            lines.append("@type Werewolf")

        return lines
