from .character import Character

class Spirit(Character):
    """
    Special handling for changeling-type characters
    """
    def __init__(self, *args, **kwargs):
        """
        Create a new Spirit object

        Ensures that the default type value is applied if it's missing
        """
        super().__init__(*args, **kwargs)

        if not self.tags('type').filled:
            self.tags('type').append('spirit')

    def _add_default_tags(self):
        """
        Add additional type-specific tags
        """
        self.tags.add_tag('ban', required=True)
