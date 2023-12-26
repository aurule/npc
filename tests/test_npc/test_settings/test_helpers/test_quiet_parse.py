from pathlib import Path
from tests.fixtures import fixture_file

from npc.settings.helpers import quiet_parse

def test_loads_valid_file():
	result = quiet_parse(fixture_file("yaml", "valid.yaml"))

	assert result["valid"] == True

def test_ignores_missing_files(tmp_path):
	result = quiet_parse(tmp_path / "missing.yaml")

	assert result is None

def test_ignores_parse_errors():
	result = quiet_parse(fixture_file("yaml", "invalid.yaml"))

	assert result is None
