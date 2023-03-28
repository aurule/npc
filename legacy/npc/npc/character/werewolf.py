from .character import Character

class Werewolf(Character):
    """
    Special handling for werewolf-type characters
    """
    def __init__(self, *args, **kwargs):
        """
        Create a new Werewolf object

        Ensures that the default type value is applied if it's missing
        """
        super().__init__(*args, **kwargs)

        if not self.tags('type').filled:
            self.tags('type').append('werewolf')

    def _add_default_tags(self):
        """
        Add additional type-specific tags
        """
        self.tags.add_tag('auspice', limit=1)
        self.tags.add_group('pack', limit=1)
        self.tags.add_group('tribe', limit=1)
        self.tags.add_group('lodge', limit=1)

    def add_compound_tags(self, tags):
        """
        Create the @werewolf compound tag

        Args:
            tags (TagContainer): Container of filled tags that can be modified

        Returns:
            TagContainer with its contents modified as needed
        """
        if self.type_key != 'werewolf':
            return tags

        if 'auspice' not in tags:
            return tags

        first_auspice = tags('auspice').first_value()
        tags.add_tag('werewolf', first_auspice)
        tags['auspice'] = tags('auspice').remaining()
        tags['type'] = tags('type').remaining()

        return tags
