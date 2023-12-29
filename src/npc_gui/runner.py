import click

from .application import NPCApplication
from .windows import MainWindow

@click.command
def run():
    app = NPCApplication([])

    mw = MainWindow()
    mw.show()

    # set up watchdog observer
    # fs_event_handler = ...
    # observer = Observer()
    # observer.schedule(fs_event_handler, pathstr..., recursive=True)
    # observer.start()

    app.exec()

    # observer.stop()
    # observer.join()
