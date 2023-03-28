from .tag import Tag

class SubTag(Tag):
    """
    Tag object used to store sub-values for a group tag
    """
    def to_header(self, parent_name: str, key_name: str):
        """
        Generate the header string for this subtag

        The header is similar to that for a normal tag, except for the @hide
        line.

        Args:
            key_name (str): Group tag value text to which this subtag is related.
        """
        if not self.filled:
            return ''

        header_lines = []
        for val in self.data:
            header_lines.append("@{} {}".format(self.name, val))
            if val in self.hidden_values:
                header_lines.append("@hide {} >> {} >> {}".format(parent_name, key_name, val))

        if self.hidden:
            header_lines.append("@hide {} >> {} >> subtags".format(parent_name, key_name))

        return "\n".join(header_lines)
