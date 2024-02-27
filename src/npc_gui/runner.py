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
    if platform.system() == "Windows":
        app.setStyle("Fusion")

    mw = MainWindow()
    mw.show()
    if campaign:
        mw.load_campaign_dir(campaign)

    # set up watchdog observer
    # fs_event_handler = ...
    # observer = Observer()
    # observer.schedule(fs_event_handler, pathstr..., recursive=True)
    # observer.start()

    app.exec()

    # observer.stop()
    # observer.join()
