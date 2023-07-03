from sqlalchemy import Select, select, func
from sqlalchemy.orm import aliased

from npc.db import character_repository
from npc.characters import Character, Tag

class CharacterListerQueryBuilder:
    """Builds a query to get characters grouped by attributes or tag values

    Attributes:
        ATTRIBUTE_PARTIALS: Dict of special names to their bespoke partials. Primarily used to handle grouping
            and sorting by character attributes.
    """

    ATTRIBUTE_PARTIALS = {
        "type": "apply_type_partial",
        "first_name": "apply_first_name_partial",
        "first_initial": "apply_first_initial_partial",
        "last_name": "apply_last_name_partial",
        "last_initial": "apply_last_initial_partial",
        "full_name": "apply_full_name_partial",
    }

    def __init__(self):
        self.query: Select = character_repository.with_tags()
        self.grouped_by: list[str] = []
        self.sorted_by: list[str] = []

    @property
    def next_group_index(self) -> int:
        """Get the next group_by index

        Returns:
            int: Index for the next entry in self.grouped_by
        """
        return len(self.grouped_by)

    @property
    def next_sort_index(self) -> int:
        """Get the next sort_by index

        Returns:
            int: Index for the next entry in self.sorted_by
        """
        return len(self.sorted_by)

    def group_by(self, *entity_names: list[str]):
        """Add a grouping clause to the query

        Chooses the correct sql partial to group the characters by the given
        entity. If the entity appears in ATTRIBUTE_PARTIALS, then the referenced
        method is used. Otherwise, entity is assumed to be a tag and the generic
        tag partial is applied.

        The entity_name is added to self.grouped_by for future reference, and
        included in the result set as a new column starting with "group".

        Args:
            entity_names (list[str]): Name of the thing to group by
        """
        for entity_name in entity_names:
            self.pick_partial(entity_name, f"group{self.next_group_index}")
            self.grouped_by.append(entity_name)

    def sort_by(self, *entity_names: list[str]):
        """Add a sorting clause to the query

        Chooses the correct sql partial to sort the characters by the given
        entity. If the entity appears in ATTRIBUTE_PARTIALS, then the referenced
        method is used. Otherwise, entity is assumed to be a tag and the generic
        tag partial is applied.

        The entity_name is added to self.sorted_by for future reference, and
        included in the result set as a new column starting with "sort".

        Sorting works identically to grouping, and is separated basically by
        the label on the column.

        Args:
            entity_names (list[str]): Name of the thing to sort by
        """
        for entity_name in entity_names:
            self.pick_partial(entity_name, f"sort{self.next_sort_index}")
            self.sorted_by.append(entity_name)

    def pick_partial(self, entity_name: str, label: str):
        """Determine which sql partial to add to the query, and apply it

        If entity_name appears in ATTRIBUTE_PARTIALS, the named method will be
        applied to the query. Otherwise, the tag partial will be used.

        Args:
            entity_name (str): Name of the entity to query
            label (str): Label for the clause
        """
        attr_partial = self.ATTRIBUTE_PARTIALS.get(entity_name)
        if attr_partial:
            partial = getattr(self, attr_partial)
            return partial(label)

        return self.apply_tag_partial(entity_name, label)

    def apply_tag_partial(self, tag_name: str, label: str):
        """Query a tag value

        This adds an explicit join on the table in order to create the new column.

        Args:
            tag_name (str): Name of the tag to query
            label (str): Label for the tag's column
        """
        grouping = aliased(Tag)
        self.query = self.query \
          .add_columns(grouping.value.label(label)) \
          .join(grouping, isouter=True) \
          .where(grouping.name == tag_name) \
          .order_by(label)

    def apply_type_partial(self, label: str):
        """Query the character's type using the type_key property

        The collision with the type tag is fine here, as that is already a very special tag which makes no
        sense to query on its own. In the absense of a consistency problem with similar entities, there isn't
        enough reason to rename this partial.

        Args:
            label (str): Label for the type column
        """
        self.query = self.query \
          .add_columns(Character.type_key.label(label)) \
          .order_by(label)

    def apply_first_name_partial(self, label: str):
        """Query the character's first name using the realname property

        This uses the custom first_word query function to limit the query to the first word of the character's
        realname property.

        Args:
            label (str): Label for the first name column
        """
        self.query = self.query \
          .add_columns(func.first_word(Character.realname).label(label)) \
          .order_by(label)

    def apply_first_initial_partial(self, label: str):
        """Query the character's first name initial using the realname property

        Args:
            label (str): Label for the first initial column
        """
        self.query = self.query \
          .add_columns(func.substr(Character.realname, 1, 1).label(label)) \
          .order_by(label)

    def apply_last_name_partial(self, label: str):
        """Query the character's last name using the realname property

        This uses the custom last_word query function to limit the query to the last word of the character's
        realname property.

        Args:
            label (str): Label for the last name column
        """
        self.query = self.query \
          .add_columns(func.last_word(Character.realname).label(label)) \
          .order_by(label)

    def apply_last_initial_partial(self, label: str):
        """Query the character's last name initial using the realname property

        Args:
            label (str): Label for the last initial column
        """
        self.query = self.query \
          .add_columns(func.substr(func.last_word(Character.realname), 1, 1).label(label)) \
          .order_by(label)

    def apply_full_name_partial(self, label: str):
        """Query the character's full name using the realname property

        The full_name entity is used for consistency with first_name and last_name, as well as to avoid
        colliding with the realname tag

        Args:
            label (str): Label for the full name column
        """
        self.query = self.query \
          .add_columns(Character.realname.label(label)) \
          .order_by(label)
