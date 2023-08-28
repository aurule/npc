from npc.characters import Tag
from npc.validation.errors.tag_errors import *

class TagValidator:
    """Validator for basic Tag correctness"""

    def __init__(self, spec):
        self.spec = spec

    def validate(self, tags: list[Tag]) -> list:
        """Validate a set of Tag records

        The tags supplied should be the full set of tags with our spec for a given character. This is because
        the min and max checks test against the total number of appearances of a given tag name.

        Args:
            tags (list[Tag]): List of Tag records to validate

        Returns:
            list: List of TagValidationError objects describing the errors found
        """
        errors: list = []
        tag_name: str = self.spec.name

        if not self.spec.definition:
            errors.append(TagUndefinedError(tag_name))
            return errors

        if self.spec.replaced_by:
            errors.append(TagReplacedError(tag_name, self.spec.replaced_by))
            return errors

        total_tags: int = len(tags)
        if self.spec.required and not total_tags:
            errors.append(TagRequiredError(tag_name))
        if total_tags < self.spec.min:
            errors.append(TagMinError(tag_name, self.spec.min, total_tags))
        if total_tags > self.spec.max:
            errors.append(TagMaxError(tag_name, self.spec.max, total_tags))

        for tag in tags:
            value: str = tag.value
            if value:
                if self.spec.no_value:
                    errors.append(TagNoValueAllowedError(tag_name, value))
                if self.spec.values and value not in self.spec.values:
                    errors.append(TagValueError(tag_name, value))
            else:
                if not self.spec.allow_empty:
                    errors.append(TagEmptyError(tag_name))

        return errors
