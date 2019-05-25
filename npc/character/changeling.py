from .character import Character

class Changeling(Character):
    """
    Special handling for changeling-type characters
    """

    def _set_default_type(self):
        """
        Set the default character type
        """
        self.tags['type'] = ['changeling']

    def type_validations(self, strict=False):
        """
        Validate the basic elements of a changeling file

        Validations:
            * Seeming is present
            * Kith is present
            * Zero or one court is present
            * Zero or one motley is present
            * Zero or one entitlement is present

        Any errors are added to the problems list.

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            None
        """
        self.validate_tag_present_and_filled('seeming')
        self.validate_tag_present_and_filled('kith')
        self.validate_tag_appears_once('court')
        self.validate_tag_appears_once('motley')
        self.validate_tag_appears_once('entitlement')

    def type_header(self):
        """
        Create changeling-specific header lines

        If both seeming and kith are present, adds a compound `@changeling`
        line. Otherwise, it lists type and seeming or kith as available.

        Returns:
            List of strings describing the changeling-specific tags for this
            character.
        """
        lines = []

        if 'seeming' in self.tags and 'kith' in self.tags:
            lines.append("@changeling {} {}".format(self.get_first('seeming'), self.get_first('kith')))
        else:
            lines.append("@type Changeling")
            if 'seeming' in self.tags:
                lines.append("@seeming {}".format(self.get_first('seeming')))
            if 'kith' in self.tags:
                lines.append("@kith {}".format(self.get_first('kith')))

        return lines
