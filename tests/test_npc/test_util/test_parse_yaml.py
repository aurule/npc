import pytest

from npc.util import parse_yaml
from npc.util.errors import ParseError
from tests.fixtures import fixture_file

class TestWithValidFile:
    def test_returns_parsed_data(self):
        valid_file: Path = fixture_file("yaml", "valid.yaml")

        result: dict = parse_yaml(valid_file)

        assert result == {"valid": True}

class TestWithMalformedFile:
    def test_throws_parse_error(self):
        invalid_file: Path = fixture_file("yaml", "invalid.yaml")

        with pytest.raises(ParseError):
            parse_yaml(invalid_file)
