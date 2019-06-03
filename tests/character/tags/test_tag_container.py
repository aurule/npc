from npc.character.tags import TagContainer, Tag, UnknownTag, Flag, GroupTag

def test_has_description():
    container = TagContainer()
    assert 'description' in container

class TestAppend:
    def test_indexes_by_tag_name(self):
        container = TagContainer()
        tag = Tag('type')
        container.append(tag)
        assert 'type' in container

    def test_ignores_if_key_exists(self):
        container = TagContainer()
        tag1 = Tag('type', 'human')
        tag2 = Tag('type', 'werewolf')
        container.append(tag1)
        container.append(tag2)

        assert container('type') == tag1

class TestCall:
    def test_gets_existing_tag(self):
        container = TagContainer()
        tag = Tag('type')
        container.append(tag)
        assert container('type') == tag

    def test_creates_uknown_tag(self):
        container = TagContainer()
        tag = Tag('type')
        container.append(tag)
        assert type(container('asdf')) is UnknownTag

def test_iterate_yields_values():
    container = TagContainer()
    tag1 = Tag('type')
    tag2 = Tag('name')
    container.append(tag1)
    container.append(tag2)
    tag_list = list(container)
    assert tag1 in tag_list
    assert tag2 in tag_list

def test_names_includes_all_tag_names():
    container = TagContainer()
    tag1 = Tag('type', 'human')
    tag2 = Tag('name')
    container.append(tag1)
    container.append(tag2)

    names = list(container.names())
    assert 'type' in names
    assert 'name' in names

def test_present_includes_only_present_tags():
    container = TagContainer()
    tag1 = Tag('type', 'human')
    tag2 = Tag('name')
    container.append(tag1)
    container.append(tag2)

    present_tags = list(container.present())
    assert tag1 in present_tags
    assert tag2 not in present_tags

class TestTagCreationHelpers:
    def test_add_tag_creates_tag_object(self):
        container = TagContainer()
        container.add_tag('type', 'human')
        assert 'type' in container
        assert container('type') == Tag('type', 'human')

    def test_add_flag_creates_flag_object(self):
        container = TagContainer()
        container.add_flag('wanderer', 'very yes')
        assert 'wanderer' in container
        assert container('wanderer') == Flag('wanderer', 'very yes')

    def test_add_group_creates_group_object(self):
        container = TagContainer()
        container.add_group('group', 'club')
        assert 'group' in container
        assert container('group') == GroupTag('group', 'club')

class TestValidation:
    def test_key_names_must_match_tag_names(self):
        container = TagContainer()
        tag1 = Tag('type')
        tag2 = Tag('name')
        container.data = {
            'fake': tag1,
            'name': tag2
        }
        container.validate()
        assert not container.valid
        assert "Tag 'type' has wrong key: 'fake'" in container.problems

    def test_container_inherits_tag_errors(self):
        container = TagContainer()
        tag = Tag('type', limit=0, required=True)
        container.append(tag)
        container.validate()
        assert not container.valid
        assert "Tag 'type' is required but limited to zero values" in container.problems
