import os
import logging

import npc
from npc.settings import Settings
from npc.campaign import Campaign

def cwd_campaign(settings: Settings) -> Campaign:
    """Make a campaign object for the nearest campaign to the current dir

    If the current dir or any of its parents is a campaign, return a new Campaign object. Otherwise, warn and
    return None.

    Args:
        settings (Settings): Settings file to use when constructing the campaign

    Returns:
        Campaign: New campaign object for the found dir
    """
    campaign_root = npc.campaign.find_campaign_root(os.getcwd())
    if not campaign_root:
        logging.warning("Not a campaign (or any of the parent directories)")
        return None
    logging.info(f"Found campaign root at {campaign_root}")

    return Campaign(campaign_root, settings = settings)
