.. _tag_group:

@group
######

:bdg-danger:`Replaced by @org`
:bdg-secondary:`Optional`
:bdg-info:`Value required`

Name of a group that the character belongs to

This is a highly multipurpose tag and can represent membership in anything from a university's faculty to a street gang.


Subtags
=======

These tags can appear immediately after @group and will be associated with that tag instance's value.

.. _tag_group_rank:

@rank
=====

:bdg-danger:`Replaced by @role`
:bdg-secondary:`Optional`
:bdg-info:`Value required`

The character's rank or role within this group

The rank tag does not have to mean a literal rank, because not all groups have that. It really just represents how people within the group see this character. A character with @group MIT Faculty might have the rank of Professor, Student, or Janitor. In the group Fifth Street Muggers, they might have the rank Lookout, or Pickpocket.

This tag is replaced by @role, since in practice, most rank values actually described the role the character performed for their group. The @org tag does support @rank, though, so explicit hierarchy ranks can be expressed.


