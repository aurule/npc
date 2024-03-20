import click
import platform

from .application import NPCApplication
from .windows import MainWindow

from npc import __version__ as npc_version

@click.command
@click.version_option(npc_version)
@click.option("-c", "--campaign", help="Path to the campaign directory to open on launch")
def run(campaign):
    """Run the NPC GUI interface
    """
    app = NPCApplication([])

    mw = MainWindow()
    mw.show()
    mw.warn_if_outdated("user")
    if campaign:
        mw.load_campaign_dir(campaign)

    app.exec()
