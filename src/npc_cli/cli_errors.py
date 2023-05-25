from click import ClickException

class CampaignNotFoundException(ClickException):
    def __init__(self):
        super().__init__("Not a campaign (or any of the parent directories)")
