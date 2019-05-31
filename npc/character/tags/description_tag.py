from .tag import Tag

class DescriptionTag(Tag):
    """
    Special tag object that holds bare text data

    This is designed to be used for the description text from a sheet. This data
    is stored, but not prefixed with a tag name.
    """
    def __init__(self, *args):
        """
        Create a new description tag

        Descriptions are always required, never hidden, and never limited.
        """
        super().__init__('description', *args, required=True, hidden=False, limit=-1)

    def to_header(self):
        """
        Generate the header string for this description

        If the description is empty, return an empty string. Otherwise, the raw
        data is joined together and returned with no '@tag' components.
        """
        if not self.present:
            return ''

        return "\n".join(self.data)
