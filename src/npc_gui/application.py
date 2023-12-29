from PySide6.QtWidgets import QApplication

class NPCApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fs_update_dispatcher = Dispatcher()

    def fs_update_handler(event):
        pass
        # self.fs_update_dispatcher.dispatch(event)
        # will receive custom events from the fsevent handler
        # and propagate to all registered listeners through the dispatcher
