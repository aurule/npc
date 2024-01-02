from PySide6.QtWidgets import QApplication

from npc.settings import Settings, app_settings

class NPCApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_settings = app_settings()
        self.campaign = None

        # self.fs_update_dispatcher = Dispatcher()

    def fs_update_handler(event):
        pass
        # self.fs_update_dispatcher.dispatch(event)
        # will receive custom events from the fsevent handler
        # and propagate to all registered listeners through the dispatcher

    @property
    def settings(self) -> Settings:
        if self.campaign:
            return self.campaign.settings
        return self.default_settings
