from pathlib import Path

class MockCampaign:
    def __init__(self, campaign_path: Path):
        self.root = campaign_path
        self.name = ""
