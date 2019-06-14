from .character import Character

class Changeling(Character):
    """
    Special handling for changeling-type characters
    """
    def __init__(self, *args, **kwargs):
        """
        Create a new Changeling object

        Ensures that the default type value is applied if it's missing
        """
        super().__init__(*args, **kwargs)

        if not self.tags('type').filled:
            self.tags('type').append('changeling')

    def _add_default_tags(self):
        """
        Add additional type-specific tags
        """
        self.tags.add_tag('seeming', required=True)
        self.tags.add_tag('kith', required=True)
        self.tags.add_tag('mask')
        self.tags.add_tag('mien')
        self.tags.add_tag('freehold')
        self.tags.add_group('court', limit=1)
        self.tags.add_group('motley', limit=1)
        self.tags.add_group('entitlement', limit=1)

    def add_compound_tags(self, tags):
        """
        Create the @changeling tag

        Args:
            tags (TagContainer): Container of filled tags that can be modified

        Returns:
            TagContainer with its contents modified
        """
        if self.type_key != 'changeling':
            return tags

        if 'seeming' not in tags:
            return tags
        if 'kith' not in tags:
            return tags

        first_seeming = tags('seeming').first_value()
        first_kith = tags('kith').first_value()
        tags.add_tag('changeling', ' '.join([first_seeming, first_kith]))
        tags['type'] = tags('type').remaining()
        tags['seeming'] = tags('seeming').remaining()
        tags['kith'] = tags('kith').remaining()

        return tags
