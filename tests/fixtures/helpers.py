import os
import pytest
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from functools import wraps
from click.testing import CliRunner

from npc.campaign import init, Campaign
from npc.characters import Character, CharacterFactory, RawTag
from npc.db import DB

def fixture_file(*fixture_path: list[str]) -> Path:
    """Get the Path to a particular fixture

    This helper loads fixtures from the tests.fixtures module. It appends the given fixture_path items using
    importlib and returns the resulting pathlike object.

    Args:
        fixture_path (list[str]): One or more path components to append

    Returns:
        Path: Pathlike object referencing the named fixture
    """
    base: Path = resources.files("tests.fixtures")
    return base.joinpath("data", *fixture_path)

@pytest.fixture
def db() -> DB:
    """Pytest fixture to supply an isolated database object

    Returns:
        DB: Database object that will not be reused elsewhere
    """
    return DB(clearSingleton=True)

@pytest.fixture
def tmp_campaign(tmp_path: Path) -> Campaign:
    """Pytest fixture to supply a campaign object initialized to a temporary directory

    This initializes a blank campaign in a temporary path, suitable for keeping a test isolated. See
    campaign.init for what is created.

    Args:
        tmp_path (Path): Temporary path for the campaign, provided by the tmp_path pytest fixture

    Returns:
        Campaign: Campaign class rooted to tmp_path, with basic directories initialized
    """
    return init(tmp_path, name="Test Campaign", system="generic")

@contextmanager
def change_cwd(new_cwd: str):
    """Execute some code within the given directory

    Changes the working directory to new_cwd for a single with... block.

    Args:
        new_cwd (str): New CWD to use
    """
    old_cwd = os.getcwd()
    os.chdir(new_cwd)
    try:
        yield
    finally:
        os.chdir(old_cwd)

@pytest.fixture
def runner() -> CliRunner:
    """Fixture that provides a CliRunner object"""
    return CliRunner()

def isolated(func):
    """Decorator to isolate a test within its tmp_path or tmp_campaign's root

    Requires that the test args include either tmp_path or tmp_campaign.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        match kwargs:
            case {"tmp_campaign": campaign}:
                jail = campaign.root
            case {"tmp_path": tpath}:
                jail = tpath
        with change_cwd(jail):
            func(*args, **kwargs)
    return wrapper

def create_character(tags: list[tuple], campaign: Campaign, db: DB, type_key="person", **kwargs) -> Character:
    """Create a new character object

    The new character and its tags are fully populated in the db. This method does not create a corresponding
    file, however.

    Args:
        tags (list[tuple]): Tag tuples to associate with the character.
        campaign (Campaign): Campaign to create the characters within
        db (DB): Database to store the characters
        type_key (str): Type for the character objects (default: `"person"`)
        **kwargs (dict): All remaining keyword args are passed to CharacterFactory.make()

    Returns:
        Character: Newly created character file. Its tags property is eager-loaded.
    """
    factory = CharacterFactory(campaign)
    rawtags = [RawTag(*tag) for tag in tags]

    character = factory.make("Test Mann", tags=rawtags, type_key=type_key, **kwargs)
    with db.session() as session:
        session.add(character)
        session.commit()
        character.tags # load the tags immediately to prevent DetachedInstanceError later
    return character

class ProgressCounter:
    """Drop-in progress bar fixture

    Instead of rendering a bar, this just increments an internal count each time its progress method is called.
    """
    def __init__(self):
        self.count = 0

    def progress(self):
        """Progress bar increment method

        Pass this as the progress_callback to test that it was called.
        """
        self.count += 1
