from npc.campaign import Campaign

def directory_list(dirs: list) -> str:
    return "\n".join([f"  {dirname}/" for dirname in dirs])

def campaign_info(campaign: Campaign) -> str:
    infos = [
        f"{'---Campaign Info---':>22}",
        f"{'Name:':>12} {campaign.name}",
        f"{'Description:':>12} {campaign.desc}",
        f"{'System:':>12} {campaign.system_key}",
        f"{'Plot Files:':>12} {campaign.latest_plot_index}",
        f"{'Sessions:':>12} {campaign.latest_session_index}",
    ]
    return "\n".join(infos)
