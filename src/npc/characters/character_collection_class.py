from ..campaign import Campaign
from ..db import DB

class CharacterCollection():
    """Class for a group of Character objects, backed by a database

    Manages the loading, creation, and fetching of Characters
    """

    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self.root = campaign.characters_dir
