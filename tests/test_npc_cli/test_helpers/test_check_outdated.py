import pytest

from tests.fixtures import MockSettings

from npc_cli.helpers import check_outdated

def test_false_against_self():
    settings = MockSettings()

    result = check_outdated(settings, "package")

    assert result is False

def test_false_on_equal_version():
    settings = MockSettings()
    settings.versions["test"] = settings.versions.get("package")

    result = check_outdated(settings, "test")

    assert result is False

def test_true_on_later_version():
    settings = MockSettings()
    settings.versions["test"] = "999.0.0"

    result = check_outdated(settings, "test")

    assert result is True
