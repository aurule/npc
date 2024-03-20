import pytest

from tests.fixtures import MockSettings

def test_false_against_self():
    settings = MockSettings()

    result = settings.package_outdated("package")

    assert result is False

def test_false_on_equal_version():
    settings = MockSettings()
    settings.versions["test"] = settings.versions.get("package")

    result = settings.package_outdated("test")

    assert result is False

def test_true_on_later_version():
    settings = MockSettings()
    settings.versions["test"] = "999.0.0"

    result = settings.package_outdated("test")

    assert result is True
