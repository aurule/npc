from npc.campaign import Campaign
from npc.characters import Character, CharacterReader, CharacterTagger
from npc.validation import CharacterValidator, TagValidator
from npc.validation.errors.tag_errors import TagDeprecatedError, TagUndefinedError
from .tag_bucket import TagBucket

import logging
logger = logging.getLogger(__name__)

class CharacterLinter:
    """Lint a character file

    This uses the character validator to check for obvious errors, then checks more opinionated attributes
    as well.
    """

    def __init__(self, character: Character, campaign: Campaign):
        self.character = character
        self.campaign = campaign
        self.errors = []

    def lint(self) -> list:
        """Check our character for problems

        Runs a character linter and then various tag linters. Does not check that the tags and character
        attributes actually match.

        Returns:
            list: List of ValidationError objects, or empty.
        """
        character_validator = CharacterValidator(self.campaign)
        self.errors = character_validator.validate(self.character)

        if not (self.character.file_loc and self.character.file_path.exists()):
            return self.errors

        reader = CharacterReader(self.character.file_path)
        tag_bucket = TagBucket(self.character)
        tagger = CharacterTagger(self.campaign, tag_bucket)
        for rawtag in reader.tags():
            tagger.apply_raw_tag(rawtag, mapped=False)

        specs = [
            spec
            for spec in self.campaign.tags.values()
            if not spec.needs_context
        ]
        self.check_tags(tag_bucket, specs)

        return self.errors

    def check_tags(self, bucket: TagBucket, available_specs: list) -> list:
        """Check a bucket of tags for errors

        The passed specs are used to run TagValidators against every tag in the bucket. In addition,
        deprecated tags are pulled from our campaign's settings to ensure they don't appear in the bucket. The
        self.errors attribute is modified by this method, as well as returned directly by it.

        Args:
            bucket (TagBucket): TagBucket of tags to examine
            available_specs (list[TagSpec]): Specs to use for validating the tags

        Returns:
            list: List of TagValidationError objects, or empty.
        """
        handled_names = []

        deprecations = self.campaign.settings.deprecated_tags.values()
        for spec in deprecations:
            if bucket.tags[spec.name]:
                self.errors.append(TagDeprecatedError(spec.name, spec.replaced_by))
            handled_names.append(spec.name)

        required_specs = (
            spec
            for spec in available_specs
            if (spec.required or spec.min) and spec.name not in handled_names
        )
        for spec in required_specs:
            logger.debug(f"tag {spec.name} is required")
            self.validate_spec(spec, bucket.tags[spec.name])
            handled_names.append(spec.name)

        remaining_specs = (
            spec
            for spec in available_specs
            if spec.name not in handled_names and spec.name in bucket.tags.keys()
        )
        for spec in remaining_specs:
            logger.debug(f"tag {spec.name} was found")
            self.validate_spec(spec, bucket.tags[spec.name])
            handled_names.append(spec.name)

        unknown_tags = (
            key
            for key in bucket.tags.keys()
            if key not in handled_names
        )
        for tag_name in unknown_tags:
            self.errors.append(TagUndefinedError(tag_name))

        return self.errors

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
