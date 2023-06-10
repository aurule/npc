from npc.campaign import Campaign
from npc.characters import Character, CharacterReader, CharacterFactory
from npc.validation import CharacterValidator, TagValidator
from .tag_bucket import TagBucket

import logging
logger = logging.getLogger(__name__)

class CharacterLinter:
    def __init__(self, character: Character, campaign: Campaign):
        self.character = character
        self.campaign = campaign
        self.errors = []

    def lint(self) -> list:
        character_validator = CharacterValidator(self.campaign)
        self.errors = character_validator.validate(self.character)

        tag_bucket = TagBucket(self.character)

        reader = CharacterReader(self.character.file_path)
        factory = CharacterFactory(self.campaign)
        tag_context_stack = [tag_bucket]
        for rawtag in reader.tags():
            factory.apply_raw_tag(rawtag, tag_bucket, tag_context_stack)


        self.check_tags(tag_bucket, self.campaign.tags.values())

    def check_tags(self, bucket: TagBucket, available_specs: list):
        handled_specs = []

        required_specs = (spec for spec in available_specs if (spec.required or spec.min))
        for spec in required_specs:
            logger.debug(f"tag {spec.name} is required")
            self.validate_spec(spec, bucket.tags[spec.name])
            self.handled_specs.append(spec.name)

        # handle deprecated tags
        # handled_specs.extend(deprecations)

        remaining_specs = (spec for spec in available_specs if spec.name not in handled_specs and spec.name in bucket.tags.keys())
        for spec in remaining_specs:
            logger.debug(f"tag {spec.name} was found")
            self.validate_spec(spec, bucket.tags[spec.name])

        # handle tags with no spec

    def validate_spec(self, spec, tags: list):
        """Validate a list of tags against the given spec, then check their subtags

        For most tags, this simply uses a TagValidator on the list of supplied tags. For tags whose definition
        allows subtags, a new set of allowed subtag specs is created. For every tag in our list, a new list of
        subtags is created and checked using check_tags() to ensure requirements, deprecations, etc. are
        handled properly.

        Args:
            spec (TagSpec): The spec to check the tags against
            tags (list): The tags to be checked
        """
        validator = TagValidator(spec)
        self.errors.extend(validator.validate(tags))
        if spec.subtags:
            subtag_specs = [self.campaign.get_tag(subtag_name).in_context(spec.name) for subtag_name in spec.subtags]
            subtag_bucket = TagBucket()
            for tag in tags:
                for subtag in tag.subtags:
                    subtag_bucket.add_tag(subtag)
                self.check_tags(subtag_bucket, subtag_specs)
